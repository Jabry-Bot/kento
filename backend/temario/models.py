from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from gimnasios.models import Gimnasio

from .requisitos import OPCIONES, TIPOS

TIPOS_ASCENSO = (
    ("examen_club", "Examen club"),
    ("examen_federacion", "Examen federación"),
    ("entrenador", "Examen entrenador"),
)

ESTADOS_PROGRESO = (
    ("pendiente", "Pendiente"),
    ("en_progreso", "En progreso"),
    ("superado", "Superado"),
)

MOTIVOS_ASCENSO = (
    ("inicial", "Alta en la disciplina"),
    ("examen", "Examen"),
    ("entrenador", "Entrenador"),
    ("importado", "Importado"),
)


class ArteMarcial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    # MMA -> K1 -> boxeo  // symmetrical= False evitamos que se creen en reversa los predecesores
    predecesor = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.nombre


class Disciplina(models.Model):
    gimnasio = models.ForeignKey(
        Gimnasio,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="disciplinas",
    )
    nombre = models.CharField(max_length=100)
    arte = models.ForeignKey(
        ArteMarcial, on_delete=models.PROTECT, related_name="disciplinas"
    )

    plantilla_origen = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        unique_together = ("gimnasio", "nombre")

    def __str__(self):
        return f"{self.nombre} ({self.gimnasio or 'plantilla'})"


class Bloque(models.Model):
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.CASCADE, related_name="bloques"
    )
    nombre = models.CharField(max_length=50)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]
        unique_together = ("disciplina", "nombre")

    def __str__(self):
        return f"{self.disciplina.nombre} - {self.nombre}"


class Grado(models.Model):
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.CASCADE, related_name="grados"
    )
    padre = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subgrados",
    )
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=7, blank=True)
    color_secundario = models.CharField(max_length=7, blank=True)
    orden = models.PositiveIntegerField(default=0)
    # Para el comparator del torneo multi
    nivel = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    tipo_ascenso = models.CharField(
        max_length=20, choices=TIPOS_ASCENSO, default="examen_club"
    )

    class Meta:
        ordering = ["orden"]

    def clean(self):
        if self.padre and self.padre.disciplina_id != self.disciplina_id:
            raise ValidationError("El grado padre tiene que ser de la misma disciplina")

    def __str__(self):
        return f"{self.disciplina.nombre} - {self.nombre}"


class Requisito(models.Model):
    grado = models.ForeignKey(
        Grado, on_delete=models.CASCADE, related_name="requisitos"
    )
    tipo = models.CharField(max_length=20, choices=OPCIONES)
    parametros = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("grado", "tipo")

    def clean(self):
        tipo = TIPOS.get(self.tipo)
        if tipo:
            tipo.validar(self.parametros)

    def __str__(self):
        return f"{self.grado} - {self.tipo}"


class Objetivo(models.Model):
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name="objetivos")
    bloque = models.ForeignKey(
        Bloque, on_delete=models.CASCADE, related_name="objetivos"
    )
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    video = models.URLField(blank=True)
    obligatorio = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return self.titulo


class Licencia(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="licencias"
    )
    arte = models.ForeignKey(ArteMarcial, on_delete=models.CASCADE)
    anio = models.PositiveIntegerField()

    class Meta:
        ordering = ["anio"]
        unique_together = ("usuario", "arte", "anio")

    def __str__(self):
        return f"{self.usuario} - {self.arte} {self.anio}"


# Con esto puedo asignar la Disciplina al alumno si se cambia
class DisciplinaAlumno(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="disciplinas"
    )
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.CASCADE, related_name="alumnos"
    )
    active = models.BooleanField(default=True)
    fecha_alta = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "disciplina")

    def __str__(self):
        return f"{self.usuario} - {self.disciplina}"

    @classmethod
    def apuntar(cls, usuario, disciplina, grado):
        inscripcion = cls.objects.create(usuario=usuario, disciplina=disciplina)
        inscripcion.ascender(grado, "inicial")
        return inscripcion

    def grado_actual(self):
        return (
            HistorialGrado.objects.filter(
                usuario=self.usuario, grado__disciplina=self.disciplina
            )
            .last()
            .grado
        )

    def ascender(self, grado, motivo, examen=None):
        if grado.disciplina_id != self.disciplina_id:
            raise ValidationError("Ese grado no es de esta disciplina")
        if grado.subgrados.exists():
            raise ValidationError("Este grado no es valido")
        return HistorialGrado.objects.create(
            usuario=self.usuario, grado=grado, motivo=motivo, examen=examen
        )


class Progreso(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="progresos"
    )
    objetivo = models.ForeignKey(
        Objetivo, on_delete=models.CASCADE, related_name="progresos"
    )
    estado = models.CharField(
        max_length=15, choices=ESTADOS_PROGRESO, default="pendiente"
    )
    nota = models.TextField(blank=True)
    evaluador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evaluaciones",
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "objetivo")

    def __str__(self):
        return f"{self.usuario} - {self.objetivo}: {self.estado}"


class Examen(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="examenes")
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name="examenes")
    fecha = models.DateField(auto_now_add=True)
    evaluador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="examenes_evaluados",
    )

    def __str__(self):
        return f"{self.usuario} - {self.grado} ({self.fecha})"


class ResultadoBloque(models.Model):
    examen = models.ForeignKey(
        Examen, on_delete=models.CASCADE, related_name="resultados"
    )
    bloque = models.ForeignKey(Bloque, on_delete=models.PROTECT)
    aprobado = models.BooleanField(default=False)

    class Meta:
        unique_together = ("examen", "bloque")

    def __str__(self):
        return f"{self.examen} - {self.bloque.nombre}: {'apto' if self.aprobado else 'no apto'}"


class HistorialGrado(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="historial_grados"
    )
    grado = models.ForeignKey(Grado, on_delete=models.PROTECT, related_name="historial")
    fecha = models.DateField(auto_now_add=True)
    motivo = models.CharField(max_length=15, choices=MOTIVOS_ASCENSO)
    examen = models.ForeignKey(Examen, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["fecha", "id"]
        indexes = [models.Index(fields=["usuario", "fecha"])]

    def clean(self):
        if self.grado.subgrados.exists():
            raise ValidationError("Este grado no es valido")

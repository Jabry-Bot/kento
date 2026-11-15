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
    arte = models.CharField(max_length=100)
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


class Licencia(models.Model):
    pass


class DisciplinaAlumno(models.Model):
    pass


class Progreso(models.Model):
    pass


class Examen(models.Model):
    pass


class ResultadoBloque(models.Model):
    pass


class HistorialGrado(models.Model):
    pass

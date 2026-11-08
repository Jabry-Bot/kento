import uuid
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

ROLES = (
    ("propietario", "Propietario"),
    ("entrenador", "Entrenador"),
    ("alumno", "Alumno"),
)


class Gimnasio(models.Model):
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to="logos/", blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Membresia(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="membresias"
    )
    gimnasio = models.ForeignKey(
        Gimnasio, on_delete=models.CASCADE, related_name="membresias"
    )
    rol = models.CharField(max_length=15, choices=ROLES)
    active = models.BooleanField(default=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "gimnasio")

    def __str__(self):
        return f"{self.gimnasio} ({self.rol}) -> {self.usuario}"


def caducidad_por_defecto():
    return timezone.now() + timedelta(days=7)


class Invitacion(models.Model):
    gimnasio = models.ForeignKey(
        Gimnasio, on_delete=models.CASCADE, related_name="invitaciones"
    )
    rol = models.CharField(max_length=15, choices=ROLES)
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    creada_por = models.ForeignKey(User, on_delete=models.CASCADE)
    # Sin parentesis se crea la fecha cuando se crea la invitacion.
    # Con parentesis se crea la fecha cuando arranca el server en DEV y PROD
    caduca = models.DateTimeField(default=caducidad_por_defecto)
    usos = models.PositiveIntegerField(default=0)
    usos_max = models.PositiveIntegerField(default=50)
    active = models.BooleanField(default=True)

    def es_valida(self):
        return (
            self.active and self.caduca > timezone.now() and self.usos < self.usos_max
        )

    def __str__(self):
        return f"{self.gimnasio} // ({self.rol} -> {self.codigo})"

from django.db import models
from django.contrib.auth.models import User


class Gimnasio(models.Model):
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to="logos/", blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Membresia(models.Model):
    ROLES = (
        ("propietario", "Propietario"),
        ("entrenador", "Entrenador"),
        ("alumno", "Alumno"),
    )
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

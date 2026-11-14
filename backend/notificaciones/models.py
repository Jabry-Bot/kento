from django.contrib.auth.models import User
from django.db import models


class Notificacion(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notificaciones"
    )
    titulo = models.CharField(max_length=100)
    texto = models.CharField(max_length=255, blank=True)
    enlace = models.CharField(max_length=200, blank=True)
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    # Aqui habrá notificar por correo
    # Tambien las notificaciones del movil mas adelante.

    @classmethod
    def avisar_entrenadores(cls, gimnasio_id, titulo, texto="", enlace=""):
        entrenadores = User.objects.filter(
            membresias__gimnasio_id=gimnasio_id,
            membresias__rol__in=("propietario", "entrenador"),
            membresias__active=True,
        )
        for entrenador in entrenadores:
            cls.objects.create(
                usuario=entrenador, titulo=titulo, texto=texto, enlace=enlace
            )

    def __str__(self):
        return f"{self.usuario} - {self.titulo}"

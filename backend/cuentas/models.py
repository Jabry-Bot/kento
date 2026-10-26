from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    google_sub = models.CharField(max_length=255, unique=True, blank=True, null=True)
    google_foto = models.URLField(blank=True)
    foto_perfil = models.ImageField(upload_to="fotos_perfil/", blank=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.email

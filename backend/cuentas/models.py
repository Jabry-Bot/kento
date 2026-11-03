from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    google_sub = models.CharField(max_length=255, unique=True, blank=True, null=True)
    google_foto = models.URLField(blank=True)
    foto_perfil = models.ImageField(upload_to="fotos_perfil/", blank=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.email

    @classmethod
    def get_google(cls, datos):
        email = datos["email"].lower()

        perfil = cls.objects.filter(google_sub=datos["sub"]).first()

        if not perfil:
            usuario = User.objects.filter(email__iexact=email).first()

            if not usuario:
                usuario = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=datos.get("given_name", ""),
                    last_name=datos.get("family_name", ""),
                )

            perfil = cls.objects.get_or_create(usuario=usuario)[0]

        perfil.google_sub = datos["sub"]
        perfil.google_foto = datos.get("picture", "")
        perfil.save()

        return perfil

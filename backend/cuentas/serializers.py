from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone

from .models import Perfil


class UsuarioSerializer(serializers.ModelSerializer):
    foto = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "foto"]

    def get_foto(self, obj):
        perfil = Perfil.objects.filter(usuario=obj).first()

        if perfil is None:
            return None
        elif perfil.foto_perfil:
            return perfil.foto_perfil.url
        return perfil.google_foto or None


class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ["fecha_nacimiento", "sexo", "peso"]

    def validate_fecha_nacimiento(self,valor):
        if valor and valor > timezone.localdate():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura")
        return valor


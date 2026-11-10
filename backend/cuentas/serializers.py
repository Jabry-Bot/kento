from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import password_validation
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

    def validate_fecha_nacimiento(self, valor):
        if valor and valor > timezone.localdate():
            raise serializers.ValidationError(
                "La fecha de nacimiento no puede ser futura"
            )
        return valor


class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "password": {"write_only": True},
        }

    def validate_email(self, valor):
        valor = valor.lower()
        if User.objects.filter(email__iexact=valor).exists():
            raise serializers.ValidationError("Ya hay una cuenta con este email")
        return valor

    def validate_password(self, valor):
        password_validation.validate_password(valor)
        return valor

    def create(self, datos):
        usuario = User.objects.create_user(
            username=datos["email"], is_active=False, **datos
        )
        Perfil.objects.create(usuario=usuario)
        return usuario


class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ["foto_perfil"]
        extra_kwargs = {"foto_perfil": {"required": True}}

    def validate_foto_perfil(self, foto):
        if foto.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("La foto no puede pasar de 10 MB")
        return foto

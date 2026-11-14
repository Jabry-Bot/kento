from cuentas.models import Perfil
from cuentas.serializers import UsuarioSerializer
from rest_framework import serializers

from .models import *


class GimnasioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gimnasio
        fields = ["id", "nombre", "ciudad", "logo"]


class MembresiaSerializer(serializers.ModelSerializer):
    gimnasio = GimnasioSerializer(read_only=True)

    class Meta:
        model = Membresia
        fields = ["id", "rol", "gimnasio"]


class InvitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitacion
        fields = ["id", "rol", "codigo", "caduca", "usos_max", "usos", "active"]
        read_only_fields = ["codigo", "usos", "active"]


class MiembroSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    ficha = serializers.SerializerMethodField()

    class Meta:
        model = Membresia
        fields = ["id", "rol", "fecha_alta", "usuario", "ficha"]

    def get_ficha(self, obj):
        perfil = Perfil.objects.filter(usuario=obj.usuario).first()
        if not perfil:
            return {"edad": None, "sexo": "", "peso": None}
        return {"edad": perfil.edad, "sexo": perfil.sexo, "peso": perfil.peso}


class SolicitudSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Solicitud
        fields = ["id", "usuario", "fecha"]


class AmonestacionSerializer(serializers.ModelSerializer):
    alumno_nombre = serializers.CharField(source="alumno.get_full_name", read_only=True)
    autor_nombre = serializers.CharField(source="autor.get_full_name", read_only=True)

    class Meta:
        model = Amonestacion
        fields = [
            "id",
            "alumno",
            "alumno_nombre",
            "autor",
            "autor_nombre",
            "motivo",
            "gravedad",
            "fecha",
        ]


class AvisoSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=100)
    texto = serializers.CharField(max_length=255, required=False, allow_blank=True)
    alumno = serializers.IntegerField(required=False)

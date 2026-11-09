from rest_framework import serializers
from cuentas.models import Perfil
from cuentas.serializers import UsuarioSerializer
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


class MiembroSerailizer(serializers.ModelSerializer):
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

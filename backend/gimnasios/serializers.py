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

from rest_framework import serializers

from .models import Gimnasio, Membresia


class GimnasioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gimnasio
        fields = ["id", "nombre", "ciudad", "logo"]


class MembresiaSerializer(serializers.ModelSerializer):
    gimnasio = GimnasioSerializer(read_only=True)

    class Meta:
        model = Membresia
        fields = ["id", "rol", "gimnasio"]

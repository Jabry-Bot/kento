from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Membresia
from .permisos import EsMiembro
from .serializers import GimnasioSerializer, MembresiaSerializer


@api_view(["GET", "POST"])
def gimnasios(request):
    if request.method == "GET":
        membresias = Membresia.objects.filter(usuario=request.user, active=True)
        return Response(MembresiaSerializer(membresias, many=True).data)
    else:
        gimnasio_srz = GimnasioSerializer(data=request.data)
        if not gimnasio_srz.is_valid():
            return Response(gimnasio_srz.errors, status=400)
        gimnasio = gimnasio_srz.save()
        Membresia.objects.create(
            usuario=request.user, gimnasio=gimnasio, rol="propietario"
        )
        return Response(gimnasio_srz.data, status=201)


@api_view(["GET", "PATCH"])
@permission_classes([EsMiembro])
def gimnasio(request, gimnasio_id):
    gimnasio = request.membresia.gimnasio

    if request.method == "GET":
        return Response(GimnasioSerializer(gimnasio).data)
    else:
        if request.membresia.rol != "propietario":
            return Response(
                {"error": "solo el propietario puede realizar cambios"}, status=403
            )
        gimnasio_srz = GimnasioSerializer(gimnasio, data=request.data, partial=True)

        if not gimnasio_srz.is_valid():
            return Response(gimnasio_srz.errors, status=400)

        gimnasio_srz.save()
        return Response(gimnasio_srz.data)

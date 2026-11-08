from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Membresia, Invitacion
from .permisos import *
from .serializers import *
from rest_framework.permissions import AllowAny


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


@api_view(["GET", "POST"])
@permission_classes([EsEntrenador])
def invitaciones(request, gimnasio_id):
    gimnasio = request.membresia.gimnasio

    if request.method == "GET":
        lista = Invitacion.objects.filter(gimnasio=gimnasio, active=True)
        return Response(InvitacionSerializer(lista, many=True).data)

    invitacion_srz = InvitacionSerializer(data=request.data)
    if not invitacion_srz.is_valid():
        return Response(invitacion_srz.errors, status=400)

    if (
        invitacion_srz.validated_data["rol"] != "alumno"
        and request.membresia.rol != "propietario"
    ):
        return Response({"error": "Solo el propietario puede hacer eso"}, status=403)

    invitacion_srz.save(gimnasio=gimnasio, creada_por=request.user)
    return Response(invitacion_srz.data)


@api_view(["DELETE"])
@permission_classes([EsEntrenador])
def anular_invitacion(request, invitacion_id, gimnasio_id):
    invitacion = Invitacion.objects.filter(
        id=invitacion_id, gimnasio_id=gimnasio_id
    ).first()
    if not invitacion:
        return Response({"error": "La invitacion no existe"}, status=404)
    invitacion.active = False
    invitacion.save()
    return Response(status=204)


@api_view(["GET"])
@permission_classes([AllowAny])
def ver_invitacion(request, codigo):
    invitacion = Invitacion.objects.filter(codigo=codigo).first()
    if not invitacion:
        return Response({"error": "No se encontro la invitacion"}, status=404)

    creador = invitacion.creada_por

    return Response(
        {
            "gimnasio": GimnasioSerializer(invitacion.gimnasio).data,
            "creador": creador.get_full_name() or creador.email,
            "rol": invitacion.rol,
            "active": invitacion.es_valida(),
        },
        status=200,
    )


@api_view(["POST"])
def aceptar_invitacion(request, codigo):
    invitacion = Invitacion.objects.filter(codigo=codigo).first()

    if not invitacion or not invitacion.es_valida():
        return Response(
            {"error": "Vuelve a solicitar otra invitacion al entrenador o propietario"},
            status=400,
        )

    membresia, creada = Membresia.objects.get_or_create(
        usuario=request.user,
        gimnasio=invitacion.gimnasio,
        # Para que solo se haga con el create. No influye el get
        defaults={"rol": invitacion.rol},
    )

    if not creada:
        if membresia.active:
            return Response({"error": "Ya perteneces a este gimansio"}, status=400)
        membresia.active = True
        membresia.rol = invitacion.rol
        membresia.save()

    invitacion.usos += 1
    invitacion.save()
    return Response(MembresiaSerializer(membresia).data, status=201)

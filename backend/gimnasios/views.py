from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from notificaciones.models import Notificacion
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import *
from .permisos import *
from .serializers import *


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


# Mas adelante convertirlo en un metodo de Invitacion
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
    if membresia.rol == "alumno":
        Notificacion.avisar_entrenadores(
            invitacion.gimnasio_id,
            "Alumno nuevo",
            f"{request.user.get_full_name() or request.user.email} se ha unido",
            f"/gimnasios/{invitacion.gimnasio_id}",
        )
    return Response(MembresiaSerializer(membresia).data, status=201)


@api_view(["GET"])
@permission_classes([EsEntrenador])
def miembros(request, gimnasio_id):
    membresias = Membresia.objects.filter(
        gimnasio_id=gimnasio_id, active=True
    ).order_by("rol")
    return Response(MiembroSerializer(membresias, many=True).data)


@api_view(["DELETE"])
@permission_classes([EsEntrenador])
def dar_de_baja(request, gimnasio_id, membresia_id):
    membresia = Membresia.objects.filter(
        id=membresia_id, gimnasio_id=gimnasio_id, active=True
    ).first()

    if not membresia:
        return Response({"error": "Este miembro no existe"}, status=404)

    if membresia.rol != "alumno" and request.membresia.rol != "propietario":
        return Response(
            {"error": "Solo un propietario puede realizar esta accion"},
            status=403,
        )

    if membresia.rol == "propietario":
        propietarios = Membresia.objects.filter(
            gimnasio_id=gimnasio_id, rol="propietario", active=True
        ).count()
        if propietarios < 2:
            return Response(
                {"error": "El gimnasio no puede quedar sin propietario"},
                status=403,
            )
    membresia.active = False
    membresia.save()
    return Response(status=204)


@api_view(["POST"])
@permission_classes([EsMiembro])
def salir(request, gimnasio_id):
    membresia = request.membresia

    if membresia.rol == "propietario":
        propietarios = Membresia.objects.filter(
            gimnasio_id=gimnasio_id, rol="propietario", active=True
        ).count()
        if propietarios < 2:
            return Response(
                {
                    "error": "Eres el unico propietario activo, no puede salir del gimnasio"
                },
                status=403,
            )
    membresia.active = False
    membresia.save()
    return Response(status=204)


@api_view(["GET"])
def buscar_gimnasios(request):
    texto = request.query_params.get("q", "").strip()
    if len(texto) < 2:
        return Response([])

    gimnasios = Gimnasio.objects.filter(
        Q(nombre__icontains=texto) | Q(ciudad__icontains=texto)
    )[:20]
    return Response(GimnasioSerializer(gimnasios, many=True).data)


@api_view(["POST"])
def solicitar(request, gimnasio_id):
    refresco = timezone.now() - timedelta(days=30)
    gimnasio = Gimnasio.objects.filter(id=gimnasio_id).first()
    if not gimnasio:
        return Response({"error": "Este gimnasio no existe"}, status=404)

    if Membresia.objects.filter(
        usuario=request.user, gimnasio=gimnasio, active=True
    ).exists():
        return Response({"error": "Ya eres miembro del gimnasio"}, status=400)
    if gimnasio.solicitudes.filter(
        Q(estado="pendiente") | Q(estado="rechazada", fecha__gte=refresco),
        usuario=request.user,
    ):
        return Response(
            {"error": "No puedes volver a solicitar este gimnasio"}, status=403
        )

    gimnasio.solicitudes.create(usuario=request.user)
    Notificacion.avisar_entrenadores(
        gimnasio.id,
        "Solicitud nueva",
        f"{request.user.get_full_name() or request.user.email} quiere unirse",
        f"/gimnasios/{gimnasio.id}",
    )
    return Response({"mensaje": "Solicitud enviada"}, status=201)


@api_view(["GET"])
@permission_classes([EsEntrenador])
def solicitudes(request, gimnasio_id):
    pendientes = Solicitud.objects.filter(
        gimnasio_id=gimnasio_id, estado="pendiente"
    ).order_by("fecha")
    return Response(SolicitudSerializer(pendientes, many=True).data)


@api_view(["PATCH"])
@permission_classes([EsEntrenador])
def responder_solicitud(request, gimnasio_id, solicitud_id):
    solicitud = Solicitud.objects.filter(
        id=solicitud_id, gimnasio_id=gimnasio_id, estado="pendiente"
    ).first()
    if not solicitud:
        return Response({"error": "Esta solicitud no existe"}, status=404)

    estado = request.data.get("estado")
    if estado not in ("aceptada", "rechazada"):
        return Response({"error": "Ese estado no existe"}, status=400)

    solicitud.resolver_solicitud(estado)
    aceptada = estado == "aceptada"
    Notificacion.objects.create(
        usuario=solicitud.usuario,
        titulo=f"Solicitud {estado}",
        texto=f"{solicitud.gimnasio.nombre} ha {'aceptado' if aceptada else 'rechazado'} tu solicitud",
        enlace=f"/gimnasios/{gimnasio_id}" if aceptada else "/",
    )
    return Response(status=204)


@api_view(["GET", "POST"])
@permission_classes([EsMiembro])
def amonestaciones(request, gimnasio_id):
    if request.method == "GET":
        amonestados = Amonestacion.objects.filter(gimnasio_id=gimnasio_id)

        if request.membresia.rol == "alumno":
            amonestados = amonestados.filter(alumno=request.user)
        else:
            alumno_id = request.query_params.get("alumno", "")
            if alumno_id.isdigit():
                amonestados = amonestados.filter(alumno_id=alumno_id)

        return Response(AmonestacionSerializer(amonestados, many=True).data)

    if request.membresia.rol == "alumno":
        return Response(
            {"error": "Solo los entrenadores pueden poner amonestaciones"}, status=403
        )

    amonestacion_srz = AmonestacionSerializer(data=request.data)
    if not amonestacion_srz.is_valid():
        return Response(amonestacion_srz.errors, status=400)

    alumno = amonestacion_srz.validated_data["alumno"]
    es_alumno = Membresia.objects.filter(
        gimnasio_id=gimnasio_id, usuario=alumno, rol="alumno", active=True
    ).exists()
    if not es_alumno:
        return Response(
            {"error": "Este alumno no pertenece a este gimnasio"}, status=400
        )

    amonestacion = amonestacion_srz.save(gimnasio_id=gimnasio_id, autor=request.user)

    Notificacion.objects.create(
        usuario=alumno,
        titulo="Amonestacion",
        texto=f"{amonestacion.gravedad}: {amonestacion.motivo}",
        enlace=f"/gimnasios/{gimnasio_id}",
    )
    return Response(amonestacion_srz.data, status=201)


@api_view(["DELETE"])
@permission_classes([EsEntrenador])
def borrar_amonestacion(request, gimnasio_id, amonestacion_id):
    amonestacion = Amonestacion.objects.filter(
        id=amonestacion_id, gimnasio_id=gimnasio_id
    ).first()
    if not amonestacion:
        return Response({"error": "Esta amonestación no existe"}, status=404)
    amonestacion.delete()
    return Response(status=204)


@api_view(["POST"])
@permission_classes([EsEntrenador])
def enviar_aviso(request, gimnasio_id):
    aviso_srz = AvisoSerializer(data=request.data)
    if not aviso_srz.is_valid():
        return Response(aviso_srz.errors, status=400)
    datos = aviso_srz.validated_data
    alumnos = User.objects.filter(
        membresias__gimnasio_id=gimnasio_id,
        membresias__rol="alumno",
        membresias__active=True,
    )
    if "alumno" in datos:
        alumnos = alumnos.filter(id=datos["alumno"])
        if not alumnos.exists():
            return Response({"error": "Ese alumno no es de este gimnasio"}, status=400)

    for alumno in alumnos:
        Notificacion.objects.create(
            usuario=alumno,
            titulo=datos["titulo"],
            texto=datos.get("texto", ""),
            enlace=f"/gimnasios/{gimnasio_id}",
        )
    return Response({"enviados": len(alumnos)}, status=201)


@api_view(["GET"])
@permission_classes([EsEntrenador])
def datos_entrenador(request, gimnasio_id):
    hoy = timezone.localdate()
    alumnos = Membresia.objects.filter(
        gimnasio_id=gimnasio_id, rol="alumno", active=True
    )
    return Response(
        {
            "alumnos": alumnos.count(),
            "altas_30_dias": alumnos.filter(
                fecha_alta__date__gte=hoy - timedelta(days=30)
            ).count(),
            "solicitudes": Solicitud.objects.filter(
                gimnasio_id=gimnasio_id, estado="pendiente"
            ).count(),
            "amonestaciones_90_dias": Amonestacion.objects.filter(
                gimnasio_id=gimnasio_id, fecha__gte=hoy - timedelta(days=90)
            ).count(),
        }
    )

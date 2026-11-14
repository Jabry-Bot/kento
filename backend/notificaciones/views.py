from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


@api_view(["GET"])
def notificaciones(request):
    lista = request.user.notificaciones.all()[:30]
    no_leidas = request.user.notificaciones.filter(leida=False).count()
    return Response(
        {
            "no_leidas": no_leidas,
            "lista": NotificacionSerializer(lista, many=True).data,
        }
    )


@api_view(["POST"])
def leer_todas(request):
    request.user.notificaciones.filter(leida=False).update(leida=True)
    return Response(status=204)

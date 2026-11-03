from django.conf import settings
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import Perfil


@api_view(["POST"])
@permission_classes([AllowAny])
def login_google(request):
    credencial = request.data.get("credential")

    if not credencial:
        return Response({"error": "Falta el token de Google"}, status=400)

    try:
        datos = id_token.verify_oauth2_token(
            credencial, google_requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        return Response({"error": "Token de Google no válido"}, status=401)

    if not datos.get("email_verified"):
        return Response({"error": "Email de Google no registrado"}, status=401)

    perfil = Perfil.get_google(datos)

    tokens = RefreshToken.for_user(perfil.usuario)

    return Response(
        {
            "access": str(tokens.access_token),
            "refresh": str(tokens),
            "usuario": UsuarioSerializer(perfil.usuario).data,
        }
    )


@api_view(["GET"])
def yo(request):
    return Response(UsuarioSerializer(request.user).data)

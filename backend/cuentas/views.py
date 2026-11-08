from django.conf import settings
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.throttling import AnonRateThrottle
from django.core.exceptions import ValidationError


# para IPs sin sesion.
class LimiteAcceso(AnonRateThrottle):
    rate = "5/min"


def resp_login(usuario):
    tokens = RefreshToken.for_user(usuario)
    return {
        "access": str(tokens.access_token),
        "refresh": str(tokens),
        "usuario": UsuarioSerializer(usuario).data,
    }


def enviar_enlace(usuario, asunto, texto, ruta):
    token = default_token_generator.make_token(usuario)
    enlace = f"{settings.FRONTEND_URL}/{ruta}/{usuario.id}/{token}"
    send_mail(
        asunto,
        f"Hola, {usuario.first_name}:\n\n{texto} \n{enlace}",
        None,
        [usuario.email],
    )


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([LimiteAcceso])
def login_email(request):
    email = str(request.data.get("email", "")).lower()
    usuario = User.objects.filter(email__iexact=email).first()

    if not usuario or not usuario.check_password(request.data.get("password", "")):
        return Response({"error": "Email o contraseña incorrectos"}, status=401)

    if not usuario.is_active:
        return Response(
            {
                "error": "Active su cuenta primero desde el enlace que le ha llegado al correo"
            },
            status=401,
        )

    return Response(resp_login(usuario))


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

    return Response(resp_login(perfil.usuario))


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([LimiteAcceso])
def registro(request):
    registro_srz = RegistroSerializer(data=request.data)
    if not registro_srz.is_valid():
        return Response(registro_srz.errors, status=400)

    usuario = registro_srz.save()
    enviar_enlace(
        usuario,
        "Confirma tu email en Kento",
        "Para activar tu cuenta, abre este enlace:",
        "verificar",
    )
    return Response(
        {"mensaje": "Te hemos enviado un correo para activar tu cuenta"}, status=201
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def verificar_email(request, usuario_id, token):
    usuario = User.objects.filter(id=usuario_id).first()

    if not usuario or not default_token_generator.check_token(usuario, token):
        return Response({"error": "El enlace no es valido o ha caducado"}, status=400)

    if usuario.is_active:
        return Response({"error": "Esta cuenta ya esta activa"}, status=400)

    usuario.is_active = True
    usuario.save()
    return Response(resp_login(usuario))


@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([LimiteAcceso])
def recuperar_pass(request):
    email = str(request.data.get("email", "")).lower()
    usuario = User.objects.filter(email__iexact=email).first()
    if usuario:
        enviar_enlace(
            usuario,
            "Cambia su contraseña de Kento",
            "Para elegir una contraseña nueva, abre este enlace. Si no lo has pedido tú, ignora este correo.",
            "nueva-pass",
        )
    return Response({"mensaje": "Si existe se le ha enviado el enlace"})


@api_view(["POST"])
@permission_classes([AllowAny])
def nueva_contrasena(request, usuario_id, token):
    usuario = User.objects.filter(id=usuario_id).first()
    if not usuario or not default_token_generator.check_token(usuario, token):
        return Response({"error": "El enlace no es valido o ha caducado"}, status=400)

    password = request.data.get("password", "")
    try:
        password_validation.validate_password(password, usuario)
    except ValidationError as error:
        return Response({"password": error.messages}, status=400)

    usuario.set_password(password)
    usuario.is_active = True
    usuario.save()
    return Response(resp_login(usuario))


@api_view(["GET"])
def yo(request):
    return Response(UsuarioSerializer(request.user).data)


@api_view(["GET", "PATCH"])
def ficha(request):
    perfil = Perfil.objects.get_or_create(usuario=request.user)[0]

    if request.method == "GET":
        return Response(FichaSerializer(perfil).data)

    ficha_srz = FichaSerializer(perfil, data=request.data, partial=True)
    if not ficha_srz.is_valid():
        return Response(ficha_srz.errors, status=400)

    ficha_srz.save()
    return Response(ficha_srz.data, status=200)

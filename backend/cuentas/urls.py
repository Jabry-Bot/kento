from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("google/", views.login_google, name="login_google"),
    path("registro/", views.registro, name="registro"),
    path(
        "verificar/<int:usuario_id>/<str:token>/",
        views.verificar_email,
        name="verificar_email",
    ),
    path("login/", views.login_email, name="login_email"),
    path("recuperar/", views.recuperar_pass, name="recuperar_pass"),
    path(
        "nueva-contrasena/<int:usuario_id>/<str:token>/",
        views.nueva_contrasena,
        name="nueva_contrasena",
    ),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("yo/", views.yo, name="yo"),
    path("yo/ficha/", views.ficha, name="ficha"),
]

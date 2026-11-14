from django.urls import path

from . import views

urlpatterns = [
    path("", views.notificaciones, name="notificaciones"),
    path("leidas/", views.leer_todas, name="leer_todas"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.gimnasios, name="gimnasios"),
    path("<int:gimnasio_id>/", views.gimnasio, name="gimnasio"),
    path("<int:gimnasio_id>/invitaciones/", views.invitaciones, name="invitaciones"),
    path(
        "<int:gimnasio_id>/invitaciones/<int:invitacion_id>/",
        views.anular_invitacion,
        name="anular_invitacion",
    ),
    path("invitaciones/<uuid:codigo>/", views.ver_invitacion, name="ver_invitacion"),
    path(
        "invitaciones/<uuid:codigo>/aceptar/",
        views.aceptar_invitacion,
        name="aceptar_invitacion",
    ),
    path("<int:gimnasio_id>/miembros/", views.miembros, name="miembros"),
    path(
        "<int:gimnasio_id>/miembros/<int:membresia_id>/",
        views.dar_de_baja,
        name="dar_de_baja",
    ),
    path("<int:gimnasio_id>/salir/", views.salir, name="salir"),
]

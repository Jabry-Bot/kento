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
    path("buscar/", views.buscar_gimnasios, name="buscar_gimnasios"),
    path("<int:gimnasio_id>/solicitar/", views.solicitar, name="solicitar"),
    path("<int:gimnasio_id>/solicitudes/", views.solicitudes, name="solicitudes"),
    path(
        "<int:gimnasio_id>/solicitudes/<int:solicitud_id>/",
        views.responder_solicitud,
        name="responder_solicitud",
    ),
    path(
        "<int:gimnasio_id>/amonestaciones/", views.amonestaciones, name="amonestaciones"
    ),
    path(
        "<int:gimnasio_id>/amonestaciones/<int:amonestacion_id>/",
        views.borrar_amonestacion,
        name="borrar_amonestacion",
    ),
]

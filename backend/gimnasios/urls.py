from django.urls import path

from . import views

urlpatterns = [
    path("", views.gimnasios, name="gimnasios"),
    path("<int:gimnasio_id>/", views.gimnasio, name="gimnasio"),
]

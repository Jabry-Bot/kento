from rest_framework.permissions import BasePermission

from .models import Membresia


def get_membresia(request, view):
    if not request.user.is_authenticated:
        return None
    gimnasio_id = view.kwargs.get("gimnasio_id")
    return Membresia.objects.filter(
        usuario=request.user, gimnasio_id=gimnasio_id, active=True
    ).first()


class EsMiembro(BasePermission):
    message = "No perteneces a este gimansio"
    roles = ("propietario", "entrenador", "alumno")

    def has_permission(self, request, view):
        membresia = get_membresia(request, view)

        if membresia is None or membresia.rol not in self.roles:
            return False

        request.membresia = membresia
        return True


class EsEntrenador(EsMiembro):
    message = "Solo los entrenadores pueden hacer esto"
    roles = ("propietario", "entrenador")


class EsPropietario(EsMiembro):
    message = "Solo el propietario puede hacer esto"
    roles = ("propietario",)

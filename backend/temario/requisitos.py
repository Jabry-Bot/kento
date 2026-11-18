# En la bd se guarda el requisito pero su valor puede ser distinto dependiento del requisito.
# Lo guardo en formato JSON para poder guardar cualquier tipo de dato. Pero no se puede meter cualquier
# cosa. Aqui se ponen los limites de lo que puede contener ese JSON para tenerlo controlado.

from django.core.exceptions import ValidationError


class Requisito:
    texto = ""
    parametros = {}

    def validar(self, parametros):
        if not isinstance(parametros, dict):
            raise ValidationError("Los parámetros tienen que ser un DTO")

        sobrantes = set(parametros) - set(self.parametros)
        if sobrantes:
            raise ValidationError(
                f"parametros que no existen {[sobrante + ' ' for sobrante in sobrantes]}"
            )

        if not parametros:
            raise ValidationError(f"{self.texto}: faltan parametros")

        for clave, obligatorio in self.parametros.items():
            valor = parametros.get(clave)
            if not valor:
                if obligatorio:
                    raise ValidationError(f"{self.texto}: falta {clave}")
                continue
            if type(valor) is not int or valor < 0:
                raise ValidationError(f"{clave} tiene que ser un entero positivo")


class Tiempo(Requisito):
    texto = "Tiempo en el grado anterior"
    parametros = {"meses": True}


class Edad(Requisito):
    texto = "Edad"
    parametros = {"minima": False, "maxima": False}

    def validar(self, parametros):
        super().validar(parametros)
        minima = parametros.get("minima")
        maxima = parametros.get("maxima")
        if minima is not None and maxima is not None and minima > maxima:
            raise ValidationError("La edad minima no puede ser mayor a la maxima")


class Licencias(Requisito):
    texto = "Licencias federativas"
    parametros = {"consecutivas": False, "alternas": False}


class Temario(Requisito):
    texto = "Objetivos superados"
    parametros = {"porcentaje": True}

    def validar(self, parametros):
        super().validar(parametros)
        if parametros["porcentaje"] > 100:
            raise ValidationError("El porcetaje no puede pasar de 100")


TIPOS = {
    "tiempo": Tiempo(),
    "edad": Edad(),
    "licencias": Licencias(),
    "temario": Temario(),
}
OPCIONES = [(tipo, requisito.texto) for tipo, requisito in TIPOS.items()]

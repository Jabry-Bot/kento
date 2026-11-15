from django.contrib import admin

from .models import *


class RequisitoInline(admin.TabularInline):
    model = Requisito
    extra = 0


class ObjetivoInline(admin.TabularInline):
    model = Objetivo
    extra = 0


@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    inlines = [RequisitoInline, ObjetivoInline]


class ResultadoBloqueInline(admin.TabularInline):
    model = ResultadoBloque
    extra = 0


@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    inlines = [ResultadoBloqueInline]


admin.site.register(ArteMarcial)
admin.site.register(Disciplina)
admin.site.register(Bloque)
admin.site.register(Requisito)
admin.site.register(Objetivo)
admin.site.register(Licencia)
admin.site.register(DisciplinaAlumno)
admin.site.register(Progreso)
admin.site.register(HistorialGrado)

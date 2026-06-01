from django.contrib import admin

from .models import Agendamento, Motorista


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'nome',
        'telefone',
    )

    search_fields = (
        'nome',
        'telefone',
    )

    ordering = (
        'nome',
    )


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'motorista',
        'status',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'motorista__nome',
    )

    ordering = (
        '-id',
    )
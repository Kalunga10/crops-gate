from django.urls import path

from . import views
from usuarios.views import alterar_senha


urlpatterns = [

    path(
        '',
        views.agendamentos,
        name='agendamentos'
    ),

    path(
        'criar/',
        views.criar_agendamento,
        name='criar_agendamento'
    ),

    path(
        'listar/',
        views.listar_agendamentos_usuarios,
        name='listar_agendamentos_usuarios'
    ),

    path(
        'detalhar/<int:id>/',
        views.detalhar_agendamento,
        name='detalhar_agendamento'
    ),

    path(
        'cancelar/<int:id>/',
        views.cancelar_agendamento,
        name='cancelar_agendamento'
    ),

    path(
    'buscar-motorista/',
    views.buscar_motorista,
    name='buscar_motorista'
),


    path(
        'alterar-senha/',
        alterar_senha,
        name='alterar_senha'
),


]

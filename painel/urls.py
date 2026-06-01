
from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.painel_view,
        name='painel'
    ),

    path(
        'agendamentos/',
        views.painel_agendamentos,
        name='painel_agendamentos'
    ),

    path(
        'ajax/agendamentos/',
        views.listar_agendamentos,
        name='listar_agendamentos'
    ),

    path(
        'ajax/alterar-status/',
        views.alterar_status_agendamento,
        name='alterar_status_agendamento'
    ),

]

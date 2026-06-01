
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from agendamentos.models import Agendamento


# =====================================
# HOME PAINEL
# =====================================

@login_required
def painel_view(request):

    return render(
        request,
        'painel/painel.html'
    )


# =====================================
# AGENDAMENTOS
# =====================================

@login_required
def painel_agendamentos(request):

    return render(
        request,
        'painel/agendamentos.html'
    )


# =====================================
# AJAX LISTAR AGENDAMENTOS
# =====================================

@login_required
def listar_agendamentos(request):

    status = request.GET.get('status')
    busca = request.GET.get('busca')

    agendamentos = Agendamento.objects.select_related(
        'motorista'
    ).only(

        'id',
        'status',
        'placa_cavalo',
        'local_descarga',
        'observacao',

        'data_opcao_1',
        'horario_opcao_1',

        'data_opcao_2',
        'horario_opcao_2',

        'data_opcao_3',
        'horario_opcao_3',

        'data_cadastro',

        'motorista__nome',
        'motorista__cpf',
        'motorista__telefone',

    ).order_by('data_cadastro')

    # =====================================
    # FILTRO STATUS
    # =====================================

    if status:

        agendamentos = agendamentos.filter(
            status=status
        )

    # =====================================
    # FILTRO BUSCA
    # =====================================

    if busca:

        agendamentos = agendamentos.filter(
            motorista__nome__icontains=busca
        ) | agendamentos.filter(
            placa_cavalo__icontains=busca
        )

    # =====================================
    # DADOS
    # =====================================

    dados = []

    for item in agendamentos:

        dados.append({

            'id': item.id,

            'status': item.status,

            'nome_motorista': item.motorista.nome,

            'cpf_motorista': item.motorista.cpf,

            'telefone_motorista': item.motorista.telefone,

            'placa_cavalo': item.placa_cavalo,

            'local_descarga': item.get_local_descarga_display(),

            'observacao': item.observacao or '',

            'data_opcao_1': (
                item.data_opcao_1.strftime('%d/%m/%Y')
                if item.data_opcao_1 else ''
            ),

            'horario_opcao_1': (
                item.horario_opcao_1.strftime('%H:%M')
                if item.horario_opcao_1 else ''
            ),

            'data_opcao_2': (
                item.data_opcao_2.strftime('%d/%m/%Y')
                if item.data_opcao_2 else ''
            ),

            'horario_opcao_2': (
                item.horario_opcao_2.strftime('%H:%M')
                if item.horario_opcao_2 else ''
            ),

            'data_opcao_3': (
                item.data_opcao_3.strftime('%d/%m/%Y')
                if item.data_opcao_3 else ''
            ),

            'horario_opcao_3': (
                item.horario_opcao_3.strftime('%H:%M')
                if item.horario_opcao_3 else ''
            ),

            'data_cadastro': item.data_cadastro.strftime('%d/%m/%Y'),

            'hora_cadastro': item.data_cadastro.strftime('%H:%M'),

            'mensagem_operacional': item.mensagem_operacional or '',

            'motivo_alteracao_status': item.motivo_alteracao_status or '',

        })

    return JsonResponse({

        'success': True,

        'agendamentos': dados

    })

from django.utils import timezone


# =====================================
# ALTERAR STATUS
# =====================================

@login_required
@require_POST
def alterar_status_agendamento(request):

    agendamento_id = request.POST.get('id')

    novo_status = request.POST.get('status')

    mensagem_operacional = request.POST.get(
        'mensagem_operacional',
        ''
    )

    motivo_alteracao_status = request.POST.get(
        'motivo_alteracao_status',
        ''
    )

    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id
    )

    # =====================================
    # VALIDA STATUS RECEBIDO
    # =====================================

    status_validos = [

        'ABERTO',
        'EM_ANALISE',
        'FINALIZADO'

    ]

    if novo_status not in status_validos:

        return JsonResponse({

            'success': False,

            'message': 'Status inválido.'

        })

    # =====================================
    # STATUS ATUAL
    # =====================================

    status_atual = agendamento.status

    # =====================================
    # REGRAS DE NEGÓCIO
    # =====================================

    if status_atual == 'ABERTO':

        permitidos = [

            'ABERTO',
            'EM_ANALISE',
            'FINALIZADO'

        ]

    elif status_atual == 'EM_ANALISE':

        permitidos = [

            'EM_ANALISE',
            'FINALIZADO'

        ]

    elif status_atual == 'FINALIZADO':

        permitidos = [

            'FINALIZADO'

        ]

    else:

        return JsonResponse({

            'success': False,

            'message': 'Status atual inválido.'

        })

    # =====================================
    # VALIDA TRANSIÇÃO
    # =====================================

    if novo_status not in permitidos:

        return JsonResponse({

            'success': False,

            'message': (
                f'Não é permitido alterar '
                f'{status_atual} para {novo_status}.'
            )

        })

    # =====================================
    # SALVA ALTERAÇÕES
    # =====================================

    agendamento.status = novo_status

    agendamento.mensagem_operacional = (
        mensagem_operacional
    )

    agendamento.motivo_alteracao_status = (
        motivo_alteracao_status
    )

    agendamento.usuario_ultima_alteracao = (
        request.user
    )

    agendamento.data_ultima_alteracao = (
        timezone.now()
    )

    agendamento.save()

    return JsonResponse({

        'success': True,

        'message': 'Status atualizado com sucesso.'

    })
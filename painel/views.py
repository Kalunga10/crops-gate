from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone

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

    # Compatível com Select2 múltiplo
    locais_filtro = (
        request.GET.getlist('local')
        or request.GET.getlist('local[]')
    )

    motorista = request.GET.get('motorista')
    placa = request.GET.get('placa')

    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    agendamentos = (
        Agendamento.objects
        .select_related('motorista')
        .order_by('data_cadastro')
    )

    # =====================================
    # DEBUG (remover depois)
    # =====================================

    #print('GET:', request.GET)
    #print('LOCAIS FILTRO:', locais_filtro)

    # =====================================
    # FILTRO STATUS
    # =====================================

    if status:

        agendamentos = agendamentos.filter(
            status=status
        )

    # =====================================
    # FILTRO BUSCA GERAL
    # =====================================

    if busca:

        agendamentos = agendamentos.filter(

            Q(motorista__nome__icontains=busca) |

            Q(placa_cavalo__icontains=busca)

        )

    # =====================================
    # FILTRO LOCAL (MÚLTIPLO)
    # =====================================

    if locais_filtro:

        agendamentos = agendamentos.filter(
            local_descarga__in=locais_filtro
        )

    # =====================================
    # FILTRO MOTORISTA
    # =====================================

    if motorista:

        agendamentos = agendamentos.filter(
            motorista__nome__icontains=motorista
        )

    # =====================================
    # FILTRO PLACA
    # =====================================

    if placa:

        agendamentos = agendamentos.filter(
            placa_cavalo__icontains=placa
        )

    # =====================================
    # FILTRO PERÍODO
    # =====================================

    if data_inicial:

        agendamentos = agendamentos.filter(
            data_cadastro__date__gte=data_inicial
        )

    if data_final:

        agendamentos = agendamentos.filter(
            data_cadastro__date__lte=data_final
        )

    # =====================================
    # LOCAIS PARA O SELECT2
    # =====================================

    locais = [

        {
            'valor': valor,
            'texto': descricao
        }

        for valor, descricao
        in Agendamento.LOCAIS_CHOICES

    ]

    # =====================================
    # DADOS
    # =====================================

    dados = []

    for item in agendamentos:

        motorista_obj = item.motorista

        dados.append({

            'id': item.id,

            'status': item.status,

            'nome_motorista':
                motorista_obj.nome if motorista_obj else '',

            'cpf_motorista':
                motorista_obj.cpf if motorista_obj else '',

            'telefone_motorista':
                motorista_obj.telefone if motorista_obj else '',

            'placa_cavalo':
                item.placa_cavalo or '',

            'local_descarga':
                item.local_descarga or '',

            'local_descarga_display':
                item.get_local_descarga_display(),

            'observacao':
                item.observacao or '',

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

            'data_cadastro':
                item.data_cadastro.strftime('%d/%m/%Y'),

            'hora_cadastro':
                item.data_cadastro.strftime('%H:%M'),

            'mensagem_operacional':
                item.mensagem_operacional or '',

            'motivo_alteracao_status':
                item.motivo_alteracao_status or '',
            
            'data_ultima_alteracao': (

                item.data_ultima_alteracao.strftime(
                    '%d/%m/%Y %H:%M'
                )

                if item.data_ultima_alteracao

                else ''

            )

        })

    return JsonResponse({

        'success': True,

        'total': len(dados),

        'agendamentos': dados,

        'locais': locais

    })


# =====================================
# ALTERAR STATUS
# =====================================

@login_required
@require_POST
def alterar_status_agendamento(request):

    agendamento_id = request.POST.get('id')
    novo_status = request.POST.get('status')

    mensagem_operacional = request.POST.get(
        'mensagem_operacional', ''
    )

    motivo_alteracao_status = request.POST.get(
        'motivo_alteracao_status', ''
    )

    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id
    )

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

    status_atual = agendamento.status

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

    if novo_status not in permitidos:

        return JsonResponse({
            'success': False,
            'message': (
                f'Não é permitido alterar '
                f'{status_atual} para {novo_status}.'
            )
        })

    agendamento.status = novo_status
    agendamento.mensagem_operacional = mensagem_operacional
    agendamento.motivo_alteracao_status = motivo_alteracao_status
    agendamento.usuario_ultima_alteracao = request.user
    agendamento.data_ultima_alteracao = timezone.now()

    agendamento.save()

    return JsonResponse({
        'success': True,
        'message': 'Status atualizado com sucesso.'
    })

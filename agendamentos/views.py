from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Agendamento, Motorista


# =====================================================
# TELA
# =====================================================

@login_required
def agendamentos(request):

    return render(
        request,
        'agendamentos/agendamentos.html'
    )


# =====================================================
# CRIAR AGENDAMENTO AJAX
# =====================================================

@login_required
@require_POST
def criar_agendamento(request):

    try:

        # =====================================================
        # DADOS MOTORISTA
        # =====================================================

        cpf = request.POST.get('cpf')

        nome_motorista = request.POST.get('nome_motorista')

        telefone = request.POST.get('telefone')

        # =====================================================
        # CRIA OU BUSCA MOTORISTA
        # =====================================================

        motorista, created = Motorista.objects.get_or_create(

            cpf=cpf,

            defaults={

                'nome': nome_motorista,

                'telefone': telefone

            }

        )

        # =====================================================
        # ATUALIZA DADOS
        # =====================================================

        if not created:

            motorista.nome = nome_motorista

            motorista.telefone = telefone

            motorista.save()

        # =====================================================
        # CRIA AGENDAMENTO
        # =====================================================

        agendamento = Agendamento.objects.create(

            solicitante=request.user,

            motorista=motorista,

            local_descarga=request.POST.get('local_descarga'),

            placa_cavalo=request.POST.get('placa_cavalo'),

            observacao=request.POST.get('observacao'),

            data_opcao_1=request.POST.get('data_opcao_1'),

            horario_opcao_1=request.POST.get('horario_opcao_1'),

            data_opcao_2=request.POST.get('data_opcao_2') or None,

            horario_opcao_2=request.POST.get('horario_opcao_2') or None,

            data_opcao_3=request.POST.get('data_opcao_3') or None,

            horario_opcao_3=request.POST.get('horario_opcao_3') or None,

        )

        # =====================================================
        # SUCESSO
        # =====================================================

        return JsonResponse({

            'success': True,

            'message': 'Solicitação enviada com sucesso.',

            'id': agendamento.id,

            'status': agendamento.status

        })

    except Exception as erro:

        return JsonResponse({

            'success': False,

            'message': str(erro)

        })


# =====================================================
# LISTAR AGENDAMENTOS
# =====================================================

@login_required
def listar_agendamentos(request):

    agendamentos = Agendamento.objects.filter(

        solicitante=request.user

    ).select_related(

        'motorista'

    )

    dados = []

    for item in agendamentos:

        dados.append({

            'id': item.id,

            'motorista': item.motorista.nome,

            'cpf': item.motorista.cpf,

            'telefone': item.motorista.telefone,

            'placa': item.placa_cavalo,

            'local_descarga': item.get_local_descarga_display(),

            'status': item.status,

            'data_cadastro': item.data_cadastro.strftime('%d/%m/%Y %H:%M'),

            'data_opcao_1': item.data_opcao_1.strftime('%d/%m/%Y'),

            'horario_opcao_1': str(item.horario_opcao_1),

            'usuario_logado': request.user.username,

        })

    return JsonResponse({

        'success': True,

        'data': dados

    })


# =====================================================
# DETALHAR AGENDAMENTO
# =====================================================

@login_required
def detalhar_agendamento(request, id):

    try:

        item = Agendamento.objects.select_related(

            'motorista'

        ).get(

            id=id,
            solicitante=request.user

        )

        return JsonResponse({

            'success': True,

            'data': {

                'id': item.id,

                'motorista': item.motorista.nome,

                'cpf': item.motorista.cpf,

                'telefone': item.motorista.telefone,

                'placa': item.placa_cavalo,

                'local_descarga': item.get_local_descarga_display(),

                'status': item.status,

                'observacao': item.observacao,

                'data_cadastro': item.data_cadastro.strftime('%d/%m/%Y %H:%M'),

            }

        })

    except Agendamento.DoesNotExist:

        return JsonResponse({

            'success': False,

            'message': 'Agendamento não encontrado.'

        })


# =====================================================
# CANCELAR AGENDAMENTO
# =====================================================

@login_required
@require_POST
def cancelar_agendamento(request, id):

    try:

        agendamento = Agendamento.objects.get(

            id=id,
            solicitante=request.user

        )

        agendamento.status = 'RECUSADO'

        agendamento.save()

        return JsonResponse({

            'success': True,

            'message': 'Agendamento cancelado.'

        })

    except Agendamento.DoesNotExist:

        return JsonResponse({

            'success': False,

            'message': 'Agendamento não encontrado.'

        })
    
# =====================================================
# BUSCAR MOTORISTA
# =====================================================

@login_required
def buscar_motorista(request):

    cpf = request.GET.get('cpf')

    try:

        motorista = Motorista.objects.get(cpf=cpf)

        return JsonResponse({

            'success': True,

            'nome': motorista.nome,

            'telefone': motorista.telefone

        })

    except Motorista.DoesNotExist:

        return JsonResponse({

            'success': False

        })
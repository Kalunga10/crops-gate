from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction
import logging
import re
from usuarios.decorators import perfil_requerido
from .models import Agendamento, Motorista

logger = logging.getLogger(__name__)


def limpar_cpf(cpf):
    return re.sub(r"\D", "", cpf or "")


@login_required
@perfil_requerido('CLASSIFICADOR')
def agendamentos(request):
    return render(request, "agendamentos/agendamentos.html")


@login_required
@require_POST
@transaction.atomic
@perfil_requerido('CLASSIFICADOR')
def criar_agendamento(request):
    try:
        cpf = limpar_cpf(request.POST.get("cpf"))
        nome_motorista = request.POST.get("nome_motorista", "").strip()
        telefone = request.POST.get("telefone", "").strip()
        local_descarga = request.POST.get("local_descarga")
        placa_cavalo = request.POST.get("placa_cavalo", "").strip().upper()

        data_opcao_1 = request.POST.get("data_opcao_1")
        horario_opcao_1 = request.POST.get("horario_opcao_1")

        if not cpf:
            return JsonResponse({"success": False, "message": "CPF é obrigatório."}, status=400)

        if not nome_motorista:
            return JsonResponse({"success": False, "message": "Nome do motorista é obrigatório."}, status=400)

        if not placa_cavalo:
            return JsonResponse({"success": False, "message": "Placa do veículo é obrigatória."}, status=400)

        if not local_descarga:
            return JsonResponse({"success": False, "message": "Local de descarga é obrigatório."}, status=400)

        if not data_opcao_1:
            return JsonResponse({"success": False, "message": "Data da opção 1 é obrigatória."}, status=400)

        if not horario_opcao_1:
            return JsonResponse({"success": False, "message": "Horário da opção 1 é obrigatório."}, status=400)

        motorista, created = Motorista.objects.get_or_create(
            cpf=cpf,
            defaults={
                "nome": nome_motorista,
                "telefone": telefone,
            },
        )

        if not created:
            motorista.nome = nome_motorista
            motorista.telefone = telefone
            motorista.save()

        agendamento = Agendamento.objects.create(
            solicitante=request.user,
            motorista=motorista,
            local_descarga=local_descarga,
            placa_cavalo=placa_cavalo,
            observacao=request.POST.get("observacao"),
            data_opcao_1=data_opcao_1,
            horario_opcao_1=horario_opcao_1,
            data_opcao_2=request.POST.get("data_opcao_2") or None,
            horario_opcao_2=request.POST.get("horario_opcao_2") or None,
            data_opcao_3=request.POST.get("data_opcao_3") or None,
            horario_opcao_3=request.POST.get("horario_opcao_3") or None,
        )

        return JsonResponse({
            "success": True,
            "message": "Solicitação enviada com sucesso.",
            "id": agendamento.id,
            "status": agendamento.status,
        })

    except Exception:
        logger.exception("Erro ao criar agendamento")
        return JsonResponse(
            {"success": False, "message": "Erro interno do servidor."},
            status=500,
        )


@login_required
@perfil_requerido('CLASSIFICADOR')
def listar_agendamentos_usuarios(request):
    agendamentos = (
        Agendamento.objects.filter(solicitante=request.user)
        .select_related("motorista")
        .order_by("data_cadastro")
    )

    dados = []

    for item in agendamentos:
        dados.append({
            "id": item.id,
            "nome_motorista": item.motorista.nome,
            "cpf_motorista": item.motorista.cpf,
            "telefone_motorista": item.motorista.telefone,
            "placa_cavalo": item.placa_cavalo,
            "local_descarga": item.get_local_descarga_display(),
            "status": item.status,
            "data_cadastro": item.data_cadastro.strftime("%d/%m/%Y %H:%M"),
            "data_opcao_1": item.data_opcao_1.strftime("%d/%m/%Y"),
            "horario_opcao_1": item.horario_opcao_1.strftime("%H:%M"),
            "usuario_logado": request.user.username,
        })

    return JsonResponse({
        "success": True,
        "agendamentos": dados
    })


@login_required
@perfil_requerido('CLASSIFICADOR')
def detalhar_agendamento(request, id):
    
    try:
        item = Agendamento.objects.select_related("motorista").get(
            id=id,
            solicitante=request.user,
        )

        return JsonResponse({
            "success": True,
            "data": {
                "id": item.id,
                "nome_motorista": item.motorista.nome,
                "cpf_motorista": item.motorista.cpf,
                "telefone_motorista": item.motorista.telefone,
                "placa_cavalo": item.placa_cavalo,
                "local_descarga": item.get_local_descarga_display(),
                "status": item.status,
                "observacao": item.observacao,
                "data_cadastro": item.data_cadastro.strftime("%d/%m/%Y %H:%M"),
            },
        })

    except Agendamento.DoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Agendamento não encontrado."},
            status=404,
        )


@login_required
@require_POST
@perfil_requerido('CLASSIFICADOR')
def cancelar_agendamento(request, id):
    try:
        agendamento = Agendamento.objects.get(
            id=id,
            solicitante=request.user,
        )

        if agendamento.status == "FINALIZADO":
            return JsonResponse(
                {"success": False, "message": "Agendamento já finalizado."},
                status=400,
            )

        agendamento.delete()

        return JsonResponse({
            "success": True,
            "message": "Agendamento cancelado.",
        })

    except Agendamento.DoesNotExist:
        return JsonResponse(
            {"success": False, "message": "Agendamento não encontrado."},
            status=404,
        )


@login_required
@perfil_requerido('CLASSIFICADOR')
def buscar_motorista(request):
    cpf = limpar_cpf(request.GET.get("cpf"))

    try:
        motorista = Motorista.objects.get(cpf=cpf)

        return JsonResponse({
            "success": True,
            "nome": motorista.nome,
            "telefone": motorista.telefone,
        })

    except Motorista.DoesNotExist:
        return JsonResponse({"success": False})

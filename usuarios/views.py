from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# =====================================================
# REDIRECIONAR USUÁRIO
# =====================================================

def redirecionar_usuario(user):

    try:

        perfil = user.perfilusuario.perfil

        # =============================================
        # CLASSIFICADOR
        # =============================================

        if perfil == 'CLASSIFICADOR':

            return redirect('/agendamentos/')

        # =============================================
        # CONSULTOR
        # =============================================

        elif perfil == 'CONSULTOR':

            return redirect('/painel/')

        # =============================================
        # COORDENADOR
        # =============================================

        elif perfil == 'COORDENADOR':

            return redirect('/gestao/')

        # =============================================
        # PERFIL INVÁLIDO
        # =============================================

        return None

    except Exception:

        return None


# =====================================================
# LOGIN
# =====================================================

def login_view(request):

    # =========================================
    # USUÁRIO JÁ LOGADO
    # =========================================

    if request.user.is_authenticated:

        redirect_response = redirecionar_usuario(
            request.user
        )

        if redirect_response:

            return redirect_response

        logout(request)

        messages.error(
            request,
            'Perfil de usuário não encontrado.'
        )

        return redirect('/login/')

    # =========================================
    # POST
    # =========================================

    if request.method == 'POST':

        username = request.POST.get('usuario')
        password = request.POST.get('senha')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # =====================================
        # LOGIN OK
        # =====================================

        if user is not None:

            login(request, user)

            redirect_response = redirecionar_usuario(
                user
            )

            if redirect_response:

                return redirect_response

            logout(request)

            messages.error(
                request,
                'Usuário sem perfil cadastrado.'
            )

            return redirect('/login/')

        # =====================================
        # LOGIN INVÁLIDO
        # =====================================

        messages.error(
            request,
            'Usuário ou senha inválidos.'
        )

        return redirect('/login/')

    # =========================================
    # GET
    # =========================================

    return render(
        request,
        'login.html'
    )

@login_required
def alterar_senha(request):

    if request.method != 'POST':

        return JsonResponse({
            'success': False,
            'message': 'Método não permitido.'
        })

    senha_atual = request.POST.get('senha_atual')
    nova_senha = request.POST.get('nova_senha')
    confirmar_senha = request.POST.get('confirmar_senha')

    # ==============================
    # VALIDAR SENHA ATUAL
    # ==============================

    if not request.user.check_password(senha_atual):

        return JsonResponse({
            'success': False,
            'message': 'Senha atual incorreta.'
        })

    # ==============================
    # CONFIRMAR SENHAS
    # ==============================

    if nova_senha != confirmar_senha:

        return JsonResponse({
            'success': False,
            'message': 'As novas senhas não conferem.'
        })

    # ==============================
    # TAMANHO MÍNIMO
    # ==============================

    if len(nova_senha) < 6:

        return JsonResponse({
            'success': False,
            'message': 'A nova senha deve possuir pelo menos 6 caracteres.'
        })

    # ==============================
    # ALTERAR SENHA
    # ==============================

    request.user.set_password(
        nova_senha
    )

    request.user.save()

    # mantém o usuário logado
    update_session_auth_hash(
        request,
        request.user
    )

    return JsonResponse({
        'success': True,
        'message': 'Senha alterada com sucesso.'
    })





# =====================================================
# LOGOUT
# =====================================================
@require_POST
def logout_view(request):

    logout(request)

    return redirect('/login/')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST


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

        else:

            return None

    except:

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

        else:

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


# =====================================================
# LOGOUT
# =====================================================

@require_POST
def logout_view(request):

    logout(request)

    return redirect('/login/')
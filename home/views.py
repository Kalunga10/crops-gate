from django.shortcuts import render, redirect

from django.contrib import messages

from django.contrib.auth import authenticate, login


def login_view(request):

    if request.user.is_authenticated:

        return redirect('/agendamentos/')

    if request.method == 'POST':

        usuario = request.POST.get('usuario')

        senha = request.POST.get('senha')

        user = authenticate(

            request,

            username=usuario,

            password=senha

        )

        if user is not None:

            login(request, user)

            return redirect('/agendamentos/')

        else:

            messages.error(

                request,

                'Usuário ou senha inválidos'

            )

            return redirect('login')

    return render(request, 'login.html')
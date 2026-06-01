from django.contrib import admin
from django.urls import path, include

from usuarios.views import login_view, logout_view


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        login_view,
        name='login'
    ),

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'agendamentos/',
        include('agendamentos.urls')
    ),
    
    path('painel/', include('painel.urls')),
]
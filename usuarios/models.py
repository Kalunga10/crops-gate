from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):

    TIPO_USUARIO = [

        ('CLASSIFICADOR', 'Classificador'),

        ('CONSULTOR', 'Consultor'),

        ('COORDENADOR', 'Coordenador'),

    ]

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE

    )

    perfil = models.CharField(

        max_length=20,

        choices=TIPO_USUARIO

    )

    def __str__(self):

        return self.user.username
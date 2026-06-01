from django.db import models


class Motorista(models.Model):

    nome = models.CharField(
        max_length=200
    )

    cpf = models.CharField(
        max_length=14,
        unique=True
    )

    telefone = models.CharField(
        max_length=20
    )

    def __str__(self):

        return self.nome
from django.db import models
from django.contrib.auth.models import User


# ==========================================
# MOTORISTA
# ==========================================

class Motorista(models.Model):

    cpf = models.CharField(
        max_length=14,
        unique=True
    )

    nome = models.CharField(
        max_length=150
    )

    telefone = models.CharField(
        max_length=20
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f'{self.nome} - {self.cpf}'


# ==========================================
# AGENDAMENTO
# ==========================================

class Agendamento(models.Model):

    STATUS_CHOICES = [

        ('ABERTO', 'Aberto'),
        ('EM_ANALISE', 'Em Análise'),
        ('FINALIZADO', 'Finalizado'),

    ]

    LOCAIS_CHOICES = [

        ('TIPN', '1 - TIPN | Porto Nacional'),
        ('TIP', '2 - TIP | Palmeirante'),
        ('TIUB', '3 - TIUB | Uberaba'),
        ('TRO', '4 - TRO | Terminal Rumo Rondonópolis'),
        ('TSS', '5 - TSS | Terminal Rumo São Simão'),
        ('TRV', '6 - TRV | Terminal Rumo Rio Verde'),
        ('TGG', '7 - TGG | Terminal de Guarujá'),
        ('BRF_RV', '8 - BRF - Rio Verde'),
        ('BRF_UB', '9 - BRF - Uberlândia'),
        ('BRF_CN', '10 - BRF - Campos Novos'),
        ('BRF_AM', '11 - BRF - Arroio do Meio'),
        ('BRF_CH', '12 - BRF - Chapecó'),
        ('BUNGE', '13 - Bunge - Maringá'),
        ('SFS', '14 - São Francisco do Sul'),
        ('TGRAO', '15 - Terminal T-Grão'),
        ('ROLANDIA', '16 - Rolândia'),
        ('PINHALZINHO', '17 - Pinhalzinho'),
        ('PARANAGUA', '18 - Paranaguá'),
        ('BARCARENA', '19 - Barcarena'),
        ('ITAITUBA', '20 - Itaituba'),
        ('OUTRO', '21 - Outro'),

    ]

    # ==========================================
    # SOLICITANTE
    # ==========================================

    solicitante = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    # ==========================================
    # MOTORISTA
    # ==========================================

    motorista = models.ForeignKey(
        'Motorista',
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    # ==========================================
    # DADOS VIAGEM
    # ==========================================

    local_descarga = models.CharField(
        max_length=30,
        choices=LOCAIS_CHOICES
    )

    placa_cavalo = models.CharField(
        max_length=8
    )

    observacao = models.TextField(
        blank=True,
        null=True
    )

    # ==========================================
    # OPÇÃO 1
    # ==========================================

    data_opcao_1 = models.DateField()

    horario_opcao_1 = models.TimeField()

    # ==========================================
    # OPÇÃO 2
    # ==========================================

    data_opcao_2 = models.DateField(
        blank=True,
        null=True
    )

    horario_opcao_2 = models.TimeField(
        blank=True,
        null=True
    )

    # ==========================================
    # OPÇÃO 3
    # ==========================================

    data_opcao_3 = models.DateField(
        blank=True,
        null=True
    )

    horario_opcao_3 = models.TimeField(
        blank=True,
        null=True
    )

    # ==========================================
    # STATUS
    # ==========================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ABERTO',
        db_index=True
    )

    # ==========================================
    # CONTROLE OPERACIONAL
    # ==========================================

    mensagem_operacional = models.TextField(
        blank=True,
        null=True
    )

    motivo_alteracao_status = models.TextField(
        blank=True,
        null=True
    )

    usuario_ultima_alteracao = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='agendamentos_alterados'
    )

    data_ultima_alteracao = models.DateTimeField(
        null=True,
        blank=True
    )

    # ==========================================
    # DATA CADASTRO
    # ==========================================

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    # ==========================================
    # META
    # ==========================================

    class Meta:

        ordering = ['data_cadastro']

        verbose_name = 'Agendamento'

        verbose_name_plural = 'Agendamentos'

    # ==========================================
    # STRING
    # ==========================================

    def __str__(self):

        return f'{self.motorista.nome} - {self.placa_cavalo}'
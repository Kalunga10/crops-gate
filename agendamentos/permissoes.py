def is_classificador(user):

    return user.groups.filter(
        name='CLASSIFICADOR'
    ).exists()


def is_consultor(user):

    return user.groups.filter(
        name='CONSULTOR'
    ).exists()


def is_coordenador(user):

    return user.groups.filter(
        name='COORDENADOR'
    ).exists()


def pode_criar_agendamento(user):

    return (

        is_classificador(user)

        or

        is_coordenador(user)

    )


def pode_alterar_status(user):

    return (

        is_consultor(user)

        or

        is_coordenador(user)

    )
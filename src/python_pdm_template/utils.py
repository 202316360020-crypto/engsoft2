"""
Este módulo contém funções utilitárias para o projeto.

Funções:
- somar: Retorna a soma de dois números.
- obter_mensagem: Retorna uma mensagem fornecida pelo usuário.
"""


def somar(a: int | float, b: int | float):
    """
    Retorna a soma de dois números.

    Args:
        a: Primeiro número.
        b: Segundo número.

    Returns:
        int | float: soma de a e b.
    """
    return a + b


def obter_mensagem():
    """
    Retorna uma mensagem de exemplo.

    Returns:
        str: mensagem digitada pelo usuário.
    """
    return input("Digite uma mensagem: ")

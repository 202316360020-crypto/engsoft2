"""
Este módulo contém funções utilitárias para o projeto.

Funções:
- somar: Retorna a soma de dois números.
- obter_mensagem: Retorna uma mensagem fornecida pelo usuário.
"""


def somar(a: int | float, b: int | float):
    """
    Retorna a soma de dois números.

    :param a: Primeiro número.
    :param b: Segundo número.
    :return: A soma de a e b.
    """
    return a + b


def obter_mensagem():
    """
    Retorna uma mensagem de exemplo.

    :return: A mensagem fornecida pelo usuário.
    """
    return input("Digite uma mensagem: ")

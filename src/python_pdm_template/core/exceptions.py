"""Exceções de domínio da QuantInvest Suite."""


class QuantInvestError(Exception):
    """Exceção base do domínio."""


class InvalidCSVError(QuantInvestError):
    """Arquivo CSV inválido ou ilegível."""


class MissingColumnsError(QuantInvestError):
    """Colunas obrigatórias ausentes no CSV."""


class OutOfOrderDatesError(QuantInvestError):
    """Datas fora de ordem cronológica ou duplicadas."""


class BankruptcyError(QuantInvestError):
    """Capital insuficiente para continuar a simulação."""
"""Métricas financeiras da QuantInvest Suite."""

from __future__ import annotations


def calculate_max_drawdown(equity_curve: list[float]) -> float:
    """Calcula o maior drawdown percentual da curva de capital."""
    if not equity_curve:
        raise ValueError("A curva de capital não pode ser vazia.")

    peak = equity_curve[0]
    max_drawdown = 0.0

    for value in equity_curve:
        peak = max(peak, value)
        if peak <= 0:
            continue
        drawdown = (peak - value) / peak * 100
        max_drawdown = max(max_drawdown, drawdown)

    return max_drawdown


def calculate_win_rate(operations: list[dict]) -> float:
    """Calcula a taxa de acerto em porcentagem."""
    if not operations:
        raise ValueError("A lista de operações não pode ser vazia.")

    winning_operations = sum(1 for operation in operations if float(operation.get("profit", 0.0)) > 0)
    return winning_operations / len(operations) * 100


def calculate_return(initial_capital: float, final_balance: float) -> float:
    """Calcula o retorno percentual total."""
    if initial_capital <= 0:
        raise ValueError("O capital inicial deve ser estritamente positivo.")

    return (final_balance - initial_capital) / initial_capital * 100
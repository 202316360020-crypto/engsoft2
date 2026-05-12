"""
Testes unitários — Métricas financeiras (core/metrics.py)

Cobre:
- Cálculo de Max Drawdown
- Cálculo de taxa de acerto
- Cálculo de retorno total
- Casos extremos (série vazia, saldo constante)
"""

import pytest
import pandas as pd


# ---------------------------------------------------------------------------
# Stubs para TDD — substitua pelo import real:
#   from core.metrics import calculate_max_drawdown, calculate_win_rate, calculate_return
# ---------------------------------------------------------------------------

def calculate_max_drawdown(equity_curve: list[float]) -> float:
    """
    Stub: calcula o Max Drawdown percentual de uma curva de capital.
    Fórmula: max((peak - trough) / peak) ao longo de toda a série.
    """
    raise NotImplementedError("Implemente calculate_max_drawdown() em core/metrics.py")


def calculate_win_rate(operations: list[dict]) -> float:
    """
    Stub: calcula a taxa de acerto.
    Cada operação deve ter a chave 'profit' (float).
    """
    raise NotImplementedError("Implemente calculate_win_rate() em core/metrics.py")


def calculate_return(initial_capital: float, final_balance: float) -> float:
    """Stub: retorno percentual = (final - inicial) / inicial * 100."""
    raise NotImplementedError("Implemente calculate_return() em core/metrics.py")


# ---------------------------------------------------------------------------
# Testes — Max Drawdown
# ---------------------------------------------------------------------------

class TestMaxDrawdown:
    """Valida o cálculo de Max Drawdown (maior queda percentual do pico)."""

    def test_constant_equity_has_zero_drawdown(self):
        equity = [10_000.0] * 10
        try:
            dd = calculate_max_drawdown(equity)
            assert dd == pytest.approx(0.0)
        except NotImplementedError:
            pytest.skip("calculate_max_drawdown() ainda não implementada.")

    def test_monotonic_uptrend_has_zero_drawdown(self):
        equity = [10_000.0, 10_500.0, 11_000.0, 11_500.0, 12_000.0]
        try:
            dd = calculate_max_drawdown(equity)
            assert dd == pytest.approx(0.0)
        except NotImplementedError:
            pytest.skip("calculate_max_drawdown() ainda não implementada.")

    def test_simple_drawdown_calculated_correctly(self):
        # Sobe para 12000, cai para 9000 → drawdown = (12000-9000)/12000 = 25%
        equity = [10_000.0, 12_000.0, 9_000.0, 9_500.0]
        try:
            dd = calculate_max_drawdown(equity)
            assert dd == pytest.approx(25.0, rel=1e-3)
        except NotImplementedError:
            pytest.skip("calculate_max_drawdown() ainda não implementada.")

    def test_max_drawdown_picks_worst_peak_to_trough(self):
        # Dois drawdowns: 10% e 40% → deve retornar 40%
        equity = [10_000.0, 11_000.0, 9_900.0,   # drawdown 1: ~10%
                  12_000.0, 7_200.0]              # drawdown 2: 40%
        try:
            dd = calculate_max_drawdown(equity)
            assert dd == pytest.approx(40.0, rel=1e-2)
        except NotImplementedError:
            pytest.skip("calculate_max_drawdown() ainda não implementada.")

    def test_single_element_returns_zero(self):
        try:
            dd = calculate_max_drawdown([10_000.0])
            assert dd == pytest.approx(0.0)
        except NotImplementedError:
            pytest.skip("calculate_max_drawdown() ainda não implementada.")

    def test_empty_list_raises_value_error(self):
        try:
            with pytest.raises((ValueError, IndexError)):
                calculate_max_drawdown([])
        except NotImplementedError:
            pytest.skip("calculate_max_drawdown() ainda não implementada.")

    def test_drawdown_is_non_negative(self):
        equity = [10_000.0, 9_000.0, 8_000.0, 11_000.0]
        try:
            dd = calculate_max_drawdown(equity)
            assert dd >= 0.0
        except NotImplementedError:
            pytest.skip("calculate_max_drawdown() ainda não implementada.")


# ---------------------------------------------------------------------------
# Testes — Taxa de Acerto
# ---------------------------------------------------------------------------

class TestWinRate:
    """Valida o cálculo da taxa de acerto (% de operações lucrativas)."""

    def test_all_winning_trades_returns_100(self):
        ops = [{"profit": 100.0}, {"profit": 50.0}, {"profit": 200.0}]
        try:
            wr = calculate_win_rate(ops)
            assert wr == pytest.approx(100.0)
        except NotImplementedError:
            pytest.skip("calculate_win_rate() ainda não implementada.")

    def test_all_losing_trades_returns_zero(self):
        ops = [{"profit": -100.0}, {"profit": -50.0}]
        try:
            wr = calculate_win_rate(ops)
            assert wr == pytest.approx(0.0)
        except NotImplementedError:
            pytest.skip("calculate_win_rate() ainda não implementada.")

    def test_mixed_trades_returns_correct_percentage(self):
        # 2 ganhos, 1 perda, 1 empate (0) → 2/4 = 50%
        ops = [{"profit": 100.0}, {"profit": -50.0}, {"profit": 200.0}, {"profit": 0.0}]
        try:
            wr = calculate_win_rate(ops)
            assert wr == pytest.approx(50.0)
        except NotImplementedError:
            pytest.skip("calculate_win_rate() ainda não implementada.")

    def test_empty_operations_raises_value_error(self):
        try:
            with pytest.raises((ValueError, ZeroDivisionError)):
                calculate_win_rate([])
        except NotImplementedError:
            pytest.skip("calculate_win_rate() ainda não implementada.")

    def test_win_rate_is_between_0_and_100(self):
        ops = [{"profit": 50.0}, {"profit": -30.0}, {"profit": 20.0}]
        try:
            wr = calculate_win_rate(ops)
            assert 0.0 <= wr <= 100.0
        except NotImplementedError:
            pytest.skip("calculate_win_rate() ainda não implementada.")


# ---------------------------------------------------------------------------
# Testes — Retorno Total
# ---------------------------------------------------------------------------

class TestCalculateReturn:
    """Valida o cálculo de retorno percentual."""

    def test_profit_returns_positive_percentage(self):
        try:
            ret = calculate_return(10_000.0, 11_000.0)
            assert ret == pytest.approx(10.0)
        except NotImplementedError:
            pytest.skip("calculate_return() ainda não implementada.")

    def test_loss_returns_negative_percentage(self):
        try:
            ret = calculate_return(10_000.0, 8_000.0)
            assert ret == pytest.approx(-20.0)
        except NotImplementedError:
            pytest.skip("calculate_return() ainda não implementada.")

    def test_no_change_returns_zero(self):
        try:
            ret = calculate_return(10_000.0, 10_000.0)
            assert ret == pytest.approx(0.0)
        except NotImplementedError:
            pytest.skip("calculate_return() ainda não implementada.")

    def test_zero_initial_capital_raises_value_error(self):
        try:
            with pytest.raises((ValueError, ZeroDivisionError)):
                calculate_return(0.0, 1_000.0)
        except NotImplementedError:
            pytest.skip("calculate_return() ainda não implementada.")

    def test_negative_initial_capital_raises_value_error(self):
        try:
            with pytest.raises(ValueError):
                calculate_return(-1_000.0, 500.0)
        except NotImplementedError:
            pytest.skip("calculate_return() ainda não implementada.")

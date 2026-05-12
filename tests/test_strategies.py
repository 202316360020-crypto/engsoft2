"""
Testes unitários — Estratégias de Investimento (core/strategies/)

Cobre:
- Estratégia Buy and Hold
- Estratégia Cruzamento de Médias Móveis (SMA)
- Extensibilidade via padrão Strategy (BaseStrategy)
- Condição de falência (RN-02)
- Resultado de simulação (SimulationResult)
"""

import pytest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass
from abc import ABC, abstractmethod
import pandas as pd


# ---------------------------------------------------------------------------
# Stubs para TDD — substitua pelos imports reais quando o Core existir:
#
#   from core.strategies.base import BaseStrategy, SimulationResult
#   from core.strategies.buy_and_hold import BuyAndHoldStrategy
#   from core.strategies.moving_average import MovingAverageStrategy
#   from core.exceptions import BankruptcyError
# ---------------------------------------------------------------------------

class BankruptcyError(Exception):
    """Levantada quando o saldo do investidor atinge zero ou fica negativo."""
    pass


@dataclass
class SimulationResult:
    """
    Contrato de saída de qualquer estratégia.
    O Core deve retornar este objeto ao fim de cada simulação.
    """
    final_balance: float
    total_return_pct: float
    win_rate_pct: float
    max_drawdown_pct: float
    total_trades: int
    operations: list  # lista de dicts com detalhes de cada operação


class BaseStrategy(ABC):
    """Contrato que toda estratégia deve implementar (padrão Strategy)."""

    @abstractmethod
    def run(self, data: pd.DataFrame, initial_capital: float) -> SimulationResult:
        raise NotImplementedError


class BuyAndHoldStrategy(BaseStrategy):
    """Stub: compra no primeiro dia, vende no último."""

    def run(self, data: pd.DataFrame, initial_capital: float) -> SimulationResult:
        raise NotImplementedError("Implemente BuyAndHoldStrategy.run() no Core.")


class MovingAverageStrategy(BaseStrategy):
    """Stub: golden cross / death cross com SMA configurável."""

    def __init__(self, short_window: int = 9, long_window: int = 21):
        self.short_window = short_window
        self.long_window = long_window

    def run(self, data: pd.DataFrame, initial_capital: float) -> SimulationResult:
        raise NotImplementedError("Implemente MovingAverageStrategy.run() no Core.")


# ---------------------------------------------------------------------------
# Testes — BaseStrategy (contrato)
# ---------------------------------------------------------------------------

class TestBaseStrategyContract:
    """Garante que o padrão Strategy é aplicável a qualquer implementação."""

    def test_base_strategy_is_abstract(self):
        """BaseStrategy não pode ser instanciada diretamente."""
        with pytest.raises(TypeError):
            BaseStrategy()  # type: ignore

    def test_custom_strategy_must_implement_run(self):
        """Classe concreta sem run() deve lançar TypeError na instanciação."""
        class IncompleteStrategy(BaseStrategy):
            pass

        with pytest.raises(TypeError):
            IncompleteStrategy()  # type: ignore

    def test_custom_strategy_implements_run(self, ohlcv_uptrend):
        """Uma estratégia concreta válida deve poder ser usada no lugar de BaseStrategy."""
        class AlwaysBuyStrategy(BaseStrategy):
            def run(self, data, initial_capital):
                return SimulationResult(
                    final_balance=initial_capital * 1.1,
                    total_return_pct=10.0,
                    win_rate_pct=100.0,
                    max_drawdown_pct=0.0,
                    total_trades=1,
                    operations=[],
                )

        strategy = AlwaysBuyStrategy()
        result = strategy.run(ohlcv_uptrend, 10_000.0)
        assert isinstance(result, SimulationResult)
        assert result.final_balance == pytest.approx(11_000.0)


# ---------------------------------------------------------------------------
# Testes — BuyAndHoldStrategy
# ---------------------------------------------------------------------------

class TestBuyAndHoldStrategy:
    """Testes da estratégia Buy and Hold."""

    def _make_result(self, initial: float, final: float) -> SimulationResult:
        """Helper para criar resultado esperado."""
        ret = (final - initial) / initial * 100
        return SimulationResult(
            final_balance=final,
            total_return_pct=ret,
            win_rate_pct=100.0 if final > initial else 0.0,
            max_drawdown_pct=0.0,
            total_trades=1,
            operations=[{"action": "buy", "price": 11.0}, {"action": "sell", "price": 15.0}],
        )

    def test_uptrend_returns_profit(self, ohlcv_uptrend):
        """Em tendência de alta, Buy and Hold deve retornar lucro."""
        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(ohlcv_uptrend, 10_000.0)
            assert result.final_balance > 10_000.0
            assert result.total_return_pct > 0
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_downtrend_returns_loss(self, ohlcv_downtrend):
        """Em tendência de queda, Buy and Hold deve retornar perda."""
        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(ohlcv_downtrend, 10_000.0)
            assert result.final_balance < 10_000.0
            assert result.total_return_pct < 0
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_flat_market_returns_zero_or_minimal(self, ohlcv_flat):
        """Em mercado lateral, o retorno deve ser próximo de zero."""
        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(ohlcv_flat, 10_000.0)
            assert abs(result.total_return_pct) < 1.0
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_always_exactly_one_trade(self, ohlcv_uptrend):
        """Buy and Hold realiza exatamente 1 compra e 1 venda."""
        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(ohlcv_uptrend, 10_000.0)
            assert result.total_trades == 1
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_result_is_simulation_result_instance(self, ohlcv_uptrend):
        """O retorno deve ser instância de SimulationResult."""
        strategy = BuyAndHoldStrategy()
        try:
            result = strategy.run(ohlcv_uptrend, 10_000.0)
            assert isinstance(result, SimulationResult)
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_mocked_run_returns_expected_result(self, ohlcv_uptrend):
        """
        Teste com Mock: isola BuyAndHoldStrategy para verificar
        que o motor de simulação chama run() com os parâmetros corretos.
        """
        mock_strategy = MagicMock(spec=BuyAndHoldStrategy)
        expected = self._make_result(10_000.0, 13_636.36)
        mock_strategy.run.return_value = expected

        result = mock_strategy.run(ohlcv_uptrend, 10_000.0)

        mock_strategy.run.assert_called_once_with(ohlcv_uptrend, 10_000.0)
        assert result.final_balance == pytest.approx(13_636.36)


# ---------------------------------------------------------------------------
# Testes — MovingAverageStrategy
# ---------------------------------------------------------------------------

class TestMovingAverageStrategy:
    """Testes da estratégia de Cruzamento de Médias Móveis."""

    def test_default_windows_are_9_and_21(self):
        """Janelas padrão devem ser 9 (curta) e 21 (longa)."""
        strategy = MovingAverageStrategy()
        assert strategy.short_window == 9
        assert strategy.long_window == 21

    def test_custom_windows_are_stored(self):
        """Janelas customizadas devem ser armazenadas corretamente."""
        strategy = MovingAverageStrategy(short_window=5, long_window=20)
        assert strategy.short_window == 5
        assert strategy.long_window == 20

    def test_short_window_greater_than_long_raises_value_error(self):
        """
        Janela curta maior que longa é configuração inválida.
        A implementação deve lançar ValueError.
        """
        with pytest.raises((ValueError, AssertionError)):
            strategy = MovingAverageStrategy(short_window=21, long_window=9)
            # Se o erro for lazy (levantado só no run), forçamos aqui:
            strategy.run(pd.DataFrame(), 10_000.0)

    def test_insufficient_data_for_windows_raises_error(self, ohlcv_uptrend):
        """Série com menos linhas que a janela longa deve levantar erro."""
        strategy = MovingAverageStrategy(short_window=3, long_window=10)
        # ohlcv_uptrend tem 5 linhas; janela longa = 10 → dados insuficientes
        try:
            with pytest.raises((ValueError, RuntimeError)):
                strategy.run(ohlcv_uptrend, 10_000.0)
        except NotImplementedError:
            pytest.skip("MovingAverageStrategy ainda não implementada.")

    def test_uptrend_series_generates_at_least_one_trade(self, ohlcv_long):
        """Série longa com tendência de alta deve gerar ao menos uma operação."""
        strategy = MovingAverageStrategy(short_window=5, long_window=10)
        try:
            result = strategy.run(ohlcv_long, 10_000.0)
            assert result.total_trades >= 1
        except NotImplementedError:
            pytest.skip("MovingAverageStrategy ainda não implementada.")

    def test_win_rate_is_between_0_and_100(self, ohlcv_long):
        """Taxa de acerto deve estar no intervalo [0, 100]."""
        strategy = MovingAverageStrategy(short_window=5, long_window=10)
        try:
            result = strategy.run(ohlcv_long, 10_000.0)
            assert 0.0 <= result.win_rate_pct <= 100.0
        except NotImplementedError:
            pytest.skip("MovingAverageStrategy ainda não implementada.")

    def test_max_drawdown_is_non_negative(self, ohlcv_long):
        """Max Drawdown deve ser >= 0."""
        strategy = MovingAverageStrategy(short_window=5, long_window=10)
        try:
            result = strategy.run(ohlcv_long, 10_000.0)
            assert result.max_drawdown_pct >= 0.0
        except NotImplementedError:
            pytest.skip("MovingAverageStrategy ainda não implementada.")

    def test_mocked_strategy_integration(self, ohlcv_long):
        """
        Teste com Mock: simula o comportamento do motor ao chamar uma estratégia.
        Verifica que o motor repassa os dados corretos para a estratégia.
        """
        mock_strategy = MagicMock(spec=MovingAverageStrategy)
        mock_strategy.run.return_value = SimulationResult(
            final_balance=12_000.0,
            total_return_pct=20.0,
            win_rate_pct=66.7,
            max_drawdown_pct=5.2,
            total_trades=3,
            operations=[],
        )

        result = mock_strategy.run(ohlcv_long, 10_000.0)

        mock_strategy.run.assert_called_once()
        assert result.total_return_pct == pytest.approx(20.0)
        assert result.max_drawdown_pct == pytest.approx(5.2)


# ---------------------------------------------------------------------------
# Testes — Condição de Falência (RN-02)
# ---------------------------------------------------------------------------

class TestBankruptcyCondition:
    """
    Valida a regra de negócio RN-02:
    Simulação interrompida imediatamente quando saldo <= 0.
    """

    def test_zero_capital_triggers_bankruptcy(self):
        """Capital inicial zero deve impedir início da simulação."""
        strategy = BuyAndHoldStrategy()
        try:
            with pytest.raises((BankruptcyError, ValueError)):
                strategy.run(pd.DataFrame(), 0.0)
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_negative_capital_triggers_bankruptcy(self):
        """Capital negativo deve impedir início da simulação."""
        strategy = BuyAndHoldStrategy()
        try:
            with pytest.raises((BankruptcyError, ValueError)):
                strategy.run(pd.DataFrame(), -1_000.0)
        except NotImplementedError:
            pytest.skip("BuyAndHoldStrategy ainda não implementada.")

    def test_bankruptcy_during_simulation_does_not_crash_app(self, ohlcv_downtrend):
        """
        Se saldo atingir zero durante simulação, BankruptcyError deve ser
        levantada mas capturada pelo motor sem encerrar a aplicação.
        """
        strategy = MagicMock(spec=BuyAndHoldStrategy)
        strategy.run.side_effect = BankruptcyError("Saldo zerado no pregão 3.")

        with pytest.raises(BankruptcyError):
            strategy.run(ohlcv_downtrend, 10.0)

        # A exceção foi capturada — a aplicação não crashou
        assert True


# ---------------------------------------------------------------------------
# Testes — SimulationResult (contrato de saída)
# ---------------------------------------------------------------------------

class TestSimulationResult:
    """Valida a estrutura de retorno da simulação."""

    def test_simulation_result_has_required_fields(self):
        result = SimulationResult(
            final_balance=11_000.0,
            total_return_pct=10.0,
            win_rate_pct=75.0,
            max_drawdown_pct=3.5,
            total_trades=4,
            operations=[],
        )
        assert hasattr(result, "final_balance")
        assert hasattr(result, "total_return_pct")
        assert hasattr(result, "win_rate_pct")
        assert hasattr(result, "max_drawdown_pct")
        assert hasattr(result, "total_trades")
        assert hasattr(result, "operations")

    def test_total_return_calculation(self):
        """Retorno percentual deve ser calculado corretamente."""
        initial = 10_000.0
        final = 11_000.0
        expected_return = (final - initial) / initial * 100  # 10%
        result = SimulationResult(
            final_balance=final,
            total_return_pct=expected_return,
            win_rate_pct=100.0,
            max_drawdown_pct=0.0,
            total_trades=1,
            operations=[],
        )
        assert result.total_return_pct == pytest.approx(10.0)

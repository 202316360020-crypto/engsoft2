"""Estratégias de negociação da QuantInvest Suite."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import override

import pandas as pd

from .exceptions import BankruptcyError
from .metrics import calculate_max_drawdown, calculate_return, calculate_win_rate
from .parser import OHLCVParser


@dataclass(slots=True)
class SimulationResult:
    """Resultado de uma simulação de investimento."""

    final_balance: float
    total_return_pct: float
    win_rate_pct: float
    max_drawdown_pct: float
    total_trades: int
    operations: list[dict]
    equity_curve: list[float] = field(default_factory=list)


class BaseStrategy(ABC):
    """Contrato comum para as estratégias."""

    @abstractmethod
    def run(self, data: pd.DataFrame, initial_capital: float) -> SimulationResult:
        """Executa a estratégia e devolve o resultado."""


def _normalize_market_data(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        raise ValueError("A série OHLCV não pode estar vazia.")

    frame = data.copy()
    if not isinstance(frame.index, pd.DatetimeIndex):
        frame.index = pd.to_datetime(frame.index)

    parser = OHLCVParser()
    parser.validate_columns(frame)
    parser.validate_chronological_order(frame)

    return frame


class BuyAndHoldStrategy(BaseStrategy):
    """Compra no primeiro candle e vende no último."""

    @override
    def run(self, data: pd.DataFrame, initial_capital: float) -> SimulationResult:
        """Executa a estratégia buy and hold e retorna o resultado.

        Args:
            data: série temporal OHLCV.
            initial_capital: capital inicial para a simulação.

        Returns:
            SimulationResult: resultado da simulação.

        Raises:
            BankruptcyError: se o capital inicial for menor ou igual a zero.
            ValueError: se os preços forem inválidos.
        """
        frame = _normalize_market_data(data)
        if initial_capital <= 0:
            raise BankruptcyError("Capital inicial deve ser positivo.")

        close_prices = frame["Close"].astype(float)
        entry_price = float(close_prices.iloc[0])
        exit_price = float(close_prices.iloc[-1])

        if entry_price <= 0 or exit_price <= 0:
            raise ValueError("Preços inválidos na série OHLCV.")

        shares = initial_capital / entry_price
        equity_curve = [shares * float(price) for price in close_prices]
        final_balance = shares * exit_price
        trade = {
            "action": self.__class__.__name__,
            "entry_date": frame.index[0].isoformat(),
            "exit_date": frame.index[-1].isoformat(),
            "entry_price": entry_price,
            "exit_price": exit_price,
            "profit": final_balance - initial_capital,
            "return_pct": calculate_return(initial_capital, final_balance),
        }

        return SimulationResult(
            final_balance=final_balance,
            total_return_pct=calculate_return(initial_capital, final_balance),
            win_rate_pct=calculate_win_rate([trade]),
            max_drawdown_pct=calculate_max_drawdown(equity_curve),
            total_trades=1,
            operations=[trade],
            equity_curve=equity_curve,
        )


class MovingAverageStrategy(BaseStrategy):
    """Estratégia baseada em cruzamento de médias móveis simples."""

    def __init__(self, short_window: int = 9, long_window: int = 21):
        """Inicializa os parâmetros da estratégia de médias móveis.

        Args:
            short_window: largura da janela curta.
            long_window: largura da janela longa.

        Raises:
            ValueError: se as janelas forem inválidas.
        """
        if short_window <= 0 or long_window <= 0:
            raise ValueError("As janelas devem ser positivas.")
        if short_window >= long_window:
            raise ValueError("short_window deve ser menor que long_window.")
        self.short_window = short_window
        self.long_window = long_window

    def run(self, data: pd.DataFrame, initial_capital: float) -> SimulationResult:
        """Executa a estratégia de cruzamento de médias móveis.

        Args:
            data: série temporal OHLCV.
            initial_capital: capital inicial para a simulação.

        Returns:
            SimulationResult: resultado da simulação.

        Raises:
            BankruptcyError: se o capital inicial for menor ou igual a zero.
            ValueError: se os dados ou preços forem inválidos.
        """
        frame = _normalize_market_data(data)
        if initial_capital <= 0:
            raise BankruptcyError("Capital inicial deve ser positivo.")
        if len(frame) < self.long_window:
            raise ValueError("Dados insuficientes para calcular as médias móveis.")

        closes = frame["Close"].astype(float)
        short_ma = closes.rolling(self.short_window, min_periods=self.short_window).mean()
        long_ma = closes.rolling(self.long_window, min_periods=self.long_window).mean()

        operations, equity_curve, final_balance = self._run_cross_strategy(
            frame.index,
            closes,
            short_ma,
            long_ma,
            initial_capital,
        )

        total_return_pct = calculate_return(initial_capital, final_balance)
        win_rate_pct = calculate_win_rate(operations) if operations else 0.0
        max_drawdown_pct = calculate_max_drawdown(equity_curve)

        return SimulationResult(
            final_balance=final_balance,
            total_return_pct=total_return_pct,
            win_rate_pct=win_rate_pct,
            max_drawdown_pct=max_drawdown_pct,
            total_trades=len(operations),
            operations=operations,
            equity_curve=equity_curve,
        )


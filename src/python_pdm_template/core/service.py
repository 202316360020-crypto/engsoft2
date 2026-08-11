"""Serviços de orquestração para CLI e GUI."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .exceptions import InvalidCSVError
from .metrics import calculate_return, calculate_win_rate
from .parser import OHLCVParser
from .strategies import BaseStrategy, BuyAndHoldStrategy, MovingAverageStrategy, SimulationResult


@dataclass(slots=True)
class SimulationRun:
    """Pacote com dados carregados e resultado da estratégia."""

    file_path: str
    data: pd.DataFrame
    result: SimulationResult


def build_strategy(strategy_name: str, short_window: int = 9, long_window: int = 21) -> BaseStrategy:
    """Constrói a estratégia solicitada."""
    normalized = strategy_name.strip().lower()
    if normalized == "buy and hold":
        return BuyAndHoldStrategy()
    if normalized in {"cruzamento de médias móveis", "cruzamento de medias moveis", "moving average"}:
        return MovingAverageStrategy(short_window=short_window, long_window=long_window)
    raise ValueError(f"Estratégia desconhecida: {strategy_name}")


def load_market_data(file_path: str, start_date: str | None = None, end_date: str | None = None) -> pd.DataFrame:
    """Carrega o CSV e aplica filtro opcional de período."""
    parser = OHLCVParser()
    frame = parser.parse(file_path)

    if start_date is not None:
        frame = frame.loc[pd.to_datetime(start_date) :]
    if end_date is not None:
        frame = frame.loc[: pd.to_datetime(end_date)]

    if frame.empty:
        raise InvalidCSVError("Não há dados no intervalo solicitado.")

    parser.validate_chronological_order(frame)
    return frame


def simulate_file(
    file_path: str,
    strategy_name: str,
    capital: float,
    start_date: str | None = None,
    end_date: str | None = None,
    short_window: int = 9,
    long_window: int = 21,
) -> SimulationRun:
    """Executa uma simulação para um único arquivo."""
    data = load_market_data(file_path, start_date=start_date, end_date=end_date)
    strategy = build_strategy(strategy_name, short_window=short_window, long_window=long_window)
    result = strategy.run(data, capital)
    return SimulationRun(file_path=file_path, data=data, result=result)


def simulate_files(
    file_paths: list[str],
    strategy_name: str,
    capital: float,
    start_date: str | None = None,
    end_date: str | None = None,
    short_window: int = 9,
    long_window: int = 21,
) -> list[SimulationRun]:
    """Executa uma simulação para vários arquivos."""
    return [
        simulate_file(
            file_path,
            strategy_name,
            capital,
            start_date=start_date,
            end_date=end_date,
            short_window=short_window,
            long_window=long_window,
        )
        for file_path in file_paths
    ]


def aggregate_runs(runs: list[SimulationRun], capital_per_file: float) -> SimulationResult:
    """Agrega múltiplas execuções em um resumo de portfólio."""
    if not runs:
        raise ValueError("É necessário informar ao menos uma execução.")

    total_final_balance = sum(run.result.final_balance for run in runs)
    total_initial_capital = capital_per_file * len(runs)
    operations = [operation for run in runs for operation in run.result.operations]
    win_rate_pct = calculate_win_rate(operations) if operations else 0.0
    max_drawdown_pct = max(run.result.max_drawdown_pct for run in runs)
    return SimulationResult(
        final_balance=total_final_balance,
        total_return_pct=calculate_return(total_initial_capital, total_final_balance),
        win_rate_pct=win_rate_pct,
        max_drawdown_pct=max_drawdown_pct,
        total_trades=sum(run.result.total_trades for run in runs),
        operations=operations,
        equity_curve=runs[0].result.equity_curve,
    )
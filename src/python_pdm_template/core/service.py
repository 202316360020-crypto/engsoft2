"""Serviços de orquestração para CLI e GUI."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .exceptions import InvalidCSVError
from .metrics import calculate_return, calculate_win_rate
from .parser import OHLCVParser
from .strategies import (
    BaseStrategy,
    BuyAndHoldStrategy,
    MovingAverageStrategy,
    SimulationResult,
)


@dataclass(slots=True)
class SimulationOptions:
    """Configurações de simulação usadas pela aplicação."""

    strategy_name: str
    capital: float
    start_date: str | None = None
    end_date: str | None = None
    short_window: int = 9
    long_window: int = 21


@dataclass(slots=True)
class SimulationRun:
    """Pacote com dados carregados e resultado da estratégia."""

    file_path: str
    data: pd.DataFrame
    result: SimulationResult


def build_strategy(strategy_name: str, short_window: int = 9, long_window: int = 21) -> BaseStrategy:
    """Constrói a estratégia solicitada.

    Args:
        strategy_name: nome da estratégia solicitada.
        short_window: janela curta para médias móveis.
        long_window: janela longa para médias móveis.

    Returns:
        BaseStrategy: instância da estratégia selecionada.

    Raises:
        ValueError: se a estratégia for desconhecida.
    """
    normalized = strategy_name.strip().lower()
    if normalized == "buy and hold":
        return BuyAndHoldStrategy()
    if normalized in {"cruzamento de médias móveis", "cruzamento de medias moveis", "moving average"}:
        return MovingAverageStrategy(short_window=short_window, long_window=long_window)
    raise ValueError(f"Estratégia desconhecida: {strategy_name}")


def load_market_data(file_path: str, start_date: str | None = None, end_date: str | None = None) -> pd.DataFrame:
    """Carrega o CSV e aplica filtro opcional de período.

    Args:
        file_path: caminho do arquivo CSV.
        start_date: data inicial para o filtro, se fornecida.
        end_date: data final para o filtro, se fornecida.

    Returns:
        pd.DataFrame: dados OHLCV filtrados pelo intervalo.

    Raises:
        InvalidCSVError: se o arquivo for inválido ou não houver dados no intervalo selecionado.
    """
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


def simulate_file(file_path: str, options: SimulationOptions) -> SimulationRun:
    """Executa uma simulação para um único arquivo.

    Args:
        file_path: caminho do arquivo CSV.
        options: opções de simulação.

    Returns:
        SimulationRun: resultado da simulação.
    """
    data = load_market_data(file_path, start_date=options.start_date, end_date=options.end_date)
    strategy = build_strategy(
        options.strategy_name,
        short_window=options.short_window,
        long_window=options.long_window,
    )
    result = strategy.run(data, options.capital)
    return SimulationRun(file_path=file_path, data=data, result=result)


def simulate_files(file_paths: list[str], options: SimulationOptions) -> list[SimulationRun]:
    """Executa uma simulação para vários arquivos.

    Args:
        file_paths: lista de arquivos para simulação.
        options: opções de simulação.

    Returns:
        list[SimulationRun]: resultados de simulação para cada arquivo.
    """
    return [simulate_file(file_path, options) for file_path in file_paths]


def aggregate_runs(runs: list[SimulationRun], capital_per_file: float) -> SimulationResult:
    """Agrega múltiplas execuções em um resumo de portfólio.

    Args:
        runs: lista de resultados de simulação para cada arquivo.
        capital_per_file: capital alocado para cada arquivo.

    Returns:
        SimulationResult: resumo consolidado de portfólio.

    Raises:
        ValueError: se a lista de execuções estiver vazia.
    """
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
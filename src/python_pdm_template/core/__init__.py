"""Núcleo funcional da QuantInvest Suite."""

from .exceptions import BankruptcyError, InvalidCSVError, MissingColumnsError, OutOfOrderDatesError
from .metrics import calculate_max_drawdown, calculate_return, calculate_win_rate
from .parser import OHLCVParser
from .strategies import BaseStrategy, BuyAndHoldStrategy, MovingAverageStrategy, SimulationResult

__all__ = [
    "BankruptcyError",
    "InvalidCSVError",
    "MissingColumnsError",
    "OutOfOrderDatesError",
    "calculate_max_drawdown",
    "calculate_return",
    "calculate_win_rate",
    "OHLCVParser",
    "BaseStrategy",
    "BuyAndHoldStrategy",
    "MovingAverageStrategy",
    "SimulationResult",
]
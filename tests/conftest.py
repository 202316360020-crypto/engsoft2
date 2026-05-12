"""
Fixtures globais reutilizadas em toda a suíte de testes da QuantInvest Suite.
"""

import pandas as pd
import pytest


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _make_ohlcv(
    dates: list[str],
    opens: list[float],
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[int],
) -> pd.DataFrame:
    """Constrói um DataFrame OHLCV a partir de listas paralelas."""
    return pd.DataFrame(
        {
            "Date": pd.to_datetime(dates),
            "Open": opens,
            "High": highs,
            "Low": lows,
            "Close": closes,
            "Volume": volumes,
        }
    ).set_index("Date")


# ---------------------------------------------------------------------------
# Fixtures de dados OHLCV
# ---------------------------------------------------------------------------

@pytest.fixture
def ohlcv_uptrend() -> pd.DataFrame:
    """Série com tendência de alta consistente (5 pregões)."""
    return _make_ohlcv(
        dates=["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"],
        opens= [10.0, 11.0, 12.0, 13.0, 14.0],
        highs= [11.5, 12.5, 13.5, 14.5, 15.5],
        lows=  [ 9.5, 10.5, 11.5, 12.5, 13.5],
        closes=[11.0, 12.0, 13.0, 14.0, 15.0],
        volumes=[1000, 1100, 1200, 1300, 1400],
    )


@pytest.fixture
def ohlcv_downtrend() -> pd.DataFrame:
    """Série com tendência de queda consistente (5 pregões)."""
    return _make_ohlcv(
        dates=["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"],
        opens= [15.0, 14.0, 13.0, 12.0, 11.0],
        highs= [15.5, 14.5, 13.5, 12.5, 11.5],
        lows=  [13.5, 12.5, 11.5, 10.5,  9.5],
        closes=[14.0, 13.0, 12.0, 11.0, 10.0],
        volumes=[1000, 1100, 1200, 1300, 1400],
    )


@pytest.fixture
def ohlcv_flat() -> pd.DataFrame:
    """Série sem variação de preço (5 pregões)."""
    return _make_ohlcv(
        dates=["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-08"],
        opens= [10.0] * 5,
        highs= [10.5] * 5,
        lows=  [ 9.5] * 5,
        closes=[10.0] * 5,
        volumes=[500] * 5,
    )


@pytest.fixture
def ohlcv_out_of_order() -> pd.DataFrame:
    """Série com datas fora de ordem cronológica (deve falhar na validação)."""
    return _make_ohlcv(
        dates=["2024-01-03", "2024-01-02", "2024-01-04"],
        opens= [11.0, 10.0, 12.0],
        highs= [12.0, 11.0, 13.0],
        lows=  [10.0,  9.0, 11.0],
        closes=[11.5, 10.5, 12.5],
        volumes=[1000, 1000, 1000],
    )


@pytest.fixture
def ohlcv_missing_column() -> pd.DataFrame:
    """Série sem a coluna 'Volume' (deve falhar na validação)."""
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-02", "2024-01-03"]),
            "Open": [10.0, 11.0],
            "High": [11.0, 12.0],
            "Low":  [ 9.0, 10.0],
            "Close":[10.5, 11.5],
        }
    ).set_index("Date")
    return df


@pytest.fixture
def ohlcv_long() -> pd.DataFrame:
    """Série longa (30 pregões) para testes de médias móveis."""
    closes = [
        10, 10.5, 11, 10.8, 11.2, 11.5, 12, 11.8, 12.2, 12.5,
        13, 12.8, 13.2, 13.5, 14, 13.8, 14.2, 14.5, 15, 14.8,
        15.2, 15.5, 16, 15.8, 16.2, 16.5, 17, 16.8, 17.2, 17.5,
    ]
    dates = pd.bdate_range(start="2024-01-02", periods=30)
    return pd.DataFrame(
        {
            "Open":   [c - 0.2 for c in closes],
            "High":   [c + 0.5 for c in closes],
            "Low":    [c - 0.5 for c in closes],
            "Close":  closes,
            "Volume": [1000] * 30,
        },
        index=dates,
    )

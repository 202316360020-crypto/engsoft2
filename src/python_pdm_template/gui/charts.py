"""Renderizacao visual da QuantInvest Suite com PNG para compatibilidade no executavel."""

from __future__ import annotations

from pathlib import Path
import tempfile
from typing import Optional
import uuid

import flet as ft
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

from .components import ThemeColors

_CHART_CACHE_DIR = Path(tempfile.gettempdir()) / "quantinvest_charts"
_CHART_CACHE_DIR.mkdir(parents=True, exist_ok=True)
_CHART_DPI = 220
_CHART_LINE_SIZE = (11.2, 3.6)


def _save_figure_to_temp_file(figure: plt.Figure, prefix: str) -> str:
    file_path = _CHART_CACHE_DIR / f"{prefix}_{uuid.uuid4().hex}.png"
    figure.savefig(file_path, dpi=_CHART_DPI, facecolor=ThemeColors.BACKGROUND, bbox_inches=None, pad_inches=0.10)
    plt.close(figure)
    return str(file_path)


def _chart_frame(title: str, subtitle: str, image_path: str | None, width: int, height: int) -> ft.Container:
    if image_path is None:
        body: ft.Control = ft.Container(
            expand=True,
            alignment=ft.alignment.Alignment(0, 0),
            content=ft.Text(subtitle, size=11, color=ThemeColors.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
        )
    else:
        body = ft.Image(
            src=image_path,
            width=width - 24,
            height=height - 54,
            fit=ft.BoxFit.CONTAIN,
            error_content=ft.Text("Falha ao renderizar grafico", size=10, color=ThemeColors.RED),
        )

    return ft.Container(
        width=width,
        height=height,
        border_radius=18,
        bgcolor=ThemeColors.SURFACE,
        padding=12,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(title, size=14, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                        ft.Text(subtitle, size=10, color=ThemeColors.TEXT_SECONDARY),
                    ],
                ),
                body,
            ],
        ),
    )


def _empty_state(title: str, subtitle: str) -> ft.Container:
    return _chart_frame(title, subtitle, None, 900, 340)


def _apply_axis_theme(axis: plt.Axes) -> None:
    axis.set_facecolor(ThemeColors.SURFACE)
    axis.grid(color=ThemeColors.BORDER, alpha=0.30, linewidth=0.8)
    axis.tick_params(colors=ThemeColors.TEXT_SECONDARY, labelsize=8)
    for spine in axis.spines.values():
        spine.set_color(ThemeColors.BORDER)


def _resolve_candlestick_columns(frame: pd.DataFrame) -> tuple[str, str, str, str] | None:
    lower_columns = {column.lower(): column for column in frame.columns}
    close_column = next((lower_columns[name] for name in ("close", "adj close", "adj_close") if name in lower_columns), None)
    if close_column is None:
        return None

    open_column = next((lower_columns[name] for name in ("open",) if name in lower_columns), close_column)
    high_column = next((lower_columns[name] for name in ("high",) if name in lower_columns), close_column)
    low_column = next((lower_columns[name] for name in ("low",) if name in lower_columns), close_column)
    return open_column, high_column, low_column, close_column


def _draw_candlesticks(axis: plt.Axes, opens: list[float], highs: list[float], lows: list[float], closes: list[float]) -> None:
    for idx, (open_value, high_value, low_value, close_value) in enumerate(zip(opens, highs, lows, closes, strict=False)):
        color = ThemeColors.GREEN if close_value >= open_value else ThemeColors.RED
        axis.vlines(idx, low_value, high_value, color=color, linewidth=1.0)
        body_bottom = min(open_value, close_value)
        body_height = max(abs(close_value - open_value), 0.04)
        axis.add_patch(Rectangle((idx - 0.32, body_bottom), 0.64, body_height, facecolor=color, edgecolor=color, alpha=0.95))


def render_line_chart(values: list[float], title: str, subtitle: str = "", width: int = 900, height: int = 340) -> ft.Container:
    """Renderiza uma curva de capital em formato de imagem.

    Argumentos:
        values: valores da curva de capital.
        title: título do gráfico.
        subtitle: texto secundário exibido abaixo do título.
        width: largura do contêiner.
        height: altura do contêiner.

    Retorna:
        ft.Container: contêiner com o gráfico ou estado vazio.
    """
    if not values:
        return _empty_state(title, subtitle or "Nenhum valor para exibir.")
    if len(values) == 1:
        return _empty_state(title, subtitle or "Apenas 1 ponto no periodo. Amplie o intervalo para ver a curva.")

    figure, axis = plt.subplots(figsize=_CHART_LINE_SIZE, dpi=_CHART_DPI)
    figure.patch.set_facecolor(ThemeColors.BACKGROUND)
    _apply_axis_theme(axis)
    figure.subplots_adjust(left=0.06, right=0.98, top=0.92, bottom=0.16)

    x_values = list(range(len(values)))
    axis.plot(x_values, values, color=ThemeColors.GREEN, linewidth=2.3)
    axis.fill_between(x_values, values, min(values), color=ThemeColors.GREEN, alpha=0.14)
    axis.set_xlim(0, len(values) - 1)

    image_path = _save_figure_to_temp_file(figure, "equity")
    return _chart_frame(title, subtitle, image_path, width, height)


def render_candlestick_chart(frame: pd.DataFrame, width: int = 900, height: int = 340) -> ft.Container:
    """Renderiza um gráfico de candles a partir de um DataFrame OHLCV.

    Argumentos:
        frame: DataFrame com colunas OHLCV.
        width: largura do contêiner.
        height: altura do contêiner.

    Retorna:
        ft.Container: contêiner com o gráfico ou estado vazio.
    """
    if frame is None or frame.empty:
        return _empty_state("Candlestick", "Abra um CSV para visualizar o OHLCV.")
    if len(frame) == 1:
        return _empty_state("Candlestick", "Apenas 1 candle no periodo. Amplie as datas para visualizar o grafico.")

    resolved_columns = _resolve_candlestick_columns(frame)
    if resolved_columns is None:
        return _empty_state("Candlestick", "A serie precisa de uma coluna Close para o desenho.")

    open_column, high_column, low_column, close_column = resolved_columns
    opens = frame[open_column].astype(float).tolist()
    highs = frame[high_column].astype(float).tolist()
    lows = frame[low_column].astype(float).tolist()
    closes = frame[close_column].astype(float).tolist()

    figure, axis = plt.subplots(figsize=_CHART_LINE_SIZE, dpi=_CHART_DPI)
    figure.patch.set_facecolor(ThemeColors.BACKGROUND)
    _apply_axis_theme(axis)
    figure.subplots_adjust(left=0.06, right=0.98, top=0.92, bottom=0.16)

    _draw_candlesticks(axis, opens, highs, lows, closes)

    axis.set_xlim(-1, len(closes))
    axis.set_ylim(min(lows) * 0.995, max(highs) * 1.005)

    image_path = _save_figure_to_temp_file(figure, "candles")
    subtitle = f"{len(frame)} candles"
    return _chart_frame("Candlestick", subtitle, image_path, width, height)


class ChartPlaceholder(ft.Container):
    """Contêiner de substituição exibido quando o gráfico real não está disponível."""

    def __init__(self, chart_type: str = "candlestick"):
        """Inicializa o placeholder do gráfico com título e descrição apropriados."""
        if chart_type == "candlestick":
            title, description = "Candlestick", "OHLCV da serie temporal"
        elif chart_type == "capital_curve":
            title, description = "Curva de Capital", "Evolucao do saldo durante a simulacao"
        else:
            title, description = "Grafico", "Visualizacao de dados"

        super().__init__(
            expand=True,
            padding=20,
            border_radius=18,
            bgcolor=ThemeColors.SURFACE,
            content=ft.Column(
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(title, size=14, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                    ft.Text(description, size=11, color=ThemeColors.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                ],
            ),
        )


class MplfinanceChart:
    """Placeholder para renderização de gráficos com mplfinance."""

    @staticmethod
    def create_candlestick(_data: pd.DataFrame) -> ft.Container:
        """Cria um gráfico de candlestick com mplfinance usando dados OHLCV.

        Argumentos:
            _data: DataFrame com preço OHLCV.

        Retorna:
            ft.Container: placeholder do gráfico.
        """
        return ChartPlaceholder("candlestick")


class PlotlyChart:
    """Placeholder para renderização de gráficos com Plotly."""

    @staticmethod
    def create_capital_curve(_balances: list[float], _dates: Optional[list[str]] = None) -> ft.Container:
        """Cria um gráfico de curva de capital com Plotly.

        Argumentos:
            _balances: lista de saldos ao longo do tempo.
            _dates: datas opcionais para cada saldo.

        Retorna:
            ft.Container: placeholder do gráfico.
        """
        return ChartPlaceholder("capital_curve")

    @staticmethod
    def create_returns_histogram(_returns: list[float], _labels: Optional[list[str]] = None) -> ft.Container:
        """Cria um histograma de retornos com Plotly.

        Argumentos:
            _returns: lista de retornos percentuais.
            _labels: rótulos opcionais para cada retorno.

        Retorna:
            ft.Container: placeholder do gráfico.
        """
        return ChartPlaceholder("returns")


class ChartManager:
    """Gerencia a renderização de gráficos e seus componentes de placeholder."""

    def __init__(self):
        """Inicializa o gerenciador de gráficos com placeholders vazios."""
        self.candlestick_chart = ChartPlaceholder("candlestick")
        self.capital_curve_chart = ChartPlaceholder("capital_curve")

    def update_candlestick(self, frame: pd.DataFrame) -> ft.Control:
        """Renderiza e atualiza o gráfico de candlestick.

        Args:
            frame: DataFrame com colunas OHLCV.

        Returns:
            ft.Control: controle que contém o gráfico renderizado.
        """
        self.candlestick_chart = render_candlestick_chart(frame)
        return self.candlestick_chart

    def update_capital_curve(self, values: list[float], title: str = "Curva de Capital", subtitle: str = "") -> ft.Control:
        """Renderiza e atualiza a curva de capital.

        Args:
            values: lista de saldos ou valores de capital.
            title: título do gráfico.
            subtitle: descrição secundária do gráfico.

        Returns:
            ft.Control: controle que contém o gráfico renderizado.
        """
        self.capital_curve_chart = render_line_chart(values, title, subtitle)
        return self.capital_curve_chart

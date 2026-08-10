"""Renderizacao visual da QuantInvest Suite em SVG puro."""

from __future__ import annotations

import base64
from html import escape
from statistics import fmean
from typing import Optional

import flet as ft
import pandas as pd

from .components import ThemeColors


def _svg_to_data_uri(svg: str) -> str:
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def _chart_frame(title: str, subtitle: str, svg: str, width: int, height: int) -> ft.Container:
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
                ft.Image(src=_svg_to_data_uri(svg), width=width - 24, height=height - 54),
            ],
        ),
    )


def _placeholder_svg(title: str, subtitle: str, icon: str) -> str:
    return f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='900' height='340' viewBox='0 0 900 340'>
      <rect width='100%' height='100%' rx='18' fill='{ThemeColors.BACKGROUND}'/>
      <rect x='18' y='18' width='864' height='304' rx='16' fill='{ThemeColors.SURFACE}' stroke='{ThemeColors.BORDER}'/>
      <text x='450' y='130' text-anchor='middle' fill='{ThemeColors.GREEN}' font-size='54' font-family='Arial, sans-serif'>{escape(icon)}</text>
      <text x='450' y='185' text-anchor='middle' fill='{ThemeColors.TEXT_PRIMARY}' font-size='24' font-family='Arial, sans-serif'>{escape(title)}</text>
      <text x='450' y='220' text-anchor='middle' fill='{ThemeColors.TEXT_SECONDARY}' font-size='14' font-family='Arial, sans-serif'>{escape(subtitle)}</text>
    </svg>
    """


def _empty_state(title: str, subtitle: str, icon: str) -> ft.Container:
    return _chart_frame(title, subtitle, _placeholder_svg(title, subtitle, icon), 900, 340)


def _line_points(values: list[float], width: int, height: int) -> tuple[list[str], list[str], float, float, float]:
    if not values:
        return [], [], 0.0, 0.0, 1.0

    left, top, right, bottom = 26, 24, 16, 28
    chart_width = max(width - left - right, 1)
    chart_height = max(height - top - bottom, 1)
    min_value = min(values)
    max_value = max(values)
    span = max(max_value - min_value, 1e-9)
    step = chart_width / max(len(values) - 1, 1)

    def y_from_value(value: float) -> float:
        return top + (max_value - value) / span * chart_height

    points = [f"{left + index * step:.1f},{y_from_value(value):.1f}" for index, value in enumerate(values)]
    baseline = [f"{left:.1f},{height - bottom}"] + points + [f"{left + chart_width:.1f},{height - bottom}"]
    return points, baseline, min_value, max_value, span


def render_line_chart(values: list[float], title: str, subtitle: str = "", width: int = 900, height: int = 340) -> ft.Container:
    if not values:
        return _empty_state(title, subtitle or "Nenhum valor para exibir.", "Line")

    points, baseline, _, _, _ = _line_points(values, width, height)
    left, top, right, bottom = 26, 24, 16, 28
    chart_width = max(width - left - right, 1)
    chart_height = max(height - top - bottom, 1)
    min_value = min(values)
    max_value = max(values)
    mid_value = fmean(values)
    span = max(max_value - min_value, 1e-9)

    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
      <rect width='100%' height='100%' rx='18' fill='{ThemeColors.BACKGROUND}'/>
      <rect x='0' y='0' width='{width}' height='{height}' rx='18' fill='{ThemeColors.SURFACE}'/>
      <line x1='{left}' y1='{top}' x2='{width - right}' y2='{top}' stroke='{ThemeColors.BORDER}' stroke-width='1'/>
      <line x1='{left}' y1='{height - bottom}' x2='{width - right}' y2='{height - bottom}' stroke='{ThemeColors.BORDER}' stroke-width='1'/>
      <polygon points="{' '.join(baseline)}" fill='{ThemeColors.GREEN}' opacity='0.08'/>
      <polyline points="{' '.join(points)}" fill='none' stroke='{ThemeColors.GREEN}' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/>
      <text x='{left}' y='18' fill='{ThemeColors.TEXT_SECONDARY}' font-size='10' font-family='Arial, sans-serif'>Media: {mid_value:,.2f}</text>
      <text x='{width - 20}' y='{height - 8}' fill='{ThemeColors.TEXT_SECONDARY}' font-size='10' text-anchor='end' font-family='Arial, sans-serif'>Ultimo: {values[-1]:,.2f}</text>
    </svg>
    """
    return _chart_frame(title, subtitle, svg, width, height)


def render_candlestick_chart(frame: pd.DataFrame, width: int = 900, height: int = 340) -> ft.Container:
    if frame is None or frame.empty:
        return _empty_state("Candlestick", "Abra um CSV para visualizar o OHLCV.", "Candlestick")

    lower_columns = {column.lower(): column for column in frame.columns}
    close_column = next((lower_columns[name] for name in ("close", "adj close", "adj_close") if name in lower_columns), None)
    if close_column is None:
        return _empty_state("Candlestick", "A serie precisa de uma coluna Close para o desenho.", "Candlestick")

    open_column = next((lower_columns[name] for name in ("open",) if name in lower_columns), close_column)
    high_column = next((lower_columns[name] for name in ("high",) if name in lower_columns), close_column)
    low_column = next((lower_columns[name] for name in ("low",) if name in lower_columns), close_column)

    opens = frame[open_column].astype(float).tolist()
    highs = frame[high_column].astype(float).tolist()
    lows = frame[low_column].astype(float).tolist()
    closes = frame[close_column].astype(float).tolist()

    left, top, right, bottom = 26, 24, 16, 28
    chart_width = max(width - left - right, 1)
    chart_height = max(height - top - bottom, 1)
    min_value = min(lows + opens + closes)
    max_value = max(highs + opens + closes)
    span = max(max_value - min_value, 1e-9)
    step = chart_width / max(len(closes), 1)

    def y_from_value(value: float) -> float:
        return top + (max_value - value) / span * chart_height

    bars = []
    for index, (open_value, high_value, low_value, close_value) in enumerate(zip(opens, highs, lows, closes)):
        x = left + index * step + step / 2
        candle_top = min(y_from_value(open_value), y_from_value(close_value))
        candle_bottom = max(y_from_value(open_value), y_from_value(close_value))
        candle_height = max(candle_bottom - candle_top, 1.0)
        color = ThemeColors.GREEN if close_value >= open_value else ThemeColors.RED
        bars.append(
            f"<line x1='{x:.1f}' y1='{y_from_value(high_value):.1f}' x2='{x:.1f}' y2='{y_from_value(low_value):.1f}' stroke='{color}' stroke-width='2'/>"
            f"<rect x='{x - step * 0.25:.1f}' y='{candle_top:.1f}' width='{step * 0.5:.1f}' height='{candle_height:.1f}' rx='2' fill='{color}' opacity='0.85'/>"
        )

    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
      <rect width='100%' height='100%' rx='18' fill='{ThemeColors.BACKGROUND}'/>
      <rect x='0' y='0' width='{width}' height='{height}' rx='18' fill='{ThemeColors.SURFACE}'/>
      <line x1='{left}' y1='{top}' x2='{width - right}' y2='{top}' stroke='{ThemeColors.BORDER}' stroke-width='1'/>
      <line x1='{left}' y1='{height - bottom}' x2='{width - right}' y2='{height - bottom}' stroke='{ThemeColors.BORDER}' stroke-width='1'/>
      {''.join(bars)}
      <text x='{left}' y='18' fill='{ThemeColors.TEXT_SECONDARY}' font-size='10' font-family='Arial, sans-serif'>Abertura: {opens[0]:,.2f}</text>
      <text x='{width - 20}' y='{height - 8}' fill='{ThemeColors.TEXT_SECONDARY}' font-size='10' text-anchor='end' font-family='Arial, sans-serif'>Fechamento: {closes[-1]:,.2f}</text>
    </svg>
    """
    subtitle = f"{len(frame)} candles"
    return _chart_frame("Candlestick", subtitle, svg, width, height)


class ChartPlaceholder(ft.Container):
    def __init__(self, chart_type: str = "candlestick"):
        if chart_type == "candlestick":
            title, description, icon = "Candlestick", "OHLCV da serie temporal", "Chart"
        elif chart_type == "capital_curve":
            title, description, icon = "Curva de Capital", "Evolucao do saldo durante a simulacao", "Trend"
        else:
            title, description, icon = "Grafico", "Visualizacao de dados", "Chart"

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
                    ft.Text(icon, size=42, color=ThemeColors.GREEN),
                    ft.Text(title, size=14, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                    ft.Text(description, size=11, color=ThemeColors.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                ],
            ),
        )


class MplfinanceChart:
    @staticmethod
    def create_candlestick(_data: pd.DataFrame) -> ft.Container:
        return ChartPlaceholder("candlestick")


class PlotlyChart:
    @staticmethod
    def create_capital_curve(_balances: list[float], _dates: Optional[list[str]] = None) -> ft.Container:
        return ChartPlaceholder("capital_curve")

    @staticmethod
    def create_returns_histogram(_returns: list[float], _labels: Optional[list[str]] = None) -> ft.Container:
        return ChartPlaceholder("returns")


class ChartManager:
    def __init__(self):
        self.candlestick_chart = ChartPlaceholder("candlestick")
        self.capital_curve_chart = ChartPlaceholder("capital_curve")

    def update_candlestick(self, frame: pd.DataFrame) -> ft.Control:
        self.candlestick_chart = render_candlestick_chart(frame)
        return self.candlestick_chart

    def update_capital_curve(self, values: list[float], title: str = "Curva de Capital", subtitle: str = "") -> ft.Control:
        self.capital_curve_chart = render_line_chart(values, title, subtitle)
        return self.capital_curve_chart

"""Renderização visual da QuantInvest Suite em SVG puro."""

from __future__ import annotations

import base64
from html import escape
from statistics import fmean

import flet as ft
import pandas as pd

from .components import ThemeColors


def _svg_to_data_uri(svg: str) -> str:
    payload = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{payload}"


def _safe_min(values: list[float]) -> float:
    return min(values) if values else 0.0


def _safe_max(values: list[float]) -> float:
    return max(values) if values else 1.0


def _chart_frame(title: str, subtitle: str, body_svg: str, width: int, height: int) -> ft.Container:
    image = ft.Image(src=_svg_to_data_uri(body_svg), expand=True)
    return ft.Container(
        width=width,
        height=height,
        padding=16,
        border_radius=18,
        bgcolor=ThemeColors.SURFACE,
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(title, size=15, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                                ft.Text(subtitle, size=11, color=ThemeColors.TEXT_SECONDARY),
                            ],
                        ),
                        ft.Container(expand=True),
                    ],
                ),
                ft.Container(expand=True, content=image),
            ],
        ),
    )


def render_candlestick_chart(data: pd.DataFrame, width: int = 900, height: int = 360) -> ft.Container:
    """Renderiza um gráfico candlestick simplificado em SVG."""

    if data.empty:
        svg = f"""
        <svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
          <rect width='100%' height='100%' rx='18' fill='{ThemeColors.BACKGROUND}'/>
          <text x='50%' y='50%' fill='{ThemeColors.TEXT_SECONDARY}' font-size='18' text-anchor='middle'>Sem dados para exibir</text>
        </svg>
        """
        return _chart_frame("Candlestick", "Aguardando arquivo CSV", svg, width, height)

    frame = data.copy()
    if not isinstance(frame.index, pd.DatetimeIndex):
        frame.index = pd.to_datetime(frame.index)

    opens = frame["Open"].astype(float).tolist()
    highs = frame["High"].astype(float).tolist()
    lows = frame["Low"].astype(float).tolist()
    closes = frame["Close"].astype(float).tolist()
    dates = [index.strftime("%d/%m") for index in frame.index]

    min_price = _safe_min(lows)
    max_price = _safe_max(highs)
    price_span = max(max_price - min_price, 1e-9)

    chart_width = width - 40
    chart_height = height - 80
    top = 40
    bottom = height - 30
    left = 20
    candle_space = chart_width / max(len(frame), 1)
    candle_width = max(4, candle_space * 0.55)

    def y_from_price(price: float) -> float:
        return top + (max_price - price) / price_span * chart_height

    grid_lines = []
    for fraction in [0.0, 0.25, 0.5, 0.75, 1.0]:
        y = top + chart_height * fraction
        price_value = max_price - price_span * fraction
        grid_lines.append(
            f"<line x1='{left}' y1='{y:.1f}' x2='{width - 16}' y2='{y:.1f}' stroke='#28302f' stroke-width='1' />"
        )
        grid_lines.append(
            f"<text x='24' y='{y - 4:.1f}' fill='{ThemeColors.TEXT_SECONDARY}' font-size='10'>{price_value:,.2f}</text>"
        )

    candle_svg = []
    for index, (open_price, high_price, low_price, close_price) in enumerate(zip(opens, highs, lows, closes, strict=False)):
        x_center = left + candle_space * index + candle_space / 2
        high_y = y_from_price(high_price)
        low_y = y_from_price(low_price)
        open_y = y_from_price(open_price)
        close_y = y_from_price(close_price)
        color = ThemeColors.GREEN if close_price >= open_price else ThemeColors.RED
        body_top = min(open_y, close_y)
        body_height = max(abs(close_y - open_y), 1.5)

        candle_svg.append(
            f"<line x1='{x_center:.1f}' y1='{high_y:.1f}' x2='{x_center:.1f}' y2='{low_y:.1f}' stroke='{color}' stroke-width='1.5' />"
        )
        candle_svg.append(
            f"<rect x='{x_center - candle_width / 2:.1f}' y='{body_top:.1f}' width='{candle_width:.1f}' height='{body_height:.1f}' rx='2' fill='{color}' opacity='0.85' />"
        )
        if index % max(len(frame) // 8, 1) == 0:
            candle_svg.append(
                f"<text x='{x_center:.1f}' y='{bottom:.1f}' fill='{ThemeColors.TEXT_SECONDARY}' font-size='10' text-anchor='middle'>{escape(dates[index])}</text>"
            )

    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
      <rect width='100%' height='100%' rx='18' fill='{ThemeColors.BACKGROUND}'/>
      {''.join(grid_lines)}
      {''.join(candle_svg)}
    </svg>
    """
    return _chart_frame("Candlestick", f"Último fechamento: {closes[-1]:,.2f}", svg, width, height)


def render_line_chart(values: list[float], title: str, subtitle: str, width: int = 900, height: int = 260) -> ft.Container:
    """Renderiza uma curva simples em SVG."""

    if not values:
        svg = f"""
        <svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
          <rect width='100%' height='100%' rx='18' fill='{ThemeColors.BACKGROUND}'/>
          <text x='50%' y='50%' fill='{ThemeColors.TEXT_SECONDARY}' font-size='18' text-anchor='middle'>Sem dados para exibir</text>
        </svg>
        """
        return _chart_frame(title, subtitle, svg, width, height)

    min_value = _safe_min(values)
    max_value = _safe_max(values)
    span = max(max_value - min_value, 1e-9)
    chart_width = width - 40
    chart_height = height - 70
    top = 26
    left = 20
    step = chart_width / max(len(values) - 1, 1)

    def y_from_value(value: float) -> float:
        return top + (max_value - value) / span * chart_height

    points = [f"{left + index * step:.1f},{y_from_value(value):.1f}" for index, value in enumerate(values)]
    area_points = [f"{left:.1f},{height - 20}"] + points + [f"{left + chart_width:.1f},{height - 20}"]
    mid_value = fmean(values)

    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>
      <rect width='100%' height='100%' rx='18' fill='{ThemeColors.BACKGROUND}'/>
      <line x1='{left}' y1='{top}' x2='{width - 16}' y2='{top}' stroke='#28302f' stroke-width='1'/>
      <line x1='{left}' y1='{height - 20}' x2='{width - 16}' y2='{height - 20}' stroke='#28302f' stroke-width='1'/>
      <polyline points="{' '.join(points)}" fill='none' stroke='{ThemeColors.GREEN}' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/>
      <polygon points="{' '.join(area_points)}" fill='{ThemeColors.GREEN}' opacity='0.08'/>
      <text x='{left}' y='18' fill='{ThemeColors.TEXT_SECONDARY}' font-size='10'>Média: {mid_value:,.2f}</text>
      <text x='{width - 20}' y='{height - 6}' fill='{ThemeColors.TEXT_SECONDARY}' font-size='10' text-anchor='end'>Último: {values[-1]:,.2f}</text>
    </svg>
    """
    return _chart_frame(title, subtitle, svg, width, height)
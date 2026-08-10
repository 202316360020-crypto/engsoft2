"""Renderização visual da QuantInvest Suite em SVG puro."""

from __future__ import annotations

import base64
from html import escape
from statistics import fmean

import flet as ft
import pandas as pd


class ChartPlaceholder(ft.Container):
    """Placeholder para gráficos enquanto o Core está em desenvolvimento."""

    def __init__(self, chart_type: str = "candlestick"):
        """
        Inicializar placeholder de gráfico.

        Args:
            chart_type: Tipo de gráfico ("candlestick" ou "capital_curve")
        """
        self.chart_type = chart_type

        # Determinar mensagem baseada no tipo
        if chart_type == "candlestick":
            title = "Gráfico Candlestick"
            description = "OHLCV da série temporal"
            icon = "📊"
        elif chart_type == "capital_curve":
            title = "Curva de Capital"
            description = "Evolução do saldo durante simulação"
            icon = "📈"
        else:
            title = "Gráfico"
            description = "Visualização de dados"
            icon = "📉"

        super().__init__(
            content=ft.Column(
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        icon,
                        size=56,
                        opacity=0.6,
                    ),
                    ft.Text(
                        title,
                        size=14,
                        weight="bold",
                        color="#00ff88",  # Verde como o tema
                    ),
                    ft.Text(
                        description,
                        size=11,
                        color="#ffffff",  # Branco para ficar visível
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Execute uma simulação para visualizar dados",
                        size=10,
                        italic=True,
                        color="#b0b0b0",  # Cinza claro
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
            bgcolor="#1a1a1a",
            border_radius=8,
            border="1px solid #333333",
            padding=20,
            expand=True,
            height=300,
        )


class MplfinanceChart:
    """
    Integração com mplfinance para gráficos candlestick.

    Será implementado quando o Core fornecer dados OHLCV.
    """

    @staticmethod
    def create_candlestick(_data: pd.DataFrame) -> ft.Container:
        """
        Criar gráfico candlestick com mplfinance.

        Args:
            data: DataFrame OHLCV com colunas (Date, Open, High, Low, Close, Volume)

        Returns:
            Container Flet com o gráfico

        Note:
            Implementação será feita após integração com Core.
        """
        # TODO: Implementar quando Core fornecer dados
        return ChartPlaceholder("candlestick")


class PlotlyChart:
    """
    Integração com plotly para gráficos interativos.

    Será implementado quando o Core fornecer dados de simulação.
    """

    @staticmethod
    def create_capital_curve(
        _balances: list[float],
        _dates: Optional[list[str]] = None
    ) -> ft.Container:
        """
        Criar gráfico de curva de capital com plotly.

        Args:
            balances: Lista de saldos ao longo do tempo
            dates: Lista de datas (opcional)

        Returns:
            Container Flet com o gráfico

        Note:
            Implementação será feita após integração com Core.
        """
        # TODO: Implementar quando Core fornecer dados de simulação
        return ChartPlaceholder("capital_curve")

    @staticmethod
    def create_returns_histogram(
        _returns: list[float],
        _labels: Optional[list[str]] = None
    ) -> ft.Container:
        """
        Criar histograma de retornos com plotly.

        Args:
            returns: Lista de retornos
            labels: Rótulos das barras (opcional)

        Returns:
            Container Flet com o histograma

        Note:
            Implementação será feita após integração com Core.
        """
        # TODO: Implementar quando Core fornecer dados de análise
        return ChartPlaceholder("returns")


class ChartManager:
    """
    Gerenciador central de gráficos.

    Coordena criação e atualização de gráficos a partir de dados do Core.
    """

    def __init__(self):
        """Inicializar gerenciador de gráficos."""
        self.candlestick_chart = ChartPlaceholder("candlestick")
        self.capital_curve_chart = ChartPlaceholder("capital_curve")

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
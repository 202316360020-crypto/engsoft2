"""Aplicação principal da GUI do QuantInvest Suite."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import flet as ft
import pandas as pd

from ..core.service import aggregate_runs, simulate_file, simulate_files
from .charts import render_candlestick_chart, render_line_chart
from .components import ThemeColors


class QuantInvestApp:
    """Dashboard de backtest com aparência próxima de uma plataforma de trading."""

    def __init__(self) -> None:
        self.page: Optional[ft.Page] = None
        self.selected_file: Optional[str] = None
        self.strategy_value: str = "Buy and Hold"
        self.capital_value: str = "10000"
        self.status_value: str = "Prévia visual pronta para integração com o Core"

        self.file_path_display: Optional[ft.TextField] = None
        self.strategy_dropdown: Optional[ft.Dropdown] = None

    def build_page(self, page: ft.Page) -> None:
        self.page = page
        page.title = "QuantInvest Suite"
        page.bgcolor = ThemeColors.BACKGROUND
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        page.window_width = 1500
        page.window_height = 940

        page.add(self._build_shell())

    def _build_shell(self) -> ft.Control:
        return ft.Container(
            expand=True,
            bgcolor=ThemeColors.BACKGROUND,
            padding=20,
            content=ft.Column(
                spacing=16,
                controls=[
                    self._build_header(),
                    self._build_metrics_row(),
                    ft.Row(spacing=16, expand=True, controls=[self.chart_area, self.equity_area]),
                    self._build_results_panel(),
                ],
            ),
        )

    def _build_header(self) -> ft.Control:
        return ft.Container(
            padding=18,
            border_radius=18,
            bgcolor=ThemeColors.SURFACE,
            content=ft.Row(
                controls=[
                    ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text("Backtest", size=11, color=ThemeColors.TEXT_SECONDARY),
                            ft.Text("QuantInvest Suite", size=24, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                            ft.Text("Motor de backtesting e análise de estratégias", size=12, color=ThemeColors.TEXT_SECONDARY),
                        ],
                    ),
                    ft.Container(expand=True),
                    ft.Container(
                        padding=10,
                        border_radius=999,
                        bgcolor="#13231d",
                        content=ft.Text("Dashboard", size=11, weight="bold", color=ThemeColors.GREEN),
                    ),
                ],
            ),
        )

    def _build_metrics_row(self) -> ft.Control:
        return ft.Row(
            spacing=16,
            controls=[
                self._metric_card("Saldo final", self.metrics["final_balance"], "Capital após a simulação"),
                self._metric_card("Retorno total", self.metrics["total_return"], "Variação percentual"),
                self._metric_card("Taxa de acerto", self.metrics["win_rate"], "Operações vencedoras"),
                self._metric_card("Max drawdown", self.metrics["max_drawdown"], "Maior retração"),
            ],
        )

    def _metric_card(self, label: str, value_control: ft.Text, subtitle: str) -> ft.Control:
        return ft.Container(
            expand=True,
            padding=18,
            border_radius=18,
            bgcolor=ThemeColors.SURFACE,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(label, size=11, color=ThemeColors.TEXT_SECONDARY),
                    value_control,
                    ft.Text(subtitle, size=10, color=ThemeColors.TEXT_SECONDARY),
                ],
            ),
        )

    def _build_results_panel(self) -> ft.Control:
        return ft.Container(
            padding=18,
            border_radius=18,
            bgcolor=ThemeColors.SURFACE,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Candlestick", size=15, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                            ft.Container(
                                expand=True,
                                border_radius=16,
                                bgcolor="#111a16",
                                content=ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("🕯️", size=44, color=ThemeColors.GREEN),
                                        ft.Text("Pré-visualização OHLCV", size=14, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                                        ft.Text("Espaço reservado para o gráfico financeiro.", size=11, color=ThemeColors.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )

    def _build_configuration_row(self) -> ft.Control:
        self.file_path_display = ft.TextField(
            label="Arquivo CSV",
            value="Nenhum arquivo selecionado",
            read_only=True,
            bgcolor=ThemeColors.SURFACE_LIGHT,
            border_color=ThemeColors.BORDER_LIGHT,
            color=ThemeColors.TEXT_PRIMARY,
        )

        self.strategy_dropdown = ft.Dropdown(
            label="Estratégia",
            value=self.strategy_value,
            options=[
                ft.dropdown.Option("Buy and Hold"),
                ft.dropdown.Option("Cruzamento de Médias Móveis"),
            ],
            bgcolor=ThemeColors.SURFACE_LIGHT,
            border_color=ThemeColors.BORDER_LIGHT,
            color=ThemeColors.TEXT_PRIMARY,
        )
        self.strategy_dropdown.on_change = self.on_strategy_changed

        self.capital_input = ft.TextField(
            label="Capital Inicial",
            value=self.capital_value,
            bgcolor=ThemeColors.SURFACE_LIGHT,
            border_color=ThemeColors.BORDER_LIGHT,
            color=ThemeColors.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.results_summary = ft.Text(
            "Nenhuma simulação executada ainda.",
            size=11,
            color=ThemeColors.TEXT_SECONDARY,
        )

        return ft.Row(
            spacing=16,
            controls=[
                ft.Container(
                    width=860,
                    padding=18,
                    border_radius=18,
                    bgcolor=ThemeColors.SURFACE,
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Text("Configuração da simulação", size=15, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                            ft.Row(
                                spacing=12,
                                controls=[
                                    ft.Container(expand=True, content=self.file_path_display),
                                    ft.Container(
                                        width=170,
                                        content=ft.ElevatedButton(
                                            "Selecionar CSV",
                                            bgcolor=ThemeColors.GREEN,
                                            color=ThemeColors.BACKGROUND,
                                            on_click=self.on_select_file_click,
                                        ),
                                    ),
                                ],
                            ),
                            ft.Row(
                                spacing=12,
                                controls=[
                                    ft.Container(expand=True, content=self.strategy_dropdown),
                                    ft.Container(expand=True, content=self.capital_input),
                                ],
                            ),
                            ft.Row(
                                spacing=12,
                                controls=[
                                    ft.Container(
                                        expand=True,
                                        content=ft.ElevatedButton(
                                            "Executar simulação",
                                            bgcolor=ThemeColors.GREEN,
                                            color=ThemeColors.BACKGROUND,
                                            on_click=self.on_simulate_click,
                                        ),
                                    ),
                                    ft.Container(
                                        expand=True,
                                        content=ft.ElevatedButton(
                                            "Limpar",
                                            bgcolor=ThemeColors.BORDER_LIGHT,
                                            color=ThemeColors.TEXT_PRIMARY,
                                            on_click=self.on_clear_click,
                                        ),
                                    ),
                                ],
                            ),
                            ft.Container(
                                padding=16,
                                border_radius=16,
                                bgcolor="#111a16",
                                content=ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Text("Resumo", size=13, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                                        self.results_summary,
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    width=320,
                    padding=18,
                    border_radius=18,
                    bgcolor=ThemeColors.SURFACE,
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Text("Painel de contexto", size=15, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                            ft.Container(
                                padding=16,
                                border_radius=16,
                                bgcolor="#111a16",
                                content=ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Text("Integração prevista", size=12, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                                        ft.Text(
                                            "A interface já está pronta para receber o Core sem acoplamento à lógica de negócio.",
                                            size=11,
                                            color=ThemeColors.TEXT_SECONDARY,
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(
                                padding=16,
                                border_radius=16,
                                bgcolor="#111a16",
                                content=ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Text("Fluxo", size=12, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                                        ft.Text(
                                            "1. Selecionar CSV\n2. Escolher estratégia\n3. Informar capital\n4. Executar",
                                            size=11,
                                            color=ThemeColors.TEXT_SECONDARY,
                                        ),
                                    ],
                                ),
                            ),
                            self.status_text if self.status_text is not None else ft.Text(self.status_value, size=11, color=ThemeColors.TEXT_SECONDARY),
                        ],
                    ),
                ),
            ],
        )

    def on_select_file_click(self, _event: ft.ControlEvent) -> None:
        """Simula a seleção de um CSV enquanto o Core não estiver integrado."""
        self.selected_file = "dados/ohlcv_exemplo.csv"
        if self.file_path_display is not None:
            self.file_path_display.value = self.selected_file
            self.file_path_display.update()
        self._set_status("Arquivo carregado e pronto para simulação")

    def on_strategy_changed(self, _event: ft.ControlEvent) -> None:
        if self.strategy_dropdown is not None and self.strategy_dropdown.value:
            self.strategy_value = str(self.strategy_dropdown.value)
            self._set_status(f"Estratégia selecionada: {self.strategy_value}")

    def on_simulate_click(self, _event: ft.ControlEvent) -> None:
        if not self.selected_file_paths:
            self.show_error("Selecione ao menos um arquivo CSV")
            return

        capital = self._parse_float_field(self.capital_input, "Capital inválido")
        short_window = self._parse_int_field(self.short_input, "Janela curta inválida")
        long_window = self._parse_int_field(self.long_input, "Janela longa inválida")
        if capital is None or short_window is None or long_window is None:
            return

        start_date = self.start_input.value.strip() if self.start_input and self.start_input.value else None
        end_date = self.end_input.value.strip() if self.end_input and self.end_input.value else None

        try:
            if len(self.selected_file_paths) == 1:
                run = simulate_file(
                    self.selected_file_paths[0],
                    self.strategy_value,
                    capital,
                    start_date=start_date,
                    end_date=end_date,
                    short_window=short_window,
                    long_window=long_window,
                )
                runs = [run]
                summary = run.result
            else:
                runs = simulate_files(
                    self.selected_file_paths,
                    self.strategy_value,
                    capital,
                    start_date=start_date,
                    end_date=end_date,
                    short_window=short_window,
                    long_window=long_window,
                )
                summary = aggregate_runs(runs, capital)

            self.current_run = runs[0]
            self._update_metrics(summary)
            self._update_visuals(runs[0].data, runs[0].result.equity_curve)
            self._update_summary(runs, summary, capital)
            self._set_status(f"Simulação concluída com {len(runs)} arquivo(s)")
        except Exception as exc:
            self.show_error(str(exc))

    def on_clear_click(self, _event: ft.ControlEvent) -> None:
        self.selected_file_paths = []
        self.strategy_value = "Buy and Hold"
        self.current_run = None

        if self.file_text is not None:
            self.file_text.value = "Nenhum arquivo selecionado"
        if self.strategy_dropdown is not None:
            self.strategy_dropdown.value = self.strategy_value
        if self.capital_input is not None:
            self.capital_input.value = "10000"
        if self.results_summary is not None:
            self.results_summary.value = "Nenhuma simulação executada ainda."

        if self.metric_final_balance is not None:
            self.metric_final_balance.value = "R$ 10.000,00"
        if self.metric_return is not None:
            self.metric_return.value = "0,00%"
            self.metric_return.color = ThemeColors.GREEN
        if self.metric_win_rate is not None:
            self.metric_win_rate.value = "0,00%"
        if self.metric_drawdown is not None:
            self.metric_drawdown.value = "0,00%"

        self._set_status("Prévia visual pronta para integração com o Core")
        self._refresh_metrics()

    def show_error(self, message: str) -> None:
        if self.page is None:
            return
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message, color=ThemeColors.RED), bgcolor=ThemeColors.SURFACE)
        self.page.snack_bar.open = True
        self.page.update()

    def _set_status(self, message: str) -> None:
        self.status_value = message
        if self.status_text is not None:
            self.status_text.value = message
        self._refresh_page()

    def _refresh_page(self) -> None:
        if self.page is not None:
            self.page.update()


def main() -> None:
    app = QuantInvestApp()
    ft.app(target=app.build_page)


if __name__ == "__main__":
    main()
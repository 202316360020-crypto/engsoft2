"""Aplicação principal da GUI do QuantInvest Suite.

Esta versão prioriza estabilidade de renderização no Flet desktop.
A tela é visual, desacoplada do Core e usa apenas controles simples.
"""

from __future__ import annotations

from typing import Optional

import flet as ft

from .components import ThemeColors


class QuantInvestApp:
    """Aplicação principal da interface gráfica."""

    def __init__(self) -> None:
        """Inicializa o estado da interface."""
        self.page: Optional[ft.Page] = None
        self.selected_file: Optional[str] = None
        self.strategy_value: str = "Buy and Hold"
        self.capital_value: str = "10000"
        self.status_value: str = "Prévia visual pronta para integração com o Core"

        self.file_path_display: Optional[ft.TextField] = None
        self.strategy_dropdown: Optional[ft.Dropdown] = None
        self.capital_input: Optional[ft.TextField] = None
        self.status_text: Optional[ft.Text] = None
        self.metric_final_balance: Optional[ft.Text] = None
        self.metric_return: Optional[ft.Text] = None
        self.metric_win_rate: Optional[ft.Text] = None
        self.metric_drawdown: Optional[ft.Text] = None
        self.results_summary: Optional[ft.Text] = None

    def build_page(self, page: ft.Page) -> None:
        """Constrói a página principal da aplicação."""
        self.page = page
        page.title = "QuantInvest Suite"
        page.bgcolor = ThemeColors.BACKGROUND
        page.window_width = 1440
        page.window_height = 920
        page.padding = 0
        page.theme_mode = ft.ThemeMode.DARK

        page.add(self._build_shell())
        page.update()

    def _build_shell(self) -> ft.Control:
        return ft.Container(
            bgcolor=ThemeColors.BACKGROUND,
            padding=20,
            content=ft.Column(
                spacing=16,
                controls=[
                    self._build_header(),
                    self._build_metrics_row(),
                    self._build_visual_row(),
                    self._build_configuration_row(),
                ],
            ),
        )

    def _build_header(self) -> ft.Control:
        self.status_text = ft.Text(self.status_value, size=12, color=ThemeColors.TEXT_SECONDARY)

        return ft.Container(
            padding=18,
            border_radius=18,
            bgcolor=ThemeColors.SURFACE,
            content=ft.Row(
                spacing=16,
                controls=[
                    ft.Container(
                        width=46,
                        height=46,
                        border_radius=14,
                        bgcolor=ThemeColors.GREEN,
                        content=ft.Text("Q", color=ThemeColors.BACKGROUND, weight="bold", size=20),
                    ),
                    ft.Column(
                        spacing=2,
                        controls=[
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
        self.metric_final_balance = ft.Text("R$ 10.000,00", size=24, weight="bold", color=ThemeColors.GREEN)
        self.metric_return = ft.Text("0,00%", size=24, weight="bold", color=ThemeColors.GREEN)
        self.metric_win_rate = ft.Text("0,00%", size=24, weight="bold", color=ThemeColors.GREEN)
        self.metric_drawdown = ft.Text("0,00%", size=24, weight="bold", color=ThemeColors.RED)

        return ft.Row(
            spacing=16,
            controls=[
                self._metric_card("Saldo Final", self.metric_final_balance, "Capital simulado"),
                self._metric_card("Retorno Total", self.metric_return, "Performance acumulada"),
                self._metric_card("Taxa de Acerto", self.metric_win_rate, "Operações lucrativas"),
                self._metric_card("Max Drawdown", self.metric_drawdown, "Maior retração"),
            ],
        )

    def _metric_card(self, label: str, value_control: ft.Text, subtitle: str) -> ft.Control:
        return ft.Container(
            width=320,
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

    def _build_visual_row(self) -> ft.Control:
        return ft.Row(
            spacing=16,
            controls=[
                ft.Container(
                    width=860,
                    height=340,
                    padding=18,
                    border_radius=18,
                    bgcolor=ThemeColors.SURFACE,
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Curva de capital", size=15, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                                    ft.Container(expand=True),
                                    ft.Text("Preview", size=11, color=ThemeColors.TEXT_SECONDARY),
                                ],
                            ),
                            ft.Container(
                                expand=True,
                                border_radius=16,
                                bgcolor="#111a16",
                                content=ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("📈", size=44, color=ThemeColors.GREEN),
                                        ft.Text("Gráfico de curva de capital", size=14, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                                        ft.Text("Será alimentado pelo Core quando a camada de simulação estiver pronta.", size=11, color=ThemeColors.TEXT_SECONDARY, text_align=ft.TextAlign.CENTER),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    width=320,
                    height=340,
                    padding=18,
                    border_radius=18,
                    bgcolor=ThemeColors.SURFACE,
                    content=ft.Column(
                        spacing=12,
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
        """Atualiza o texto de status quando a estratégia muda."""
        if self.strategy_dropdown is not None:
            self.strategy_value = str(self.strategy_dropdown.value)
            self._set_status(f"Estratégia selecionada: {self.strategy_value}")

    def on_simulate_click(self, _event: ft.ControlEvent) -> None:
        """Executa a simulação mock da interface."""
        if self.selected_file is None:
            self.show_error("Selecione um arquivo CSV")
            return

        capital = self._parse_capital_value()
        if capital is None:
            return

        strategy = self.strategy_value
        final_balance, total_return_pct, win_rate_pct, max_drawdown_pct, total_trades = self._build_mock_result(strategy, capital)

        final_balance = capital * (1 + total_return_pct / 100)

        if self.metric_final_balance is not None:
            self.metric_final_balance.value = f"R$ {final_balance:,.2f}"
        if self.metric_return is not None:
            self.metric_return.value = f"{total_return_pct:.2f}%"
            self.metric_return.color = ThemeColors.GREEN if total_return_pct >= 0 else ThemeColors.RED
        if self.metric_win_rate is not None:
            self.metric_win_rate.value = f"{win_rate_pct:.1f}%"
        if self.metric_drawdown is not None:
            self.metric_drawdown.value = f"{max_drawdown_pct:.2f}%"
        if self.results_summary is not None:
            self.results_summary.value = (
                f"Estratégia: {strategy} | Saldo final: R$ {final_balance:,.2f} | "
                f"Trades: {total_trades} | Drawdown: {max_drawdown_pct:.2f}%"
            )

        self._set_status(f"Simulação concluída com {strategy}")
        self._refresh_metrics()

    def on_clear_click(self, _event: ft.ControlEvent) -> None:
        """Limpa os campos e retorna a interface ao estado inicial."""
        self.selected_file = None
        self.strategy_value = "Buy and Hold"
        self.capital_value = "10000"

        if self.file_path_display is not None:
            self.file_path_display.value = "Nenhum arquivo selecionado"
        if self.strategy_dropdown is not None:
            self.strategy_dropdown.value = "Buy and Hold"
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
        """Exibe uma mensagem de erro na própria interface."""
        if self.page is None:
            return

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ThemeColors.RED),
            bgcolor=ThemeColors.SURFACE,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _set_status(self, message: str) -> None:
        self.status_value = message
        if self.status_text is not None:
            self.status_text.value = message
            self.status_text.update()

    def _refresh_metrics(self) -> None:
        if self.page is not None:
            self.page.update()

    def _parse_capital_value(self) -> float | None:
        if self.capital_input is None or not self.capital_input.value:
            self.show_error("Informe um capital válido")
            return None

        try:
            capital = float(self.capital_input.value)
        except ValueError:
            self.show_error("Capital deve ser um número válido")
            return None

        if capital <= 0:
            self.show_error("Capital deve ser maior que zero")
            return None

        return capital

    def _build_mock_result(self, strategy: str, capital: float) -> tuple[float, float, float, float, int]:
        if strategy == "Buy and Hold":
            total_return_pct = 12.4
            win_rate_pct = 100.0
            max_drawdown_pct = 4.2
            total_trades = 1
        else:
            total_return_pct = 18.6
            win_rate_pct = 66.7
            max_drawdown_pct = 7.8
            total_trades = 6

        final_balance = capital * (1 + total_return_pct / 100)
        return final_balance, total_return_pct, win_rate_pct, max_drawdown_pct, total_trades


def main() -> None:
    """Ponto de entrada da GUI."""
    app = QuantInvestApp()
    ft.app(target=app.build_page)


if __name__ == "__main__":
    main()

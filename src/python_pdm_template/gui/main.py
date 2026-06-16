"""
Aplicação principal da GUI - QuantInvest Suite.

Interface Flet com tema escuro e estilo financeiro para simulação
de estratégias de investimento.
"""

from typing import Optional

import flet as ft

from .charts import ChartManager
from .components import (
    CustomButton,
    CustomDropdown,
    CustomTextField,
    ResultMetric,
    ThemeColors,
)


class QuantInvestApp:
    """Aplicação principal do QuantInvest Suite."""

    def __init__(self):
        """Inicializar aplicação."""
        self.page: Optional[ft.Page] = None
        self.chart_manager = ChartManager()
        self.selected_file: Optional[str] = None
        self.simulation_results: dict = {}

        self.file_picker = ft.FilePicker()
        self.file_path_display = None
        self.strategy_dropdown = None
        self.capital_input = None
        self.results_panel = None
        self.metric_saldo = None
        self.metric_retorno = None
        self.metric_acerto = None
        self.metric_drawdown = None

    # ========================================================================
    # CALLBACKS
    # ========================================================================

    def on_file_selected(self, e: ft.FilePickerResultEvent) -> None:
        """Callback ao selecionar arquivo."""
        if e.files:
            self.selected_file = e.files[0].path
            self.file_path_display.value = self.selected_file
            self.file_path_display.update()

    def on_strategy_changed(self, e: ft.ControlEvent) -> None:
        """Callback ao mudar estratégia."""
        pass

    def on_simulate_click(self, e: ft.ControlEvent) -> None:
        """Callback ao clicar em 'Executar Simulação'."""
        if not self.selected_file:
            self.show_error("Selecione um arquivo CSV")
            return

        if not self.strategy_dropdown.value:
            self.show_error("Selecione uma estratégia")
            return

        try:
            capital = float(self.capital_input.value)
            if capital <= 0:
                self.show_error("Capital deve ser maior que zero")
                return
        except ValueError:
            self.show_error("Capital deve ser um número válido")
            return

        # Ponte para o Core — será substituído pela chamada real
        self.run_simulation_mock(capital)

    def run_simulation_mock(self, capital: float) -> None:
        """Executar simulação mock (até Core estar pronto)."""
        self.simulation_results = {
            "final_balance": capital * 1.15,
            "total_return_pct": 15.0,
            "win_rate_pct": 62.5,
            "max_drawdown_pct": 8.3,
            "total_trades": 8,
        }
        self.update_results_panel()

    def update_results_panel(self) -> None:
        """Atualizar painel de resultados."""
        if not self.simulation_results:
            return

        results = self.simulation_results

        # Atualizar valores das métricas
        # ResultMetric agora é Container → Column → [Text(label), Row]
        self.metric_saldo.content.controls[1].controls[0].value = f"R$ {results['final_balance']:,.2f}"
        self.metric_retorno.content.controls[1].controls[0].value = f"{results['total_return_pct']:.2f}"
        self.metric_acerto.content.controls[1].controls[0].value = f"{results['win_rate_pct']:.1f}"
        self.metric_drawdown.content.controls[1].controls[0].value = f"{results['max_drawdown_pct']:.2f}"

        # Mudar cor do retorno baseado em positivo/negativo
        positive_return = results['total_return_pct'] > 0
        self.metric_retorno.content.controls[1].controls[0].color = (
            ThemeColors.GREEN if positive_return else ThemeColors.RED
        )

        self.results_panel.visible = True
        self.page.update()

    def show_error(self, message: str) -> None:
        """Mostrar mensagem de erro."""
        snack = ft.SnackBar(
            ft.Text(message, color=ThemeColors.RED),
            bgcolor=ThemeColors.SURFACE,
        )
        self.page.snack_bar = snack
        snack.open = True
        self.page.update()

    # ========================================================================
    # CONSTRUÇÃO DA UI
    # ========================================================================

    def build_input_section(self) -> ft.Column:
        """Seção de inputs."""
        self.file_picker.on_result = self.on_file_selected
        self.file_path_display = ft.TextField(
            label="CSV",
            read_only=True,
            border_radius=6,
            bgcolor=ThemeColors.SURFACE_LIGHT,
            border_color=ThemeColors.BORDER_LIGHT,
        )

        file_btn = CustomButton(
            "Selecionar CSV",
            on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["csv"]),
        )
        self.strategy_dropdown = CustomDropdown(
            "Estratégia",
            ["Buy and Hold", "Cruzamento de Médias Móveis"],
        )
        self.strategy_dropdown.on_change = self.on_strategy_changed
        self.capital_input = CustomTextField("Capital (R$)", value="10000")

        return ft.Column(
            spacing=12,
            controls=[
                ft.Container(
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text(
                                "⚙️ Configuração da Simulação",
                                size=15,
                                weight="bold",
                                color=ThemeColors.GREEN,
                            ),
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Container(self.file_path_display, expand=True),
                                    ft.Container(file_btn, width=140),
                                ],
                            ),
                            ft.Row(
                                spacing=8,
                                controls=[
                                    ft.Container(self.strategy_dropdown, expand=True),
                                    ft.Container(self.capital_input, expand=True),
                                ],
                            ),
                        ],
                    ),
                    bgcolor=ThemeColors.SURFACE,
                    padding=16,
                    border_radius=8,
                    border=f"1px solid {ThemeColors.BORDER}",
                ),
            ],
        )

    def build_controls_section(self) -> ft.Row:
        """Seção de botões de controle."""
        simulate_button = CustomButton(
            "▶ Executar Simulação",
            on_click=self.on_simulate_click,
            primary=True,
        )
        clear_button = CustomButton(
            "↻ Limpar",
            on_click=lambda _: self.on_clear_click(),
            primary=False,
        )

        return ft.Row(
            spacing=12,
            controls=[
                ft.Container(content=simulate_button, expand=True),
                ft.Container(content=clear_button, expand=True, width=140),
            ],
        )

    def build_results_section(self) -> ft.Column:
        """Seção de resultados."""
        self.metric_saldo = ResultMetric("Saldo Final", "R$ 0,00", unit="", positive=True)
        self.metric_retorno = ResultMetric("Retorno Total", "0,00", unit="%", positive=True)
        self.metric_acerto = ResultMetric("Taxa de Acerto", "0,00", unit="%", positive=True)
        self.metric_drawdown = ResultMetric("Max Drawdown", "0,00", unit="%", positive=False)

        self.results_panel = ft.Column(
            spacing=12,
            visible=False,
            controls=[
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(self.metric_saldo, expand=True),
                        ft.Container(self.metric_retorno, expand=True),
                    ],
                ),
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(self.metric_acerto, expand=True),
                        ft.Container(self.metric_drawdown, expand=True),
                    ],
                ),
            ],
        )

        return ft.Column(
            spacing=12,
            controls=[
                ft.Container(
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Text(
                                "📊 Resultados da Simulação",
                                size=15,
                                weight="bold",
                                color=ThemeColors.GREEN,
                            ),
                            self.results_panel,
                        ],
                    ),
                    bgcolor=ThemeColors.SURFACE,
                    padding=16,
                    border_radius=8,
                    border=f"1px solid {ThemeColors.BORDER}",
                ),
            ],
        )

    def build_charts_section(self) -> ft.Column:
        """Seção de gráficos."""
        return ft.Column(
            spacing=12,
            controls=[
                ft.Container(
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Text(
                                "📈 Visualização de Dados",
                                size=15,
                                weight="bold",
                                color=ThemeColors.GREEN,
                            ),
                            ft.Row(
                                spacing=12,
                                controls=[
                                    ft.Container(
                                        self.chart_manager.candlestick_chart,
                                        expand=True,
                                        border_radius=8,
                                    ),
                                    ft.Container(
                                        self.chart_manager.capital_curve_chart,
                                        expand=True,
                                        border_radius=8,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    bgcolor=ThemeColors.SURFACE,
                    padding=16,
                    border_radius=8,
                    border=f"1px solid {ThemeColors.BORDER}",
                ),
            ],
        )

    def on_clear_click(self) -> None:
        """Limpar simulação."""
        self.selected_file = None
        self.simulation_results = {}
        self.file_path_display.value = ""
        self.results_panel.visible = False
        self.chart_manager.reset()
        self.page.update()

    def build_main_content(self) -> ft.Container:
        """Conteúdo principal - VERSÃO SIMPLES."""
        return ft.Container(
            content=ft.Column(
                spacing=16,
                controls=[
                    # Seção inputs - SIMPLIFICADA
                    ft.Container(
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Text(
                                    "⚙️ Configuração da Simulação",
                                    size=15,
                                    weight="bold",
                                    color=ThemeColors.GREEN,
                                ),
                                ft.TextField(label="Arquivo CSV", read_only=True),
                                ft.Row(spacing=8, controls=[
                                    ft.Dropdown(label="Estratégia", options=[
                                        ft.dropdown.Option("Buy and Hold"),
                                        ft.dropdown.Option("Cruzamento de Médias"),
                                    ]),
                                    ft.TextField(label="Capital", value="10000"),
                                ]),
                                ft.ElevatedButton("Selecionar CSV", on_click=lambda _: print("Click")),
                            ],
                        ),
                        bgcolor=ThemeColors.SURFACE,
                        padding=16,
                        border_radius=8,
                    ),
                    # Seção botões - SIMPLIFICADA
                    ft.Row(
                        spacing=12,
                        controls=[
                            ft.ElevatedButton("▶ Executar", bgcolor="#00ff88"),
                            ft.ElevatedButton("↻ Limpar", bgcolor="#666666"),
                        ],
                    ),
                ],
            ),
            padding=20,
            expand=True,
        )

    def build_header(self) -> ft.Container:
        """Header da aplicação."""
        return ft.Container(
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
                controls=[
                    ft.Text("📊", size=32),
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                "QuantInvest Suite",
                                size=24,
                                weight="bold",
                                color=ThemeColors.GREEN,
                            ),
                            ft.Text(
                                "Motor de Backtesting de Estratégias Financeiras",
                                size=12,
                                color=ThemeColors.TEXT_SECONDARY,
                            ),
                        ],
                    ),
                ],
            ),
            padding=20,
            bgcolor=ThemeColors.SURFACE,
            border_radius=0,
            border=f"0 0 1px 0 solid {ThemeColors.BORDER}",
        )

    def build_page(self, page: ft.Page) -> None:
        """Construir página da aplicação."""
        self.page = page

        page.title = "QuantInvest Suite"
        page.bgcolor = ThemeColors.BACKGROUND
        page.window_width = 1400
        page.window_height = 900
        page.padding = 0

        main_layout = ft.Column(
            spacing=0,
            controls=[
                self.build_header(),
                self.build_main_content(),
            ],
            expand=True,
        )

        page.add(main_layout)
        page.update()


def main() -> None:
    """Função principal - executar aplicação."""
    app = QuantInvestApp()
    ft.app(target=app.build_page)


if __name__ == "__main__":
    main()

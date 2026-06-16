"""
Aplicação principal da GUI - QuantInvest Suite.
VERSÃO SIMPLIFICADA - SEM COMPONENTES CUSTOMIZADOS
"""

import flet as ft
from .charts import ChartManager

class QuantInvestApp:
    def __init__(self):
        self.page = None
        self.chart_manager = ChartManager()
        self.selected_file = None
        self.simulation_results = {}

    def build_page(self, page: ft.Page):
        self.page = page
        page.title = "QuantInvest Suite"
        page.bgcolor = "#0f0f0f"
        page.window_width = 1400
        page.window_height = 900
        page.padding = 0
        
        # HEADER
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("📊", size=32),
                    ft.Column(
                        controls=[
                            ft.Text("QuantInvest Suite", size=24, weight="bold", color="#00ff88"),
                            ft.Text("Motor de Backtesting", size=12, color="#b0b0b0"),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor="#1a1a1a",
            border=f"0 0 1px 0 solid #333333",
        )
        
        # MAIN CONTENT
        main = ft.Container(
            content=ft.Column(
                controls=[
                    # Input section
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("⚙️ Configuração", size=15, weight="bold", color="#00ff88"),
                                ft.TextField(label="CSV", read_only=True),
                                ft.Row(
                                    controls=[
                                        ft.Dropdown(
                                            label="Estratégia",
                                            width=500,
                                            options=[
                                                ft.dropdown.Option("Buy and Hold"),
                                                ft.dropdown.Option("Cruzamento de Médias"),
                                            ],
                                        ),
                                        ft.TextField(label="Capital (R$)", value="10000", width=200),
                                    ],
                                    spacing=8,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton("Selecionar CSV", color="#000000", bgcolor="#00ff88"),
                                    ],
                                ),
                            ],
                            spacing=10,
                        ),
                        padding=16,
                        bgcolor="#1a1a1a",
                        border=f"1px solid #333333",
                        border_radius=8,
                    ),
                    
                    # Buttons
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("▶ Executar Simulação", color="#000000", bgcolor="#00ff88"),
                            ft.ElevatedButton("↻ Limpar", color="#ffffff", bgcolor="#444444"),
                        ],
                        spacing=12,
                    ),
                    
                    # Results section (initially hidden)
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("📊 Resultados", size=15, weight="bold", color="#00ff88"),
                                ft.Row(
                                    controls=[
                                        ft.Card(
                                            content=ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text("Saldo Final", size=11, color="#b0b0b0"),
                                                        ft.Text("R$ 10,000.00", size=22, weight="bold", color="#00ff88"),
                                                    ],
                                                    spacing=4,
                                                ),
                                                padding=16,
                                            ),
                                        ),
                                        ft.Card(
                                            content=ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text("Retorno Total", size=11, color="#b0b0b0"),
                                                        ft.Text("0.00%", size=22, weight="bold", color="#00ff88"),
                                                    ],
                                                    spacing=4,
                                                ),
                                                padding=16,
                                            ),
                                        ),
                                    ],
                                    spacing=12,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Card(
                                            content=ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text("Taxa de Acerto", size=11, color="#b0b0b0"),
                                                        ft.Text("0.00%", size=22, weight="bold", color="#00ff88"),
                                                    ],
                                                    spacing=4,
                                                ),
                                                padding=16,
                                            ),
                                        ),
                                        ft.Card(
                                            content=ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text("Max Drawdown", size=11, color="#b0b0b0"),
                                                        ft.Text("0.00%", size=22, weight="bold", color="#ff3333"),
                                                    ],
                                                    spacing=4,
                                                ),
                                                padding=16,
                                            ),
                                        ),
                                    ],
                                    spacing=12,
                                ),
                            ],
                            spacing=12,
                        ),
                        padding=16,
                        bgcolor="#1a1a1a",
                        border=f"1px solid #333333",
                        border_radius=8,
                    ),
                ],
                spacing=16,
            ),
            padding=20,
            expand=True,
        )
        
        # Add to page
        page.add(
            ft.Column(
                controls=[header, main],
                spacing=0,
                expand=True,
            )
        )
        page.update()

def main():
    app = QuantInvestApp()
    ft.app(target=app.build_page)

if __name__ == "__main__":
    main()

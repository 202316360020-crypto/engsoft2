"""Aplicação principal da GUI do QuantInvest Suite."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Optional

import flet as ft
import pandas as pd

from ..core.parser import OHLCVParser
from ..core.service import aggregate_runs, simulate_file, simulate_files
from .charts import render_candlestick_chart, render_line_chart
from .components import AccentPill, CustomButton, CustomCard, DateSelectorCard, ResultMetric, ThemeColors


class QuantInvestApp:
    """Dashboard de backtest com aparência próxima de uma plataforma de trading."""

    def __init__(self) -> None:
        self.page: Optional[ft.Page] = None
        self.selected_file_paths: list[str] = []
        self.strategy_value = "Buy and Hold"
        self.status_value = "Pronto para carregar uma série OHLCV"
        self.current_run = None

        self.file_picker: Optional[ft.FilePicker] = None
        self.file_text: Optional[ft.Text] = None
        self.status_text: Optional[ft.Text] = None
        self.error_text: Optional[ft.Text] = None
        self.summary_text: Optional[ft.Text] = None
        self.operations_area: Optional[ft.Column] = None
        self.chart_area: Optional[ft.Container] = None
        self.equity_area: Optional[ft.Container] = None
        self.error_container: Optional[ft.Container] = None
        self.start_date_value: str | None = None
        self.end_date_value: str | None = None
        self.start_selector: Optional[DateSelectorCard] = None
        self.end_selector: Optional[DateSelectorCard] = None
        self.start_picker: Optional[ft.DatePicker] = None
        self.end_picker: Optional[ft.DatePicker] = None

        self.metrics: dict[str, ft.Text] = {}
        self.capital_input: Optional[ft.TextField] = None
        self.short_input: Optional[ft.TextField] = None
        self.long_input: Optional[ft.TextField] = None
        self.strategy_dropdown: Optional[ft.Dropdown] = None

    def build_page(self, page: ft.Page) -> None:
        self.page = page
        page.title = "QuantInvest Suite"
        page.bgcolor = ThemeColors.BACKGROUND
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        page.window_width = 1500
        page.window_height = 940

        self.file_picker = ft.FilePicker()
        page.services.append(self.file_picker)
        page.add(self._build_shell())

    def _build_shell(self) -> ft.Control:
        return ft.Container(
            expand=True,
            bgcolor=ThemeColors.BACKGROUND,
            padding=18,
            content=ft.Row(spacing=18, controls=[self._build_sidebar(), self._build_main_area()]),
        )

    def _build_sidebar(self) -> ft.Control:
        self.file_text = ft.Text("Nenhum arquivo selecionado", size=11, color=ThemeColors.TEXT_SECONDARY)
        self.status_text = ft.Text(self.status_value, size=11, color=ThemeColors.TEXT_SECONDARY)
        self.error_text = ft.Text(
            "",
            size=10,
            color=ThemeColors.TEXT_SECONDARY,
        )
        self.strategy_dropdown = ft.Dropdown(
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
        self.capital_input = ft.TextField(label="Capital inicial", value="10000", bgcolor=ThemeColors.SURFACE_LIGHT, border_color=ThemeColors.BORDER_LIGHT, color=ThemeColors.TEXT_PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
        self.short_input = ft.TextField(
            label="Curta",
            value="9",
            bgcolor=ThemeColors.SURFACE_LIGHT,
            border_color=ThemeColors.BORDER_LIGHT,
            color=ThemeColors.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.long_input = ft.TextField(
            label="Longa",
            value="21",
            bgcolor=ThemeColors.SURFACE_LIGHT,
            border_color=ThemeColors.BORDER_LIGHT,
            color=ThemeColors.TEXT_PRIMARY,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.start_selector = DateSelectorCard("Data inicial", "Todo o período", on_click=self._open_start_picker)
        self.end_selector = DateSelectorCard("Data final", "Todo o período", on_click=self._open_end_picker)
        self.start_picker = ft.DatePicker(
            help_text="Selecione a data inicial",
            field_label_text="Data inicial",
            field_hint_text="Escolha no calendário",
            entry_mode=ft.DatePickerEntryMode.CALENDAR,
            on_change=self._on_start_date_change,
        )
        self.end_picker = ft.DatePicker(
            help_text="Selecione a data final",
            field_label_text="Data final",
            field_hint_text="Escolha no calendário",
            entry_mode=ft.DatePickerEntryMode.CALENDAR,
            on_change=self._on_end_date_change,
        )

        self.error_container = ft.Container(
            padding=14,
            border_radius=14,
            bgcolor="#2a1111",
            border=ft.Border(
                top=ft.BorderSide(1, ThemeColors.RED_DARK),
                right=ft.BorderSide(1, ThemeColors.RED_DARK),
                bottom=ft.BorderSide(1, ThemeColors.RED_DARK),
                left=ft.BorderSide(1, ThemeColors.RED_DARK),
            ),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text("Erros", size=12, weight="bold", color=ThemeColors.RED),
                    self.error_text,
                ],
            ),
            visible=False,
        )

        return ft.Container(
            width=330,
            padding=18,
            border_radius=18,
            bgcolor=ThemeColors.SURFACE,
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(width=40, height=40, border_radius=12, bgcolor=ThemeColors.GREEN, content=ft.Text("Q", color=ThemeColors.BACKGROUND, weight="bold", size=20)),
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text("QuantInvest", size=20, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                                    ft.Text("Backtests com leitura clara e foco em decisão", size=11, color=ThemeColors.TEXT_SECONDARY),
                                ],
                            ),
                        ],
                    ),
                    ft.Container(height=1, bgcolor=ThemeColors.BORDER),
                    ft.Text("Preparação", size=13, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                    CustomButton("Selecionar CSV(s)", on_click=self.on_select_file_click, primary=True),
                    self.file_text,
                    self.strategy_dropdown,
                    self.capital_input,
                    ft.Text("Cruzamento de médias", size=11, weight="bold", color=ThemeColors.TEXT_SECONDARY),
                    ft.Row(spacing=10, controls=[ft.Container(expand=True, content=self.short_input), ft.Container(expand=True, content=self.long_input)]),
                    ft.Row(spacing=10, controls=[ft.Container(expand=True, content=self.start_selector), ft.Container(expand=True, content=self.end_selector)]),
                    CustomButton("Executar simulação", on_click=self.on_simulate_click, primary=True),
                    CustomButton("Limpar campos", on_click=self.on_clear_click, primary=False),
                    ft.Container(
                        padding=14,
                        border_radius=14,
                        bgcolor="#111a16",
                        content=ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text("Status", size=12, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                                self.status_text,
                            ],
                        ),
                    ),
                    self.error_container,
                ],
            ),
        )

    def _build_main_area(self) -> ft.Control:
        self.metrics = {
            "final_balance": ft.Text("R$ 0,00", size=24, weight="bold", color=ThemeColors.GREEN),
            "total_return": ft.Text("0,00%", size=24, weight="bold", color=ThemeColors.GREEN),
            "win_rate": ft.Text("0,00%", size=24, weight="bold", color=ThemeColors.GREEN),
            "max_drawdown": ft.Text("0,00%", size=24, weight="bold", color=ThemeColors.RED),
        }

        self.chart_area = ft.Container(expand=True, content=render_candlestick_chart(pd.DataFrame()))
        self.equity_area = ft.Container(expand=True, content=render_line_chart([], "Curva de capital", "Resultado da estratégia"))
        self.summary_text = ft.Text("Carregue um CSV para visualizar a execução.", size=11, color=ThemeColors.TEXT_SECONDARY)
        self.operations_area = ft.Column(spacing=6, controls=[])

        return ft.Container(
            expand=True,
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
                            ft.Text("Backtest profissional", size=11, color=ThemeColors.TEXT_SECONDARY),
                            ft.Text("QuantInvest Suite", size=28, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                            ft.Text("Simulação de estratégias, validação de CSV e leitura visual da performance em uma única tela.", size=12, color=ThemeColors.TEXT_SECONDARY),
                        ],
                    ),
                    ft.Container(expand=True),
                    AccentPill("Live Dashboard"),
                ],
            ),
        )

    def _build_metrics_row(self) -> ft.Control:
        return ft.Row(
            spacing=16,
            controls=[
                self._metric_card("Saldo final", self.metrics["final_balance"], "Capital ao término da execução"),
                self._metric_card("Retorno total", self.metrics["total_return"], "Evolução percentual do capital"),
                self._metric_card("Trades lucrativos", self.metrics["win_rate"], "Operações vencedoras / operações fechadas"),
                self._metric_card("Max drawdown", self.metrics["max_drawdown"], "Maior retração observada"),
            ],
        )

    def _metric_card(self, label: str, value_control: ft.Text, subtitle: str) -> ft.Control:
        return CustomCard(
            ft.Column(
                spacing=8,
                controls=[
                    ft.Text(label, size=11, color=ThemeColors.TEXT_SECONDARY),
                    value_control,
                    ft.Text(subtitle, size=10, color=ThemeColors.TEXT_SECONDARY),
                ],
            ),
            expand=True,
        )

    def _build_results_panel(self) -> ft.Control:
        return CustomCard(
            ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Resumo da execução", size=15, weight="bold", color=ThemeColors.TEXT_PRIMARY),
                            ft.Container(expand=True),
                            ft.Text("Operações", size=11, color=ThemeColors.TEXT_SECONDARY),
                        ],
                    ),
                    self.summary_text,
                    ft.Container(height=1, bgcolor=ThemeColors.BORDER),
                    self.operations_area,
                ],
            ),
            expand=True,
        )

    async def on_select_file_click(self, _event: ft.ControlEvent) -> None:
        if self.file_picker is None:
            return
        selected_files = await self.file_picker.pick_files(allow_multiple=True, allowed_extensions=["csv"])
        paths = [file.path for file in selected_files or [] if file.path]
        self._set_selected_files(paths)

    def _open_start_picker(self, _event: ft.ControlEvent) -> None:
        if self.page is not None and self.start_picker is not None:
            self.page.show_dialog(self.start_picker)

    def _open_end_picker(self, _event: ft.ControlEvent) -> None:
        if self.page is not None and self.end_picker is not None:
            self.page.show_dialog(self.end_picker)

    def _on_start_date_change(self, _event: ft.ControlEvent) -> None:
        if self.start_picker is None or self.start_picker.value is None:
            return
        value = self.start_picker.value
        if hasattr(value, "date"):
            value = value.date()
        self.start_date_value = value.isoformat()
        if self.start_selector is not None:
            self.start_selector.set_value(self.start_date_value)
        self._refresh_page()

    def _on_end_date_change(self, _event: ft.ControlEvent) -> None:
        if self.end_picker is None or self.end_picker.value is None:
            return
        value = self.end_picker.value
        if hasattr(value, "date"):
            value = value.date()
        self.end_date_value = value.isoformat()
        if self.end_selector is not None:
            self.end_selector.set_value(self.end_date_value)
        self._refresh_page()

    def _set_selected_files(self, paths: list[str]) -> None:
        self.selected_file_paths = paths
        self.start_date_value = None
        self.end_date_value = None
        if self.start_selector is not None:
            self.start_selector.set_value(None)
        if self.end_selector is not None:
            self.end_selector.set_value(None)
        if self.file_text is not None:
            if not paths:
                self.file_text.value = "Nenhum arquivo selecionado"
            elif len(paths) == 1:
                self.file_text.value = Path(paths[0]).name
            else:
                self.file_text.value = f"{len(paths)} arquivos selecionados"
            self.file_text.update()

        date_range = self._get_selected_files_date_range(paths)
        if date_range is not None:
            start_date, end_date = date_range
            if self.file_text is not None and paths:
                selected_label = self.file_text.value or "Arquivo selecionado"
                self.file_text.value = f"{selected_label}\nIntervalo: {start_date} a {end_date}"
                self.file_text.update()
            self._set_status(
                f"Arquivos prontos para simulação. Intervalo disponível: {start_date} a {end_date}."
            )
        else:
            self._set_status("Arquivos prontos para simulação. Filtros de data reiniciados.")

    def _get_selected_files_date_range(self, paths: list[str]) -> tuple[str, str] | None:
        if not paths:
            return None

        parser = OHLCVParser()
        min_date: pd.Timestamp | None = None
        max_date: pd.Timestamp | None = None

        for file_path in paths:
            try:
                frame = parser.parse(file_path)
            except Exception:
                continue

            if frame.empty:
                continue

            current_min = pd.Timestamp(frame.index.min())
            current_max = pd.Timestamp(frame.index.max())
            min_date = current_min if min_date is None else min(min_date, current_min)
            max_date = current_max if max_date is None else max(max_date, current_max)

        if min_date is None or max_date is None:
            return None

        return min_date.date().isoformat(), max_date.date().isoformat()

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

        strategy_name = self.strategy_value
        if self.strategy_dropdown is not None and self.strategy_dropdown.value:
            strategy_name = str(self.strategy_dropdown.value)
            self.strategy_value = strategy_name

        start_date = self.start_date_value
        end_date = self.end_date_value

        try:
            if len(self.selected_file_paths) == 1:
                run = simulate_file(
                    self.selected_file_paths[0],
                    strategy_name,
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
                    strategy_name,
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
            candle_count = len(runs[0].data)
            if candle_count < 2:
                self._set_status("Simulação concluída, mas o período filtrado retornou apenas 1 candle. Amplie as datas.")
            elif strategy_name.strip().lower() == "buy and hold" and runs[0].result.total_trades <= 1:
                self._set_status(f"Simulação concluída com {len(runs)} arquivo(s). Estratégia Buy and Hold gera 1 operação por arquivo.")
            else:
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
        self.start_date_value = None
        self.end_date_value = None
        if self.start_selector is not None:
            self.start_selector.set_value(None)
        if self.end_selector is not None:
            self.end_selector.set_value(None)
        if self.short_input is not None:
            self.short_input.value = "9"
        if self.long_input is not None:
            self.long_input.value = "21"

        self._update_metrics(None)
        self._update_visuals(pd.DataFrame(), [])
        self._update_summary([], None, None)
        self._set_status("Pronto para carregar uma série OHLCV")
        self._refresh_page()

    def _update_visuals(self, data, equity_curve: list[float]) -> None:
        if self.chart_area is not None:
            self.chart_area.content = render_candlestick_chart(data)
        if self.equity_area is not None:
            self.equity_area.content = render_line_chart(equity_curve, "Curva de capital", "Evolução do saldo")
        self._refresh_page()

    def _update_metrics(self, summary) -> None:
        if summary is None:
            self.metrics["final_balance"].value = "R$ 0,00"
            self.metrics["total_return"].value = "0,00%"
            self.metrics["win_rate"].value = "0/0"
            self.metrics["max_drawdown"].value = "0,00%"
            self.metrics["final_balance"].color = ThemeColors.GREEN
            self.metrics["total_return"].color = ThemeColors.GREEN
            self.metrics["win_rate"].color = ThemeColors.GREEN
            self.metrics["max_drawdown"].color = ThemeColors.RED
        else:
            winning_trades = sum(1 for operation in summary.operations if float(operation.get("profit", 0.0)) > 0)
            closed_trades = summary.total_trades
            self.metrics["final_balance"].value = f"R$ {summary.final_balance:,.2f}"
            self.metrics["total_return"].value = f"{summary.total_return_pct:.2f}%"
            self.metrics["win_rate"].value = f"{winning_trades}/{closed_trades}"
            self.metrics["max_drawdown"].value = f"{summary.max_drawdown_pct:.2f}%"
            self.metrics["final_balance"].color = ThemeColors.GREEN if summary.final_balance >= 0 else ThemeColors.RED
            self.metrics["total_return"].color = ThemeColors.GREEN if summary.total_return_pct >= 0 else ThemeColors.RED
            self.metrics["win_rate"].color = ThemeColors.GREEN if closed_trades > 0 and winning_trades / closed_trades >= 0.5 else ThemeColors.RED
            self.metrics["max_drawdown"].color = ThemeColors.RED
        self._refresh_page()

    def _update_summary(self, runs, summary, capital: float | None) -> None:
        if self.summary_text is None or self.operations_area is None:
            return

        if not runs:
            self.summary_text.value = "Carregue um CSV para visualizar a execução."
            self.operations_area.controls = []
        else:
            file_names = ", ".join(Path(run.file_path).name for run in runs)
            capital_display = f"R$ {capital:,.2f}" if capital is not None else "-"
            self.summary_text.value = f"Execução concluída com {len(runs)} arquivo(s) | Estratégia: {self.strategy_value} | Capital inicial: {capital_display} | Arquivos: {file_names}"
            operation_lines = [
                ft.Text(
                    f"{index + 1}. {Path(run.file_path).name} — saldo final R$ {run.result.final_balance:,.2f} | trades {run.result.total_trades}",
                    size=11,
                    color=ThemeColors.TEXT_SECONDARY,
                )
                for index, run in enumerate(runs)
            ]
            first_run = runs[0]
            if not first_run.data.empty:
                period_start = first_run.data.index.min().date().isoformat()
                period_end = first_run.data.index.max().date().isoformat()
                operation_lines.append(
                    ft.Text(
                        f"Período analisado: {period_start} a {period_end} | candles {len(first_run.data)}",
                        size=11,
                        color=ThemeColors.TEXT_SECONDARY,
                    )
                )
            if len(runs) == 1 and first_run.result.operations:
                for operation in first_run.result.operations[:8]:
                    entry_date = str(operation.get("entry_date") or "-")[:10]
                    exit_date = str(operation.get("exit_date") or "-")[:10]
                    entry_price = float(operation.get("entry_price", 0.0))
                    exit_price = float(operation.get("exit_price", 0.0))
                    profit = float(operation.get("profit", 0.0))
                    profit_label = "lucro" if profit >= 0 else "prejuízo"
                    operation_lines.append(
                        ft.Text(
                            f"{profit_label}: entrada {entry_date} (R$ {entry_price:,.2f}) -> saída {exit_date} (R$ {exit_price:,.2f}) | P/L R$ {profit:,.2f}",
                            size=10,
                            color=ThemeColors.GREEN if profit >= 0 else ThemeColors.RED,
                        )
                    )
            if summary is not None:
                operation_lines.append(
                    ft.Text(
                        f"Resumo consolidado — retorno {summary.total_return_pct:.2f}% | drawdown {summary.max_drawdown_pct:.2f}%",
                        size=11,
                        color=ThemeColors.TEXT_SECONDARY,
                    )
                )
            self.operations_area.controls = operation_lines
        self._refresh_page()

    def _parse_float_field(self, field: Optional[ft.TextField], error_message: str) -> float | None:
        if field is None or not field.value:
            self.show_error(error_message)
            return None
        try:
            value = float(field.value.replace(",", "."))
        except ValueError:
            self.show_error(error_message)
            return None
        if value <= 0:
            self.show_error(error_message)
            return None
        return value

    def _parse_int_field(self, field: Optional[ft.TextField], error_message: str) -> int | None:
        if field is None or not field.value:
            self.show_error(error_message)
            return None
        try:
            value = int(field.value)
        except ValueError:
            self.show_error(error_message)
            return None
        if value <= 0:
            self.show_error(error_message)
            return None
        return value

    def show_error(self, message: str) -> None:
        if self.page is None:
            return
        if self.error_container is not None:
            self.error_container.visible = True
        if self.error_text is not None:
            self.error_text.value = message
            self.error_text.color = ThemeColors.RED
        if self.status_text is not None:
            self.status_text.value = f"Erro: {message}"
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message, color=ThemeColors.RED), bgcolor=ThemeColors.SURFACE)
        self.page.snack_bar.open = True
        self.page.update()

    def _set_status(self, message: str) -> None:
        self.status_value = message
        if self.status_text is not None:
            self.status_text.value = message
        if self.error_text is not None:
            self.error_text.value = ""
            self.error_text.color = ThemeColors.TEXT_SECONDARY
        if self.error_container is not None:
            self.error_container.visible = False
        self._refresh_page()

    def _refresh_page(self) -> None:
        if self.page is not None:
            self.page.update()


def main() -> None:
    app = QuantInvestApp()
    ft.app(target=app.build_page)


if __name__ == "__main__":
    main()

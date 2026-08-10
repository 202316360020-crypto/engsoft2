"""Componentes reutilizáveis da GUI."""

from __future__ import annotations

import flet as ft


# ============================================================================
# CORES DO TEMA
# ============================================================================
class ThemeColors:
    """Paleta de cores do tema escuro financeiro."""

    # Fundo e superfícies
    BACKGROUND = "#0f0f0f"
    SURFACE = "#1a1a1a"
    SURFACE_LIGHT = "#252525"

    # Cores primárias
    GREEN = "#00ff88"      # Verde neon (altas/lucro)
    GREEN_DARK = "#00dd77"
    RED = "#ff3333"        # Vermelho (baixas/perda)
    RED_DARK = "#cc2222"

    # Neutras
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    BORDER = "#333333"
    BORDER_LIGHT = "#444444"
    BORDER_HOVER = "#5a5a5a"
    SURFACE_ELEVATED = "#232323"
    SURFACE_HOVER = "#262626"
    SHADOW = "#000000"


def _border(color: str) -> ft.Border:
    return ft.Border(
        top=ft.BorderSide(1, color),
        right=ft.BorderSide(1, color),
        bottom=ft.BorderSide(1, color),
        left=ft.BorderSide(1, color),
    )


def _notify(page: ft.Page | None) -> None:
    if page is not None:
        page.update()


# ============================================================================
# WIDGETS CUSTOMIZADOS
# ============================================================================

class CustomTextField(ft.TextField):
    """TextField customizado com tema escuro."""

    def __init__(self, label: str, **kwargs):
        """
        Inicializar campo de texto customizado.

        Args:
            label: Rótulo do campo
            **kwargs: Argumentos adicionais para ft.TextField
        """
        super().__init__(
            label=label,
            bgcolor=ThemeColors.SURFACE_LIGHT,
            border_color=ThemeColors.BORDER_LIGHT,
            focused_border_color=ThemeColors.GREEN,
            label_style=ft.TextStyle(color=ThemeColors.TEXT_SECONDARY, size=11),
            text_style=ft.TextStyle(color=ThemeColors.TEXT_PRIMARY, size=12),
            cursor_color=ThemeColors.GREEN,
            border_radius=6,
            content_padding=12,
            **kwargs
        )


class CustomDropdown(ft.Dropdown):
    """Dropdown customizado com tema escuro."""

    def __init__(self, label: str, options: list[str], **kwargs):
        """
        Inicializar dropdown customizado.

        Args:
            label: Rótulo do dropdown
            options: Lista de opções
            **kwargs: Argumentos adicionais para ft.Dropdown
        """
        dropdown_options = [ft.dropdown.Option(opt) for opt in options]

        super().__init__(
            label=label,
            options=dropdown_options,
            bgcolor=ThemeColors.SURFACE_LIGHT,
            border_color=ThemeColors.BORDER_LIGHT,
            focused_border_color=ThemeColors.GREEN,
            label_style=ft.TextStyle(color=ThemeColors.TEXT_SECONDARY, size=11),
            text_style=ft.TextStyle(color=ThemeColors.TEXT_PRIMARY, size=12),
            border_radius=6,
            content_padding=12,
            **kwargs
        )


class CustomButton(ft.Container):
    """Botão customizado com tema escuro."""

    def __init__(self, text: str, on_click=None, primary: bool = True, **kwargs):
        """
        Inicializar botão customizado.

        Args:
            text: Texto do botão
            on_click: Callback ao clicar
            primary: Se é botão primário (verde) ou secundário (cinza)
            **kwargs: Argumentos adicionais para ft.Container
        """
        self._primary = primary
        self._default_bg = ThemeColors.GREEN if primary else ThemeColors.SURFACE_ELEVATED
        self._hover_bg = ThemeColors.GREEN_DARK if primary else ThemeColors.SURFACE_HOVER
        self._text_color = ThemeColors.BACKGROUND if primary else ThemeColors.TEXT_PRIMARY

        super().__init__(
            content=ft.Text(
                text,
                color=self._text_color,
                weight="bold",
                size=13,
            ),
            on_click=on_click,
            on_hover=self._on_hover,
            bgcolor=self._default_bg,
            padding=14,
            border_radius=12,
            border=_border(ThemeColors.BORDER_LIGHT),
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
            **kwargs
        )

    def _on_hover(self, event: ft.HoverEvent) -> None:
        self.bgcolor = self._hover_bg if event.data == "true" else self._default_bg
        self.update()


class CustomCard(ft.Container):
    """Card customizado com tema escuro."""

    def __init__(self, body: ft.Control, title: str | None = None, **kwargs):
        """
        Inicializar card customizado.

        Args:
            content: Conteúdo do card
            title: Título opcional do card
            **kwargs: Argumentos adicionais para ft.Container
        """
        # Se houver título, criar um card com header
        self._base_bg = ThemeColors.SURFACE
        self._hover_bg = ThemeColors.SURFACE_HOVER

        if title:
            header = ft.Container(
                content=ft.Text(
                    title,
                    size=14,
                    weight="bold",
                    color=ThemeColors.TEXT_PRIMARY,
                ),
                padding=12,
            )

            body = ft.Container(
                content=body,
                padding=16,
            )

            card_content = ft.Column([header, body])
        else:
            card_content = ft.Container(
                content=body,
                padding=16,
            )

        super().__init__(
            content=card_content,
            bgcolor=self._base_bg,
            border_radius=14,
            border=_border(ThemeColors.BORDER),
            on_hover=self._on_hover,
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
            **kwargs
        )

    def _on_hover(self, event: ft.HoverEvent) -> None:
        self.bgcolor = self._hover_bg if event.data == "true" else self._base_bg
        self.update()


class ResultMetric(ft.Container):
    """Widget para exibir uma métrica de resultado."""

    def __init__(self, label: str, value: str, unit: str = "", positive: bool = True):
        """
        Inicializar widget de métrica.

        Args:
            label: Rótulo da métrica
            value: Valor a exibir
            unit: Unidade (%, $, etc)
            positive: Se o valor é positivo (verde) ou negativo (vermelho)
        """
        color = ThemeColors.GREEN if positive else ThemeColors.RED

        super().__init__(
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text(
                        label,
                        size=11,
                        color=ThemeColors.TEXT_SECONDARY,
                        weight="w500",
                    ),
                    ft.Row(
                        spacing=4,
                        controls=[
                            ft.Text(
                                value,
                                size=22,
                                weight="bold",
                                color=color,
                            ),
                            ft.Text(
                                unit,
                                size=11,
                                color=ThemeColors.TEXT_SECONDARY,
                                weight="w500",
                            ),
                        ],
                    ),
                ],
            ),
            bgcolor=ThemeColors.SURFACE,
            border_radius=14,
            padding=16,
            border=_border(ThemeColors.BORDER),
        )


class SectionHeader(ft.Container):
    """Header customizado para seções."""

    def __init__(self, title: str):
        """
        Inicializar header de seção.

        Args:
            title: Título da seção
        """
        super().__init__(
            content=ft.Text(
                title,
                size=16,
                weight="bold",
                color=ThemeColors.TEXT_PRIMARY,
            ),
            padding=12,
        )


class AccentPill(ft.Container):
    """Etiqueta pequena com resposta visual no hover."""

    def __init__(self, text: str, accent: str = ThemeColors.GREEN):
        self._base_bg = "#13231d"
        self._hover_bg = "#173226"
        self._accent = accent

        super().__init__(
            content=ft.Text(text, size=11, weight="bold", color=accent),
            padding=10,
            border_radius=999,
            bgcolor=self._base_bg,
            border=_border("#1d3d2e"),
            on_hover=self._on_hover,
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
        )

    def _on_hover(self, event: ft.HoverEvent) -> None:
        self.bgcolor = self._hover_bg if event.data == "true" else self._base_bg
        self.update()


class DateSelectorCard(ft.Container):
    """Cartão compacto para seleção de data."""

    def __init__(self, label: str, placeholder: str, on_click=None):
        self._base_bg = ThemeColors.SURFACE_ELEVATED
        self._hover_bg = ThemeColors.SURFACE_HOVER
        self._label_text = ft.Text(label, size=11, color=ThemeColors.TEXT_SECONDARY)
        self._value_text = ft.Text(placeholder, size=11, weight="bold", color=ThemeColors.TEXT_SECONDARY)

        super().__init__(
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        spacing=6,
                        controls=[
                            ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color=ThemeColors.GREEN),
                            self._label_text,
                        ],
                    ),
                    self._value_text,
                ],
            ),
            on_click=on_click,
            on_hover=self._on_hover,
            padding=12,
            border_radius=14,
            bgcolor=self._base_bg,
            border=_border(ThemeColors.BORDER_LIGHT),
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
        )

    def set_value(self, value: str | None) -> None:
        if value:
            self._value_text.value = value
            self._value_text.color = ThemeColors.TEXT_PRIMARY
        else:
            self._value_text.value = "Todo o período"
            self._value_text.color = ThemeColors.TEXT_SECONDARY
        self.update()

    def _on_hover(self, event: ft.HoverEvent) -> None:
        self.bgcolor = self._hover_bg if event.data == "true" else self._base_bg
        self.update()

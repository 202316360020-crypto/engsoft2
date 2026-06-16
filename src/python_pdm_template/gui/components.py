"""
Componentes reutilizáveis da GUI.

Widgets customizados com tema escuro e estilo financeiro para
facilitar o desenvolvimento da interface.
"""

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
        bg_color = ThemeColors.GREEN if primary else ThemeColors.BORDER_LIGHT
        text_color = ThemeColors.BACKGROUND if primary else ThemeColors.TEXT_PRIMARY

        super().__init__(
            content=ft.Text(
                text,
                color=text_color,
                weight="bold",
                size=13,
            ),
            on_click=on_click,
            bgcolor=bg_color,
            padding=14,
            border_radius=6,
            **kwargs
        )


class CustomCard(ft.Container):
    """Card customizado com tema escuro."""

    def __init__(self, content: ft.Control, title: str | None = None, **kwargs):
        """
        Inicializar card customizado.

        Args:
            content: Conteúdo do card
            title: Título opcional do card
            **kwargs: Argumentos adicionais para ft.Container
        """
        # Se houver título, criar um card com header
        if title:
            header = ft.Container(
                content=ft.Text(
                    title,
                    size=14,
                    weight="bold",
                    color=ThemeColors.GREEN,
                ),
                padding=12,
            )

            body = ft.Container(
                content=content,
                padding=16,
            )

            card_content = ft.Column([header, body])
        else:
            card_content = ft.Container(
                content=content,
                padding=16,
            )

        super().__init__(
            content=card_content,
            bgcolor=ThemeColors.SURFACE,
            border_radius=8,
            **kwargs
        )


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
            border_radius=8,
            padding=16,
            border=f"1px solid {ThemeColors.BORDER}",
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
                color=ThemeColors.GREEN,
            ),
            padding=12,
        )

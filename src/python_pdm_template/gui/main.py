"""Compatibilidade com a aplicação principal da GUI."""

from .main_new import QuantInvestApp, main

__all__ = ["QuantInvestApp", "main"]


if __name__ == "__main__":
    main()

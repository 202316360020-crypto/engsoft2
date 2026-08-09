"""Entrypoint para rodar a GUI da QuantInvest Suite."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from python_pdm_template.gui.main import main


if __name__ == "__main__":
    main()

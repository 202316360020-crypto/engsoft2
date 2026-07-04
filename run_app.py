#!/usr/bin/env python
"""Script simples para rodar a aplicação."""

from python_pdm_template.gui.main_new import main
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))


if __name__ == "__main__":
    main()

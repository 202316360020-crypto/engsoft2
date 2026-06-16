"""
Entrypoint para rodar a GUI da QuantInvest Suite.

Executa: python gui_app.py
"""

from python_pdm_template.gui.main import main
import sys
from pathlib import Path

# Adicionar src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Importar e rodar

if __name__ == "__main__":
    main()

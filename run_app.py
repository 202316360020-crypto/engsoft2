#!/usr/bin/env python
"""Script simples para rodar a aplicação."""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa e roda
from python_pdm_template.gui.main_new import main

if __name__ == '__main__':
    main()

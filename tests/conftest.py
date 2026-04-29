"""
Arquivo de configuração do pytest para o pacote de testes.

Este arquivo pode ser usado para:
- Definir fixtures globais para os testes.
- Configurar hooks do pytest.
- Adicionar opções de linha de comando personalizadas.
- Realizar configurações iniciais antes da execução dos testes.

Para mais informações, consulte a documentação do pytest: https://docs.pytest.org/
"""

# Exemplo de fixture global
import pytest

@pytest.fixture
def exemplo_fixture():
    """Uma fixture de exemplo que pode ser usada em testes."""
    return "dados de exemplo"
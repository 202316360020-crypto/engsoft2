"""
Arquivos de teste precisam ser nomeados com o prefixo `test_` ou sufixo `_test`.

O pytest só reconhece automaticamente arquivos com esses nomes.

Este arquivo contém exemplos de testes utilizando pytest, incluindo:
- Um teste simples para validar uma função.
- Um teste que utiliza o recurso de monkeypatching do pytest para modificar 
comportamentos durante o teste.

O objetivo é demonstrar como usar o pytest e seus recursos para criar testes eficazes.
"""

from python_pdm_template.utils import obter_mensagem, somar

# Teste simples


def test_somar():
    """Teste simples para a função somar."""
    resultado = somar(2, 3)
    assert resultado == 5  # noqa: PLR2004

# Teste com monkeypatching


def test_obter_mensagem(monkeypatch):  # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
    """
    Teste que utiliza monkeypatching. 

    O objetivo aqui é substituir a função input() do Python por uma função personalizada
    durante o teste, para evitar a necessidade de interação do usuário. O teste verifica
    se a função obter_mensagem() retorna a mensagem modificada corretamente.
    """

    # Função substituta para o monkeypatch
    def mensagem_alternativa(prompt: str):  # noqa: ARG001
        return "Mensagem modificada"

    # Aplicando o monkeypatch para substituir a função input() do python por
    # mensagem_alternativa.
    #   - a ideia aqui é de evitar a interacao do usuario durante os testes
    #     automatizados.
    #   - para isso, uma das tecnicas que podemos usar é o monkeypatch (substituicao
    #     temporaria de uma funcao ou classe por outra funcao ou classe).
    monkeypatch.setattr("builtins.input", mensagem_alternativa)  # pyright: ignore[reportUnknownMemberType]

    # Verificando se a função foi substituída corretamente
    #   - o assert testa se uma condicao é True
    #   - se essa condicao for False, o assert levanta um erro (excecao) nos testes
    #     automatizados
    resultado = obter_mensagem()
    assert resultado == "Mensagem modificada"

# Comentários adicionais:
# - O pytest é um framework de testes poderoso e fácil de usar para Python.
# - O recurso de monkeypatching permite substituir funções, métodos ou atributos
#   durante o teste, útil para isolar dependências externas.
# - O uso de asserts no pytest é direto e fornece mensagens úteis em caso de falha.
# - Para rodar os testes, use o comando `pytest tests/` no terminal.

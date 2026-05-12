# Testes — QuantInvest Suite

Esta pasta contém toda a suíte de testes automatizados do projeto, organizada por tipo e módulo.

## Estrutura

```
tests/
├── conftest.py                   # Fixtures globais reutilizáveis (dados OHLCV)
├── pytest.ini                    # Configuração do pytest e cobertura
├── test_parser.py                # Testes do parser OHLCV (validação de CSV)
├── test_strategies.py            # Testes das estratégias (Buy and Hold, MM)
├── test_metrics.py               # Testes das métricas (Drawdown, win rate, retorno)
└── test_defects_and_validation.py # Testes de defeito, validação e integração
```

## Como rodar

```bash
# Instalar dependências de teste
pip install pytest pytest-cov pytest-mock

# Rodar todos os testes com relatório de cobertura
pytest

# Rodar apenas testes unitários
pytest -m unit

# Rodar apenas testes de integração
pytest -m integration

# Gerar relatório HTML de cobertura
pytest --cov=core --cov-report=html
# Abrir htmlcov/index.html no navegador
```

## Abordagem TDD

Os testes foram escritos **antes da implementação** (Test-Driven Development).
Enquanto o Core ainda não existe, cada arquivo usa **stubs** (classes com
`raise NotImplementedError`) no lugar das implementações reais.

Os testes com stub ativo retornam `pytest.skip()` — ou seja, **não falham**,
apenas são pulados. Conforme o Core for implementado:

1. Remova o stub do arquivo de teste
2. Descomente o `import` real (ex: `from core.parser import OHLCVParser`)
3. Os testes começarão a rodar de verdade

## Uso de Mock objects

Mock objects (`unittest.mock.MagicMock`) são usados para:

- **Isolar camadas**: testar o CLI sem depender do Core real
- **Simular falhas**: testar BankruptcyError sem precisar zerar o capital de verdade
- **Verificar chamadas**: garantir que o motor chama `strategy.run()` com os parâmetros corretos
- **Simular I/O**: testar o parser sem precisar de arquivos CSV reais em disco

## Meta de cobertura

A configuração do `pytest.ini` falha o CI se a cobertura cair abaixo de **80%**
(requisito RNF-05 do DEF).

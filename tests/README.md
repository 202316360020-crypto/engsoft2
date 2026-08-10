# Testes

Suíte automatizada da QuantInvest Suite.

## Cobertura

- `conftest.py`: fixtures de dados OHLCV.
- `test_parser.py`: leitura e validação de CSV.
- `test_strategies.py`: estratégias Buy and Hold e médias móveis.
- `test_metrics.py`: retorno, win rate e drawdown.
- `test_defects_and_validation.py`: validações e integração.

## Execução

```bash
.\.venv\Scripts\python.exe -m pytest
```

## Observação

Os testes acompanham a evolução do núcleo funcional do projeto e servem como referência para o comportamento esperado da aplicação.

# QuantInvest Suite

Aplicação Python para simulação e análise de estratégias de investimento sobre séries OHLCV.

## Visão geral

- Interface gráfica em Flet para selecionar CSVs, escolher estratégia e visualizar resultados.
- CLI para executar backtests em arquivos individuais ou em lote.
- Núcleo em `src/python_pdm_template/core/` com parser, estratégias e métricas.
- Testes automatizados em `tests/` cobrindo validação, integração e regras de negócio.

## Execução

Com a virtualenv criada em `.venv`, execute a interface com:

```bash
.\.venv\Scripts\python.exe run_app.py
```

Ou use a CLI:

```bash
.\.venv\Scripts\python.exe -m python_pdm_template --file caminho\para\arquivo.csv
```

## Estrutura principal

- `src/python_pdm_template/core/`: parser, estratégias, métricas e serviços de simulação.
- `src/python_pdm_template/gui/`: dashboard Flet e componentes visuais.
- `tests/`: suíte de testes e fixtures.
- `pyproject.toml`: dependências, scripts e configuração de ferramentas.


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

## Executar o projeto

1. **Rodar o projeto**:
   - Após instalar as dependências, você pode executar o projeto diretamente usando:
     ```bash
     python -m pdm run python src/python_pdm_template/__main__.py
     ```

O PDM nao apenas controla dependencias e executa o projeto, ele também pode compilar o projeto Python em arquivos `.WHL` e publicá-los no repositório oficial de pacotes do Python ([PyPi](https://pypi.org/)).

Para mais informações sobre as essas e outras funcionalidades disponíveis no PDM, consulte a [documentação oficial](https://pdm.fming.dev/).

## Estrutura do projeto

- [**``.github/workflows/``**](.github/workflows): Configurações do GitHub Workflows para automacao de CI/CD (Integração Contínua e Entrega Contínua).
- [**``.vscode/``**](.vscode): Configurações do Visual Studio Code.
- [**``src/``**](src/python_pdm_template/): Contém o código-fonte do projeto.
- [**``tests/``**](tests): Contém os testes do projeto.
- [**``pyproject.toml``**](pyproject.md): Arquivo de configuração do projeto, incluindo dependências e metadados.

Cada pasta ou arquivo acima tem um ``README.md`` explicando sua finalidade, como funciona, e como usar cada uma delas. **Clique nos links acima e leia com atenção cada um dos READMEs para entender melhor o projeto.**
- Em cada um dos links acima **há tarefas para você realizar**, para praticar o que foi explicado no README. 
- As tarefas poderão ser **utilizadas para fins de avaliação na disciplina.** Assim, realize todas as tarefas propostas e envie suas respostas no nosso Google Classroom.
## Integrante
Abner Azevedo - contribuição inicial


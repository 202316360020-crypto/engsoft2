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

## Formato do CSV e parâmetros

O arquivo de entrada precisa ter as colunas `Date`, `Open`, `High`, `Low`, `Close` e `Volume`, em ordem cronológica.

Se você escolher a estratégia de cruzamento de médias móveis, os valores padrão `9` e `21` significam o tamanho das janelas de cálculo em períodos:

- `9` = média curta, que reage mais rápido ao preço.
- `21` = média longa, que suaviza mais o movimento e serve de referência.

Os filtros de data também podem ser usados para limitar a simulação a um trecho específico da série; se você não definir nada, o sistema usa todo o CSV.

## Gerar executável

O projeto pode ser empacotado com PyInstaller para Windows. Para gerar um build local da GUI em uma pasta única e portátil, execute:

```powershell
.\build_portable.cmd
```

O pacote final fica em `portable\QuantInvest\` e o arquivo pronto para levar em pendrive fica em `portable\QuantInvest-portable.zip`.

Use apenas o conteúdo de `portable\QuantInvest\` para executar a aplicação em outro computador. As pastas `pyinstaller-build\`, `release\` e `release-console\` são artefatos internos de geração e não fazem parte do pacote final.

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



# Arquivo `pyproject.toml`

Este arquivo serve para configurar um projeto de programa Python moderno. Nele você pode configurar varios aspectos do seu programa (nome, versao, descricao, dependencias, etc), como veremos a seguir.

## Estrutura do arquivo `pyproject.toml`

O arquivo `pyproject.toml` é dividido em varias seções, cada uma com uma funcao diferente. As principais secoes sao:
- `[project]`: Configuracoes gerais do projeto (nome, versao, descricao, autores, dependencias, etc).
- `[dependency-groups]`: Configuracoes de dependencias adicionais do projeto (dependencias de desenvolvimento, dependencias opcionais, etc).
- `[build-system]`: Configuracoes para o ambiente de build do projeto (quem ira compilar o projeto, etc).
- `[tool.pdm]`: Configuracoes para o ambiente do PDM no Python.
- `[tool.pdm.build]`: Configuracoes para o ambiente de build do PDM no Python.
-  `[tool.pytest.ini_options]`: Configuracoes para a ferramenta de testes automatizados `pytest`.
-  `[tool.pyright]`: Configuracoes para a ferramenta de análise estática de código Python `pyright`/`pylance`.
-  `[tool.ruff.lint]`: Configuracoes para a ferramenta de análise estática de código Python `ruff`.

Outras seções podem ser adicionadas conforme as necessidades e ferramentas utilizadas no projeto. 

Segue uma explicação detalhada de cada uma das seções mencionadas acima.

### Seção \[project\]

Esta parte do arquivo descreve configuracoes gerais do projeto (nome, versao, descricao, autores, depdendencias, versao do python suportada, arquivos de licença e classificadores).

```toml
[project]
name = "python_pdm_template" # este é o nome do seu programa/projeto python
version = "0.1.0" # versao atual do programa
description = "Template base para qualquer projeto Python baseado em PDM" # descricao do programa
authors = [ # lista contendo o nome dos autores do programa
  { 
    name = "Autor 1", 
    email = "fulano@gmail.com" 
  },
  { 
    name = "Autor 2", 
    email = "cicrano@hotmail.com" 
  },
] 
dependencies = [ # lista de dependencias (bibliotecas externas) que o programa precisa para funcionar
  # Exemplo: 
  #    flask
  #    django
  #    fastapi
  #    PyQt6
  #    requests
  #    urllib3
]
requires-python = ">=3.14" # versao do python que este programa é compativel
readme = "README.md" # arquivo de README do programa
license-files = ["LICEN[CS]E*", "README.md"] # arquivos de licença de uso do programa (LICENSE)
classifiers = ["Programming Language :: Python :: 3"] # tags usadas para descrever o programa, o que ele faz, e outros aspectos relevantes (facilita a comunidade python encontrar seu programa no PyPi)
```

### Seção \[dependency-groups\]

Esta secao descreve dependencias adicionais do programa, como dependencias de desenvolvimento. Estas dependencias sao OPCIONAIS para o programa funcionar (adicionam funcionalidades que nao sao essenciais).

No caso das dependencias de desenvolvimento, estas sao obrigatorias somente para a etapa de desenvolvimento do sistema (o usuario final nao precisa delas para rodar seu programa).

```toml
[dependency-groups]
dev = [ # descreve dependencias de desenvolvimento (pytest, linters, compiladores, etc)
    "pytest>=9.0.2",
    "pytest-cov>=7.0.0",
]
```

#### Secoes do PDM

As secoes abaixo descrevem configuracoes para o ambiente do PDM no Python.

```toml
[build-system]
requires = ["pdm-backend"] # quem ira compilar o programa Python
build-backend = "pdm.backend" # quem ira compilar o programa Python

[tool.pdm]
distribution = true # este programa, quando compilado, deve gerar arquivos python executáveis (do tipo .WHL) ?

[tool.pdm.build]
package-dir = "src" # onde esta o codigo fonte do programa
```

#### Secoes do ``pytest``

As secoes abaixo descrevem configuracoes para a ferramenta de testes automatizados `pytest`.

```toml
[tool.pytest.ini_options]
testpaths = ["tests"] # onde estao os testes a serem realizados
addopts = "--cache-clear --ff --cov=src --cov-report=html --cov-report=term --cov-report=xml" # como os testes devem ser executados
```

As opcoes abaixo, contidas em `addopts`, indicam como os testes devem ser executados:
- `--cache-clear`: Ignore cache de testes (evita que testes antigos sejam salvos no cache para uso futuro, causando erros em potencial no futuro)
- `--ff`: Execute o ultimo teste que falhou antes dos demais testes (na pratica, essa opcao faz com que o ``pytest`` mostre os erros logo de cara pra gente)
- `--cov=src`: Execute testes de cobertura usando `coverage` no ``pytest``. Testes de cobertura sao basicamente uma forma de identificar quanto do código fonte foi de fato analisado pelos testes do ``pytest`` (armazenados na pasta `tests/`). Os testes de cobertura nos retornam um percentual de 0-100 para cada arquivo contido na pasta `src/`, indicando quantas linhas de código foram efetivamente testadas
    - **Ex**: suponha que tenho uma arquivo `src/utils.py` e este arquivo tem ao todo 50 linhas de código. Digamos que criei o arquivo de teste `tests/test_utils.py` para verificar as funcionalidades desse arquivo ``src/utils.py``. Nesse arquivo de teste, os testes que descrevi foram capazes de testar 10 das 50 linhas de ``src/utils.py``. Logo, o teste de cobertura ira indicar que 10/50 linhas foram testadas, ou seja, ele ira indicar que apenas `10/50*100 = 20%` das linhas de `src/utils.py` foram testadas.
- `--cov-report=html`: Gere uma pagina html `htmlcov/index.html` para mostrar os resultados dos testes de cobertura.
- ``--cov-report=term``: Mostre os resultados dos testes de cobertura no terminal (PowerShell, bash, etc).
- ``--cov-report=xml``: Gere um arquivo XML contendo os resultados dos testes de cobertura. Este arquivo pode ser usado posteriormente por ferramentas externas de controle de qualidade para verificacoes automatizadas do projeto Python.

Para mais informacoes sobre como usar o `pytest`, abra a documentacao da pasta [``tests/``](tests) deste repositorio.


### Seção  ``pyright``/`pylance`

A Microsoft, em conjunto com a comunidade Python, criou uma ferramenta de Intellisense poderosa, chamada de `pyright` ou `pylance`. Esta ferramenta consegue detectar problemas no código fonte Python sem precisar executar o programa. Ela também ajuda na escrita do código através de recursos como "auto-completar", "auto-corrigir" e "verificacao de tipos de dados".

Para tudo isso funcionar, é preciso instalar a extensao ``Pylance`` no VSCode e configurar o ``pyright`` no arquivo `pyproject.toml`, conforme descrito abaixo:

```toml
[tool.pyright]
# Specify the language server (Pylance should be set by default if using Pyright)
languageServer = "Pylance"
diagnosticMode= "workspace"     # verificar todos os arquivos contidos no projeto
typeCheckingMode = "strict"     # ativar modo de verificacao de tipos do Python
extraPaths = ["src"]            # Onde esta os codigos fonte do programa
indexing = true                 # Ativar indexacao de arquivos (melhora desempenho do pyrigth)
useLibraryCodeForTypes = true   # Use biblioteca de tipos para melhorar a identificacao de tipos de dados no Python

# CODE ISSUES
reportImportCycles = "error"      # Importacao circular - importacoes que criam ciclos entre modulos
reportUnreachable = "error"             # unreachable code

# INHERITANCE ISSUES
reportMissingSuperCall = "error"           # missing super() call in a constructor
reportUninitializedInstanceVariable = "error"  # uninitialized instance variables

# TYPE ISSUES
reportPropertyTypeMismatch = "error" # Property type mismatch - type of property does not match type of getter/setter

# arquivos a serem ANALISADOS pelo pyright
include = [
    "src",
    "tests",
]

# arquivos a serem EXCLUIDOS da analise do pyright
exclude = [
    ".venv",
    "__pycache__",
    "build",
    "dist",
    ".mypy_cache",
    ".pytest_cache",
]
```

### Seção  ``ruff``

Alem do `pyright`/`pylance`, temos outra ferramenta de análise estática de código Python (*linter*) chamada de `ruff`. O `ruff` identifica erros que as demais ferramentas que ja configuramos nao conseguem.

Para usar o Ruff, precisamos:
1. Instalar a extensao `Ruff` no VSCode
2. Configurar o `ruff` no arquivo `pyproject.toml`, conforme abaixo:

```toml
[tool.ruff.lint]
select = [
    "A", # erros de colisao com nomes existentes (ex: variaveis com mesmo nome de variaveis built-in do Python, variaveis com mesmo nome de modulos do Python, etc)
    "B", # erros de bugs (ex: variaveis nao usadas, variaveis definidas mais de uma vez, etc)
    "D", # erros de docstrings (ex: docstrings faltando, docstrings com formato incorreto, etc)
    "F", # erros identificados pelo Flake8 (ex: erros de sintaxe, erros de indentacao, etc)
    "N", # erros de nomes de variáveis, funções, classes, etc (ex: variáveis com nomes pouco descritivos, funções com nomes que nao seguem o padrão snake_case, etc)
    "S", # erros de segurança (ex: uso de funções inseguras, uso de bibliotecas com vulnerabilidades conhecidas, etc)
    "DOC", # erros de documentação (ex: docstrings faltando, docstrings com formato incorreto, etc)
    "SLF", # erros de uso de membros privados de outras classes (ex: acessar atributos ou métodos privados de outras classes, etc)
    "RET", # erros de retorno de funções (funções que nao retornam nada, ou que retornam tipos de dados diferentes em blocos de código diferentes, etc)
    "ARG", # erros de argumentos de funções (ex: argumentos nao usados, argumentos definidos mais de uma vez, etc)
    "PIE", # erros de Pie (ex: Enums com valores duplicados, Enums com valores que não são do tipo esperado, etc)
    "PLE", # erros de Pylint gerais (ex: __bool__() que retorna valores inesperados, variáveis que podem ser usadas antes de serem definidas, etc)
    "PLW", # erros de warning de Pylint (código que pode ser melhorado, código que pode ser simplificado, etc)
    "PLR", # erros de refactor de Pylint (refactoring de código, código duplicado, código que pode ser simplificado, etc)
    "SIM", # erros de simplicidade do código (código complexo que pode ser simplificado)
    "C90", # erros de complexidade ciclomática (funcoes/métodos com muitas linhas de código, muitos loops, etc)
    "C4", # erros de list/dict comprehensions (performance ruim)
]
```

É possivel configurar o `ruff` para identificar outros tipos de erros. Para isso, basta adicionar as *tags* correspondentes na lista `select` do `ruff`, conforme descrito na [documentação oficial do ruff](https://docs.astral.sh/ruff/rules/).

## Tarefas para hoje
1. Leia com atenção o arquivo `pyproject.toml` deste repositório, e entenda o que cada seção do arquivo faz. Se tiver dúvidas, pergunte para mim. Pode usar IA também para auxiliar nesse processo.
2. Altere o arquivo `pyproject.toml` para:
   1. Configurar o nome do seu projeto Python (ex: `meu_projeto_python`).
   2. Configurar a versão do seu projeto Python (ex: `0.1.0`).
   3. Configurar a descrição do seu projeto Python (ex: `Este é o meu projeto Python baseado em PDM`).
   4. Configurar o nome e email dos autores do projeto Python.
   5. Adicionar pelo menos uma dependência ao projeto (ex: `flask`, `django`, `fastapi`, `pyqt`, ou outra que você desejar).
   6. Configurar a versão do Python que seu projeto suporta (ex: `>=3.10`).
   7. Configurar dependencies de desenvolvimento (ex: `pytest`, `pytest-cov`, `ruff`, `pyright`, `pylint`, etc).
   8. Verificar se todas as dependencias foram instaladas corretamente, rodando o comando `python -m pdm install` no terminal.
3. Execute o projeto usando o comando `python -m pdm run python src/python_pdm_template/__main__.py` 
   - Verifique se o programa rodou corretamente. Se tiver dúvidas, pergunte para mim. Pode usar IA também para auxiliar nesse processo.
4. Verifique se os testes automatizados estão rodando corretamente usando o comando `python -m pdm run pytest`. 
   - Verifique se os testes de cobertura estão sendo gerados corretamente. 
   - Se tiver dúvidas, pergunte para mim. Pode usar IA também para auxiliar nesse processo.
5. Teste o `pyright` e o `ruff` fazendo algum erro de código no arquivo `src/python_pdm_template/utils.py` 
   - **Exemplo de erros**: 
     - criar uma variável e nao usar ela, 
     - criar uma função que nao retorna nada, 
     - criar uma função que retorna tipos de dados diferentes em blocos de código diferentes, 
     - acessar um atributo privado de outra classe
   - Verifique se o `pyright` e o `ruff` identificaram os erros corretamente. 
   - Se tiver dúvidas, pergunte para mim. Pode usar IA também para auxiliar nesse processo.
6. Compile o projeto usando o comando `python -m pdm build` 
   - Verifique se os arquivos `.WHL` foram gerados corretamente na pasta `dist/`. 
   - Se tiver dúvidas, pergunte para mim. Pode usar IA também para auxiliar nesse processo.
7. Instale o arquivo `.WHL` gerado usando o comando `python -m pip install dist/seu_arquivo.whl`    

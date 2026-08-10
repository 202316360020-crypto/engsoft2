# `pyproject.toml`

Arquivo de configuração central do projeto Python.

## Seções principais
- `[project]`: metadados do projeto, dependências e versão suportada do Python.
- `[dependency-groups]`: dependências de desenvolvimento.
- `[build-system]`: backend usado para build.
- `[tool.pdm]` e `[tool.pdm.build]`: configuração do empacotamento com PDM.
- `[tool.pytest.ini_options]`: configuração do pytest e cobertura.
- `[tool.pyright]`: análise estática com Pyright/Pylance.
- `[tool.ruff.lint]`: regras de lint com Ruff.

## Exemplo de configuração de projeto
```toml
[project]
name = "python_pdm_template"
version = "0.1.0"
description = "Aplicação Python para simulação e análise de estratégias de investimento"
authors = [
  { name = "Abner Azevedo", email = "abner@example.com" },
  { name = "Daniel Martins", email = "daniel@example.com" },
]
dependencies = [
  "pandas>=3.0.3",
  "numpy>=2.4.4",
]
requires-python = ">=3.12"
readme = "README.md"
license-files = ["LICEN[CS]E*", "README.md"]
classifiers = ["Programming Language :: Python :: 3"]
```

## Dependências de desenvolvimento
```toml
[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "pytest-cov>=7.0.0",
]
```

## PDM
```toml
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[tool.pdm]
distribution = true

[tool.pdm.build]
package-dir = "src"
```

## Pytest
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cache-clear --ff --cov=src --cov-report=html --cov-report=term --cov-report=xml"
```

## Pyright
```toml
[tool.pyright]
languageServer = "Pylance"
diagnosticMode = "workspace"
typeCheckingMode = "strict"
extraPaths = ["src"]
indexing = true
useLibraryCodeForTypes = true
```

## Ruff
```toml
[tool.ruff.lint]
select = [
    "A",
    "B",
    "D",
    "F",
    "N",
    "S",
    "DOC",
    "SLF",
    "RET",
    "ARG",
    "PIE",
    "PLE",
    "PLW",
    "PLR",
    "SIM",
    "C90",
    "C4",
]
```
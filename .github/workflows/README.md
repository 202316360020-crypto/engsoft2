# CI/CD com GitHub Actions

Este diretório reúne a documentação dos workflows usados no projeto.

## Estrutura
- Os arquivos de workflow ficam em `.github/workflows/`.
- Cada arquivo define jobs executados em eventos como `push`, `pull_request` ou `workflow_dispatch`.
- Em caso de falha, o GitHub Actions interrompe o workflow e mostra os detalhes na aba `Actions` do repositório.

## Exemplo de pipeline para Python com PDM
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Instalar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.14'

      - name: Instalar PDM
        run: python -m pip install pdm

      - name: Instalar dependências
        run: python -m pdm install

      - name: Rodar testes
        run: python -m pdm run pytest
```

## Recomendações
- Automatize testes antes de merge ou deploy.
- Gere relatórios de cobertura e artefatos para análise posterior.
- Adapte os workflows conforme a necessidade do projeto.
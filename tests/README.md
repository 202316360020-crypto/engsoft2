# Testes com Pytest

Esta pasta contém os testes do projeto e está configurada para ser utilizada com o framework de testes [``pytest``](https://docs.pytest.org/).

## Como usar

1. Certifique-se de que o pytest está instalado no ambiente Python do projeto. Caso não esteja, instale-o com o seguinte comando:

   ```bash
   python -m pdm add -d pytest pytest-cov
   ```

2. Para executar todos os testes desta pasta, utilize o seguinte comando na raiz do projeto:

   ```bash
   python -m pdm run pytest
   ```

3. Para executar um teste específico, forneça o caminho do arquivo de teste ou da pasta. Por exemplo:

   ```bash
   python -m pdm run pytest tests/test_exemplo.py
   ```

4. Utilize a opção `-v` para obter mais detalhes sobre os testes executados:

   ```bash
   python -m pdm run pytest -v
   ```

## Cobertura de Código (Coverage)

O projeto está configurado para usar o [pytest-cov](https://pytest-cov.readthedocs.io/) para medir a cobertura de código durante a execução dos testes.

### Como funciona

- O **coverage** (cobertura) mede qual porcentagem do código-fonte é executada durante os testes.
- Isso ajuda a identificar partes do código que não estão sendo testadas.
- O projeto está configurado para gerar automaticamente relatórios de cobertura ao executar os testes.

### Relatórios gerados

Ao executar `python -m pdm run pytest`, três tipos de relatórios são gerados automaticamente:

1. **Relatório no terminal**: Exibe a cobertura diretamente no console após a execução dos testes.

2. **Relatório HTML** (pasta `htmlcov/`):
   - Contém um relatório visual detalhado em formato HTML.
   - Para visualizar, abra o arquivo `htmlcov/index.html` no navegador.
   - A pagina HTML que foi aberta mostrará uma tabela, contendo a cobertura de código de cada arquivo `.py` da pasta `src/`
   - Ao clicar em um dos arquivos `.py`, você verá linha por linha qual código foi executado (VERDE) e qual não foi (VERMELHO).

3. **Arquivo XML** (`coverage.xml`):
   - Formato XML usado por ferramentas de integração contínua (CI/CD).
   - Útil para integração com plataformas como GitHub Actions, GitLab CI, SonarCloud, etc.

### Configuração
A configuração do coverage está no arquivo `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=html --cov-report=term --cov-report=xml"
```

## Estrutura de pastas e arquivos

- **`tests/conftest.py`**: Arquivo de configuração do pytest, onde podem ser definidas *fixtures* e *hooks* globais. 
  - **Fixture**: Uma função que fornece um ambiente de teste pré-configurado (ex: banco de dados, arquivos temporários, etc) para ser usado em múltiplos testes.
  - **Hook**: Função que é chamada em determinados momentos do ciclo de vida dos testes (ex: antes de cada teste, depois de cada teste, etc) para realizar ações específicas (ex: limpar recursos, gerar relatórios, etc).
  - Pergunte a IA acerca de exemplos de *fixtures* e *hooks*, e sobre como usar eles no `conftest.py`.
- **Arquivos de teste**: Devem seguir o padrão `test_*.py` ou `*_test.py` para serem automaticamente descobertos pelo pytest.

Para mais informações, consulte a [documentação oficial do pytest](https://docs.pytest.org/).

## Tarefa de hoje - Criar um novo teste
1. Crie um novo arquivo de teste chamado `test_modulo4.py` dentro da pasta `tests/`.
2. No arquivo `test_modulo4.py`, escreva um teste para a função `saudacao()` que você criou no ``módulo4.py``. O teste deve verificar se a função retorna a string ``"Olá, mundo!"``.
3. Execute os testes para verificar se o novo teste está funcionando corretamente. 
   - Se o teste passar, significa que a função `saudacao()` está retornando o valor esperado. 
   - Se o teste falhar, revise o código da função `saudacao()` e do teste para identificar e corrigir o problema.
4. Verifique o relatório de cobertura (arquivo `htmlcov/index.html`) para garantir que o teste está cobrindo a função `saudacao()`. 
   - O relatório deve indicar que a função `saudacao()` foi executada durante os testes, contribuindo para a cobertura de código do projeto.
   - Verifique se as demais funcoes do projeto (ex: `despedida()`, `metodo_privado()`, etc) estão sendo cobertas pelos testes, e se não estiverem, escreva testes para cobrir elas também.
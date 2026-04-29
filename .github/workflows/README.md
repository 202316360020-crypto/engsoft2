# CI/CD com GitHub Actions

Este diretório deve conter os arquivos de workflow do GitHub Actions para automação de testes, builds e deploys do projeto.

## O que é GitHub Actions?
O [GitHub Actions](https://docs.github.com/pt/actions) permite criar pipelines de integração contínua (CI) e entrega contínua (CD) diretamente no repositório.

## Como funciona
- Os arquivos de workflow são escritos em YAML e ficam na pasta `.github/workflows/`.
- Cada arquivo define um ou mais jobs (tarefas) que são executados em eventos como push, pull request ou tags.
- Caso haja alguma falha em um job, o GitHub Actions para o workflow e notifica os colaboradores do repositório por email.

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

## Dicas
- Use secrets do GitHub para armazenar tokens e senhas que voce deseja acessar em cada workflow `.yml`.
- Crie arquivos `.yml` para diferentes etapas do projeto (ex: ``tests.yml``, ``ci.yml``, ``deploy.yml``).
  - O arquivo `test.yml` pode, por exemplo, rodar os testes automatizados e de cobertura com pytest (**já incluído neste template**).
  - O arquivo `ci.yml` pode ser configurado para rodar *linters*, formatadores e outras ferramentas de qualidade de código (ex: ``ruff``, `pyright`, `pylint`, etc).
  - O arquivo `deploy.yml` pode ser configurado para fazer deploy automático para produção ou *staging*, usando ferramentas como ``Docker``, ``Heroku``, ``AWS``, `pdm publish`, `InnoSetup`, etc.

Consulte a [documentação oficial](https://docs.github.com/pt/actions) para exemplos e boas práticas.

## Recomendações
- Sempre automatize testes antes de fazer ``git merge`` ou deploys.
- Gere relatórios de cobertura e artefatos para análise posterior.
- Adapte os workflows conforme as necessidades do seu projeto.

## Tarefa de hoje - Configurar o workflow de CI para rodar o linter `ruff`
1. Leia com atenção o arquivo `ci.yml` deste repositório, e entenda o que cada etapa do pipeline faz. 
   - Se tiver dúvidas, pergunte para mim. Utilize IAs generativas se necessário para entender melhor o que é o GitHub Actions, como ele funciona e como o arquivo `ci.yaml` está configurado.
2. Inclua no arquivo `ci.yml` uma etapa para rodar o `ruff` e identificar erros de formatação, erros de tipo, erros de segurança, etc. Para isso, basta adicionar as seguintes etapas no arquivo `ci.yml`:
  ```yaml
  # no arquivo ".github/workflows/ci.yml", adicione:
        - name: Rodar ruff
          run: python -m pdm run ruff check src/
  ```
3. O workflow `ci.yaml` deve rodar quando houver um ``git push`` no repositório ou quando você for na aba ``Actions -> Integracao Continua`` e clicar no botao ``Executar``. 
   - Se quiser, voce pode configurar o workflow para rodar com outros eventos, alem do ``push`` (ex: tags, releases, etc). 
   - Para isso, basta alterar a seção `on` do arquivo `ci.yaml`, conforme descrito na [documentação oficial do GitHub Actions](https://docs.github.com/pt/actions/using-workflows/events-that-trigger-workflows).
4. Teste o workflow fazendo um `git push`. 
   - Verifique se o workflow rodou corretamente e se o `ruff` identificou algum erro de formatação, erro de tipo, erro de segurança, etc. 
   - Quando um erro ocorre em um workflow, o **GitHub Actions** para a execução do workflow e **envia um email** para os colaboradores do repositório, informando sobre a falha.
   - Voce pode acessar os detalhes do erro clicando no email ou indo na aba `Actions` do repositório, clicando no workflow que falhou, e depois clicando no job que falhou. 
   - Caso surja algum erro, identifique o problema e corrija-o. Faça um novo `git push` para verificar se o erro foi corrigido e se o workflow rodou corretamente.
     - **LEMBRETE**: Erros em um workflow podem ocorrer por diversos motivos, como:
       - Erros detectados pelo `ruff` no codigo fonte (ex: erro de formatação, erro de tipo, erro de segurança, etc)
       - Erros de configuração do workflow (ex: sintaxe incorreta no arquivo `ci.yaml`, nome do comando errado, etc)
       - Erros de ambiente (ex: versão do Python incompatível, dependências não instaladas, etc)
       - Leia com calma a mensagem de erro para entender melhor o que aconteceu, e utilize IAs generativas se necessário para entender melhor o erro e como corrigi-lo. Sinta-se livre para me perguntar sobre o erro, e como corrigi-lo.
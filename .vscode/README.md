# Configuração do VS Code para projetos Python com PDM

Este diretório pode conter arquivos de configuração específicos do VS Code, como:
- `extensions.json`: lista de extensões recomendadas para o projeto
- `settings.json`: configurações do editor para o projeto

## Arquivo ``extensions.json``

- Este arquivo descreve as extensoes do VSCode que este projeto precisa.
- Quando este arquivo esta presente, o proprio VsCode ira emitir uma mensagem sobre extensoes recomendadas, para que voce as instale.

### Tarefa de hoje - Instalar as extensoes recomendadas para o projeto
1. Abra o arquivo `extensions.json` e veja quais extensoes estão listadas.
2. Instale as extensoes recomendadas no VSCode.
   - Para isso, basta clicar no botao "Instalar" que aparece na mensagem de recomendacao de extensoes do VSCode
   - Voce também pode procurar as extensoes manualmente na loja de extensoes do VSCode e instalar elas. **As extensoes recomendadas para este projeto sao:**
     - Python (Microsoft)
     - autopep8 (Microsoft)
     - Pylance (Microsoft)
     - SonarQube for IDE (SonarSource)
     - Ruff (charliermarsh)
     - PlantUML (jebbs)
     - GitHub Copilot Chat (GitHub)
     - Even Better TOML (tamasfe)
     - Markdown All in One (yu zhang)
     - Markdown Preview Github Styling (Matt Bierner)

## Arquivo ``settings.json``

### Tarefa de hoje - Configurar o SonarCloud no projeto
O SonarCloud é um analisador de código (``linter``) que identifica problemas comuns em programas, SEM executar o programa (a análise é feita lendo codigo apenas). Para ele funcionar, você precisará:

1.  Criar uma conta no SonarCloud ([http://sonarcloud.io/login](http://sonarcloud.io/login)) usando suas credenciais do GitHub
2.  Adicionar seu repositório do GitHub ao SonarCloud 
    - **IMPORTANTE:** o SonarCloud é um padrao da industria de Eng. de Soft. e portanto é uma ferramenta paga. PORÉM, se o **repositorio no GitHub for PUBLICO**, o SonarCloud pode ser usado de forma gratuita. Assim, garanta que seu repositório esta marcado como ``público`` no GitHub.
3. Instale a extensao ``SonarQube for IDE`` no VSCode 
4. Configure a extensao ``SonarQube for IDE``, adicionando as seguintes linhas no arquivo ``.vscode/settings.json``:
```json
"sonarlint.connectedMode.project": { // configuracao do SonarCloud
    // id do seu usuario (clique no seu projeto, no menu a esquerda clique em Information, copie o OrganizationKey e cole ele aqui)
    "connectionId": "nome-de-usuario-no-sonarcloud", 
    // id do seu repositorio (clique no seu projeto, no menu a esquerda clique em Information, copie o ProjectKey e cole ele aqui)
    "projectKey": "nome-do-projeto-no-sonarcloud", 
},
```
   - ``connectionId``: Representa seu ID de usuario no SonarCloud
   - ``projectKey``: Representa o ID do seu repositorio GitHub no SonarCloud
1. Após configurar o SonarCloud, o SonarLint irá analisar seu código e identificar problemas de qualidade, segurança, bugs, etc. Ele também irá gerar relatórios de cobertura de testes, para que voce possa acompanhar a qualidade do seu código.
2. Verifique se o SonarCloud esta funcionando corretamente, fazendo uma alteração no código que gere um problema de qualidade.
   - **Exemplos de problemas:** 
     - variavel nao utilizada
     - função sem docstring
     - f-string sem comandos de formatação internamente
   - O SonarLint deve identificar o problema e gerar um alerta no VSCode com o código do problema (ex: ``sonarqube: S1234``).
   - Qualquer duvida sobre o SonarCloud, ou sobre como configurar ele, pergunte para mim. 
   - Utilize IA se necessário para entender melhor o que é o SonarCloud, e como ele funciona.

## Dicas gerais
- Consulte a [documentação oficial do VS Code](https://code.visualstudio.com/docs/python/python-tutorial) para mais detalhes e exemplos.

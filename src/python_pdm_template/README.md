# Estrutura de Projeto Python Modular

Este diretório segue o padrão moderno de organização de projetos Python, utilizando uma pasta `src/` para separar o código-fonte principal dos demais arquivos do projeto.

## Por que usar a pasta `src/`?

- **Evita conflitos de importação:** Ao manter o código dentro de `src/`, você garante que os testes e scripts externos não importem acidentalmente arquivos do diretório raiz.
- **Facilita a modularização:** Permite que o projeto seja organizado em múltiplos módulos e subpacotes, tornando o código mais limpo e escalável.
- **Melhora a manutenção:** Separar o código-fonte dos arquivos de configuração, documentação e testes facilita a navegação e manutenção do projeto.


## Arquivos `__init__.py` 

- Torna a pasta um pacote Python, permitindo importações entre módulos e subpacotes.
- **Deve estar presente em TODAS as pastas e subpastas** que contenham arquivos Python `.py`.
  - Sem esse arquivo, o Python não reconhece o diretório como parte do pacote, o que pode causar erros de importação.
- Pode ser vazio ou conter código de inicialização do pacote.

## Arquivo `__main__.py`

- Define pontos de entrada do projeto (onde o programa começa)

## Estrutura típica

```
raiz-do-projeto/
│   README.md
│   pyproject.toml
│   ...
├── src/
│   └── nome_do_pacote/
│       ├── __init__.py
│       ├── __main__.py
│       ├── modulo1.py
│       ├── modulo2.py
│       ├── modulo3/
│       │   ├── __init__.py
│       │   ├── submodulo1.py
│       │   └── ...
│       └── ...
├── tests/
│   ├── test_modulo1.py
│   ├── test_modulo2.py
|   ├── modulo3/
│   │   ├── test_submodulo1.py
│   │   └── ...
│   └── ...
```

## Vantagens para projetos profissionais

- Facilita publicação no PyPI
- Evita problemas de importação durante testes (ex: pacotes não encontrados, versões erradas, etc.)
  - Todos os pacotes são instalados corretamente no ambiente virtual (pasta `.venv/`), seguindo as versões especificadas no `pyproject.toml`
- Permite crescimento do projeto sem bagunça
- Adota boas práticas recomendadas pela comunidade Python

## Tarefa de hoje - Criar um novo módulo e submódulo
1. Altere o nome da pasta `python_pdm_template` para um nome mais significativo para seu projeto (ex: `meu_projeto`, `app`, etc). 
   - **IMPORTANTE:** Lembre-se de atualizar o arquivo `pyproject.toml` para refletir a mudança de nome do pacote.
2. Crie um novo arquivo `modulo4.py` dentro da pasta `src/nome_do_pacote/` e adicione uma função simples (ex: `def saudacao(): return "Olá, mundo!"`).
3. Crie uma nova pasta `modulo5/` dentro de `src/nome_do_pacote/`, e dentro dela crie os seguintes arquivos:
   - `__init__.py` (pode ser vazio, mas precisa estar presente para que o Python reconheça a pasta como parte do pacote)
   - `submodulo1.py` com uma função simples (ex: `def despedida(): return "Adeus, mundo!"`).
4. O `modulo5` é um módulo que contém submódulos. O `submodulo1` é um módulo dentro do `modulo5`, e ambos fazem parte do pacote `nome_do_pacote`. Para acessar as funcoes criadas, voce deve importar elas usando o caminho completo do pacote (veja exemplo abaixo):    
    ```python
    from nome_do_pacote.modulo4 import saudacao
    from nome_do_pacote.modulo5.submodulo1 import despedida
    ```
    - Para que isso funcione, garanta que o arquivo `__init__.py` esteja presente em todas as pastas e subpastas do projeto (isto é, as subpastas de `src/nome_do_pacote/`), para que o Python reconheça elas como parte do pacote.
5. Importe as funções criadas no `__main__.py` e chame elas para verificar se estão funcionando corretamente (veja exemplo abaixo).
   ```python
    # No arquivo src/nome_do_pacote/__main__.py
    from nome_do_pacote.modulo4 import saudacao
    from nome_do_pacote.modulo5.submodulo1 import despedida
    
    def main():
        print(saudacao())
        print(despedida())

    if __name__ == "__main__":
        main()
   ```
   - Note que as funções `saudacao()` e `despedida()` estão sendo importadas usando o caminho completo do pacote, seguindo a estrutura de pastas do projeto.
   - Conforme mais submodulos vao sendo criados, o caminho de importacao pode ficar muito longo e complexo. Para evitar isso, voce pode importar as funcoes diretamente no arquivo `__init__.py` de cada modulo, para que elas possam ser acessadas diretamente pelo pacote (ex: `from nome_do_pacote.modulo5 import despedida`).
6. Modifique o arquivo `src/nome_do_pacote/modulo5/__init__.py` para importar as funções criadas nos submódulos (veja um exemplo de como fazer isso abaixo).
   - **Exemplo**:
    ```python
    # No arquivo src/nome_do_pacote/modulo5/__init__.py
    from nome_do_pacote.modulo5.submodulo1 import *
    ```
7. Modifique oo `__main__.py` para importar os modulos diretamente(veja exemplo abaixo). 
  ```python
  # No arquivo src/nome_do_pacote/__main__.py
  from nome_do_pacote.modulo4 import saudacao
  from nome_do_pacote.modulo5 import despedida

  def main():
      print(saudacao())
      print(despedida())

  if __name__ == "__main__":
      main()
  ```
  - Verifique se as funções estão funcionando corretamente, e se o código continua funcionando.
  - **Problema**: O uso do `import *` nos arquivos `__init__.py` pode causar problemas de *namespace*, como:
    - Funcoes, classes ou variáveis de diferentes submódulos com mesmo nome (ex: se houver uma função `despedida()` em outro submódulo, o Python não saberá qual delas usar)
    - Todas as funcoes, variaveis e classes do submodulo foram exportadas para `__init__.py`, 
      - Isto pode causar problemas de segurança e manutenção do código (acesso indevido a funcoes, classes, variaveis privadas).
  - **Solucao**: Usar a variável especial do Python `__all__` para indicar quais funções, classes ou variáveis devem ser exportadas pelo módulo.
8. No arquivo `src/nome_do_pacote/modulo5/submodulo1.py`, adicione a variável `__all__` para indicar quais funções, classes ou variáveis devem ser exportadas pelo submódulo (quando alguem usar o comando de importacao `from nome_do_pacote.modulo5.submodulo1 import *`). 
   - **Exemplo**:
    ```python
    # No arquivo src/nome_do_pacote/modulo5/submodulo1.py
    def metodo_privado():
        return "Este metodo nao sera exportado, pois ele nao foi incluido na variavel __all__ abaixo"

    def despedida():
        print("despedida() consegue ver o método privado:")
        print(metodo_privado())
        print()
        print("Até logo!")
        print()

    __all__ = ['despedida']
    ```
  - Note que as funcoes, classes, etc que sao exportadas por `__all__` devem ser escritas como **strings dentro de uma lista**, e devem corresponder exatamente ao nome da funcao, classe, variavel, etc que voce deseja exportar. 
   - No exemplo acima, apenas a função `despedida()` foi incluída na variável `__all__`, o que significa que apenas ela será exportada quando alguém usar o comando de importação `from nome_do_pacote.modulo5.submodulo1 import *`. 
   - O método privado `metodo_privado()` não foi incluído na variável `__all__`, o que significa que ele não será exportado e não poderá ser acessado usando `import *`.  
   - Se você tentar acessar o método privado `metodo_privado()` através de `from nome_do_pacote.modulo5 import metodo_privado`, você receberá um erro de importação, pois ele não foi exportado pelo ``submódulo1`` (modulo5 nao sabe nada sobre ``metodo_privado()``).
   - Com isso, você pode controlar quais funções, classes ou variáveis são expostas para outros módulos, e quais são mantidas privadas dentro do submódulo.
9. Importe as funções criadas no `__main__.py` e chame elas para verificar se estão funcionando corretamente (veja exemplo abaixo).
  ```python
  # No arquivo src/nome_do_pacote/__main__.py
  from nome_do_pacote.modulo4 import saudacao
  from nome_do_pacote.modulo5 import despedida

  def main():
      print(saudacao())
      print(despedida())

  if __name__ == "__main__":
      main()
  ```
  - Note que ``__main__.py`` tem acesso função `despedida`, e ela chama o método privado `metodo_privado()`. 
  - No entanto, ``__main__.py`` nao consegue acessar  `metodo_privado()` diretamente, pois ele não esta disponível em `nome_do_pacote.modulo5`.
  - Verifique isso modificando o `__main__.py` da seguinte forma:
    ```python
    # No arquivo src/nome_do_pacote/__main__.py
    from nome_do_pacote.modulo4 import saudacao
    from nome_do_pacote.modulo5 import despedida, metodo_privado # aqui deve aparecer um erro, pois metodo_privado nao é exportado pelo submodulo1
    
    # TODO: adicione 'metodo_privado' na variavel __all__ do submodulo1.py, e veja o que acontece no __main__.py (sera que o erro some?)
    ```
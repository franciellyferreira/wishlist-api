
# Wishlist API

[![made-with-python](img/made-with-python.svg)](https://www.python.org/)
[![GPLv3 license](img/licence-gpl3.svg)](LICENSE)
[![Documentation Status](img/docs.svg)](https://documenter.getpostman.com/view/2628786/Tz5jf1Ne)
[![Open Source Love svg1](img/open-source.svg)](https://github.com/franciellyferreira/wishlist-api)

Wishlist API foi desenvolvida para apoiar as ações de marketing da empresa. 
Ela oferece funcionalidades para manipular a lista de produtos favoritos dos 
clientes da plataforma.


### Documentação

Para usar o API e consultar os endpoints acesse a 
[documentação](https://documenter.getpostman.com/view/2628786/Tz5jf1Ne).


### O que você precisa para executar esse projeto?

- Versão Python do projeto
  - [Versão recomandada](runtime.txt)

- Criar ambiente virtual
  - Recomendo o uso do [PyEnv](https://github.com/pyenv/pyenv)

- Instalar dependências
  - Rodar o comando:
    > make install

- Banco de dados
  - Usado para desenvolvimento o banco de dados SQLite, porém para publicação 
    em produção recomenda-se usar o PostgreSQL. Para testar com o PostgreSQL local, 
    faça a instalação dele no seu computador, crie o banco de dados e substitua 
    a env no *base.py* (conforme exemplo abaixo):
    ```
    DATABASE_URI = os.environ.get(
        'DATABASE_URI',
        'postgresql://user:pass@host/db_name'
    )
    ```

- Criar as tabelas no banco de dados
  - Rodar o comando:
    > make migrations

- Criar chave para o projeto:
  - Rodar o comando:
    > make generate-key
      
  - Copiar chave gerada e colar no substituir no *base.py*:
    ```
    SECRET_KEY = 'chave'
    ```

- Executar o projeto
    - Rodar o comando:
        > make runserver


### Make

Para facilitar na manutenção e desenvolvimento do código, foi adicionado o Makefile
para disponibilizar os principais comandos úteis. 

- Listar todos:
  > make


#### Tabela de comandos

make + comando | descrição
------------- | -------------
make check | Verifica aplicação
make clean | Limpa variáveis de ambiente local
make create-app | Cria um novo app
make generate-key | Gera uma secret_key
make help | Lista todos os comandos do make
make install | Instala as dependências
make migrate | Gera as migrations
make migrations | Instala as migrations
make runserver | Rodar o projeto
make safety-check | Verificar versões das dependências
make test | Rodar todos os testes
make test-coverage | Rodar os testes e verificar a cobertura
make test-coverage-html | Rodar os testes, verificar a cobertura e gerar html


## Licença

GRU 3 [[Arquivo](LICENSE)] © Franciélly Ferreira, 2021-03

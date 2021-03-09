
# Wishlist API

[![GPLv3](https://img.shields.io/badge/licence-GPLv3-lightgrey)](LICENSE)
[![Python](https://img.shields.io/badge/3.9.1-Python-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/3.0.13-Django-green)](https://www.djangoproject.com/)
[![Django Rest Framework](https://img.shields.io/badge/3.12-Rest%20Framework-red)](https://www.django-rest-framework.org/)
[![Documentation](https://img.shields.io/badge/docs-passing-brightgreen)](https://documenter.getpostman.com/view/2628786/Tz5jf1Ne)

Wishlist API foi desenvolvida para apoiar as ações de marketing da empresa. 
Ela oferece funcionalidades para manipular clientes e a lista de produtos 
favoritos deles na plataforma.


### Documentação

Para usar o API e consultar os endpoints acesse a 
[documentação](https://documenter.getpostman.com/view/2628786/Tz5jf1Ne).


### O que você precisa para executar esse projeto?

- Versão Python do projeto
  - [Versão recomendada](runtime.txt)

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
      
  - Copiar chave gerada e substituir no *base.py*:
    ```
    SECRET_KEY = 'chave'
    ```

- Executar o projeto
    - Rodar o comando:
        > make runserver


### Make

Para facilitar a manutenção e o desenvolvimento do código, foi adicionado o 
Makefile. Ele disponibiliza os principais comandos úteis para trabalhar com 
este projeto.

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
make lint | Verifica padrão PEP8 e ordenação dos imports
make migrate | Gera as migrations
make migrations | Instala as migrations
make runserver | Rodar o projeto
make safety-check | Verificar versões das dependências
make shell | Acessa o shell do Python
make test | Rodar todos os testes
make test-coverage | Rodar os testes, verificar a cobertura e gerar html


## Licença

GRU 3 [[Arquivo](LICENSE)] © Franciélly Ferreira, 2021-03

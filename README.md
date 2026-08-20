# DB Postgres

Template para provisionar um banco PostgreSQL e aplicar arquivos SQL locais em uma ordem configurável, registrando o commit e o estado de execução.

## Status e escopo

O script Python do repositório orquestra a conexão bootstrap, a criação da role e do banco quando necessário, a criação da estrutura de versionamento e a aplicação das entradas definidas em config.yaml. O SQL de negócio fica em sql/.

## Principais componentes

- scripts/apply_sql.py: carrega .env e config.yaml, expande variáveis de ambiente e conecta ao PostgreSQL.
- config.yaml: define o motor, conexões, sql_path, tabela de versão, arquivo de schema e execution_order.
- sql/versionamento.sql: cria controle_versoes, com versão, commit, comentário e data de aplicação.
- sql/atualiza_controle_versoes_identity.sql: atualiza as colunas de identidade da tabela de versões.
- A tabela controle_scripts_sql registra checksum, commit e data de cada script aplicado.
- Cada entrada de execution_order pode usar os modos always, on_change, once ou never.
- GitHub Actions para validação e para aplicar SQL após push em main.

## Pré-requisitos

- Python com acesso para instalar as dependências de requirements.txt.
- Um servidor PostgreSQL acessível pelas credenciais configuradas.
- Permissão bootstrap para criar a role e o banco quando eles ainda não existirem.

Dependências fixadas no repositório:

- psycopg2-binary 2.9.9
- PyYAML 6.0.2
- python-dotenv 1.0.1

## Instalação e configuração

Linux:

~~~bash
cp .env.example .env
python -m pip install -r requirements.txt
~~~

Windows PowerShell:

~~~powershell
Copy-Item .env.example .env
python -m pip install -r requirements.txt
~~~

Preencha .env com as variáveis usadas por config.yaml:

| Variável | Finalidade |
| --- | --- |
| POSTGRES_HOST | Host do PostgreSQL. |
| POSTGRES_PORT | Porta do PostgreSQL. |
| POSTGRES_DB | Banco da aplicação. |
| POSTGRES_USER | Usuário dono do banco da aplicação. |
| POSTGRES_PASSWORD | Senha do usuário dono. |
| POSTGRES_ROOT_DB | Banco usado na conexão bootstrap. |
| POSTGRES_ROOT_USER | Usuário bootstrap. |
| POSTGRES_ROOT_PASSWORD | Senha do usuário bootstrap. |

Não versione .env nem substitua os secrets por valores reais no repositório.

## Execução

Na raiz do repositório:

~~~bash
python scripts/apply_sql.py
~~~

O script usa GITHUB_SHA e GITHUB_COMMIT_MESSAGE quando fornecidos; caso contrário, obtém o commit e a mensagem atuais do Git. Antes de aplicar as migrações, garante a role e o banco configurados, executa o schema de versionamento e aplica os arquivos na ordem definida em config.yaml. A execução registra uma nova linha em controle_versoes.

A configuração atual executa sql/atualiza_controle_versoes_identity.sql uma vez. Para adicionar scripts, inclua uma entrada SQL válida em database.execution_order.

## Testes e qualidade

Os comandos usados pelo workflow CI/CD são:

~~~bash
python -m py_compile scripts/apply_sql.py
python -m unittest discover -s tests -v
~~~

O workflow também valida os arquivos essenciais, a nomenclatura dos SQL e bloqueia SQL destrutivo contendo TRUNCATE ou DROP DATABASE/TABLE/SCHEMA. O workflow Apply SQL On Main instala as dependências e executa o script após push em main.

## Estrutura do projeto

~~~text
sql/
  atualiza_controle_versoes_identity.sql
  versionamento.sql
scripts/
  apply_sql.py
tests/
  test_apply_sql.py
config.yaml
.env.example
requirements.txt
.github/workflows/
  ci-cd.yml
  apply-sql-on-main.yml
~~~

## Consulta da versão atual

~~~sql
SELECT versao, commit_id, comentario_commit, aplicado_em
FROM controle_versoes
ORDER BY versao DESC
LIMIT 1;
~~~

## Contribuição

Inclua novas migrações na ordem definida em config.yaml, mantenha o modo de execução explícito e valide o script e os testes antes de abrir uma pull request.

## Licença

Este projeto está sob a licença MIT. Consulte LICENSE para o texto completo.

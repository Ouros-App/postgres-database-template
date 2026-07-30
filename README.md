# DB Postgres

Template para banco PostgreSQL versionado por arquivos SQL locais.

O diretorio `sql/` guarda os arquivos SQL. A ordem de execucao fica em `config.yaml`. O Python so orquestra: garante banco e role, executa os SQL e grava a versao atual do banco com commit e comentario.

O script e Python puro. Roda do mesmo jeito em Windows e Linux, sem depender de bash.

## Uso

Linux:

```bash
cp .env.example .env
pip install -r requirements.txt
python scripts/apply_sql.py
```

Windows:

```powershell
Copy-Item .env.example .env
pip install -r requirements.txt
python scripts\apply_sql.py
```

## Como funciona

1. `scripts/apply_sql.py` carrega `.env` e `config.yaml`.
2. Se faltar, cria usuario e banco usando `POSTGRES_ROOT_DB` e `POSTGRES_ROOT_USER`.
3. Executa os SQL na ordem definida em `database.execution_order`.
4. Usa `database.version_schema_file` para garantir a tabela de versionamento.
5. Grava `versao`, `commit_id`, `comentario_commit` e `aplicado_em`.
6. Toda execucao gera uma nova linha de versao.

## Configuracao

```yaml
database:
  sql_path: sql
  version_table: controle_versoes
  version_schema_file: versionamento.sql
  execution_order:
    - versionamento.sql
```

## Query da versao atual

```sql
SELECT versao, commit_id, comentario_commit, aplicado_em
FROM controle_versoes
ORDER BY versao DESC
LIMIT 1;
```

## Estrutura esperada

```text
db-postgres/
|- sql/
|  |- versionamento.sql
|- scripts/
|  |- apply_sql.py
|- config.yaml
|- .env.example
|- .env
`- requirements.txt
```

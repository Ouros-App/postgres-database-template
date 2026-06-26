# DB Postgres

Template para banco PostgreSQL versionado com migracoes SQL em GitHub.

O foco e manter a estrutura pronta para DB as code:
- migracoes numeradas por versao
- controle de execucao no banco
- criacao automatica do banco quando necessario
- configuracao separada entre `config.yaml` e `.env`

## Como Funciona

1. O `scripts/migrate.py` carrega as variaveis do `.env`
2. O script le o `config.yaml` para saber banco, usuario e tabela de controle
3. Se o banco nao existir, ele conecta com o usuario admin e cria o banco
4. As migracoes sao buscadas em `migrations/`
5. O fluxo aplica apenas o que ainda nao foi registrado em `controle_versoes`

## Estrutura

- `migrations/`: scripts SQL numerados no formato `V1__descricao.sql`
- `scripts/migrate.py`: ponto de entrada da migracao
- `config.yaml`: configuracao do ambiente e credenciais organizadas
- `.env.example`: variaveis sensiveis de exemplo
- `requirements.txt`: dependencias Python

## Arquivos

### `config.yaml`

Define:
- nome do projeto
- host e porta do PostgreSQL
- nome do banco
- usuario e senha da aplicacao
- usuario e senha admin para criacao do banco
- pasta de migracoes
- nome da tabela de controle

### `.env`

Copie o exemplo e ajuste os valores reais:

```bash
cp .env.example .env
```

## Variaveis

- `POSTGRES_HOST`: host do servidor PostgreSQL
- `POSTGRES_PORT`: porta do servidor PostgreSQL
- `POSTGRES_DB`: nome do banco da aplicacao
- `POSTGRES_USER`: usuario dono do banco
- `POSTGRES_PASSWORD`: senha do usuario dono do banco
- `POSTGRES_ADMIN_USER`: usuario com permissao para criar banco
- `POSTGRES_ADMIN_PASSWORD`: senha do usuario admin

## Regras

- apenas DDL
- scripts idempotentes
- execucao sequencial por versao
- transacao por arquivo
- sem commitar segredos

## Uso

```bash
python scripts/migrate.py
```

## Exemplo de migracao

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL
);
```

## Estrutura Esperada

```text
db-postgres/
├── migrations/
│   └── V1__init.sql
├── scripts/
│   └── migrate.py
├── config.yaml
├── .env.example
├── .env
└── requirements.txt
```

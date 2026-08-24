import os
import tempfile
import unittest
from pathlib import Path

from scripts.apply_sql import load_config, sql_entries


class ApplySqlTest(unittest.TestCase):
    def test_load_config_reads_sql_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.yaml").write_text(
                "\n".join(
                    [
                        "database:",
                        "  host: ${POSTGRES_HOST}",
                        "  port: ${POSTGRES_PORT}",
                        "  name: ${POSTGRES_DB}",
                        "  bootstrap:",
                        "    db: ${POSTGRES_ROOT_DB}",
                        "    user: ${POSTGRES_ROOT_USER}",
                        "    password: ${POSTGRES_ROOT_PASSWORD}",
                        "  owner:",
                        "    user: ${POSTGRES_USER}",
                        "    password: ${POSTGRES_PASSWORD}",
                        "  sql_path: sql",
                        "  version_table: controle_versoes",
                        "  version_schema_file: versionamento.sql",
                        "  execution_order: []",
                    ]
                ),
                encoding="utf-8",
            )
            os.environ.update(
                {
                    "POSTGRES_HOST": "localhost",
                    "POSTGRES_PORT": "5432",
                    "POSTGRES_DB": "app",
                    "POSTGRES_ROOT_DB": "root_db",
                    "POSTGRES_ROOT_USER": "ouros_root",
                    "POSTGRES_ROOT_PASSWORD": "root",
                    "POSTGRES_USER": "app",
                    "POSTGRES_PASSWORD": "app",
                }
            )
            cfg = load_config(root)
            self.assertEqual(cfg["database"]["sql_path"], "sql")
            self.assertEqual(cfg["database"]["version_schema_file"], "versionamento.sql")
            self.assertEqual(cfg["database"]["execution_order"], [])

    def test_execution_order_preserves_multiple_scripts_and_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sql_dir = root / "sql"
            sql_dir.mkdir()
            for name in ("banco_ouros_fisico.sql", "atualiza_password.sql"):
                (sql_dir / name).write_text("", encoding="utf-8")

            cfg = {
                "database": {
                    "sql_path": "sql",
                    "execution_order": [
                        {"file": "banco_ouros_fisico.sql", "mode": "on_change"},
                        {"file": "atualiza_password.sql", "mode": "once"},
                    ],
                }
            }

            entries = sql_entries(root, cfg)
            self.assertEqual(
                [(path.name, mode) for path, mode in entries],
                [
                    ("banco_ouros_fisico.sql", "on_change"),
                    ("atualiza_password.sql", "once"),
                ],
            )


if __name__ == "__main__":
    unittest.main()

# mysql-mcp — instalacja

**Typ:** MCP | **Opis:** Dostęp read-only do bazy MySQL — zapytania, schemat, diagnostyka

**Pliki:**
- `mcp_servers/mysql/server.py`
- `mcp_servers/mysql/__init__.py`
- `scripts/run-mysql-mcp.sh`
- `scripts/load-env.sh`

**MCP entry:**
```json
{ "command": "bash", "args": ["scripts/run-mysql-mcp.sh"], "cwd": "." }
```

**Python deps:** `pip install fastmcp pymysql python-dotenv`

**Setup:** uzupełnij `.env.mysql`

**Wymagane dane (zbierz od użytkownika przed setup):**
| Zmienna | Opis | Przykład |
|---------|------|---------|
| `MYSQL_HOST` | Host bazy danych | `localhost` lub `db.example.com` |
| `MYSQL_PORT` | Port (domyślnie 3306) | `3306` |
| `MYSQL_USER` | Użytkownik read-only | `app_readonly` |
| `MYSQL_PASSWORD` | Hasło użytkownika | `secret` |
| `MYSQL_DATABASE` | Nazwa bazy | `myapp_db` |

Utwórz `.env.mysql` z powyższymi wartościami przed uruchomieniem MCP.

# kanboard-mcp — instalacja

**Typ:** MCP | **Opis:** Zarządzanie zadaniami — backlog, tworzenie, edycja, handoff briefy

**Pliki:**
- `mcp_servers/kanboard/server.py`
- `mcp_servers/kanboard/__init__.py`
- `kanboard_setup/.env.example`
- `scripts/run-kanboard-mcp.sh`
- `scripts/load-env.sh`

**MCP entry:**
```json
{ "command": "python3", "args": ["mcp_servers/kanboard/server.py"], "cwd": "." }
```

**Python deps:** `pip install fastmcp requests python-dotenv`

**Setup:** `npm run init-kb`

**Wymagane dane (zbierz od użytkownika przed setup):**
| Zmienna | Opis | Przykład |
|---------|------|---------|
| `KANBOARD_URL` | Adres Kanboard z `/jsonrpc.php` | `https://kanboard.example.com/jsonrpc.php` |
| `KANBOARD_API_TOKEN` | Token API z ustawień konta | `abc123...` |
| `KANBOARD_PROJECT_ID` | ID projektu w Kanboard | `1` |

Zapisywane do `kanboard_setup/.env` przez `npm run init-kb`.

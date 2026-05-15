# Agent Guide

## Sources
- `docs/teams/COMMON.md`
- `docs/teams/AI_ROUTING.md`
- `docs/teams/AI_HOSTS_AND_MCP.md` (Claude, Cursor, Codex, Gemini — równorówny workflow; GitHub MCP per host)
- `handoff/`

## Workflow
1. Weź brief.
2. Zmień kod i uruchom testy.
3. Zamknij brief.
4. Jeśli agent ma czytać lub edytować pliki repo, użyj lokalnego Filesystem MCP: `npm run filesystem-mcp`.

## Kanboard
- `KANBOARD_PROJECT` ustawia projekt
- jeśli puste, zapytaj użytkownika i zapisz `handoff/ASK_PROJECT_NAME.md`
- Kanboard MCP wymaga ustawionych `KANBOARD_URL` i `KANBOARD_TOKEN`; bez tego serwer nie wystartuje
- Najprościej trzymaj je w repo-root `.env`; legacy `kanboard_setup/.env` nadal działa, jeśli już go używasz
- Lokalny start MCP: `npm run kanboard-mcp`
- Pobieranie ticketów i backlogu odbywa się przez MCP tools, np. `kanboard_get_backlog`, `kanboard_get_task`, `kanboard_create_handoff`, `kanboard_move_task`
- Usuwanie ticketu: `kanboard_delete_task(task_id, confirm=true)` używa Kanboard `removeTask`
- Inicjalizacja / aktualizacja konfiguracji z MCP: `kb_init(host, url, user, token, project)`; jeśli brakuje danych, tool zwraca pytania i czeka na ponowne wywołanie z odpowiedziami
- Status połączenia i test RPC: `kanboard_connection_status`

### Szybki setup (nowy projekt / nowe środowisko)
- `npm run init-kb` zapisuje `kanboard_setup/.env` i testuje połączenie z Kanboard (`getVersion`)
- Jeśli chcesz jeden wspólny lokalny plik, przenieś też te wartości do repo-root `.env`

### Start projektu (repo + Kanboard)
- `npm run start-project` podłącza repozytoria do `apps/` i zawsze uruchamia `npm run init-kb`

## Komendy
- `list <project> Backlog`
- `show <id>`
- `handoff <id>`
- `claim`
- `move <id> <column>`

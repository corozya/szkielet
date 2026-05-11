# Workflow Repository

- `kanboard_setup/` - Kanboard tooling
- `handoff/` - aktywne briefy
- `docs/teams/` - instrukcje agentów

Kod aplikacji jest w repozytorium produktu.

## Setup Kanboard (one-command)

1. Zainstaluj zależności (Node.js 18+):
   - `npm install` (w tym repo)
2. Skonfiguruj i przetestuj połączenie:
   - `npm run init-kb`

Skrypt zapisze konfigurację do `kanboard_setup/.env` i zweryfikuje API metodą `getVersion`.
Kanboard MCP wymaga jawnie ustawionych `KANBOARD_URL` i `KANBOARD_TOKEN`; bez tego serwer nie wystartuje.
Pobieranie backlogu i ticketów odbywa się przez MCP tools, np. `kanboard_get_backlog`, `kanboard_get_task` i `kanboard_create_handoff`.
Do szybkiej weryfikacji konfiguracji użyj `kanboard_connection_status` - pokazuje parametry połączenia i testuje `getVersion`.
Start lokalny przez wrapper: `npm run kanboard-mcp`.

## Start projektu (repo + Kanboard)

Jedna komenda do onboardingu projektu dla agentów:

- `npm run start-project`

Proces:
- pyta o URL repozytoriów (po jednym) i klonuje je do `apps/<repo>/` (gałąź `main`)
- dopisuje `apps/` do `.gitignore`, żeby nie commitować kodu aplikacji do “szkieletu”
- zawsze uruchamia `npm run init-kb` i dopytuje o konfigurację Kanboard

Regułka do wklejenia dla agentów:

> Uruchom `npm run start-project`. Skrypt podłączy repozytoria do `apps/` (pyta po jednym URL, zawsze `main`, nie nadpisuje istniejących katalogów), dopisze `apps/` do `.gitignore`, a potem zawsze uruchomi `npm run init-kb` i doprowadzi do poprawnej konfiguracji Kanboard.

## Agenci: Claude, Cursor, Codex, Gemini

Workflow i handoff są **wspólne** dla wszystkich tych środowisk. Sugestie „który model na jaki typ zadania” są w `docs/teams/AI_ROUTING.md`; pełna lista hostów, zasady i **GitHub MCP** (Cursor, Claude, Codex, Gemini): `docs/teams/AI_HOSTS_AND_MCP.md`.

Codex ma projektowy wpis MCP w [`.codex/config.toml`](/home/corozya/www/szkielet/.codex/config.toml), bez twardej ścieżki do katalogu użytkownika. Jeśli Twoja instalacja używa tylko `~/.codex/config.toml`, skopiuj ten blok do konfiguracji globalnej i ustaw `cwd` na aktualny root repo.

Szybki start MCP w Cursorze: skopiuj `.cursor/mcp.json.example` → `.cursor/mcp.json`, wstaw PAT, zrestartuj IDE.

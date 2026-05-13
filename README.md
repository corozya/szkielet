# Workflow Repository

- `kanboard_setup/` - Kanboard tooling
- `handoff/` - aktywne briefy
- `docs/teams/` - instrukcje agentów

Kod aplikacji jest w repozytorium produktu.

## Dokumentacja marketingowa

- **Strategia (mix kanałów, kalendarz, cele):** [marketing/MARKETING_PLAN.md](marketing/MARKETING_PLAN.md)
- **Google Ads (kampania, budżet, Shopping/Search):** [marketing/google-ads/campaign-plan-small-budget.md](marketing/google-ads/campaign-plan-small-budget.md)
- **Frazy pod Search (GSC):** [docs/ads_ready_phrases.md](docs/ads_ready_phrases.md)
- **Feed Merchant Center (XML w repo):** [marketing/google-ads/google_merchant_feed.xml](marketing/google-ads/google_merchant_feed.xml)

## Setup Kanboard (one-command)

1. Zainstaluj zależności (Node.js 18+):
   - `npm install` (w tym repo)
2. Skonfiguruj i przetestuj połączenie:
   - `npm run init-kb`

Skrypt zapisze konfigurację do `kanboard_setup/.env` i zweryfikuje API metodą `getVersion`.
Kanboard MCP wymaga jawnie ustawionych `KANBOARD_URL` i `KANBOARD_TOKEN`; bez tego serwer nie wystartuje.
Pobieranie backlogu i ticketów odbywa się przez MCP tools, np. `kanboard_get_backlog`, `kanboard_get_task` i `kanboard_create_handoff`.
Do aktualizacji parametrów z poziomu MCP użyj `kb_init` np. z `project`.
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

### MySQL MCP

Lokalny, read-only serwer MySQL startujesz przez:

- `npm run mysql-mcp`

Konfiguracja trafia do `.env.mysql`:

1. Skopiuj [`.env.mysql.example`](/home/corozya/www/szkielet/.env.mysql.example) do `.env.mysql`.
2. Uzupełnij `MYSQL_HOST`, `MYSQL_USER` i opcjonalnie `MYSQL_PASSWORD` oraz `MYSQL_DATABASE`.
3. Jeśli chcesz użyć innej ścieżki, ustaw `MYSQL_ENV_FILE`.

Serwer udostępnia narzędzia do:

- sprawdzania połączenia
- listowania baz
- listowania tabel
- opisu tabel
- wykonywania wyłącznie read-only zapytań SQL

### Filesystem MCP

Lokalny serwer Filesystem startujesz przez:

- `npm run filesystem-mcp`

Domyślnie ma dostęp tylko do katalogu repozytorium, więc nie widzi całego `HOME`.
To jest najbezpieczniejszy wariant, jeśli agent ma czytać i edytować pliki tego szkieletu.

### Memory MCP

Lokalny serwer pamięci uruchamiasz przez:

- `npm run memory-mcp`

Domyślnie zapisuje dane do `.memory/memory.jsonl`, więc pamięć jest lokalna dla repozytorium.
Jeśli chcesz użyć innej ścieżki, ustaw `MEMORY_FILE_PATH` w `.env.memory`.

Serwer udostępnia standardowy knowledge graph memory:

- tworzenie encji
- tworzenie relacji
- dodawanie i usuwanie obserwacji
- wyszukiwanie i odczyt grafu

### Analytics MCP

Żeby `analytics` startował w nowym klonie, potrzebujesz:

1. Skopiować [`.env.analytics.example`](/home/corozya/www/szkielet/.env.analytics.example) do `.env.analytics`.
2. Uzupełnić `GOOGLE_APPLICATION_CREDENTIALS` i `GOOGLE_PROJECT_ID`.
3. Upewnić się, że plik credentials istnieje.
4. Mieć w `PATH` binarkę `analytics-mcp`.

Jeśli chcesz używać ADC przez `gcloud`, najprościej:

- `gcloud auth application-default login`
- sprawdź, czy istnieje `~/.config/gcloud/application_default_credentials.json`
- ustaw `GOOGLE_PROJECT_ID` w `.env.analytics` albo w shellu

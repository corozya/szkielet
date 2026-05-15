# Środowiska AI i GitHub MCP

## Dozwolone hosty

Praca agentów jest **równoważna** w dowolnym z poniższych środowisk:

| Host | Typowe użycie |
|------|----------------|
| **Claude** | Claude Code (CLI), Claude Desktop |
| **Cursor** | IDE + Composer / Agent |
| **OpenAI Codex** | CLI lub rozszerzenie IDE z MCP |
| **Google Gemini CLI** | Terminal (`gemini`) |

Źródło prawdy dla procesu: `docs/teams/COMMON.md`, `docs/teams/AGENT_GUIDE.md`, `handoff/`. Host nie zmienia kolejności kroków (brief → implementacja → aktualizacja handoffu).

**`docs/teams/AI_ROUTING.md`** opisuje **sugerowaną kolejność modeli** wg typu zadania (np. architektura vs UI). To nie jest lista dozwolonych narzędzi: możesz realizować ten sam brief w Cursorze, Claude Code, Codexie lub Gemini — o ile masz dostęp do repozytorium i ewentualnie MCP.

## GitHub MCP (repozytorium z poziomu agenta)

Wspólny serwer: [GitHub MCP Server](https://github.com/github/github-mcp-server) — [spis instalacji](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/README.md).

Potrzebny jest [GitHub PAT](https://github.com/settings/personal-access-tokens/new) z zakresami dopasowanymi do operacji (np. `repo`; dla Actions — `workflow`). **Nie commituj tokenu** do tego repozytorium.

### Skrót konfiguracji per host

| Host | Gdzie konfiguracja | Oficjalny przewodnik |
|------|--------------------|----------------------|
| **Cursor** | `~/.cursor/mcp.json` lub `.cursor/mcp.json` w projekcie (w repo jest `.cursor/mcp.json.example`) | [install-cursor.md](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-cursor.md) |
| **Claude Code** | `claude mcp add-json …` lub plik konfiguracyjny wg scope (`local` / `user`); Desktop: `claude_desktop_config.json` | [install-claude.md](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md) |
| **Codex** | Projektowy [`.codex/config.toml`](/home/corozya/www/szkielet/.codex/config.toml) z lokalnym `cwd = "."`; fallback: `~/.codex/config.toml` | [install-codex.md](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-codex.md) |
| **Gemini CLI** | `~/.gemini/settings.json` lub `.gemini/settings.json` w projekcie; PAT często jako `GITHUB_MCP_PAT` w `~/.gemini/.env` | [install-gemini-cli.md](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-gemini-cli.md) |

Zdalny endpoint (Streamable HTTP), jeśli host go obsługuje: `https://api.githubcopilot.com/mcp/` — szczegóły w przewodnikach powyżej. Alternatywa: lokalny Docker `ghcr.io/github/github-mcp-server`.

## Rekomendowany zestaw dla tego repo

Jeśli używasz tu `Codex`, `Gemini`, `Cursor` i `Claude`, najpraktyczniejszy zestaw MCP to:

- `GitHub` jako zdalny serwer do repo i PR-ów
- `Kanboard` jako lokalny serwer do backlogu i handoffów
- `Context7` jako lokalny serwer do aktualnej dokumentacji bibliotek
- `Playwright` jako lokalny serwer tylko dla zadań UI, smoke-testów i E2E
- `Filesystem` jako lokalny serwer do pracy na plikach tego repo
- `Google Analytics` jako lokalny serwer tylko dla analityki i raportów biznesowych
- `MySQL` jako lokalny, read-only serwer do diagnostyki baz
- `Memory` jako lokalny knowledge graph do trwałych notatek i relacji

### Jeden lokalny `.env`

W tym repo najwygodniej utrzymywać wszystkie lokalne sekrety w jednym repo-root `.env`.
Wrappers MCP czytają go jako pierwszy. Starsze pliki typu `.env.analytics`, `.env.google-ads`, `.env.gsc` i `kanboard_setup/.env` są nadal wspierane jako kompatybilne override, ale dla MySQL zalecamy wyłącznie `.env`.

W skrócie:

| MCP | Zalecenie | Powód |
|-----|-----------|-------|
| GitHub | wszędzie | mniej ręcznego kopiowania diffów, issue i logów CI |
| Kanboard | wszędzie w tym repo | bez przepisywania ticketów i statusów |
| Context7 | wszędzie, gdy pracujesz z bibliotekami | aktualne API i mniej halucynacji |
| Playwright | lokalnie, tylko przy UI/E2E | pewna weryfikacja frontu bez ręcznego klikania |
| Filesystem | lokalnie, tylko dla tego repo | bezpieczny dostęp do plików projektu bez całego `$HOME` |
| Google Analytics | lokalnie, tylko przy analytics | pytania o użytkowników, eventy i raporty bez ręcznego klikania po UI |
| MySQL | lokalnie, gdy potrzebujesz podglądu bazy | schemat i dane bez wychodzenia z agenta |
| Memory | lokalnie, gdy chcesz trwałej pamięci projektu | notatki i relacje między encjami bez ręcznego przepisywania |

Minimalny zestaw, który warto utrzymać stale:

1. `GitHub`
2. `Kanboard`
3. `Context7`
4. `Filesystem` tylko jeśli chcesz pracować na plikach repo z poziomu agenta
5. `Playwright` tylko jeśli regularnie sprawdzasz UI
6. `Google Analytics` tylko jeśli faktycznie analizujesz GA
7. `MySQL`, jeśli pracujesz z lokalną bazą
8. `Memory`, jeśli chcesz zachować trwały kontekst projektu

### Google Ads MCP

Do zarządzania kampaniami Google Ads używaj lokalnego wrappera `scripts/run-google-ads-mcp.sh`.
Serwer: [`googleads/google-ads-mcp`](https://github.com/googleads/google-ads-mcp) (oficjalny, od Google).

#### Wymagania

- **Developer token** w trybie **Standard Access** — wymagany do pracy na prawdziwych danych kampanii.
  Wniosek o token złożony 2026-05-13 przez formularz: https://support.google.com/adspolicy/contact/new_token_application
  Po akceptacji (ok. 3 dni robocze) Google wyśle odpowiedź na `corozya@gmail.com`.
  Token wklej do `.env.google-ads` jako `GOOGLE_ADS_DEVELOPER_TOKEN`.
- `GOOGLE_APPLICATION_CREDENTIALS` — plik JSON z OAuth2 (jak w Analytics)
- `GOOGLE_PROJECT_ID` — projekt w Google Cloud
- MCC ID: `721-197-3072`

> Bez Standard Access token działa tylko w trybie testowym (fikcyjne dane).

Dodaj do konfiguracji MCP hosta:

```json
{
  "google-ads": {
    "command": "bash",
    "args": ["scripts/run-google-ads-mcp.sh"],
    "cwd": "."
  }
}
```

---

### Google Analytics MCP

Do Analytics w tym repo używaj lokalnego wrappera `scripts/run-google-analytics-mcp.sh` albo skrótu `npm run analytics-mcp`.
Serwer udostępnia `get_account_summaries` bez `property_id`; `GA4_PROPERTY_ID` wpływa tylko na narzędzia raportowe, które pracują na konkretnej właściwości.

Gotowe konfiguracje per host:

- Cursor: skopiuj `.cursor/mcp.json.example` do `.cursor/mcp.json`
- Claude: użyj `.claude/mcp.json.example` jako źródła dla `claude mcp add-json` albo Desktop configu
- Codex: wpis jest już obecny w `.codex/config.toml`
- Gemini: wpis jest już obecny w `.gemini/settings.json`

Jeśli chcesz wkleić to ręcznie, ten sam serwer wygląda tak:

```json
{
  "analytics": {
    "command": "bash",
    "args": ["scripts/run-google-analytics-mcp.sh"],
    "cwd": "."
  }
}
```

Ważne:

- `GOOGLE_APPLICATION_CREDENTIALS` i `GOOGLE_PROJECT_ID` muszą być ustawione
- `GA4_PROPERTY_ID` jest opcjonalne i potrzebne tylko wtedy, gdy chcesz domyślną właściwość dla raportów
- jeśli host ma whitelistę MCP, dodaj tam też serwer `analytics`

### Weryfikacja

- Cursor: Settings → Tools & Integrations → MCP (status serwera `github`).
- Claude Code: `claude mcp list`.
- Codex: `/mcp` w UI lub dokumentacja OpenAI.
- Codex w tym szablonie: użyj projektu-local [`.codex/config.toml`](/home/corozya/www/szkielet/.codex/config.toml) albo skopiuj blok do `~/.codex/config.toml` jeśli Twoja instalacja ignoruje konfigurację w repo.
- Gemini CLI: w sesji `gemini` wpisz `/mcp list`, albo w shellu: `gemini mcp list` ([dokumentacja MCP w Gemini CLI](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html)).

### Claude Code / Claude Desktop

Konfiguruj przez `claude mcp add-json` albo przez plik konfiguracyjny Desktop.
Rekomendacja dla tego repo:

- `github` -> `https://api.githubcopilot.com/mcp/`
- `kanboard` -> lokalny `scripts/run-kanboard-mcp.sh`
- `context7` -> `npx -y @upstash/context7-mcp@latest`
- `playwright` -> `npx -y @playwright/mcp@latest`
- `filesystem` -> lokalny `scripts/run-filesystem-mcp.sh`
- `mysql` -> lokalny `scripts/run-mysql-mcp.sh`
- `memory` -> lokalny `scripts/run-memory-mcp.sh`

Jeśli używasz jedynie Claude Desktop, trzymaj to samo zestawienie w jego configu poza repo.

Przykładowe polecenie testowe: „List my GitHub repositories”.

#### Gemini: „nie widzi” GitHub MCP — typowe przyczyny

1. **Brak wpisu w `settings.json`** — Gemini czyta `mcpServers` z `~/.gemini/settings.json` **albo** z `.gemini/settings.json` w katalogu projektu (zależnie od scope). Konfiguracja Cursora (`.cursor/mcp.json`) **nie** jest używana przez Gemini CLI.
2. **Zmienna z PAT** — dla zdalnego GitHub MCP ustaw `GITHUB_MCP_PAT` (np. w `~/.gemini/.env` albo `export GITHUB_MCP_PAT=ghp_...` w tym samym terminalu co `gemini`). Bez wartości nagłówek `Authorization` jest pusty i serwer się nie zestawi.
3. **Whitelist `mcp.allowed`** — jeśli w `settings.json` masz `"mcp": { "allowed": ["…"] }`, musi tam być też nazwa serwera z `mcpServers` (np. `"github"`). W przeciwnym razie CLI **pominie** wszystkie inne serwery ([opis `mcp.allowed`](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html)).
4. **Transport** — dla hostowanego GitHub MCP użyj **`httpUrl`** (Streamable HTTP), nie myl z polem `url` (SSE).
5. **CLI** — `gemini mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer $GITHUB_MCP_PAT"` (patrz `gemini mcp add` w dokumentacji powyżej) zamiast ręcznej edycji JSON, jeśli wolisz.

## Uwagi

- Pakiet npm `@modelcontextprotocol/server-github` jest **przestarzały**; używaj oficjalnego serwera / obrazu z dokumentacji GitHuba.
- Dla Desktop / wersji bez Streamable HTTP często pozostaje konfiguracja przez Docker — patrz odpowiedni plik `install-*.md`.

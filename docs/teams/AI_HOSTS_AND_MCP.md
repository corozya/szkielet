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
- `Google Analytics` jako lokalny serwer tylko dla analityki i raportów biznesowych

W skrócie:

| MCP | Zalecenie | Powód |
|-----|-----------|-------|
| GitHub | wszędzie | mniej ręcznego kopiowania diffów, issue i logów CI |
| Kanboard | wszędzie w tym repo | bez przepisywania ticketów i statusów |
| Context7 | wszędzie, gdy pracujesz z bibliotekami | aktualne API i mniej halucynacji |
| Playwright | lokalnie, tylko przy UI/E2E | pewna weryfikacja frontu bez ręcznego klikania |
| Google Analytics | lokalnie, tylko przy analytics | pytania o użytkowników, eventy i raporty bez ręcznego klikania po UI |

Minimalny zestaw, który warto utrzymać stale:

1. `GitHub`
2. `Kanboard`
3. `Context7`
4. `Playwright` tylko jeśli regularnie sprawdzasz UI
5. `Google Analytics` tylko jeśli faktycznie analizujesz GA

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

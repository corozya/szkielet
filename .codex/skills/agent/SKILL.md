---
name: agent
description: Instaluje agenta AI lub integrację MCP z repozytorium scaffold bez klonowania. Wywołaj /agent <nazwa>.
---

# agent Skill (Codex)

Jako agent pobierasz pliki i edytujesz konfiguracje samodzielnie. Nie używasz skryptów instalacyjnych.

## Wywołanie

`/agent <nazwa>` — np. `/agent frontend`, `/agent kanboard`, `/agent backend`

## Procedura

### Krok 1 — Ustal integrację
Wyodrębnij nazwę z polecenia. Jeśli brak — pokaż listę numerowaną z manifestu i zapytaj: *"Które chcesz zainstalować? Podaj numery lub nazwy."* Pozwól wybrać kilka.

### Krok 2 — Źródło manifestu (priorytet)

1. Lokalny `scaffold-manifest.json` → przeczytaj (Read)
2. `SCAFFOLD_REPO` w `.env` → pobierz `https://raw.githubusercontent.com/{owner}/{repo}/main/scaffold-manifest.json`
3. Brak obu → zapytaj o URL repo

### Krok 3 — Pobierz pliki

Dla każdego z `integration.files`:
- URL: `https://raw.githubusercontent.com/{owner}/{repo}/main/{filePath}`
- Sprawdź czy istnieje (Read), zapytaj o nadpisanie
- Zapisz przez Write

### Krok 4 — Konfiguracja MCP

Dla `type === "mcp"`:
- Wykryj hosty: `.claude/` → `.claude/mcp.json`, `.cursor/` → `.cursor/mcp.json`, `.gemini/` → `.gemini/settings.json`, `.codex/` → `mcp.json`
- Dopisz `integration.mcp_entry` pod kluczem `integration.id` w każdym pliku

Dla `type === "agent"`: zapisz do `agents/{id}/`

### Krok 5 — Finalizacja

- Poinformuj o `python_deps` jeśli istnieją
- Zapytaj czy uruchomić `setup_cmd` (np. `npm run init-kb`)
- Podsumuj co zainstalowano

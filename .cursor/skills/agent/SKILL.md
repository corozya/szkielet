---
name: agent
description: Instaluje agenta AI lub integrację MCP do projektu z repozytorium scaffold. Użyj /agent <nazwa> np. /agent frontend, /agent kanboard.
---

# agent Skill (Cursor)

Jako agent wykonujesz instalację samodzielnie — używasz narzędzi do pobierania plików i edycji konfiguracji. Nie uruchamiasz skryptów instalacyjnych.

## Procedura

### Krok 1 — Ustal integrację
Wyodrębnij nazwę z polecenia: `/agent frontend` → `frontend`, `/agent kanboard` → `kanboard`.
Jeśli brak nazwy — pokaż listę numerowaną z manifestu i zapytaj: *"Które chcesz zainstalować? Podaj numery lub nazwy."* Pozwól wybrać kilka.

### Krok 2 — Pobierz manifest

Sprawdź w kolejności:
1. Lokalny plik `scaffold-manifest.json` — jeśli istnieje, przeczytaj go
2. Zmienna `SCAFFOLD_REPO` w `.env` — jeśli ustawiona (np. `owner/repo`), pobierz:
   `https://raw.githubusercontent.com/{owner}/{repo}/main/scaffold-manifest.json`
3. Zapytaj użytkownika o URL repo

### Krok 3 — Pobierz i zapisz pliki

Dla każdego pliku z `integration.files`:
- Pobierz: `https://raw.githubusercontent.com/{owner}/{repo}/main/{filePath}`
- Jeśli plik istnieje — zapytaj o nadpisanie
- Zapisz do projektu zachowując ścieżkę

### Krok 4 — Patchuj konfigurację MCP (tylko type === "mcp")

Wykryj hosty sprawdzając katalogi `.claude/`, `.cursor/`, `.gemini/`, `.codex/`.

Dla każdego wykrytego hosta przeczytaj jego `mcp.json` (lub `settings.json` dla Gemini), dodaj wpis z `integration.mcp_entry` pod kluczem `integration.id`, zapisz.

### Krok 5 — Konfiguracja i podsumowanie

Jeśli `integration.python_deps` — poinformuj o instalacji pip.
Jeśli `integration.setup_cmd` — zapytaj czy uruchomić (np. `npm run init-kb`).
Podsumuj: co zainstalowano, które hosty skonfigurowano, co jeszcze trzeba zrobić.

## Zasady

- Pobieraj tylko pojedyncze pliki przez URL raw GitHub — nie klonuj repo
- Zawsze pytaj przed nadpisaniem istniejących plików
- Dla agentów (type === "agent"): zapisz pliki do `agents/{id}/`, nie patchuj MCP

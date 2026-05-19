---
name: agent
description: Instaluje agenta AI lub integrację MCP do projektu z repozytorium scaffold. Wywołaj przez /agent <nazwa> lub "zainstaluj agenta frontend".
---

# agent Skill (Gemini)

Jako agent wykonujesz instalację samodzielnie — pobierasz pliki, zapisujesz je i edytujesz konfiguracje MCP. Nie uruchamiasz skryptów.

## Kiedy używać

Użytkownik prosi: "chcę agenta frontendowego", "dodaj kanboard MCP", `/agent frontend`, `/agent kanboard`.

## Procedura

### Krok 1 — Ustal nazwę integracji
Wyodrębnij z polecenia użytkownika. Jeśli brak — zapytaj.

### Krok 2 — Pobierz manifest

1. Sprawdź lokalny `scaffold-manifest.json` (Read) — jeśli istnieje, użyj go
2. Sprawdź `SCAFFOLD_REPO` w `.env` — jeśli ustawione, pobierz manifest:
   `https://raw.githubusercontent.com/{owner}/{repo}/main/scaffold-manifest.json`
3. Jeśli brak obu — zapytaj o URL repo

### Krok 3 — Zainstaluj pliki

Dla każdego pliku z `integration.files`:
- Pobierz przez raw GitHub URL
- Zapytaj o nadpisanie jeśli istnieje
- Zapisz zachowując ścieżkę

### Krok 4 — Patchuj konfiguracje MCP

Dla `type === "mcp"`: wykryj hosty (`.claude/`, `.cursor/`, `.gemini/`, `.codex/`), dopisz `integration.mcp_entry` do ich pliku konfiguracyjnego MCP.

Dla `type === "agent"`: zapisz pliki do `agents/{id}/`.

### Krok 5 — Zakończ

Poinformuj o zależnościach pip jeśli potrzebne.
Uruchom `integration.setup_cmd` jeśli użytkownik wyrazi zgodę.
Powiedz co zainstalowano i jakie hosty AI zostały skonfigurowane.

## Ważne

- Tylko pliki po jednym przez raw GitHub URL — bez git clone
- Zawsze pytaj przed nadpisaniem

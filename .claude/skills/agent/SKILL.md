---
name: agent
description: Instaluje agenta AI lub integrację MCP do bieżącego projektu z repozytorium scaffold. Użyj /agent <nazwa> np. /agent frontend, /agent kanboard, /agent seo.
triggers: ["agent", "install-agent", "dodaj agenta", "zainstaluj agenta", "dodaj mcp", "zainstaluj integrację"]
---

# agent — Instalator integracji i agentów AI

Jako agent wykonujesz instalację samodzielnie używając narzędzi (WebFetch, Read, Write, Edit, Bash). Nie uruchamiasz skryptów — robisz to wszystko sam.

## Procedura

### Krok 1 — Ustal nazwę integracji

Wyodrębnij nazwę z polecenia użytkownika: `/agent frontend` → `frontend`, `/agent kanboard` → `kanboard`.

Jeśli użytkownik nie podał nazwy — zapytaj: "Jaką integrację chcesz zainstalować? Dostępne: frontend, backend, kanboard, mysql-mcp, filesystem-mcp, memory-mcp"

### Krok 2 — Pobierz manifest

**Opcja A — lokalny manifest (priorytet):**
Sprawdź czy istnieje `scaffold-manifest.json` w CWD. Jeśli tak — przeczytaj go narzędziem Read.

**Opcja B — zdalny manifest:**
Sprawdź `SCAFFOLD_REPO` w `.env`. Jeśli ustawione np. `owner/repo`, pobierz:
```
https://raw.githubusercontent.com/{owner}/{repo}/main/scaffold-manifest.json
```
użyj WebFetch.

Jeśli brak obu — zapytaj użytkownika o URL repozytorium scaffold (np. `https://github.com/owner/repo`).

### Krok 3 — Znajdź integrację w manifeście

Z pobranego JSON znajdź obiekt gdzie `id` lub `name` pasuje do żądanej nazwy.

Przykład wpisu:
```json
{
  "id": "kanboard",
  "type": "mcp",
  "files": ["mcp_servers/kanboard/server.py", "kanboard_setup/.env.example"],
  "mcp_entry": { "command": "python3", "args": ["mcp_servers/kanboard/server.py"], "cwd": "." },
  "setup_cmd": "npm run init-kb"
}
```

Jeśli integracja nie istnieje — powiedz użytkownikowi jakie ID są dostępne.

### Krok 4 — Pobierz i zapisz pliki

Dla każdego pliku z `integration.files`:

1. Pobierz zawartość przez WebFetch:
   ```
   https://raw.githubusercontent.com/{owner}/{repo}/main/{filePath}
   ```

2. Sprawdź czy plik już istnieje (Read). Jeśli istnieje — zapytaj użytkownika czy nadpisać.

3. Zapisz plik narzędziem Write, zachowując oryginalną ścieżkę względną.

4. Jeśli plik jest wykonywalny (`.sh`) — ustaw uprawnienia:
   ```bash
   chmod +x {ścieżka}
   ```

### Krok 5 — Patchuj konfiguracje MCP (tylko dla type === "mcp")

Wykryj obecnych hostów AI sprawdzając obecność katalogów:
- `.claude/` → plik `.claude/mcp.json`
- `.cursor/` → plik `.cursor/mcp.json`
- `.gemini/` → plik `.gemini/settings.json`
- `.codex/` lub `codex.json` → plik `mcp.json`

Dla każdego wykrytego hosta:
1. Przeczytaj istniejący plik konfiguracji (Read). Jeśli nie istnieje — zacznij od `{"mcpServers": {}}`.
2. Dodaj lub zaktualizuj wpis pod kluczem `integration.id` używając wartości z `integration.mcp_entry`.
3. Zapisz plik (Write lub Edit).

### Krok 6 — Obsługa zależności Python (jeśli integration.python_deps)

Poinformuj użytkownika:
```
Wymagane zależności Python: pip install fastmcp requests python-dotenv
```
Zapytaj czy uruchomić teraz. Jeśli tak:
```bash
pip install {integration.python_deps.join(" ")}
```

### Krok 7 — Uruchom setup_cmd (jeśli istnieje)

Jeśli `integration.setup_cmd` jest ustawione (np. `npm run init-kb`):
- Zapytaj użytkownika: "Integracja wymaga konfiguracji. Uruchomić teraz: `{setup_cmd}`?"
- Jeśli tak — uruchom przez Bash i przeprowadź użytkownika przez pytania konfiguracyjne.

### Krok 8 — Podsumowanie

Powiedz użytkownikowi:
- ✓ co zostało zainstalowane (lista plików)
- ✓ które hosty AI zostały skonfigurowane
- → co jeszcze trzeba zrobić (np. restart hosta AI, uruchomienie setup_cmd)

## Przykład pełnego przebiegu

```
Użytkownik: /agent kanboard
Agent:
1. Czyta SCAFFOLD_REPO z .env → owner/repo
2. WebFetch → scaffold-manifest.json → znajduje "kanboard"
3. WebFetch → mcp_servers/kanboard/server.py → Write do CWD
4. WebFetch → kanboard_setup/.env.example → Write do CWD
5. Wykrywa .claude/ i .cursor/ → patchuje mcp.json w obu
6. "Kanboard wymaga konfiguracji. Uruchomić npm run init-kb?"
7. Uruchamia init-kb → użytkownik podaje URL/token
8. "✓ Kanboard MCP zainstalowany. Zrestartuj Claude Code."
```

## Ważne zasady

- Nigdy nie klonuj całego repo — tylko pobieraj pojedyncze pliki przez WebFetch
- Zawsze pytaj przed nadpisaniem istniejących plików
- Jeśli `SCAFFOLD_REPO` nie jest ustawione i nie ma lokalnego manifestu — zapytaj użytkownika o URL zanim zaczniesz cokolwiek pobierać
- Dla agentów (type === "agent"): kopiuj pliki do `agents/{id}/`, nie patchuj MCP

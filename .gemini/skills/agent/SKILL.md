---
name: agent
description: Instaluje agenta AI lub integrację MCP do projektu z repozytorium scaffold (bez klonowania). Wywołaj przez /agent <nazwa> lub "zainstaluj agenta frontend".
---

# agent Skill (Gemini)

Pobiera konfigurację ze zdalnego repozytorium scaffold i instaluje wybranego agenta lub serwer MCP.

## Kiedy używać

- Użytkownik prosi o agenta: "chcę agenta frontendowego", "dodaj kanboard MCP", "zainstaluj integrację mysql"
- Wywołanie przez slash command: `/agent frontend`, `/agent kanboard`

## Procedura

### Krok 1 — Ustal integrację
Wyodrębnij nazwę z polecenia użytkownika (frontend, backend, kanboard, mysql-mcp, itp.)

### Krok 2 — Sprawdź manifest
```bash
cat scaffold-manifest.json 2>/dev/null
```
Jeśli brak pliku — sprawdź `.env`:
```bash
grep SCAFFOLD_REPO .env 2>/dev/null
```

### Krok 3 — Uruchom instalację
```bash
node bin/install-from-repo.js --id <nazwa>
```

### Krok 4 — Zweryfikuj
- Dla MCP: sprawdź `.gemini/settings.json` — powinien zawierać nowy wpis
- Dla agenta: sprawdź `agents/<nazwa>/AGENT.md`

## Ustawienie SCAFFOLD_REPO (jednorazowe)

Dodaj do `.env`:
```
SCAFFOLD_REPO=owner/repo
```
Wtedy nie trzeba podawać URL przy każdej instalacji.

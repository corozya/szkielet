---
name: agent
description: Instaluje agenta AI lub integrację MCP do projektu z repozytorium scaffold (bez klonowania). Użyj: /agent frontend, /agent kanboard, /agent seo.
---

# agent Skill (Cursor)

Pobiera konfigurację agenta/integracji MCP ze zdalnego repo scaffold i instaluje ją w bieżącym projekcie.

## Wywołanie

```
/agent <nazwa>
```

Przykłady: `/agent frontend`, `/agent kanboard`, `/agent backend`, `/agent mysql-mcp`

## Procedura

1. Sprawdź czy istnieje lokalny `scaffold-manifest.json` — jeśli tak, użyj go
2. Jeśli nie — sprawdź `SCAFFOLD_REPO` w `.env`
3. Uruchom instalator:

```bash
node bin/install-from-repo.js --id <nazwa>
```

Lub interaktywnie (bez podanej nazwy):
```bash
npm run install-from-repo
```

4. Sprawdź wynik — `.cursor/mcp.json` powinien zawierać nowy wpis MCP

## Konfiguracja

Ustaw raz w `.env`:
```
SCAFFOLD_REPO=owner/repo
GITHUB_TOKEN=ghp_...   # tylko dla prywatnych repo
```

## Dostępne typy

- `agent` — kopiuje definicję agenta AI do `agents/<nazwa>/`
- `mcp` — instaluje serwer MCP i aktualizuje `.cursor/mcp.json`
- `workflow` — kopiuje skrypty i narzędzia workflow

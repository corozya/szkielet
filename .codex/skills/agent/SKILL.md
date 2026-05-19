---
name: agent
description: Instaluje agenta AI lub integrację MCP z repozytorium scaffold bez klonowania. Wywołaj: /agent <nazwa>.
---

# agent Skill (Codex)

Instaluje agenta lub serwer MCP z repozytorium scaffold do bieżącego projektu.

## Wywołanie

```
/agent <nazwa>
```

Np.: `/agent frontend`, `/agent kanboard`, `/agent backend`

## Workflow

1. Sprawdź lokalny `scaffold-manifest.json` lub `SCAFFOLD_REPO` w `.env`
2. Uruchom:
   ```bash
   node bin/install-from-repo.js --id <nazwa>
   ```
3. Dla MCP: sprawdź `mcp.json` w katalogu projektu
4. Uruchom ewentualne setup_cmd z manifest (np. `npm run init-kb`)

## Konfiguracja w .env

```
SCAFFOLD_REPO=owner/repo          # źródło integracji
GITHUB_TOKEN=ghp_...              # dla prywatnych repo
```

## Dostępne integracje

Lista w `scaffold-manifest.json`. Typy: `mcp`, `agent`, `workflow`.

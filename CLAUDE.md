# Project Orchestrator — Claude

Zasady/role: `docs/teams/COMMON.md`
Workflow: `docs/teams/AGENT_GUIDE.md`
Hosty AI (Claude, Cursor, Codex, Gemini) + GitHub MCP: `docs/teams/AI_HOSTS_AND_MCP.md`
Aktywne zadania: `handoff/`

## Kanboard (quick init)

- Setup: `npm install` → `npm run init-kb`
- Konfiguracja ląduje w `kanboard_setup/.env` (sekrety; nie commitować)

## Start projektu (repo + Kanboard)

- Uruchom: `npm run start-project`
- To podłączy repozytoria do `apps/` i zawsze odpali `npm run init-kb`

## Narzędzia — zawsze używaj dedykowanych (oszczędność tokenów)

- Zamiast `cat`/`head`/`tail` → narzędzie **Read**
- Zamiast `find`/`ls` → narzędzie **Glob**
- Zamiast `grep`/`rg` → narzędzie **Grep**
- `Bash` tylko dla: SSH, docker compose, deploy, komend systemowych bez dedykowanego narzędzia

## MCP rekomendowane dla tego repo

- `GitHub MCP`
- `Kanboard MCP`
- `Context7 MCP`
- `Playwright MCP` lokalny, tylko dla UI i E2E
- `MySQL MCP` lokalny, read-only, jeśli repo korzysta z bazy
- `Memory MCP` lokalny, jeśli chcesz trwałych notatek w repo

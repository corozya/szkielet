# Project Orchestrator — Claude

Zasady/role: `docs/teams/COMMON.md`
Workflow: `docs/teams/AGENT_GUIDE.md`
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

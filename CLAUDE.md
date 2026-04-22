# Project Orchestrator — Claude

Zasady/role: `docs/teams/COMMON.md`
Workflow: `docs/teams/AGENT_GUIDE.md`
Aktywne zadania: `handoff/`

## Narzędzia — zawsze używaj dedykowanych (oszczędność tokenów)

- Zamiast `cat`/`head`/`tail` → narzędzie **Read**
- Zamiast `find`/`ls` → narzędzie **Glob**
- Zamiast `grep`/`rg` → narzędzie **Grep**
- `Bash` tylko dla: SSH, docker compose, deploy, komend systemowych bez dedykowanego narzędzia

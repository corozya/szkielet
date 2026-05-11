# Project Orchestrator — Codex

Zasady/role: `docs/teams/COMMON.md`  
Workflow: `docs/teams/AGENT_GUIDE.md`  
Aktywne zadania: `handoff/`

## MCP

- Repo zawiera projektowe wpisy MCP w [`.codex/config.toml`](/home/corozya/www/szkielet/.codex/config.toml)
- Jeśli Twoja instalacja Codexa czyta tylko `~/.codex/config.toml`, skopiuj ten sam blok i ustaw `cwd` na root sklonowanego repo
- Lokalny MySQL MCP startuje przez `npm run mysql-mcp` po uzupełnieniu `.env.mysql`
- Lokalny Memory MCP startuje przez `npm run memory-mcp` i zapisuje dane do `.memory/memory.jsonl`

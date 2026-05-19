---
name: scaffold
description: Czyta README repozytorium scaffold i instaluje wybrane integracje (MCP, agenci AI) do projektu.
---

# scaffold Skill (Codex)

Gdy użytkownik podaje URL do README repozytorium scaffold, pobierasz go i instalujesz wybrane integracje.

## Procedura

1. WebFetch README (raw URL)
2. Znajdź sekcję `## Instalacja przez agenta AI`
3. Zapytaj które integracje zainstalować
4. Dla każdej:
   - WebFetch pliki z `raw.githubusercontent.com/{owner}/{repo}/main/{plik}`
   - Write do projektu
   - MCP: Edit `mcp.json` — dopisz `mcp_entry`
5. Bash `setup_cmd` jeśli użytkownik wyrazi zgodę

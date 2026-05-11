# AI Routing

## Hosty (IDE / CLI)

**Dozwolone środowiska pracy:** Claude (Code / Desktop), Cursor, OpenAI Codex, Google Gemini CLI — każde z nich może realizować ten sam workflow i briefy z `handoff/`. Ten plik **nie** ogranicza wyboru hosta; opisuje tylko sugestie wyboru **modelu** do typu zadania.

Szczegóły (w tym GitHub MCP na każdym hoście): `docs/teams/AI_HOSTS_AND_MCP.md`.

## Default (sugestia modelu, nie hosta)
- architektura: Claude -> Gemini -> Codex
- duże pliki / mechanika: Gemini
- UI / React / boilerplate: Codex
- małe poprawki: Copilot

## Rules
1. Sprawdź `handoff/`.
2. Jeśli jest brief, każdy agent może pracować.
3. Cross-cutting nie dawaj Copilotowi.

## Sygnał
```markdown
**Suggested AI:** Claude
**Fallback AI:** Codex
**Context size needed:** Large
```

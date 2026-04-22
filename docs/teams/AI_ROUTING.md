# AI Routing

## Default
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

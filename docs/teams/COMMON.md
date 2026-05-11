# Common Standards

## Roles & Workflow

### 👨‍💼 Orchestrator (You)
1. Write briefs for Architect → `handoff/TASK_NAME.md`
2. Answer Architect's questions
3. Merge and push code to main
4. Release: `bash scripts/release-prod.sh`

### 🏗️ Architect Agent
1. Read brief from Orchestrator (contains small tasks)
2. Check if tasks are clear and small
3. If unclear → ask Orchestrator individually
4. **Monitor agents' progress** ← watch `handoff/`
5. **Answer agents' questions in "Questions/Issues" section** ← MANDATORY
6. Verify all ✅ tasks are complete

### 👨‍💻 Specialists (Backend/Frontend/DevOps)
1. Read brief (your role's section)
2. Pick tasks yourself (mark status)
3. Do work + tests
4. Commit to `main` (`git commit`)
5. If question/issue → add to brief
6. Wait for push from Orchestrator/Architect

### 📖 Documentation by Role
- `ARCHITECTURE.md` — Architect Agent
- `BACKEND.md` — Backend Developer
- `FRONTEND.md` — Frontend Developer
- `DEVOPS.md` — DevOps Engineer

## Handoff — Process

### Brief Template
```
handoff/TASK_NAME.md:

# Task: [ID] - [Title]

## Context
[What's needed, why]

## Expected Outcome
[What should be done]

## Backend Tasks
- [ ] [Small task 1] `status: TODO`
- [ ] [Small task 2] `status: TODO`

## Frontend Tasks
- [ ] [Small task 1] `status: TODO`
- [ ] [Small task 2] `status: TODO`

## DevOps Tasks
- [ ] [Small task 1] `status: TODO`

## Validation
[How to test the complete task]

## Questions/Issues for Architect
(agents add questions here if needed)
```

### Workflow
1. **Orchestrator** writes brief with small tasks (checkboxes)
2. **Architect** reviews, asks Orchestrator if needed
3. **Agents** (Backend/Frontend/DevOps):
   - Read brief
   - Pick tasks (mark `status: IN PROGRESS`)
   - Do work + tests
   - Commit to `main` (`git commit`)
   - Mark ✅ (checkbox) when done / update brief
   - If issue → add to "Questions/Issues" section
4. **Architect** answers agents' questions (MANDATORY)
5. **Architect** verifies completed tasks (tests pass, code OK)
   - If OK → approve ✅
   - If issue → add feedback to brief
6. **Orchestrator** after ✅ all tasks + Architect verification: merge, push, release

### Task Statuses
- `TODO` — waiting
- `IN PROGRESS` — someone is working
- `DONE` ✅ — complete

## Definition of Done
1. Code tested.
2. Commit has proper format.
3. Brief completed.
4. No regressions.

## Środowiska AI

Dozwolone hosty: **Claude**, **Cursor**, **OpenAI Codex**, **Google Gemini CLI** — wspólny workflow i `handoff/`; wybór hosta nie zastępuje COMMON / AGENT_GUIDE. GitHub MCP i konfiguracja per host: `docs/teams/AI_HOSTS_AND_MCP.md`. Dla pracy na plikach repo używaj lokalnego Filesystem MCP przez `npm run filesystem-mcp`.

## DoD
1. Kod przetestowany.
2. Commit ma poprawny format.
3. Brief zakończony.
4. Brak regresji.

## Git
- Each agent commits own changes (locally on `main`).
- Format: `feat(scope): description` or `fix(scope): description`.
- Orchestrator or Architect does the push (after review).
- Tests must pass before push.

## Release
- Orchestrator: `bash scripts/release-prod.sh`
- Creates tag `prod-YYYYMMDD-HHMMSS`
- GitHub Actions handles production deploy

## Token Efficiency
- Write concisely.
- Read only what you need.
- Use `rtk`.

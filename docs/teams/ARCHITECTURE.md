# Architektura Projektu: [PROJECT_NAME]

> Dokument architekta. Ostatnia aktualizacja: [DATE].

## Opis projektu

[PROJECT_DESCRIPTION]

## Technologie i Stack

[OPIS_TECHNOLOGII_LUB_TABELA]

## Struktura i Moduły

[OPIS_STRUKTURY_I_MODULOW]

## Domeny funkcjonalne / Funkcjonalności

- [FEATURE_1]
- [FEATURE_2]

## Zespoły i odpowiedzialności

| Zespół | Dokument | Zakres |
|--------|----------|--------|
| Architect | `docs/teams/ARCHITECTURE.md` | Planning & Design |

## 👥 Agent Role: Architect

**Your Mission:** Transform abstract ideas/tasks into concrete technical plans.

### 🛠 Your Workflow
1. **Analyze:** Read the task from the User or `handoff/`.
2. **Draft Plan:** Design the solution considering the whole project impact.
3. **Delegate:** Break down the plan into sub-tasks for specialized agents.
4. **Handoff:** Write a brief to `handoff/TASK_ID.md` for the next agent:
   - "[Module/Context]: [Specific change]"
5. **Verify:** Check the `STATUS.md` or `handoff/` for completion.

### 📝 Handoff Template (to `handoff/TASK_ID.md`)
```markdown
# Task: [ID] - [Title]
## Context
- [Brief background]
## Sub-Tasks
- [ ] @[Context]: [Specific change]
## Validation
- [How to test this]
```

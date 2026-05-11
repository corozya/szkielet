---
name: kb-backlog-review
description: Fetches Kanboard Backlog, selects top tasks, generates handoff briefs, and summarizes findings.
---

# kb-backlog-review Skill

Use when the user asks to review Kanboard tickets/backlog for this repo (e.g. “pobierz zgłoszenia”, “sprawdź zgłoszenia”, “przejrzyj backlog”).

## Preflight
- If `kanboard_setup/.env` is missing or Kanboard calls fail, run `npm run init-kb` and retry.

## Commands
- `kanboard_get_backlog(project_ref="<KANBOARD_PROJECT>")`
- `kanboard_create_handoff(task_id=<ID>)`

## Deliverable
- Fetch and summarize **all** Backlog tasks.
- Generate `handoff` briefs for **all** Backlog tasks (avoid `--force` unless asked).

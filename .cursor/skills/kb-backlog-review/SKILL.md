---
name: kb-backlog-review
description: Fetches Kanboard Backlog, selects top tasks, generates handoff briefs, and summarizes findings.
---

# kb-backlog-review (Cursor)

Use when asked to check Kanboard submissions/tickets.

## Preflight
- If `kanboard_setup/.env` is missing or Kanboard calls fail: run `npm run init-kb` and retry.

## Commands
- List backlog:
  - `kanboard_get_backlog(project_ref="<KANBOARD_PROJECT>")`
- Generate brief:
  - `kanboard_create_handoff(task_id=<ID>)`

## Output
- Briefs in `handoff/` for **all** Backlog tasks + summary of **all** tasks.

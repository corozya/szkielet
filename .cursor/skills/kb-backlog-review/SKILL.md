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
  - `python3 kanboard_setup/kb_manager.py list "<KANBOARD_PROJECT>" Backlog`
- Generate brief:
  - `python3 kanboard_setup/kb_manager.py handoff <ID>`

## Output
- Briefs in `handoff/` for **all** Backlog tasks + summary of **all** tasks.


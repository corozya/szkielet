---
name: kb-backlog-review
description: Fetches Kanboard Backlog, selects top tasks, generates handoff briefs, and summarizes findings.
---

# kb-backlog-review (Codex)

Use this when the user asks any of:
- “pobierz zgłoszenia”
- “sprawdź zgłoszenia”
- “przejrzyj backlog”
- “pobierz listę zadań z Kanboard”
- “sprawdź co jest w Backlogu”

## Preflight (must do before fetching)
1. Check Kanboard config:
   - `kanboard_setup/.env` exists
   - has `KANBOARD_URL`, `KANBOARD_USER`, `KANBOARD_TOKEN`
2. If config is missing OR any Kanboard call fails:
   - run `npm install` (if needed)
   - run `npm run init-kb`
   - retry the Kanboard command

## Commands (repo standard)
- List backlog:
  - `python3 kanboard_setup/kb_manager.py list "<KANBOARD_PROJECT>" Backlog`

## Required behavior
- Fetch **all** tasks in Backlog (not just top 3).
- Summarize **each** task (ID + title + 1-line note: what it is / why it matters / missing info).
- Generate `handoff` **for all Backlog tasks**:
  - `python3 kanboard_setup/kb_manager.py handoff <ID>`

## Safety (large backlogs)
- If Backlog is very large, generate handoffs in batches (e.g. 10 at a time) and keep going until done.
- If a handoff folder already exists, do not delete it unless explicitly requested (avoid `--force` by default).

## Expected output
- Handoff folders under `handoff/` for all Backlog tasks (each with `brief.md`)
- A summary covering all tasks (ordered as in Backlog list), plus:
  - any duplicates / near-duplicates
  - missing requirements that block many tasks


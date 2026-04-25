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

- For selected tasks create brief(s) in `handoff/`:
  - `python3 kanboard_setup/kb_manager.py handoff <ID>`

## Expected output
- 1–3 handoff folders under `handoff/` (with `brief.md`)
- A short summary:
  - top 3 tasks (ID + title)
  - why selected now (impact / urgency / dependencies)
  - any missing info / next questions


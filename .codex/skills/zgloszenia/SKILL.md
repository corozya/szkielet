---
name: zgloszenia
description: Pobiera zgłoszenia z Kanboard dla tego repo, tworzy pliki `handoff/TASK_*.md` i oznacza przetworzone zadania jako Done.
---

# Zgłoszenia

Use this skill when the user asks to:
- `zgloszenia`
- `pobierz zgłoszenia`
- `sprawdź zgłoszenia`
- `przejrzyj backlog`
- `pobierz listę zadań z Kanboard`

## Workflow
1. Check whether `kanboard_setup/.env` exists.
2. If it is missing, run `npm run init-kb`.
3. Run `npm run zgloszenia`.
4. Verify the generated `handoff/TASK_*.md` files.
5. Summarize how many tasks were created and closed.

## Behavior
- Reads Kanboard project settings from `kanboard_setup/.env`.
- Fetches active tasks from Kanboard.
- Writes one handoff file per task into `handoff/`.
- Marks processed tasks as Done in Kanboard.

## Notes
- Treat `KANBOARD_TOKEN` as secret.
- If the user wants a read-only backlog review, use `kb-backlog-review` instead.

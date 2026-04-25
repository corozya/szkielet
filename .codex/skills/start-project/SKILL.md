---
name: start-project
description: One-command project initialization (clones app repos, adds .gitignore, runs init-kb).
---

# start-project Skill (Codex)

Use for fresh project setup (first-time environment init).

## Workflow
1. Run `npm install` (once per clone)
2. Run `npm run start-project`
3. Enter git URLs when prompted (empty line to finish)
4. Wait for cloning and Kanboard init to complete

## Result
- `apps/` contains cloned repositories
- `.gitignore` updated to ignore `apps/`
- `kanboard_setup/.env` created (Kanboard credentials)

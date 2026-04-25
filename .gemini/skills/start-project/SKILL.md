---
name: start-project
description: One-command project initialization (clones app repos into apps/, adds .gitignore, runs init-kb).
---

# start-project Skill (Gemini)

Use when setting up a fresh instance of this repo (developer/agent first time).

## What happens
1. Creates `apps/` directory
2. Adds `apps/` to `.gitignore`
3. Prompts you to paste git URLs (one per line, empty to finish)
4. Clones each repo to `apps/<reponame>`
5. Runs `npm run init-kb` (Kanboard setup)

## Commands
```bash
npm install
npm run start-project
```

## Notes
- `apps/` is gitignored — repos are cloned separately, not committed
- `kanboard_setup/.env` is created with Kanboard credentials (secret, not committed)

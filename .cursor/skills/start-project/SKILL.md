---
name: start-project
description: One-command project initialization (clones repos into apps/, runs init-kb for Kanboard).
---

# start-project Skill (Cursor)

Use for fresh project setup.

## Commands
```bash
npm install
npm run start-project
```

## What it does
- Creates `apps/` and adds to `.gitignore`
- Clones app repositories (you provide git URLs)
- Sets up Kanboard config

## Notes
- Applications go in `apps/` but are not committed
- Kanboard secrets stored in `kanboard_setup/.env`

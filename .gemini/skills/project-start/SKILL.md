---
name: project-start
description: One command onboarding: attach repos into apps/, ensure apps/ gitignored, then ALWAYS run npm run init-kb.
---

# project-start

Use when the user says: "start projektu", "zainicjuj projekt", "onboarding projektu".

## What to run
- `npm run start-project`

## What it does
- Clones 1..N repos into `apps/<repoName>/` (branch `main`)
- Ensures `apps/` is in `.gitignore`
- Runs `npm run init-kb` (always)


---
name: project-start
description: One command onboarding: attach repos into apps/, ensure apps/ gitignored, then ALWAYS run npm run init-kb.
---

# project-start

Use when the user says: "start projektu", "zainicjuj projekt", "onboarding projektu".

## Goal
- Attach one or more code repositories under `apps/<repoName>/`
- Ensure `apps/` is excluded from the skeleton repo (`.gitignore`)
- Always run `npm run init-kb` to (re)configure Kanboard

## Flow (interactive)
1. Run `npm run start-project`
2. Script asks for repo URLs one by one (empty input ends)
3. Repos are cloned to `apps/<repoName>/` using branch `main`
4. Then `npm run init-kb` is executed (always)

## Guardrails
- If `apps/<repoName>/` exists: stop (do not pull, do not delete)
- Never commit secrets from `kanboard_setup/.env`


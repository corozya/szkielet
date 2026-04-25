---
name: init-kb
description: Interactive Kanboard initializer (writes kanboard_setup/.env and tests JSON-RPC via getVersion).
---

# init-kb Skill (Codex)

Use when Kanboard credentials/config are missing or a new environment needs setup.

## Workflow
- Run `npm install` (once per clone)
- Run `npm run init-kb`
- Confirm `kanboard_setup/.env` was created/updated
- Confirm the connection test succeeded (`getVersion`)

## Non-interactive mode
- `node ./bin/init-kb.js --url <URL> --user <USER> --token <TOKEN> [--project <NAME>] [--env-path <PATH>] [--no-test]`

## Security
- Treat `KANBOARD_TOKEN` as secret.
- Never commit `kanboard_setup/.env` (use `kanboard_setup/.env.example` instead).


---
name: init-kb
description: One-command Kanboard setup for this repo (writes kanboard_setup/.env, tests getVersion, enables kb tooling).
---

# init-kb Skill (Cursor)

Use this when a developer/agent needs Kanboard access configured for this workspace.

## What to run
- `npm install`
- `npm run init-kb`

This writes `kanboard_setup/.env` used by `kanboard_setup/kb_manager.py`.

## Non-interactive mode
- `node ./bin/init-kb.js --url <URL> --user <USER> --token <TOKEN> [--project <NAME>] [--no-test]`

## Important
- Do not commit `kanboard_setup/.env` (contains secrets).


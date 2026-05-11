---
name: init-kb
description: One-command Kanboard setup for this repo (writes kanboard_setup/.env, tests getVersion, enables Kanboard MCP tooling).
---

# init-kb Skill (Cursor)

Use this when a developer/agent needs Kanboard access configured for this workspace.

## What to run
- `npm install`
- `npm run init-kb`

This writes `kanboard_setup/.env` used by the Kanboard MCP server.

## Non-interactive mode
- `node ./bin/init-kb.js --host <HOST> --user <USER> --token <TOKEN> [--project <NAME>] [--no-test]`
- alias: `--url <JSONRPC_ENDPOINT>`

## Important
- Do not commit `kanboard_setup/.env` (contains secrets).

---
name: init-kb
description: Initializes Kanboard config for this repo (asks for URL/user/token/project, writes kanboard_setup/.env, tests connection via getVersion).
---

# init-kb Skill

Use this skill when Kanboard configuration is missing or a new developer/environment needs a one-command setup.

## What it does
- Runs `npm run init-kb` to collect `KANBOARD_URL`, `KANBOARD_USER`, `KANBOARD_TOKEN`, `KANBOARD_PROJECT`
- Writes them to `kanboard_setup/.env` (the source of truth for Kanboard tooling in this repo)
- Tests the JSON-RPC connection by calling `getVersion`

## Usage
- Interactive:
  - `npm install`
  - `npm run init-kb`

- Non-interactive (CI / pipe):
  - `node ./bin/init-kb.js --host <HOST> --user <USER> --token <TOKEN> [--project <NAME>] [--no-test]`
  - alias: `--url <JSONRPC_ENDPOINT>`

## Notes
- Never commit `kanboard_setup/.env` (it contains secrets). Use `kanboard_setup/.env.example` for sharing defaults.


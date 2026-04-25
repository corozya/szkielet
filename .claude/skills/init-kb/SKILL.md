---
name: init-kb
description: Initializes Kanboard config for this repo (prompts for host/user/token/project, writes kanboard_setup/.env, tests JSON-RPC).
---

# init-kb Skill

Interactive one-command setup for Kanboard integration in this repo.

## What it does
- Collects Kanboard credentials: `KANBOARD_URL`, `KANBOARD_USER`, `KANBOARD_TOKEN`, `KANBOARD_PROJECT`
- Writes them to `kanboard_setup/.env` (source of truth for all Kanboard tooling)
- Tests JSON-RPC connection via `getVersion` to confirm credentials work

## Usage

**Interactive mode** (recommended):
```bash
npm install
npm run init-kb
```

**Non-interactive mode** (CI/CD):
```bash
node ./bin/init-kb.js --host <HOST> --user <USER> --token <TOKEN> [--project <NAME>] [--no-test]
# or
node ./bin/init-kb.js --url <JSONRPC_ENDPOINT> --user <USER> --token <TOKEN> [--no-test]
```

## Environment variables created
- `KANBOARD_URL` — Kanboard JSON-RPC endpoint
- `KANBOARD_USER` — API user
- `KANBOARD_TOKEN` — API token (secret!)
- `KANBOARD_PROJECT` — Project name (optional)

## Security note
- `kanboard_setup/.env` contains secrets. Never commit it.
- Use `kanboard_setup/.env.example` to share non-secret defaults.

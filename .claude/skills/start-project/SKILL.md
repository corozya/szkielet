---
name: start-project
description: One-command project initialization (clones app repos into apps/, adds .gitignore, runs init-kb).
---

# start-project Skill

Complete project setup for a fresh environment.

## What it does
- Creates `apps/` directory (contains cloned application repos)
- Adds `apps/` to `.gitignore` (repos are not committed, only references)
- Prompts for git URLs of repositories to clone
- Clones each repo to `apps/<reponame>`
- Automatically runs `npm run init-kb` to configure Kanboard

## Usage

```bash
npm install
npm run start-project
```

Then:
1. Enter git URLs of repos to attach (one per line, empty to finish)
2. Each repo is cloned to `apps/<reponame>`
3. Kanboard config is initialized (prompts for credentials if needed)

## Output structure
```
.
├── apps/
│   ├── PROJECTS.json  (lista podłączonych projektów — dla agentów)
│   ├── <app1>/        (cloned from git URL 1)
│   ├── <app2>/        (cloned from git URL 2)
│   └── .../
├── kanboard_setup/
│   └── .env           (Kanboard credentials, do not commit)
└── ...
```

## apps/PROJECTS.json

Po pobraniu repozytoriów skill tworzy `apps/PROJECTS.json` zawierający:
```json
[
  {
    "name": "repo-name",
    "url": "https://github.com/...",
    "path": "apps/repo-name",
    "fullPath": "/absolute/path/to/apps/repo-name"
  }
]
```

**Dla agentów**: wczytaj ten plik żeby wiedzieć gdzie są projekty.

# Task: DEVOPS-002 — Production deploy on git tags (GitHub Actions)

## Goal
- Add production CD that deploys on **new git tag**.
- Target server: `ubuntu@147.135.208.80`
- Keep existing staging deploy (`./deploy_to_rpi.sh`) intact.

## Constraints / Standards
- **No direct production push:** follow `beta -> prod` tagging flow (per `AGENTS.md` / `docs/teams/COMMON.md`).
- Deployment must not overwrite server secrets (`.env*`) or persistent Kanboard data (`kanboard_setup/data/...`).

## Proposed flow
1. Developer tags a commit as `beta-*` (staging).
2. After verification, developer tags **the same commit** as `prod-*`.
3. GitHub Actions triggers on `prod-*` and:
   - builds frontend assets (`backend-api`),
   - rsyncs repo (with excludes) to the production host,
   - runs `docker compose -f docker-compose.prod.yml up -d --build`,
   - runs composer + artisan steps.

## Status
- [ ] Implemented
- [ ] Verified
- [ ] Closed

#!/usr/bin/env bash
# After handoff briefs are closed (STATUS: DONE), commit orchestrator + app repo changes.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

# shellcheck source=handoff-lib.sh
source "$(dirname "$0")/handoff-lib.sh"

input=$(cat)
status=$(echo "$input" | jq -r '.status // "completed"')

if [[ "$status" != "completed" ]]; then
  exit 0
fi

# Still open briefs — handoff-stop-check.sh handles follow-up
if [[ -n "$(handoff_pending_tasks)" ]]; then
  exit 0
fi

if ! handoff_all_registered_done; then
  exit 0
fi

mapfile -t tasks < <(handoff_registered_tasks)
subject=$(handoff_build_commit_subject "${tasks[@]}")

commit_body="Handoff closed in this session:
$(printf -- '- %s\n' "${tasks[@]}")"

committed=0

commit_in_repo() {
  local repo_path="$1"
  local add_cmd=("${@:2}")

  [[ -d "$repo_path" ]] || return 0
  [[ -d "$repo_path/.git" ]] || return 0

  (
    cd "$repo_path"
    "${add_cmd[@]}" 2>/dev/null || true
    if git diff --cached --quiet; then
      return 0
    fi
    git commit -m "$subject" -m "$commit_body"
    committed=1
  )
}

# Orchestrator: handoff docs only (avoid accidental png/sql commits)
if [[ -d "$ROOT/.git" ]]; then
  commit_in_repo "$ROOT" git add handoff/
fi

# Application repo under apps/* (tracked files only)
app_repo=$(handoff_find_app_repo || true)
if [[ -n "$app_repo" ]]; then
  commit_in_repo "$app_repo" git add -u
fi

if [[ "$committed" -eq 1 ]]; then
  handoff_cleanup_state_if_idle
fi

exit 0

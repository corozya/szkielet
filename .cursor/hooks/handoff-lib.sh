#!/usr/bin/env bash
# Shared helpers for handoff closure hooks (sourced, not executed directly).

HANDOFF_STATE_DIR=".cursor/hooks/state"
HANDOFF_ACTIVE_LIST="${HANDOFF_STATE_DIR}/handoff-active.list"

handoff_register() {
  local task="$1"
  [[ -n "$task" ]] || return 0
  mkdir -p "$HANDOFF_STATE_DIR"
  touch "$HANDOFF_ACTIVE_LIST"
  if ! grep -qxF "$task" "$HANDOFF_ACTIVE_LIST" 2>/dev/null; then
    echo "$task" >>"$HANDOFF_ACTIVE_LIST"
  fi
}

handoff_register_from_text() {
  local text="$1"
  [[ -n "$text" ]] || return 0

  local token path base
  while IFS= read -r token; do
    handoff_register "$token"
  done < <(printf '%s' "$text" | grep -oE 'TASK_[0-9]+[a-zA-Z0-9_-]*' || true)

  while IFS= read -r path; do
    base=$(basename "$path" .md)
    handoff_register "$base"
  done < <(printf '%s' "$text" | grep -oE 'handoff/[A-Za-z0-9_.-]+\.md' || true)
}

handoff_brief_is_todo() {
  local task="$1"
  local file="handoff/${task}.md"
  [[ -f "$file" ]] || return 1
  grep -qE 'STATUS:[[:space:]]*TODO' "$file"
}

handoff_brief_is_done() {
  local task="$1"
  local file="handoff/${task}.md"
  [[ -f "$file" ]] || return 1
  grep -qE 'STATUS:[[:space:]]*DONE' "$file"
}

handoff_registered_tasks() {
  [[ -f "$HANDOFF_ACTIVE_LIST" ]] || return 0
  grep -v '^[[:space:]]*$' "$HANDOFF_ACTIVE_LIST" 2>/dev/null || true
}

handoff_all_registered_done() {
  local task
  local any=0
  while IFS= read -r task; do
    [[ -n "$task" ]] || continue
    any=1
    handoff_brief_is_done "$task" || return 1
  done < <(handoff_registered_tasks)
  [[ "$any" -eq 1 ]]
}

handoff_task_commit_scope() {
  local task="$1"
  if [[ "$task" =~ ^TASK_[0-9]+_([^_]+) ]]; then
    printf '%s' "${BASH_REMATCH[1]}"
    return 0
  fi
  printf '%s' "handoff"
}

handoff_task_title() {
  local task="$1"
  local file="handoff/${task}.md"
  [[ -f "$file" ]] || { printf '%s' "$task"; return; }
  local title
  title=$(grep -m1 '^# ' "$file" | sed 's/^# //' || true)
  [[ -n "$title" ]] && printf '%s' "$title" || printf '%s' "$task"
}

handoff_build_commit_subject() {
  local tasks=("$@")
  local first="${tasks[0]}"
  local scope
  scope=$(handoff_task_commit_scope "$first")
  if ((${#tasks[@]} == 1)); then
    printf 'feat(%s): %s' "$scope" "$(handoff_task_title "$first")"
  else
    local names
    names=$(IFS=', '; echo "${tasks[*]}")
    printf 'feat(%s): close handoff tasks %s' "$scope" "$names"
  fi
}

handoff_find_app_repo() {
  local d
  for d in apps/*/; do
    [[ -d "${d}.git" ]] || continue
    (cd "$d" && pwd)
    return 0
  done
  return 1
}

handoff_pending_tasks() {
  [[ -f "$HANDOFF_ACTIVE_LIST" ]] || return 0
  local task
  while IFS= read -r task; do
    [[ -n "$task" ]] || continue
    if handoff_brief_is_todo "$task"; then
      printf '%s\n' "$task"
    fi
  done <"$HANDOFF_ACTIVE_LIST"
}

handoff_cleanup_state_if_idle() {
  [[ -f "$HANDOFF_ACTIVE_LIST" ]] || return 0
  if [[ -z "$(handoff_pending_tasks)" ]]; then
    rm -f "$HANDOFF_ACTIVE_LIST"
  fi
}

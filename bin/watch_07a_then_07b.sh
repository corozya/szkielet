#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

FILE_07A="${ROOT_DIR}/handoff/07a_BETA_SUPERADMIN_BACKEND.md"
FILE_07B="${ROOT_DIR}/handoff/07b_BETA_PANEL_UI.md"

INTERVAL_SECONDS="${INTERVAL_SECONDS:-10}"

status_value() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    return 1
  fi

  rg --no-heading --line-number '^\*\*Status:\*\*' "$file" \
    | head -n 1 \
    | sed -E 's/^.*\*\*Status:\*\* *//'
}

is_done_status() {
  local status="$1"
  local normalized
  normalized="$(printf '%s' "$status" | tr '[:upper:]' '[:lower:]')"

  [[ "$normalized" == done* ]] || [[ "$normalized" == completed* ]] || [[ "$normalized" == ukończone* ]]
}

print_snapshot() {
  local status_07a status_07b
  status_07a="$(status_value "$FILE_07A" 2>/dev/null || true)"
  status_07b="$(status_value "$FILE_07B" 2>/dev/null || true)"

  printf '[%s] 07a=%s | 07b=%s\n' "$(date '+%F %T')" "${status_07a:-<missing>}" "${status_07b:-<missing>}"
}

echo "Watching handoff for 07a completion; will notify to start 07b."
echo "Files:"
echo "- $FILE_07A"
echo "- $FILE_07B"
echo "Interval: ${INTERVAL_SECONDS}s (override via INTERVAL_SECONDS=...)"
echo

print_snapshot

while true; do
  if [[ ! -f "$FILE_07A" ]]; then
    echo
    echo "07a file is missing; treating as completed/closed."
    echo "Start 07b: review ${FILE_07B} and begin implementation."
    exit 0
  fi

  status_07a="$(status_value "$FILE_07A" 2>/dev/null || true)"
  if [[ -n "$status_07a" ]] && is_done_status "$status_07a"; then
    echo
    echo "07a status is '$status_07a' -> OK to start 07b."
    echo "Start 07b: review ${FILE_07B} and begin implementation."
    exit 0
  fi

  sleep "$INTERVAL_SECONDS"
done

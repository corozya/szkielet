#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

# shellcheck source=handoff-lib.sh
source "$(dirname "$0")/handoff-lib.sh"

input=$(cat)
prompt=$(echo "$input" | jq -r '.prompt // empty')

if printf '%s' "$prompt" | grep -qiE 'handoff/|TASK_[0-9]+'; then
  handoff_register_from_text "$prompt"
fi

echo '{"continue":true}'

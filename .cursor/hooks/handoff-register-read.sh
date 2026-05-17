#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

# shellcheck source=handoff-lib.sh
source "$(dirname "$0")/handoff-lib.sh"

input=$(cat)
file_path=$(echo "$input" | jq -r '.file_path // empty')

if [[ "$file_path" =~ /handoff/([A-Za-z0-9_.-]+)\.md$ ]]; then
  handoff_register "${BASH_REMATCH[1]}"
fi

echo '{"permission":"allow"}'

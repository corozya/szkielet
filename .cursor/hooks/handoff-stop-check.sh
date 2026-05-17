#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

# shellcheck source=handoff-lib.sh
source "$(dirname "$0")/handoff-lib.sh"

input=$(cat)
status=$(echo "$input" | jq -r '.status // "completed"')
loop_count=$(echo "$input" | jq -r '.loop_count // 0')

if [[ "$status" != "completed" ]]; then
  exit 0
fi

pending=$(handoff_pending_tasks)
if [[ -z "$pending" ]]; then
  handoff_cleanup_state_if_idle
  exit 0
fi

if [[ "$loop_count" -ge 3 ]]; then
  exit 0
fi

list=$(printf '%s\n' "$pending" | sed 's/^/- `/' | sed 's/$/.md`/' | paste -sd '\n' -)

msg=$(cat <<EOF
Zamknij zadania handoff z tej sesji (zasady: \`docs/teams/COMMON.md\`, stan: \`handoff/README.md\`):
1. W każdym briefie: \`<!-- STATUS: DONE -->\` oraz \`state: done\` w sekcji Status.
2. Zaktualizuj \`handoff/README.md\` (Aktywne → Zakończone, data weryfikacji).
3. Jeśli dotyczy — wpis w \`handoff/SPRINT_PLAN.md\`.

Niezamknięte briefy:
${list}
EOF
)

jq -n --arg msg "$msg" '{followup_message: $msg}'

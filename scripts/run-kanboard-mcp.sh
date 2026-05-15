#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
source "${repo_root}/scripts/load-env.sh"

load_env_file "${repo_root}/.env"
load_env_file "${KANBOARD_ENV_FILE:-${repo_root}/kanboard_setup/.env}"

if [[ -z "${KANBOARD_URL:-}" || -z "${KANBOARD_TOKEN:-}" ]]; then
  cat >&2 <<'EOF'
Kanboard MCP wymaga ustawionych KANBOARD_URL i KANBOARD_TOKEN.
Ustaw je w repo-root `.env` albo uruchom: npm run init-kb
EOF
  exit 1
fi

exec python3 "${repo_root}/mcp_servers/kanboard/server.py"

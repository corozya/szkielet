#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
source "${repo_root}/scripts/load-env.sh"

load_env_file "${MYSQL_ENV_FILE:-${repo_root}/.env}"

if [[ -z "${MYSQL_HOST:-}" || -z "${MYSQL_USER:-}" ]]; then
  cat >&2 <<'EOF'
MySQL MCP wymaga ustawionych MYSQL_HOST i MYSQL_USER.
Ustaw je w repo-root `.env`.
EOF
  exit 1
fi

exec python3 "${repo_root}/mcp_servers/mysql/server.py"

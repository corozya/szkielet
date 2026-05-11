#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
env_file="${MYSQL_ENV_FILE:-${repo_root}/.env.mysql}"

if [[ -f "${env_file}" ]]; then
  while IFS= read -r line || [[ -n "${line}" ]]; do
    line="${line%$'\r'}"
    [[ -z "${line}" || "${line}" == \#* || "${line}" != *"="* ]] && continue

    key="${line%%=*}"
    value="${line#*=}"
    key="${key//[[:space:]]/}"
    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"
    value="${value%\"}"
    value="${value#\"}"

    if [[ -z "${!key:-}" ]]; then
      export "${key}=${value}"
    fi
  done < "${env_file}"
fi

if [[ -z "${MYSQL_HOST:-}" || -z "${MYSQL_USER:-}" ]]; then
  cat >&2 <<'EOF'
MySQL MCP wymaga ustawionych MYSQL_HOST i MYSQL_USER.
Skopiuj .env.mysql.example do .env.mysql i uzupełnij dane.
EOF
  exit 1
fi

exec python3 "${repo_root}/mcp_servers/mysql/server.py"

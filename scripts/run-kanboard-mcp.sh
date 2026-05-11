#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
env_file="${KANBOARD_ENV_FILE:-${repo_root}/kanboard_setup/.env}"

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

if [[ -z "${KANBOARD_URL:-}" || -z "${KANBOARD_TOKEN:-}" ]]; then
  cat >&2 <<'EOF'
Kanboard MCP wymaga ustawionych KANBOARD_URL i KANBOARD_TOKEN.
Uruchom: npm run init-kb
EOF
  exit 1
fi

exec python3 "${repo_root}/mcp_servers/kanboard/server.py"

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Używa serwera GSC z repozytorium marketing
gsc_repo="/home/corozya/www/marketing/mcp_servers/gsc"
default_adc="${HOME}/.config/gcloud/application_default_credentials.json"
runtime_root="${TMPDIR:-/tmp}/szkielet-gsc-mcp"

source "${repo_root}/scripts/load-env.sh"

load_env_file "${repo_root}/.env"
load_env_file "${repo_root}/.env.gsc"
load_env_file "${repo_root}/.env.analytics"

if [ ! -d "${gsc_repo}" ]; then
  echo "Missing ${gsc_repo}. Upewnij się że repo marketing jest sklonowane." >&2
  exit 1
fi

if [ -z "${GSC_CREDENTIALS_PATH:-}" ] && [ -z "${GSC_OAUTH_CLIENT_SECRETS_FILE:-}" ]; then
  if [ -f "${default_adc}" ]; then
    export GSC_CREDENTIALS_PATH="${default_adc}"
  fi
fi

if [ -z "${GSC_CREDENTIALS_PATH:-}" ] && [ -z "${GSC_OAUTH_CLIENT_SECRETS_FILE:-}" ]; then
  echo "GSC credentials nie skonfigurowane. Uruchom: gcloud auth application-default login" >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv nie jest dostępny na PATH." >&2
  exit 1
fi

mkdir -p "${runtime_root}/state" "${runtime_root}/cache"
export XDG_STATE_HOME="${XDG_STATE_HOME:-${runtime_root}/state}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-${runtime_root}/cache}"
export UV_CACHE_DIR="${UV_CACHE_DIR:-${runtime_root}/cache/uv}"

exec uv run --directory "${gsc_repo}" python gsc_server.py

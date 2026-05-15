#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
gsc_repo="${repo_root}/mcp_servers/gsc"
default_adc="${HOME}/.config/gcloud/application_default_credentials.json"
runtime_root="${TMPDIR:-/tmp}/codex-gsc-mcp"

source "${repo_root}/scripts/load-env.sh"

if [ ! -d "${gsc_repo}" ]; then
  echo "Missing mcp_servers/gsc. Clone AminForou/mcp-gsc into that path first." >&2
  exit 1
fi

load_env_file "${repo_root}/.env"
load_env_file "${repo_root}/.env.gsc"
load_env_file "${repo_root}/.env.analytics"

if [ -z "${GSC_CREDENTIALS_PATH:-}" ] && [ -z "${GSC_OAUTH_CLIENT_SECRETS_FILE:-}" ]; then
  if [ -n "${GOOGLE_APPLICATION_CREDENTIALS:-}" ] && [ -f "${GOOGLE_APPLICATION_CREDENTIALS}" ]; then
    export GSC_CREDENTIALS_PATH="${GOOGLE_APPLICATION_CREDENTIALS}"
  elif [ -f "${default_adc}" ]; then
    export GSC_CREDENTIALS_PATH="${default_adc}"
  fi
fi

if [ -z "${GSC_CREDENTIALS_PATH:-}" ] && [ -z "${GSC_OAUTH_CLIENT_SECRETS_FILE:-}" ]; then
  echo "GSC credentials are not configured." >&2
  echo "Set them in ${repo_root}/.env or create ${repo_root}/.env.gsc from .env.gsc.example." >&2
  echo "If you use gcloud ADC, run: gcloud auth application-default login" >&2
  exit 1
fi

if [ -n "${GSC_CREDENTIALS_PATH:-}" ] && [ ! -f "${GSC_CREDENTIALS_PATH}" ]; then
  echo "GSC_CREDENTIALS_PATH points to a missing file: ${GSC_CREDENTIALS_PATH}" >&2
  exit 1
fi

if [ -n "${GSC_OAUTH_CLIENT_SECRETS_FILE:-}" ] && [ ! -f "${GSC_OAUTH_CLIENT_SECRETS_FILE}" ]; then
  echo "GSC_OAUTH_CLIENT_SECRETS_FILE points to a missing file: ${GSC_OAUTH_CLIENT_SECRETS_FILE}" >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not available on PATH." >&2
  exit 1
fi

if [ -n "${GSC_CREDENTIALS_PATH:-}" ] && [ -z "${GSC_OAUTH_CLIENT_SECRETS_FILE:-}" ]; then
  export GSC_SKIP_OAUTH="${GSC_SKIP_OAUTH:-true}"
fi

mkdir -p "${runtime_root}/state" "${runtime_root}/cache"
export XDG_STATE_HOME="${XDG_STATE_HOME:-${runtime_root}/state}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-${runtime_root}/cache}"
export UV_CACHE_DIR="${UV_CACHE_DIR:-${runtime_root}/cache/uv}"

exec uv run --directory "${gsc_repo}" python gsc_server.py

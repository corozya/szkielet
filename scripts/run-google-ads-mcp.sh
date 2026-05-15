#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
analytics_env="${repo_root}/.env.analytics"
google_ads_env="${repo_root}/.env.google-ads"
default_adc="${HOME}/.config/gcloud/application_default_credentials.json"
runtime_root="${HOME}/.cache/codex-google-ads-mcp"

source "${repo_root}/scripts/load-env.sh"

load_env_file "${repo_root}/.env"
load_env_file "${analytics_env}"
load_env_file "${google_ads_env}"

if [ -z "${GOOGLE_APPLICATION_CREDENTIALS:-}" ] && [ -f "${default_adc}" ]; then
  export GOOGLE_APPLICATION_CREDENTIALS="${default_adc}"
fi

if [ -z "${GOOGLE_PROJECT_ID:-}" ] && [ -n "${GOOGLE_CLOUD_PROJECT:-}" ]; then
  export GOOGLE_PROJECT_ID="${GOOGLE_CLOUD_PROJECT}"
fi

if [ -z "${GOOGLE_PROJECT_ID:-}" ] && command -v gcloud >/dev/null 2>&1; then
  google_project_id="$(gcloud config get-value project 2>/dev/null || true)"
  if [ -n "${google_project_id}" ] && [ "${google_project_id}" != "(unset)" ]; then
    export GOOGLE_PROJECT_ID="${google_project_id}"
  fi
fi

if [ -z "${GOOGLE_APPLICATION_CREDENTIALS:-}" ]; then
  echo "GOOGLE_APPLICATION_CREDENTIALS is not set and ${default_adc} does not exist." >&2
  echo "Set it in ${repo_root}/.env or create ${repo_root}/.env.analytics from .env.analytics.example." >&2
  echo "You can also run: gcloud auth application-default login" >&2
  exit 1
fi

if [ ! -f "${GOOGLE_APPLICATION_CREDENTIALS}" ]; then
  echo "GOOGLE_APPLICATION_CREDENTIALS points to a missing file: ${GOOGLE_APPLICATION_CREDENTIALS}" >&2
  exit 1
fi

if [ -z "${GOOGLE_PROJECT_ID:-}" ]; then
  echo "GOOGLE_PROJECT_ID is not set." >&2
  echo "Set it in ${repo_root}/.env or ${repo_root}/.env.analytics, or export it in your shell." >&2
  exit 1
fi

if [ -z "${GOOGLE_ADS_DEVELOPER_TOKEN:-}" ]; then
  echo "GOOGLE_ADS_DEVELOPER_TOKEN is not set." >&2
  echo "Set it in ${repo_root}/.env or create ${repo_root}/.env.google-ads from .env.google-ads.example." >&2
  exit 1
fi

export GOOGLE_CLOUD_PROJECT="${GOOGLE_PROJECT_ID}"

# Keep pipx state in a writable location even when $HOME is read-only in the MCP sandbox.
mkdir -p "${runtime_root}/state" "${runtime_root}/cache"
export XDG_STATE_HOME="${XDG_STATE_HOME:-${runtime_root}/state}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-${runtime_root}/cache}"

exec pipx run --spec git+https://github.com/googleads/google-ads-mcp.git google-ads-mcp

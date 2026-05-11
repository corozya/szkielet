#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
env_file="${repo_root}/.env.analytics"
default_adc="${HOME}/.config/gcloud/application_default_credentials.json"

if [ -f "${env_file}" ]; then
  set -a
  # Local, untracked secrets/config for Analytics MCP.
  . "${env_file}"
  set +a
fi

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
  echo "Create ${repo_root}/.env.analytics from .env.analytics.example or run: gcloud auth application-default login" >&2
  exit 1
fi

if [ ! -f "${GOOGLE_APPLICATION_CREDENTIALS}" ]; then
  echo "GOOGLE_APPLICATION_CREDENTIALS points to a missing file: ${GOOGLE_APPLICATION_CREDENTIALS}" >&2
  exit 1
fi

if [ -z "${GOOGLE_PROJECT_ID:-}" ]; then
  echo "GOOGLE_PROJECT_ID is not set." >&2
  echo "Set it in ${repo_root}/.env.analytics or your shell environment." >&2
  exit 1
fi

export GOOGLE_CLOUD_PROJECT="${GOOGLE_PROJECT_ID}"

if ! command -v analytics-mcp >/dev/null 2>&1; then
  echo "analytics-mcp is not available on PATH." >&2
  echo "Install it before starting Codex, then retry." >&2
  echo "If you are cloning this repo fresh, also check ${repo_root}/README.md -> Analytics MCP." >&2
  exit 1
fi

if [ -n "${GA4_PROPERTY_ID:-}" ]; then
  exec python3 "${repo_root}/scripts/run-google-analytics-mcp-default-property.py"
fi

exec analytics-mcp

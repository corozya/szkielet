#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
analytics_env="${repo_root}/.env.analytics"
google_ads_env="${repo_root}/.env.google-ads"
default_adc="${HOME}/.config/gcloud/application_default_credentials.json"

if [ -f "${analytics_env}" ]; then
  set -a
  . "${analytics_env}"
  set +a
fi

if [ -f "${google_ads_env}" ]; then
  set -a
  . "${google_ads_env}"
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

if [ -z "${GOOGLE_ADS_DEVELOPER_TOKEN:-}" ]; then
  echo "GOOGLE_ADS_DEVELOPER_TOKEN is not set." >&2
  echo "Create ${repo_root}/.env.google-ads from .env.google-ads.example or export it in your shell." >&2
  exit 1
fi

export GOOGLE_CLOUD_PROJECT="${GOOGLE_PROJECT_ID}"

exec pipx run --spec git+https://github.com/googleads/google-ads-mcp.git google-ads-mcp

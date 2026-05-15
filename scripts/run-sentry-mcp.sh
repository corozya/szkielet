#!/bin/bash
# Script to run Sentry MCP server with auth token from environment.
# Upstream Sentry MCP expects SENTRY_ACCESS_TOKEN; keep SENTRY_AUTH_TOKEN as a local alias.
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

source "${repo_root}/scripts/load-env.sh"

# Local, untracked secrets/config for Sentry MCP.
load_env_file "${repo_root}/.env"

if [ -z "${SENTRY_AUTH_TOKEN:-}" ] && [ -z "${SENTRY_ACCESS_TOKEN:-}" ]; then
  echo "SENTRY_AUTH_TOKEN or SENTRY_ACCESS_TOKEN is required" >&2
  exit 1
fi

if [ -z "${SENTRY_ACCESS_TOKEN:-}" ] && [ -n "${SENTRY_AUTH_TOKEN:-}" ]; then
  export SENTRY_ACCESS_TOKEN="${SENTRY_AUTH_TOKEN}"
fi

if [ -z "${EMBEDDED_AGENT_PROVIDER:-}" ]; then
  if [ -n "${OPENAI_API_KEY:-}" ]; then
    export EMBEDDED_AGENT_PROVIDER="openai"
  elif [ -n "${ANTHROPIC_API_KEY:-}" ]; then
    export EMBEDDED_AGENT_PROVIDER="anthropic"
  fi
fi

npx -y @sentry/mcp-server

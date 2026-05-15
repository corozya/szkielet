#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

source "${repo_root}/scripts/load-env.sh"
load_env_file "${repo_root}/.env"

exec uv \
  --directory "${repo_root}/mcp_servers/facebook" \
  run facebook-mcp-server

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

source "${repo_root}/scripts/load-env.sh"
load_env_file "${repo_root}/.env"

if [[ -z "${MS_CLARITY:-}" ]]; then
  echo "MS_CLARITY is not set. Set it in ${repo_root}/.env." >&2
  exit 1
fi

# Oficjalny serwer MCP — bez globalnej instalacji (`npm i -g`).
# Dokumentacja: https://github.com/microsoft/clarity-mcp-server
exec npx -y @microsoft/clarity-mcp-server --clarity_api_token="${MS_CLARITY}"

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

source "${repo_root}/scripts/load-env.sh"
load_env_file "${repo_root}/.env"

if [[ -z "${MS_CLARITY:-}" ]]; then
  echo "MS_CLARITY is not set. Set it in ${repo_root}/.env." >&2
  exit 1
fi

export CLARITY_API_TOKEN="${MS_CLARITY}"

exec clarity-mcp-server

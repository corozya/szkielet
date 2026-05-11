#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
memory_file="${MEMORY_FILE_PATH:-${repo_root}/.memory/memory.jsonl}"

mkdir -p "$(dirname "${memory_file}")"
export MEMORY_FILE_PATH="${memory_file}"

exec npx -y @modelcontextprotocol/server-memory

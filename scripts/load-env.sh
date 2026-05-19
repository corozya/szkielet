#!/usr/bin/env bash

# Shared dotenv loader for local MCP wrapper scripts.
# Shell variables already set in the parent environment keep precedence.
__load_env_preexisting_names="$(env | cut -d= -f1)"

__load_env_is_preexisting() {
  local name="${1:-}"

  case $'\n'"${__load_env_preexisting_names}"$'\n' in
    *$'\n'"${name}"$'\n'*) return 0 ;;
  esac

  return 1
}

load_env_file() {
  local env_file="${1:-}"

  if [[ -z "${env_file}" || ! -f "${env_file}" ]]; then
    return 0
  fi

  while IFS= read -r line || [[ -n "${line}" ]]; do
    line="${line%$'\r'}"
    [[ -z "${line}" || "${line}" == \#* || "${line}" != *"="* ]] && continue

    local key="${line%%=*}"
    local value="${line#*=}"

    key="${key//[[:space:]]/}"
    value="${value#"${value%%[![:space:]]*}"}"
    value="${value%"${value##*[![:space:]]}"}"
    value="${value%\"}"
    value="${value#\"}"

    if __load_env_is_preexisting "${key}"; then
      continue
    fi

    export "${key}=${value}"
  done < "${env_file}"
}

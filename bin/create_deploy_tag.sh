#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  bin/create_deploy_tag.sh beta [<tag>] [--no-push]
  bin/create_deploy_tag.sh prod [<tag>] [--no-push]
  bin/create_deploy_tag.sh <beta-*> [--no-push]
  bin/create_deploy_tag.sh <prod-*> [--no-push]

Defaults:
  - If <tag> is omitted for beta/prod, a tag is generated:
      beta-YYYYMMDD-HHMM
      prod-YYYYMMDD-HHMM

Rules:
  - Creating a `prod-*` tag requires that the current commit (HEAD) already has a `beta-*` tag.
  - By default the script pushes the tag to `origin` (so CI can deploy).
USAGE
}

NO_PUSH=0
ARGS=()
for arg in "$@"; do
  case "$arg" in
    --no-push) NO_PUSH=1 ;;
    -h|--help) usage; exit 0 ;;
    *) ARGS+=("$arg") ;;
  esac
done

if [ "${#ARGS[@]}" -lt 1 ]; then
  usage
  exit 2
fi

kind="${ARGS[0]}"
tag="${ARGS[1]:-}"

if [[ "$kind" == beta-* || "$kind" == prod-* ]]; then
  tag="$kind"
  kind="${tag%%-*}"
fi

if [ -z "$tag" ]; then
  stamp="$(date +%Y%m%d-%H%M)"
  tag="${kind}-${stamp}"
fi

if [[ "$tag" != beta-* && "$tag" != prod-* ]]; then
  echo "❌ Tag must start with beta- or prod- (got: $tag)"
  exit 2
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "❌ Working tree not clean. Commit/stash before tagging."
  exit 1
fi

if [[ "$tag" == prod-* ]]; then
  if ! git tag --points-at HEAD "beta-*" | grep -q .; then
    echo "❌ Refusing to create $tag: HEAD has no beta-* tag. Tag beta first (staging), then promote to prod."
    exit 1
  fi
fi

if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
  echo "❌ Tag already exists: $tag"
  exit 1
fi

msg="Deploy ${tag} ($(date -Iseconds))"
git tag -a "$tag" -m "$msg"
echo "✅ Created tag: $tag"

if [ "$NO_PUSH" = "1" ]; then
  echo "ℹ️  Not pushing tag (--no-push)."
  exit 0
fi

git push origin "$tag"
echo "🚀 Pushed tag to origin: $tag"

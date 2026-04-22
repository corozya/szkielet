#!/bin/bash

# 🛡️ LOCAL_AUDITOR - Automated Code Audit via Qwen2.5
# Runs on pre-commit or manually

set -e

OLLAMA_URL="http://localhost:11434"
# Model selection:
# - If LOCAL_AUDITOR_MODEL includes a tag (e.g. qwen2.5-coder:1.5b) -> use exact.
# - If it's untagged (e.g. qwen2.5-coder) -> prefer :1.5b if present, otherwise first matching tag.
BASE_MODEL="${LOCAL_AUDITOR_MODEL:-qwen2.5-coder}"
MODEL="$BASE_MODEL"
AUDIT_FILE="handoff/AUDIT_RESULT.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Curl timeouts (seconds) to avoid hanging in restricted environments.
# Override via env if needed.
CURL_CONNECT_TIMEOUT="${CURL_CONNECT_TIMEOUT:-1}"
CURL_MAX_TIME_TAGS="${CURL_MAX_TIME_TAGS:-2}"
CURL_MAX_TIME_GENERATE="${CURL_MAX_TIME_GENERATE:-180}"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "🛡️  Starting LOCAL_AUDITOR..."

# 1. Check Ollama availability
if ! command -v curl >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  curl not found${NC}"
    echo "   Audit skipped."
    exit 0
fi

if ! command -v jq >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  jq not found${NC}"
    echo "   Audit skipped."
    exit 0
fi

TAGS_JSON="$(curl -fsS --connect-timeout "$CURL_CONNECT_TIMEOUT" --max-time "$CURL_MAX_TIME_TAGS" \
    "$OLLAMA_URL/api/tags" 2>/dev/null || true)"

if [ -z "$TAGS_JSON" ] || ! echo "$TAGS_JSON" | jq -e '.models' >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Ollama not available at $OLLAMA_URL${NC}"
    echo "   Audit skipped. Ensure Ollama is running: ollama serve"
    echo "   If you are running inside a sandbox with networking disabled, run the commit outside the sandbox or allow network access."
    exit 0
fi

if [[ "$BASE_MODEL" != *:* ]]; then
    # Prefer small CPU-friendly tag if available.
    if echo "$TAGS_JSON" | jq -e --arg m "${BASE_MODEL}:1.5b" '.models[]?.name == $m' >/dev/null 2>&1; then
        MODEL="${BASE_MODEL}:1.5b"
    else
        MODEL="$(echo "$TAGS_JSON" | jq -r --arg base "${BASE_MODEL}:" '.models[]?.name | select(startswith($base))' | head -n 1)"
    fi

    if [ -z "$MODEL" ]; then
        echo -e "${YELLOW}⚠️  Ollama is running but model $BASE_MODEL is not available${NC}"
        echo "   Audit skipped. Pull the model: ollama pull $BASE_MODEL"
        exit 0
    fi
else
    if ! echo "$TAGS_JSON" | jq -e --arg model "$MODEL" '.models[]?.name == $model' >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Ollama is running but model $MODEL is not available${NC}"
        echo "   Audit skipped. Pull the model: ollama pull ${MODEL%%:*}"
        exit 0
    fi
fi

# 2. Get staged diff
DIFF=$(git diff --cached --no-color)

if [ -z "$DIFF" ]; then
    echo "📋 No staged changes to audit"
    exit 0
fi

echo "📤 Sending diff to $MODEL..."

# 3. Send to Qwen2.5
PROMPT="You are a code security and quality auditor. Review the following git diff and identify:
1. Security vulnerabilities
2. Logic errors
3. Performance issues
4. Code quality problems

Be concise. List only critical/important issues.
At the end, output exactly one line in the form: AUDIT_STATUS: OK|ISSUES|CRITICAL

---
DIFF:
$DIFF
---

Provide your findings in markdown format."

# Build JSON safely with jq
JSON=$(jq -n \
  --arg model "$MODEL" \
  --arg prompt "$PROMPT" \
  '{model: $model, prompt: $prompt, stream: false}')

RAW_WITH_STATUS="$(curl -sS -X POST "$OLLAMA_URL/api/generate" \
  -H "Content-Type: application/json" \
  --connect-timeout "$CURL_CONNECT_TIMEOUT" --max-time "$CURL_MAX_TIME_GENERATE" \
  -d "$JSON" -w "\n__HTTP_STATUS__%{http_code}" 2>/dev/null || true)"

HTTP_STATUS="${RAW_WITH_STATUS##*__HTTP_STATUS__}"
RAW="${RAW_WITH_STATUS%__HTTP_STATUS__*}"

RESPONSE="$(echo "$RAW" | jq -r '.response // empty' 2>/dev/null || echo "")"
OLLAMA_ERROR="$(echo "$RAW" | jq -r '.error // empty' 2>/dev/null || echo "")"

if [ -z "$RESPONSE" ]; then
    echo -e "${YELLOW}⚠️  Failed to get response from $MODEL${NC}"
    if [ -n "$OLLAMA_ERROR" ]; then
        echo "   Ollama error: $OLLAMA_ERROR"
    elif [ -n "$HTTP_STATUS" ] && [ "$HTTP_STATUS" != "200" ]; then
        echo "   HTTP status: $HTTP_STATUS"
    else
        echo "   No response payload (timeout or invalid JSON)."
    fi
    echo "   Audit skipped."
    exit 0
fi

# 4. Save result
mkdir -p handoff
AUDIT_STATUS="$(echo "$RESPONSE" | grep -E '^AUDIT_STATUS:\s*(OK|ISSUES|CRITICAL)\s*$' | tail -n 1 | sed 's/^[^:]*:[[:space:]]*//')"
if [ -z "$AUDIT_STATUS" ]; then
    AUDIT_STATUS="ISSUES"
fi

cat > "$AUDIT_FILE" << EOF
# 🛡️ Audit Result - LOCAL_AUDITOR

**Date:** $TIMESTAMP
**Model:** $MODEL
**Diff Lines:** $(echo "$DIFF" | wc -l)

---

## Findings

$RESPONSE

---

**Status:** $AUDIT_STATUS
EOF

echo "✅ Audit complete. Results saved to $AUDIT_FILE"

# 5. Exit with warning if critical issues found
if [ "$AUDIT_STATUS" = "CRITICAL" ]; then
    echo -e "${RED}⚠️  Critical issues detected. Review $AUDIT_FILE before committing.${NC}"
    exit 1
fi

exit 0

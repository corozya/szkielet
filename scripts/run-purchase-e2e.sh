#!/usr/bin/env bash
# Uruchamia test E2E pełnego procesu zakupowego (purchase-flow.spec.js).
# Aktywuje produkt testowy przez SQL, przechodzi przez kreator → checkout → PayU,
# weryfikuje zamówienie w bazie, a na koniec deaktywuje produkt.
#
# Użycie:
#   ./scripts/run-purchase-e2e.sh [--headed] [--debug]
#
# Zmienne środowiskowe (można też ustawić w .env.e2e obok tego skryptu):
#   E2E_BASE_URL          URL środowiska (domyślnie: https://reczniki-haftowane.pl)
#   TEST_PRODUCT_ID       ID produktu testowego w bazie (wymagane)
#   TEST_PRODUCT_SLUG     Slug produktu testowego (wymagane)
#   RECAPTCHA_BYPASS_TOKEN  Token bypass z backendu .env (wymagane)
#   E2E_DB_HOST / PORT / USER / PASSWORD / NAME  Dane MySQL
#   BETA_AUTH_USER / BETA_AUTH_PASSWORD           Basic auth (jeśli potrzebne)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
FRONTEND_DIR="${REPO_ROOT}/apps/reczniki-haftowane/frontend"

# ── Kolory ────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
info()    { echo -e "${CYAN}[E2E]${NC} $*"; }
success() { echo -e "${GREEN}[OK]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
error()   { echo -e "${RED}[ERR]${NC}  $*" >&2; }

# ── Wczytaj .env.e2e jeśli istnieje ──────────────────────────
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/load-env.sh"
load_env_file "${SCRIPT_DIR}/../.env.e2e"
load_env_file "${FRONTEND_DIR}/.env.local"

# ── Opcje CLI ─────────────────────────────────────────────────
HEADED=""
DEBUG_FLAG=""
for arg in "$@"; do
  case "$arg" in
    --headed) HEADED="--headed" ;;
    --debug)  DEBUG_FLAG="--debug" ;;
  esac
done

# ── Wartości domyślne ─────────────────────────────────────────
export E2E_BASE_URL="${E2E_BASE_URL:-https://reczniki-haftowane.pl}"
export E2E_DB_HOST="${E2E_DB_HOST:-127.0.0.1}"
export E2E_DB_PORT="${E2E_DB_PORT:-3306}"
export E2E_DB_NAME="${E2E_DB_NAME:-reczniki}"
export INCLUDE_PURCHASE_E2E=1

# ── Walidacja wymaganych zmiennych ────────────────────────────
MISSING=0
for var in TEST_PRODUCT_ID TEST_PRODUCT_SLUG RECAPTCHA_BYPASS_TOKEN E2E_DB_USER E2E_DB_PASSWORD; do
  if [[ -z "${!var:-}" ]]; then
    error "Brak zmiennej: ${var}"
    MISSING=1
  fi
done

if [[ $MISSING -eq 1 ]]; then
  echo ""
  echo "  Ustaw brakujące zmienne w pliku .env.e2e (obok scripts/) lub eksportuj je:"
  echo ""
  echo "    TEST_PRODUCT_ID=<id>"
  echo "    TEST_PRODUCT_SLUG=<slug>"
  echo "    RECAPTCHA_BYPASS_TOKEN=<token z backendu .env>"
  echo "    E2E_DB_USER=<user>"
  echo "    E2E_DB_PASSWORD=<hasło>"
  echo "    E2E_DB_HOST=<host>  (domyślnie: 127.0.0.1)"
  echo "    E2E_DB_NAME=<baza>  (domyślnie: reczniki)"
  echo ""
  exit 1
fi

# ── Info startowe ─────────────────────────────────────────────
echo ""
info "=== Purchase E2E Test ==="
info "Środowisko : ${E2E_BASE_URL}"
info "Produkt    : ID=${TEST_PRODUCT_ID}  slug=${TEST_PRODUCT_SLUG}"
info "Baza       : ${E2E_DB_USER}@${E2E_DB_HOST}:${E2E_DB_PORT}/${E2E_DB_NAME}"
[[ -n "$HEADED" ]] && info "Tryb       : headed (widoczna przeglądarka)"
echo ""

# ── Uruchom Playwright ────────────────────────────────────────
cd "${FRONTEND_DIR}"

set +e
npx playwright test purchase-flow \
  --project=chromium \
  --reporter=list \
  ${HEADED} \
  ${DEBUG_FLAG}
EXIT_CODE=$?
set -e

echo ""
if [[ $EXIT_CODE -eq 0 ]]; then
  success "Test zakończony sukcesem."
else
  error "Test nie przeszedł (kod wyjścia: ${EXIT_CODE})."
  info  "Trace: ${FRONTEND_DIR}/playwright-results/"
  info  "Aby otworzyć trace: npx playwright show-trace playwright-results/*/trace.zip"
fi

exit $EXIT_CODE

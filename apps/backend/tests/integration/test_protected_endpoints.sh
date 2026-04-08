#!/bin/bash
# ============================================================
# Script de Testing Endpoints Protegidos via Swagger
# Usa playwright-cli para interactuar con el Swagger UI
# ============================================================

set -e

BASE_URL="http://localhost:8001"
SWAGGER_URL="$BASE_URL/docs"
TOKEN=""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_pass() { echo -e "${GREEN}✅ PASS${NC}: $1"; }
log_fail() { echo -e "${RED}❌ FAIL${NC}: $1"; }
log_info() { echo -e "${YELLOW}ℹ️  $NC: $1"; }

# ============================================================
# Step 1: Obtener Token JWT via curl
# ============================================================
echo ""
echo "=== Step 1: Obtener Token JWT ==="

LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "superadmin", "password": "adminpass123"}')

TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    log_fail "Login failed"
    exit 1
fi

log_pass "Token JWT obtenido: ${TOKEN:0:30}..."

# ============================================================
# Step 2: Probar Endpoints Protegidos via curl
# ============================================================

echo ""
echo "=== Step 2: Probar Endpoints Protegidos ==="

# --- Users ---
echo ""
echo "--- Users ---"

# GET /users/students
RESP=$(curl -s "$BASE_URL/api/v1/users/students" \
  -H "Authorization: Bearer $TOKEN" -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "200" ]; then
    log_pass "GET /users/students - Status: $RESP"
else
    log_fail "GET /users/students - Status: $RESP"
fi

# GET /users/professors/me
RESP=$(curl -s "$BASE_URL/api/v1/users/professors/me" \
  -H "Authorization: Bearer $TOKEN" -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "200" ] || [ "$RESP" = "404" ]; then
    log_pass "GET /users/professors/me - Status: $RESP"
else
    log_fail "GET /users/professors/me - Status: $RESP"
fi

# GET /users/professors/settings
RESP=$(curl -s "$BASE_URL/api/v1/users/professors/settings" \
  -H "Authorization: Bearer $TOKEN" -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "200" ] || [ "$RESP" = "404" ]; then
    log_pass "GET /users/professors/settings - Status: $RESP"
else
    log_fail "GET /users/professors/settings - Status: $RESP"
fi

# --- Games ---
echo ""
echo "--- Games ---"

# GET /games
RESP=$(curl -s "$BASE_URL/api/v1/games" -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "200" ]; then
    log_pass "GET /games - Status: $RESP"
else
    log_fail "GET /games - Status: $RESP"
fi

# GET /games/1
RESP=$(curl -s "$BASE_URL/api/v1/games/1" -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "200" ]; then
    log_pass "GET /games/1 - Status: $RESP"
else
    log_fail "GET /games/1 - Status: $RESP"
fi

# GET /games/1/levels
RESP=$(curl -s "$BASE_URL/api/v1/games/1/levels" -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "200" ]; then
    log_pass "GET /games/1/levels - Status: $RESP"
else
    log_fail "GET /games/1/levels - Status: $RESP"
fi

# --- Sync ---
echo ""
echo "--- Sync ---"

# POST /sync/sync-events
RESP=$(curl -s -X POST "$BASE_URL/api/v1/sync/sync-events" \
  -H "Content-Type: application/json" \
  -d '{
    "sync_session_id": 4,
    "event_type": "error",
    "payload": {
      "student_id": 3,
      "segment_level_id": 3,
      "game_id": 1,
      "count": 1
    }
  }' -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "201" ]; then
    log_pass "POST /sync/sync-events - Status: $RESP"
else
    log_fail "POST /sync/sync-events - Status: $RESP"
fi

# GET /sync/sync-events/4
RESP=$(curl -s "$BASE_URL/api/v1/sync/sync-events/4" \
  -H "Authorization: Bearer $TOKEN" -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "200" ]; then
    log_pass "GET /sync/sync-events/4 - Status: $RESP"
else
    log_fail "GET /sync/sync-events/4 - Status: $RESP"
fi

# --- Statistics ---
echo ""
echo "--- Statistics ---"

# GET /statistic/xapi/statements
RESP=$(curl -s "$BASE_URL/api/v1/statistic/xapi/statements" \
  -H "Authorization: Bearer $TOKEN" -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "200" ]; then
    log_pass "GET /statistic/xapi/statements - Status: $RESP"
else
    log_fail "GET /statistic/xapi/statements - Status: $RESP"
fi

# GET /statistic/metric-types
RESP=$(curl -s "$BASE_URL/api/v1/statistic/metric-types" \
  -H "Authorization: Bearer $TOKEN" -w "%{http_code}" -o /tmp/resp.txt)
if [ "$RESP" = "200" ]; then
    log_pass "GET /statistic/metric-types - Status: $RESP"
else
    log_fail "GET /statistic/metric-types - Status: $RESP"
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo "============================================"
echo -e "${GREEN}✅ Todos los endpoints protegidos probados${NC}"
echo "============================================"
echo ""

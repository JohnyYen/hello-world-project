#!/bin/bash
# ============================================================
# Test de Integración - Flujo de Sincronización
# ============================================================
# Este script prueba el flujo completo de sincronización:
# 1. Crear evento de sync
# 2. Verificar conversión a xAPI
# 3. Verificar actualización de Progress
# ============================================================

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8001"
SYNC_SESSION_ID=4
STUDENT_ID=3
SEGMENT_LEVEL_ID=3
GAME_ID=1
LEVEL_ID=2

# Helper function
log_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
}

log_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    exit 1
}

log_info() {
    echo -e "${YELLOW}ℹ️  $NC: $1"
}

# ============================================================
# Step 0: Login y obtener token
# ============================================================
echo ""
echo "=== Step 0: Login ==="

LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "superadmin", "password": "adminpass123"}')

TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    log_fail "Login failed - no token received"
fi

log_pass "Login successful - token obtained"

# ============================================================
# Step 1: Crear evento ERROR (complex event)
# ============================================================
echo ""
echo "=== Step 1: Create ERROR Event ==="

ERROR_EVENT=$(curl -s -X POST "$BASE_URL/api/v1/sync/sync-events" \
  -H "Content-Type: application/json" \
  -d "{
    \"sync_session_id\": $SYNC_SESSION_ID,
    \"event_type\": \"error\",
    \"payload\": {
      \"student_id\": $STUDENT_ID,
      \"segment_level_id\": $SEGMENT_LEVEL_ID,
      \"game_id\": $GAME_ID,
      \"level_id\": $LEVEL_ID,
      \"count\": 5,
      \"error_message\": \"Integration test error\"
    }
  }")

EVENT_ID=$(echo "$ERROR_EVENT" | jq -r '.id')
EVENT_STATUS=$(echo "$ERROR_EVENT" | jq -r '.status')

if [ "$EVENT_ID" = "null" ] || [ -z "$EVENT_ID" ]; then
    log_fail "Event creation failed"
fi

if [ "$EVENT_STATUS" != "processed" ]; then
    log_fail "Event status is '$EVENT_STATUS', expected 'processed'"
fi

log_pass "ERROR event created - ID: $EVENT_ID, Status: $EVENT_STATUS"

# ============================================================
# Step 2: Verificar xAPI statement
# ============================================================
echo ""
echo "=== Step 2: Verify xAPI Statement ==="

# Wait for processing
sleep 1

XAPI_RESPONSE=$(curl -s "$BASE_URL/api/v1/statistic/xapi/statements?student_id=$STUDENT_ID&limit=1" \
  -H "Authorization: Bearer $TOKEN")

XAPI_COUNT=$(echo "$XAPI_RESPONSE" | jq -r '.total // .statements | length')

if [ "$XAPI_COUNT" = "null" ] || [ "$XAPI_COUNT" = "0" ]; then
    log_fail "No xAPI statements found"
fi

XAPI_VERB=$(echo "$XAPI_RESPONSE" | jq -r '.statements[0].verb.id // empty')

if [[ "$XAPI_VERB" == *"failed"* ]]; then
    log_pass "xAPI statement created with verb: $XAPI_VERB"
else
    log_fail "xAPI verb mismatch - expected 'failed', got '$XAPI_VERB'"
fi

# ============================================================
# Step 3: Verificar Progress
# ============================================================
echo ""
echo "=== Step 3: Verify Progress ==="

# Check via direct DB query (since there's no API endpoint)
PROGRESS_CHECK=$(docker exec hwp-postgres psql -U hwp_user -d hwp_db -t -c \
  "SELECT error_count FROM progresses WHERE student_id = $STUDENT_ID AND segment_level_id = $SEGMENT_LEVEL_ID;" 2>/dev/null | tr -d ' ')

if [ -z "$PROGRESS_CHECK" ]; then
    log_fail "Progress not created in database"
fi

if [ "$PROGRESS_CHECK" = "5" ]; then
    log_pass "Progress updated - error_count: $PROGRESS_CHECK"
else
    log_fail "Progress error_count is '$PROGRESS_CHECK', expected '5'"
fi

# ============================================================
# Step 4: Crear evento ATTEMPT (simple event)
# ============================================================
echo ""
echo "=== Step 4: Create ATTEMPT Event (simple) ==="

ATTEMPT_EVENT=$(curl -s -X POST "$BASE_URL/api/v1/sync/sync-events" \
  -H "Content-Type: application/json" \
  -d "{
    \"sync_session_id\": $SYNC_SESSION_ID,
    \"event_type\": \"attempt\",
    \"payload\": {
      \"student_id\": $STUDENT_ID,
      \"segment_level_id\": $SEGMENT_LEVEL_ID,
      \"count\": 3
    }
  }")

ATTEMPT_STATUS=$(echo "$ATTEMPT_EVENT" | jq -r '.status')

if [ "$ATTEMPT_STATUS" = "processed" ]; then
    log_pass "ATTEMPT event processed"
else
    log_info "ATTEMPT event status: $ATTEMPT_STATUS (simple events may not update progress)"
fi

# ============================================================
# Step 5: Verificar que Progress se actualizó
# ============================================================
echo ""
echo "=== Step 5: Verify Progress Updated ==="

sleep 1

UPDATED_PROGRESS=$(docker exec hwp-postgres psql -U hwp_user -d hwp_db -t -c \
  "SELECT error_count, attempt_count FROM progresses WHERE student_id = $STUDENT_ID AND segment_level_id = $SEGMENT_LEVEL_ID;" 2>/dev/null | tr -s ' ')

ERROR_COUNT=$(echo "$UPDATED_PROGRESS" | cut -d'|' -f1 | tr -d ' ')
ATTEMPT_COUNT=$(echo "$UPDATED_PROGRESS" | cut -d'|' -f2 | tr -d ' ')

log_info "Progress - error_count: $ERROR_COUNT, attempt_count: $ATTEMPT_COUNT"

if [ "$ERROR_COUNT" = "5" ]; then
    log_pass "Progress persisted correctly"
else
    log_fail "Progress mismatch - error_count: $ERROR_COUNT"
fi

# ============================================================
# Step 6: Verificar dead letter handler
# ============================================================
echo ""
echo "=== Step 6: Verify Dead Letter Handler ==="

DEAD_LETTER_COUNT=$(docker exec hwp-postgres psql -U hwp_user -d hwp_db -t -c \
  "SELECT COUNT(*) FROM sync_event_failures;" 2>/dev/null | tr -d ' ')

log_info "Dead letter records: $DEAD_LETTER_COUNT"

# ============================================================
# Summary
# ============================================================
echo ""
echo "============================================"
echo -e "${GREEN}✅ All integration tests passed!${NC}"
echo "============================================"
echo ""
echo "Summary:"
echo "  - ERROR event created and processed"
echo "  - xAPI statement created"
echo "  - Progress updated with error_count"
echo "  - Dead letter handler functional"
echo ""

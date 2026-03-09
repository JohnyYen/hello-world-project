#!/bin/bash

# ralph-afk.sh - Bucle de ejecución automática para un proyecto específico
# Uso: ./ralph-afk.sh <iteraciones> <proyecto>

# Cargar utilidades comunes
source "$(dirname "$0")/lib/ralph-common.sh"

ITERATIONS=$1
PROJECT=$2
START_TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

if [ -z "$ITERATIONS" ] || [ -z "$PROJECT" ]; then
    echo -e "${RED}Error: Argumentos insuficientes.${NC}"
    echo "Uso: $0 <iteraciones> <proyecto>"
    exit 1
fi

# Validaciones iniciales
check_opencode
validate_project "$PROJECT" || exit 1

# Manejo de señales (Ctrl+C)
cleanup() {
    echo -e "\n${YELLOW}⚠️  Bucle interrumpido por el usuario.${NC}"
    log_summary "$PROJECT" "ABORTED: Loop interrupted by user (SIGINT)"
    exit 1
}
trap cleanup SIGINT

echo -e "${GREEN}🤖 Iniciando bucle Ralph AFK ($ITERATIONS iteraciones) para: $PROJECT${NC}"
log_summary "$PROJECT" "STARTED: AFK Loop for $PROJECT ($ITERATIONS iterations)"

# Obtener el prompt desde la fuente de verdad (SSOT)
FINAL_PROMPT=$(get_prompt "$PROJECT" "$APP_PATH")

for ((i=1; i<=$ITERATIONS; i++)); do
    ITER_TIMESTAMP=$(date "+%Y%m%d_%H%M%S")
    ITER_LOG="$PROJECT_LOG_DIR/${ITER_TIMESTAMP}_iter_${i}.log"
    
    echo -e "${YELLOW}--- Iteración $i de $ITERATIONS ---${NC}"
    
    # Ejecutar opencode y capturar salida
    # Usamos temporal file para poder buscar el patrón COMPLETE en el resultado
    set +e
    opencode run "@$PRD_PATH @$AGENTS_PATH @$PROGRESS_PATH $FINAL_PROMPT" 2>&1 | tee "$ITER_LOG"
    EXIT_CODE=${PIPESTATUS[0]}
    set -e

    if [ $EXIT_CODE -ne 0 ]; then
        echo -e "${RED}❌ Error en la iteración $i.${NC}"
        log_summary "$PROJECT" "FAILED: Iteration $i failed (Log: $(basename "$ITER_LOG"))"
        exit $EXIT_CODE
    fi

    # Verificar si se completaron todas las tareas
    if grep -q "<promise>COMPLETE</promise>" "$ITER_LOG"; then
        echo -e "${GREEN}✅ Todas las tareas de $PROJECT en el PRD han sido completadas tras $i iteraciones.${NC}"
        log_summary "$PROJECT" "COMPLETE: All tasks finished at iteration $i (Log: $(basename "$ITER_LOG"))"
        exit 0
    fi

    log_summary "$PROJECT" "SUCCESS: Iteration $i finished (Log: $(basename "$ITER_LOG"))"
done

echo -e "${GREEN}🏁 Se han completado las $ITERATIONS iteraciones para $PROJECT.${NC}"
log_summary "$PROJECT" "FINISHED: All $ITERATIONS iterations completed for $PROJECT"

#!/bin/bash

# ralph-once.sh - Ejecuta una sola tarea para un proyecto específico utilizando el SSOT prompt

# Cargar utilidades comunes
source "$(dirname "$0")/lib/ralph-common.sh"

PROJECT=$1
TIMESTAMP=$(date "+%Y%m%d_%H%M%S")

# Validaciones iniciales
check_opencode
validate_project "$PROJECT" || exit 1

echo -e "${GREEN}🚀 Iniciando Ralph para el proyecto: $PROJECT en $APP_PATH${NC}"

# Obtener el prompt desde la fuente de verdad (SSOT)
FINAL_PROMPT=$(get_prompt "$PROJECT" "$APP_PATH")

# Definir archivos de log
ITER_LOG="$PROJECT_LOG_DIR/${TIMESTAMP}_once.log"

log_summary "$PROJECT" "STARTED: Single run for $PROJECT"

# Ejecutar opencode y capturar salida
set +e # No queremos que el script muera aquí para poder loguear el resultado
opencode run "@$PRD_PATH @$AGENTS_PATH @$PROGRESS_PATH $FINAL_PROMPT" 2>&1 | tee "$ITER_LOG"
EXIT_CODE=${PIPESTATUS[0]}

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Tarea completada con éxito.${NC}"
    log_summary "$PROJECT" "SUCCESS: Single run completed (Log: ${TIMESTAMP}_once.log)"
else
    echo -e "${RED}❌ Hubo un error en la ejecución de la tarea.${NC}"
    log_summary "$PROJECT" "FAILED: Single run failed with exit code $EXIT_CODE (Log: ${TIMESTAMP}_once.log)"
    exit $EXIT_CODE
fi

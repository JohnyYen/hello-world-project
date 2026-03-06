#!/bin/bash

# ralph-afk.sh - Bucle de ejecución automática para un proyecto específico
# Uso: ./ralph-afk.sh <iteraciones> <proyecto>
# Ejemplo: ./ralph-afk.sh 5 backend

ITERATIONS=$1
PROJECT=$2

if [ -z "$ITERATIONS" ] || [ -z "$PROJECT" ]; then
  echo "Error: Argumentos insuficientes."
  echo "Uso: $0 <iteraciones> <proyecto>"
  exit 1
fi

case $PROJECT in
  backend)
    APP_PATH="apps/backend"
    ;;
  frontend)
    APP_PATH="apps/frontend"
    ;;
  game)
    APP_PATH="apps/game"
    ;;
  *)
    echo "Error: Proyecto desconocido '$PROJECT'. Usa: backend, frontend o game."
    exit 1
    ;;
esac

set -e

echo "🤖 Iniciando bucle Ralph AFK ($ITERATIONS iteraciones) para: $PROJECT"

for ((i=1; i<=$ITERATIONS; i++)); do
  echo "--- Iteración $i de $ITERATIONS ---"
  
  result=$(opencode run -p "@apps/frontend/PRD.json @$APP_PATH/AGENTS.md @progress.txt \
  1. Identifica la siguiente tarea pendiente (\"passes\": false) en el PRD.json para el proyecto $PROJECT. \
  2. Lee el AGENTS.md en $APP_PATH y sigue TODAS sus reglas críticas y estándares. \
  3. Has una nueva rama siguiendo el estandar, implementa la tarea y ejecuta los comandos de verificación (test/lint) del AGENTS.md. \
  4. Si hay éxito, marca \"passes\": true en el PRD.json. \
  5. Actualiza progress.txt y realiza el commit. \
  6. Si no quedan tareas pendientes para $PROJECT, responde con <promise>COMPLETE</promise>. \
  SOLO TRABAJA EN UNA TAREA.")

  echo "$result"

  if [[ "$result" == *"<promise>COMPLETE</promise>"* ]]; then
    echo "✅ Todas las tareas de $PROJECT en el PRD han sido completadas tras $i iteraciones."
    exit 0
  fi
done

echo "🏁 Se han completado las $ITERATIONS iteraciones para $PROJECT."

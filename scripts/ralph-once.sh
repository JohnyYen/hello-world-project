#!/bin/bash

# ralph-once.sh - Ejecuta una sola tarea para un proyecto específico
# Uso: ./ralph-once.sh <proyecto>
# Ejemplo: ./ralph-once.sh frontend

PROJECT=$1

if [ -z "$PROJECT" ]; then
  echo "Error: Debes especificar un proyecto (backend, frontend, game)"
  echo "Uso: $0 <proyecto>"
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

echo "🚀 Iniciando Ralph para el proyecto: $PROJECT en $APP_PATH"

opencode run "@$APP_PATH/PRD.json @$APP_PATH/AGENTS.md @progress.txt \
1. Lee el PRD.json e identifica la primera tarea con \"passes\": false que corresponda al dominio de $PROJECT. \
2. Lee el AGENTS.md en $APP_PATH para entender las reglas críticas y comandos de verificación de este proyecto. \
3. Has una nueva rama siguiendo la convención, implementa la tarea siguiendo estrictamente los patrones arquitectónicos y de código definidos en el AGENTS.md. \
4. Ejecuta los comandos de verificación (test/lint) indicados en el AGENTS.md. \
5. Si las pruebas pasan, cambia \"passes\": true en el PRD.json para esa tarea. \
6. Actualiza progress.txt con el detalle de lo implementado. \
7. Crea un commit siguiendo el estilo conventional-commits definido. \
SOLO REALIZA UNA TAREA A LA VEZ."

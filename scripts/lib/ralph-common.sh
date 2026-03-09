#!/bin/bash

# ralph-common.sh - Shared utilities for Ralph automation scripts

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ensure logs directory exists
LOG_DIR="logs/ralph"

check_opencode() {
    if ! command -v opencode &> /dev/null; then
        echo -e "${RED}Error: 'opencode' CLI no está instalado o no está en el PATH.${NC}"
        exit 1
    fi
}

validate_project() {
    local project=$1
    if [ -z "$project" ]; then
        echo -e "${RED}Error: No se especificó el proyecto.${NC}"
        return 1
    fi

    case $project in
        backend|frontend|game|dummy)
            APP_PATH="apps/$project"
            ;;
        *)
            echo -e "${RED}Error: Proyecto desconocido '$project'. Usa: backend, frontend o game.${NC}"
            return 1
            ;;
    esac

    if [ ! -d "$APP_PATH" ]; then
        echo -e "${RED}Error: El directorio del proyecto '$APP_PATH' no existe.${NC}"
        return 1
    fi

    # Define dynamic paths
    PRD_PATH="$APP_PATH/PRD.json"
    AGENTS_PATH="$APP_PATH/AGENTS.md"
    PROGRESS_PATH="$APP_PATH/progress.txt"

    # Strict validations
    if [ ! -f "$PRD_PATH" ]; then
        echo -e "${RED}Error: No se encontró el PRD en '$PRD_PATH'.${NC}"
        exit 1
    fi

    if [ ! -f "$AGENTS_PATH" ]; then
        echo -e "${RED}Error: No se encontró el AGENTS.md en '$AGENTS_PATH'.${NC}"
        exit 1
    fi

    # Ensure progress file exists
    if [ ! -f "$PROGRESS_PATH" ]; then
        echo -e "${YELLOW}Aviso: Creando '$PROGRESS_PATH'...${NC}"
        touch "$PROGRESS_PATH"
    fi

    # Set up logging for this project
    PROJECT_LOG_DIR="$LOG_DIR/$project"
    mkdir -p "$PROJECT_LOG_DIR"
    SUMMARY_LOG="$PROJECT_LOG_DIR/summary.log"

    return 0
}

get_prompt() {
    local project=$1
    local app_path=$2
    local template="scripts/prompts/ralph-master-instruction.md"

    if [ ! -f "$template" ]; then
        echo -e "${RED}Error: No se encontró el template de instrucciones en '$template'.${NC}"
        exit 1
    fi

    # Replace placeholders using sed
    # We use | as delimiter for sed to avoid issues with path slashes
    cat "$template" | sed "s|{{PROJECT}}|$project|g; s|{{APP_PATH}}|$app_path|g"
}

log_summary() {
    local project=$1
    local message=$2
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    local summary_file="logs/ralph/$project/summary.log"
    echo "[$timestamp] $message" >> "$summary_file"
}

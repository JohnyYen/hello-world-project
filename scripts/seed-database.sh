#!/bin/bash
#
# Database Seeder Wrapper Script
# This script runs the database seeder with the correct Python environment
#

set -e

# Get the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/apps/backend"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}Hello World Project - Database Seeder${NC}"
echo -e "${GREEN}============================================================${NC}"
echo

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${RED}❌ Error: Backend directory not found at $BACKEND_DIR${NC}"
    exit 1
fi

# Check if seeder script exists
if [ ! -f "$SCRIPT_DIR/seed_database.py" ]; then
    echo -e "${RED}❌ Error: Seeder script not found at $SCRIPT_DIR/seed_database.py${NC}"
    exit 1
fi

# Find Python executable (try different options)
PYTHON_CMD=""
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo -e "${RED}❌ Error: Python not found${NC}"
    exit 1
fi

# Check if we're in a virtual environment or need to activate one
if [ -f "$BACKEND_DIR/.venv/bin/activate" ]; then
    echo -e "${YELLOW}Activating backend virtual environment...${NC}"
    source "$BACKEND_DIR/.venv/bin/activate"
elif [ -f "$BACKEND_DIR/.venv/bin/python" ]; then
    PYTHON_CMD="$BACKEND_DIR/.venv/bin/python"
    echo -e "${YELLOW}Using virtual environment Python: $PYTHON_CMD${NC}"
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    # Try to load from .env file
    ENV_FILE="$BACKEND_DIR/.env"
    if [ -f "$ENV_FILE" ]; then
        echo -e "${YELLOW}Loading environment from: $ENV_FILE${NC}"
        export $(grep -v '^#' "$ENV_FILE" | xargs)
    else
        echo -e "${YELLOW}⚠️  Warning: DATABASE_URL not set and no .env file found${NC}"
        echo -e "${YELLOW}   Please set DATABASE_URL in your environment or create .env file${NC}"
    fi
fi

# Check if PostgreSQL is running in Docker and use correct credentials
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "hwp-postgres"; then
    echo -e "${YELLOW}✓ Detected PostgreSQL container (hwp-postgres)${NC}"
    
    # Load docker-compose credentials
    DOCKER_ENV_FILE="$PROJECT_ROOT/infraestructure/docker/.env"
    if [ -f "$DOCKER_ENV_FILE" ]; then
        export $(grep -v '^#' "$DOCKER_ENV_FILE" | xargs)
        DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
        export DATABASE_URL
        echo -e "${GREEN}  Using Docker credentials: $DATABASE_URL${NC}"
    fi
elif [[ "$DATABASE_URL" == *"@postgresql_db:"* ]] || [[ "$DATABASE_URL" == *"@postgres:"* ]]; then
    # Convert Docker network hostname to localhost (fallback)
    echo -e "${YELLOW}⚠️  Detected Docker network hostname in DATABASE_URL${NC}"
    echo -e "${YELLOW}   Converting to localhost for local execution...${NC}"
    DATABASE_URL=$(echo "$DATABASE_URL" | sed 's/@postgresql_db:/@localhost:/' | sed 's/@postgres:/@localhost:/')
    export DATABASE_URL
    echo -e "${GREEN}   Updated DATABASE_URL: $DATABASE_URL${NC}"
fi

# Run the seeder
echo
echo -e "${YELLOW}Running database seeder...${NC}"
echo

cd "$PROJECT_ROOT"
$PYTHON_CMD "$SCRIPT_DIR/seed_database.py" "$@"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo
    echo -e "${GREEN}✓ Seeder completed successfully!${NC}"
else
    echo
    echo -e "${RED}❌ Seeder failed with exit code: $exit_code${NC}"
fi

exit $exit_code

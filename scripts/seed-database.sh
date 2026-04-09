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

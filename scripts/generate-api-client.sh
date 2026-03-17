#!/bin/bash
# API Client Generator Script
# Generates TypeScript client from OpenAPI specification

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
OPENAPI_SPEC="packages/api-contract/openapi.yaml"
OUTPUT_DIR="packages/api-client-ts"
GENERATOR="typescript-fetch"

echo -e "${GREEN}🚀 Generating API client from OpenAPI spec...${NC}"
echo "  Spec:    $OPENAPI_SPEC"
echo "  Output:  $OUTPUT_DIR"
echo "  Generator: $GENERATOR"
echo ""

# Check if OpenAPI spec exists
if [ ! -f "$OPENAPI_SPEC" ]; then
    echo -e "${RED}❌ Error: OpenAPI spec not found at $OPENAPI_SPEC${NC}"
    exit 1
fi

# Check if openapi-generator-cli is available
if ! command -v openapi-generator-cli &> /dev/null; then
    echo -e "${YELLOW}⚠️  openapi-generator-cli not found in PATH${NC}"
    echo "  Installing via npx..."
    OPENAPI_CMD="npx @openapitools/openapi-generator-cli"
else
    OPENAPI_CMD="openapi-generator-cli"
fi

# Clean output directory
echo -e "${YELLOW}🗑️  Cleaning existing output directory...${NC}"
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Generate client
echo -e "${GREEN}⚡ Generating TypeScript client...${NC}"
$OPENAPI_CMD generate \
    -i "$OPENAPI_SPEC" \
    -g "$GENERATOR" \
    -o "$OUTPUT_DIR" \
    --additional-properties=modelPropertyNaming=original,enumNameSuffix=Enum,useSingleRequestParameter=true,typescriptThreePlus=true

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ API client generated successfully!${NC}"
    echo ""
    echo "Generated files in: $OUTPUT_DIR"
    echo ""
    echo "To use the client in your frontend:"
    echo "  1. Add to your frontend package.json:"
    echo "     \"@local/api-client\": \"workspace:*\""
    echo ""
    echo "  2. Import in your code:"
    echo "     import { DefaultApi } from '@local/api-client'"
    echo ""
else
    echo -e "${RED}❌ Error: Generation failed${NC}"
    exit 1
fi

#!/bin/bash

# Flask API Base - Flake8 Linting Script
# This script runs Flake8 linting on the codebase

# Set Python warnings to be ignored to avoid noise
export PYTHONWARNINGS=ignore

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running Flake8 linting...${NC}"

# Run Flake8 with configuration from .flake8
python -m flake8 . "$@"

# Check the exit code
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Linting passed! No issues found.${NC}"
else
    echo -e "${RED}✗ Linting failed! Please fix the issues above.${NC}"
fi 
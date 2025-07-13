#!/bin/bash

# Flask API Base - Code Formatting Script
# This script runs automatic code formatting using Black and isort

# Set Python warnings to be ignored to avoid noise
export PYTHONWARNINGS=ignore

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running automatic code formatting...${NC}"

# Run isort to fix import ordering
echo -e "${BLUE}Step 1: Fixing import ordering with isort...${NC}"
python -m isort . --check-only --diff
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Fixing import issues...${NC}"
    python -m isort .
    echo -e "${GREEN}✓ Import ordering fixed!${NC}"
else
    echo -e "${GREEN}✓ Import ordering is already correct!${NC}"
fi

# Run Black to fix code formatting
echo -e "${BLUE}Step 2: Fixing code formatting with Black...${NC}"
python -m black --check --diff .
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Fixing formatting issues...${NC}"
    python -m black .
    echo -e "${GREEN}✓ Code formatting fixed!${NC}"
else
    echo -e "${GREEN}✓ Code formatting is already correct!${NC}"
fi

echo -e "${GREEN}🎉 Automatic formatting completed!${NC}"
echo -e "${BLUE}Run ./run_lint.sh to check remaining issues${NC}" 
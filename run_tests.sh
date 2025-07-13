#!/bin/bash
# Convenient script to run tests with warnings suppressed

# Set the warning suppression environment variable
export PYTHONWARNINGS=ignore

# Run pytest with any passed arguments
echo "Running tests with warnings suppressed..."
python -m pytest "$@"

# Reset the environment variable
unset PYTHONWARNINGS 
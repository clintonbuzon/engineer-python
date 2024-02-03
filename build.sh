#!/bin/bash

set -e

echo "------------------------------------------"
echo "Installing required python dependencies..."
echo "------------------------------------------"
pip3 install -r requirements.txt

echo "------------------------------------------"
echo "Linting the code..."
echo "------------------------------------------"
isort . || exit 1
ruff clean || exit 1
ruff format || exit 1
ruff check || exit 1

echo "------------------------------------------"
echo "Running tests..."
echo "------------------------------------------"
python3 -m pytest -v || exit 1
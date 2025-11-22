#!/bin/bash
# SKILL: Complexity Hunter
# Description: Finds code with high Cyclomatic Complexity (Rank C or worse)
# Invariant: Code should be simple (Rank A or B)
# Usage: ./check_complexity.sh [target_dir]

TARGET_DIR=${1:-.}

echo "🔍 Hunting for complex code (Radon) in $TARGET_DIR..."

# Ensure uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "---------------------------------------------------"
echo "Cyclomatic Complexity Report (Only C, D, E, F)"
echo "---------------------------------------------------"

# Use uv run --with to execute radon ephemerally
# Run radon via uv
uv run radon cc "$TARGET_DIR" -a -n C --exclude "tests/*,venv/*,node_modules/*,.agents/*,sia/*"

# Log usage
uv run sia/skills/metrics.py check_complexity target="$TARGET_DIR"

echo "✅ Complexity check complete."

echo "---------------------------------------------------"
echo "Maintainability Index (Bottom 10)"
echo "---------------------------------------------------"
uv run --with radon radon mi "$TARGET_DIR" --sort --min A --exclude "tests/*,venv/*,node_modules/*,.venv/*,sia/*" | head -n 10

#!/bin/bash
# SKILL: Architecture Enforcer
# Description: Visualizes dependencies to check DDD layering
# Invariant: Domain layer should NOT depend on Infrastructure
# Usage: ./visualize_architecture.sh [target_dir] [output_file]

TARGET_DIR=${1:-.}
OUTPUT_FILE=${2:-architecture_graph.svg}

echo "🗺️  Generating Architecture Map (Pydeps) for $TARGET_DIR..."

if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed."
    exit 1
fi

# Generate graph
# --noshow: Don't try to open the image immediately
# --max-bacon 2: Limit depth to keep it readable
# --exclude: Ignore tests and external libs
uv run --with pydeps pydeps "$TARGET_DIR" \
    --exclude "tests/*" "venv/*" "migrations/*" "sia/*" ".venv/*" \
    --noshow \
    --max-bacon 2 \
    --output "$OUTPUT_FILE"

# Log usage
uv run sia/skills/metrics.py visualize_architecture target="$TARGET_DIR" output="$OUTPUT_FILE"

echo "✅ Graph generated at $OUTPUT_FILE"

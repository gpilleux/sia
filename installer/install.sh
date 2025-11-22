#!/bin/bash
# SIA Installer Script
# Usage: ./install.sh

set -e

echo "🚀 Installing SIA Framework..."

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "❌ 'uv' is not installed. Please install it first."
    exit 1
fi

# 1. Run Auto-Discovery & Instruction Assembly
echo "---------------------------------------------------"
uv run sia/installer/auto_discovery.py

echo "---------------------------------------------------"
echo "✅ SIA Installation Complete!"
echo "   - Configuration: .sia.detected.yaml"
echo "   - Instructions: .github/copilot-instructions.md"

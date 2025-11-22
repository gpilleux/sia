#!/bin/bash
# SIA Installer Script (macOS/Linux)
# Usage: bash installer/install.sh

set -e

echo ""
echo "========================================"
echo " SIA Framework Installer (Unix)"
echo "========================================"
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=macOS;;
    *)          PLATFORM="UNKNOWN:${OS}"
esac

echo "[INFO] Detected Platform: ${PLATFORM}"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 is not installed"
    echo "Please install Python 3.10+ from:"
    if [ "$PLATFORM" = "macOS" ]; then
        echo "  brew install python@3.10"
    elif [ "$PLATFORM" = "Linux" ]; then
        echo "  sudo apt install python3 python3-pip  # Debian/Ubuntu"
        echo "  sudo yum install python3 python3-pip  # RHEL/CentOS"
    fi
    exit 1
fi

# Check for uv
if ! command -v uv &> /dev/null; then
    echo "[INFO] 'uv' is not installed. Installing..."
    pip3 install uv || {
        echo "[ERROR] Failed to install uv"
        exit 1
    }
fi

echo ""
echo "[STEP 1/2] Running Auto-Discovery..."
echo "---------------------------------------------------"
uv run sia/installer/auto_discovery.py || {
    echo "[ERROR] Auto-discovery failed"
    exit 1
}

echo ""
echo "---------------------------------------------------"
echo "[SUCCESS] SIA Installation Complete!"
echo ""
echo "  Created:"
echo "  - Configuration: .sia.detected.yaml"
echo "  - Instructions: .github/copilot-instructions.md"
echo ""
echo "Next steps:"
echo "  1. Review .sia.detected.yaml"
echo "  2. Read .github/copilot-instructions.md"
echo "  3. Start using GitHub Copilot with SIA!"
echo ""

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
echo "[STEP 1/3] Creating .sia/ Directory Structure..."
echo "---------------------------------------------------"
mkdir -p .sia/agents
mkdir -p .sia/knowledge/active
mkdir -p .sia/knowledge/_archive
mkdir -p .sia/requirements
mkdir -p .sia/requirements/_archive
mkdir -p .sia/skills

# Create README files for each directory
cat > .sia/README.md << 'EOF'
# SIA Project Configuration

This directory contains the SIA framework integration for this project.

## Structure
- `agents/`: Project-specific agent definitions
- `knowledge/`: Active and archived knowledge base
- `requirements/`: Requirements management (active and archived)
- `skills/`: Project-specific automation skills

See `sia/README.md` for complete framework documentation.
EOF

cat > .sia/agents/README.md << 'EOF'
# Project Agents

Define project-specific agents here. The SUPER AGENT will populate this
directory during repository initialization.

## Next Steps
Ask GitHub Copilot: "Initialize SIA agents for this repository"
EOF

cat > .sia/knowledge/active/README.md << 'EOF'
# Active Knowledge Base

Active research, decisions, and domain knowledge.

## Document Lifecycle
See `.github/DOCUMENT_LIFECYCLE.md` for archival protocol.
EOF

cat > .sia/requirements/README.md << 'EOF'
# Requirements Management

See `sia/requirements/README.md` for complete workflow.

## Quick Start
1. Define requirements in natural language
2. SUPER AGENT decomposes into QUANT tasks
3. Execute, verify, archive
EOF

cat > .sia/skills/README.md << 'EOF'
# Project Skills

Project-specific automation scripts.

## Framework Skills
Reusable skills available in `sia/skills/`
EOF

# Copy INIT_REQUIRED template
cp sia/templates/INIT_REQUIRED.template.md .sia/INIT_REQUIRED.md

echo "   ✅ .sia/ structure created"
echo "   ✅ .sia/INIT_REQUIRED.md created (one-time init instructions)"

echo ""
echo "[STEP 2/3] Running Smart Initialization..."
echo "---------------------------------------------------"
# Run smart_init.py which handles migration, population, and auto-discovery
uv run --with pyyaml python3 sia/installer/smart_init.py || {
    echo "[ERROR] Smart initialization failed"
    exit 1
}

echo ""
echo "---------------------------------------------------"
echo "[STEP 3/3] Repository Initialization Required"
echo "---------------------------------------------------"
echo ""
echo "[SUCCESS] SIA Installation Complete!"
echo ""
echo "  Created:"
echo "  - Directory: .sia/ (agents, knowledge, requirements, skills)"
echo "  - Configuration: .sia.detected.yaml"
echo "  - Instructions: .github/copilot-instructions.md"
echo "  - Init Protocol: .sia/INIT_REQUIRED.md (one-time)"
echo ""
echo "⚠️  IMPORTANT: Repository requires SUPER AGENT initialization"
echo ""
echo "Next steps:"
echo "  1. Open this project in VS Code with GitHub Copilot"
echo "  2. Ask Copilot: 'Initialize SIA for this repository'"
echo ""
echo "     The SUPER AGENT will:"
echo "     - Analyze repository structure and domain"
echo "     - Generate project SPR (.sia/agents/<project>.md)"
echo "     - Detect specialized agents (e.g., Repository Guardian)"
echo "     - Create initial knowledge base"
echo "     - Populate skills catalog"
echo "     - Delete .sia/INIT_REQUIRED.md (auto-cleanup)"
echo ""
echo "  3. Review generated files in .sia/"
echo "  4. Start working with natural language requirements!"
echo ""
echo "📖 Documentation:"
echo "  - Framework: sia/README.md"
echo "  - Quick Start: sia/QUICKSTART.md"
echo "  - Distribution: sia/DISTRIBUTION.md"
echo ""

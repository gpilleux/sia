#!/bin/bash
# Setup GitHub Copilot CLI integration
# This script installs and configures Copilot CLI for agent spawning

set -e

echo "🚀 GitHub Copilot CLI Integration Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Node.js version
echo "1️⃣  Checking prerequisites..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js v22 or higher."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 22 ]; then
    echo "⚠️  Node.js version $NODE_VERSION detected. Recommended: v22 or higher."
fi

# Check npm version
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm v10 or higher."
    exit 1
fi

NPM_VERSION=$(npm --version | cut -d'.' -f1)
if [ "$NPM_VERSION" -lt 10 ]; then
    echo "⚠️  npm version $NPM_VERSION detected. Recommended: v10 or higher."
fi

echo "✅ Prerequisites OK"
echo ""

# Install Copilot CLI
echo "2️⃣  Installing GitHub Copilot CLI..."
if command -v copilot &> /dev/null; then
    CURRENT_VERSION=$(npm list -g @github/copilot --depth=0 2>/dev/null | grep @github/copilot | awk '{print $2}' || echo "unknown")
    echo "ℹ️  Copilot CLI already installed (version: $CURRENT_VERSION)"
    read -p "   Update to latest version? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        npm install -g @github/copilot
        echo "✅ Updated to latest version"
    fi
else
    npm install -g @github/copilot
    echo "✅ Installed successfully"
fi
echo ""

# Create custom agents directory
echo "3️⃣  Setting up custom agents..."
COPILOT_AGENTS_DIR="$HOME/.copilot/agents"
mkdir -p "$COPILOT_AGENTS_DIR"

# Copy custom agents
cp .github/copilot-agents/research-specialist "$COPILOT_AGENTS_DIR/"
cp .github/copilot-agents/ddd-refactoring "$COPILOT_AGENTS_DIR/"

echo "✅ Custom agents installed:"
echo "   - research-specialist"
echo "   - ddd-refactoring"
echo ""

# Setup MCP config
echo "4️⃣  Setting up MCP server configuration..."
MCP_CONFIG="$HOME/.copilot/mcp-config.json"

# Get absolute path to project
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Create MCP config with absolute path
cat > "$MCP_CONFIG" <<EOF
{
  "mcpServers": {
    "dipres-analyzer-tools": {
      "command": "python",
      "args": ["$PROJECT_ROOT/skills/mcp_server.py"],
      "env": {
        "DATABASE_URL": "\${DATABASE_URL}",
        "OPENAI_API_KEY": "\${OPENAI_API_KEY}"
      }
    }
  }
}
EOF

echo "✅ MCP config created at: $MCP_CONFIG"
echo ""

# Test installation
echo "5️⃣  Testing installation..."
if copilot --help &> /dev/null; then
    echo "✅ Copilot CLI responding"
else
    echo "❌ Copilot CLI not responding. Please check installation."
    exit 1
fi

# Check authentication
echo ""
echo "6️⃣  Checking authentication..."
echo "ℹ️  You need to authenticate with GitHub to use Copilot CLI."
echo ""
read -p "Do you want to authenticate now? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting Copilot CLI for authentication..."
    echo "Use the /login command in the session."
    echo ""
    copilot --banner || true
else
    echo "⚠️  Skipping authentication. Run 'copilot' and use /login when ready."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "   1. Authenticate: copilot → /login"
echo "   2. Test agent: ./skills/spawn_copilot_agent.sh \"Analyze this codebase\""
echo "   3. Test MCP: copilot --additional-mcp-config ~/.copilot/mcp-config.json"
echo ""
echo "📖 Documentation: .agents/copilot_cli_agent.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

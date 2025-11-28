#!/bin/bash
# Setup script for MCP server integration with VS Code

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Setting up MCP Server for VS Code Integration"
echo "=================================================="
echo ""

# Step 1: Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker Desktop."
    exit 1
fi
echo "  ✅ Docker installed"

if ! command -v uv &> /dev/null; then
    echo "⚠️  uv not found (optional for local dev mode)"
else
    echo "  ✅ uv installed"
fi

# Step 2: Check GEMINI_API_KEY
if [ -z "$GEMINI_API_KEY" ]; then
    echo ""
    echo "⚠️  GEMINI_API_KEY not set in environment"
    echo "   Set it with: export GEMINI_API_KEY='your_key_here'"
    echo "   Or add to ~/.zshrc for persistence"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "  ✅ GEMINI_API_KEY configured"
fi

# Step 3: Check database
echo ""
echo "🗄️  Checking database..."

if docker ps --format '{{.Names}}' | grep -q 'indexer-db'; then
    echo "  ✅ Database (indexer-db) is running"
else
    echo "  ⚠️  Database not running. Starting..."
    cd "$PROJECT_ROOT/../repo_indexer"
    docker compose up -d indexer-db
    echo "  ✅ Database started"
fi

# Step 4: Build Docker image
echo ""
echo "🏗️  Building MCP server Docker image..."

cd "$SCRIPT_DIR"
docker build -t sia/repo-indexer-mcp:latest .

if [ $? -eq 0 ]; then
    echo "  ✅ Docker image built successfully"
else
    echo "  ❌ Docker build failed"
    exit 1
fi

# Step 5: Test Docker image
echo ""
echo "🧪 Testing Docker image..."

timeout 5 docker run --rm -i \
    --network repo_indexer_repo-indexer-network \
    -e DATABASE_URL=postgresql+asyncpg://indexer:indexer123@indexer-db:5432/repo_indexer \
    -e GEMINI_API_KEY="${GEMINI_API_KEY:-test}" \
    sia/repo-indexer-mcp:latest &

DOCKER_PID=$!
sleep 3

if ps -p $DOCKER_PID > /dev/null; then
    echo "  ✅ Container starts successfully (stdio mode)"
    kill $DOCKER_PID 2>/dev/null || true
else
    echo "  ❌ Container failed to start"
    exit 1
fi

# Step 6: Verify VS Code config
echo ""
echo "📝 Verifying VS Code configuration..."

if [ -f "$PROJECT_ROOT/.vscode/mcp.json" ]; then
    echo "  ✅ .vscode/mcp.json exists"
else
    echo "  ❌ .vscode/mcp.json not found"
    echo "     Creating from template..."
    mkdir -p "$PROJECT_ROOT/.vscode"
    cp "$SCRIPT_DIR/mcp.json.template" "$PROJECT_ROOT/.vscode/mcp.json"
    echo "  ✅ Created .vscode/mcp.json"
fi

# Step 7: Final instructions
echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Open VS Code in: $PROJECT_ROOT"
echo "2. Reload window: Cmd+Shift+P → 'Developer: Reload Window'"
echo "3. Open Copilot Chat"
echo "4. Try: '@workspace search for vector store in repo_indexer using MCP'"
echo ""
echo "Configuration files:"
echo "  - MCP Server: $SCRIPT_DIR/repo_indexer_mcp.py"
echo "  - VS Code Config: $PROJECT_ROOT/.vscode/mcp.json"
echo "  - Docker Image: sia/repo-indexer-mcp:latest"
echo ""
echo "Troubleshooting:"
echo "  - View logs: docker logs <container_id>"
echo "  - Rebuild: docker build -t sia/repo-indexer-mcp:latest ."
echo "  - See VSCODE_SETUP.md for detailed guide"
echo ""

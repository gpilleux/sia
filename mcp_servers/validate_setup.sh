#!/bin/bash
# Quick validation script for MCP server setup
# Run this to verify everything is working before testing in VS Code

set -e

echo "🔍 MCP Server Validation Script"
echo "================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Test 1: Check Docker image exists
echo "Test 1: Docker image..."
if docker images | grep -q "sia/repo-indexer-mcp"; then
    echo "  ✅ Docker image found"
else
    echo "  ❌ Docker image not found"
    echo "     Run: docker build -t sia/repo-indexer-mcp:latest ."
    exit 1
fi

# Test 2: Check database is running
echo ""
echo "Test 2: Database connectivity..."
if docker ps | grep -q "indexer-db"; then
    echo "  ✅ Database container running"
    
    # Test connection
    if docker exec indexer-db psql -U indexer -d repo_indexer -c "SELECT COUNT(*) FROM code_chunks" &>/dev/null; then
        CHUNK_COUNT=$(docker exec indexer-db psql -U indexer -d repo_indexer -t -c "SELECT COUNT(*) FROM code_chunks" | xargs)
        echo "  ✅ Database accessible ($CHUNK_COUNT chunks indexed)"
    else
        echo "  ❌ Can't query database"
        exit 1
    fi
else
    echo "  ❌ Database not running"
    echo "     Run: cd ../repo_indexer && docker compose up -d"
    exit 1
fi

# Test 3: Check network exists
echo ""
echo "Test 3: Docker network..."
if docker network ls | grep -q "repo_indexer_repo-indexer-network"; then
    echo "  ✅ Docker network exists"
else
    echo "  ⚠️  Network not found, will be created by docker compose"
fi

# Test 4: Check VS Code config
echo ""
echo "Test 4: VS Code configuration..."
if [ -f "../.vscode/mcp.json" ]; then
    echo "  ✅ .vscode/mcp.json exists"
    
    # Validate JSON
    if command -v jq &>/dev/null; then
        if jq empty ../.vscode/mcp.json 2>/dev/null; then
            echo "  ✅ Valid JSON syntax"
        else
            echo "  ❌ Invalid JSON syntax"
            exit 1
        fi
    fi
else
    echo "  ⚠️  .vscode/mcp.json not found"
    echo "     Run: ./setup_vscode.sh"
fi

# Test 5: Environment variables
echo ""
echo "Test 5: Environment variables..."
if [ -z "$GEMINI_API_KEY" ]; then
    echo "  ⚠️  GEMINI_API_KEY not set"
    echo "     Embeddings will fail. Set with: export GEMINI_API_KEY='your_key'"
else
    echo "  ✅ GEMINI_API_KEY configured"
fi

# Test 6: Quick container spawn test
echo ""
echo "Test 6: Container startup test..."
CONTAINER_ID=$(docker run -d --rm \
    --network repo_indexer_repo-indexer-network \
    -e DATABASE_URL=postgresql+asyncpg://indexer:indexer123@indexer-db:5432/repo_indexer \
    -e GEMINI_API_KEY="${GEMINI_API_KEY:-test}" \
    sia/repo-indexer-mcp:latest)

sleep 2

if docker ps | grep -q "$CONTAINER_ID"; then
    echo "  ✅ Container started successfully"
    docker stop "$CONTAINER_ID" &>/dev/null
    echo "  ✅ Container stopped"
else
    echo "  ❌ Container failed to start"
    docker logs "$CONTAINER_ID"
    exit 1
fi

# Summary
echo ""
echo "================================="
echo "✅ All validation tests passed!"
echo "================================="
echo ""
echo "Next steps:"
echo "1. Open VS Code in project root"
echo "2. Reload window: Cmd+Shift+P → 'Developer: Reload Window'"
echo "3. Open Copilot Chat"
echo "4. Test query:"
echo "   '@workspace Use the repo-indexer MCP tool to search for"
echo "   \"vector store implementation\" in repo_indexer codebase'"
echo ""
echo "Troubleshooting:"
echo "  - MCP logs: Check VS Code Developer Tools Console"
echo "  - Container logs: docker logs <container_id>"
echo "  - See VSCODE_SETUP.md for detailed guide"
echo ""

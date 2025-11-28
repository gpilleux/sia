#!/bin/bash
# Launch MCP Inspector for interactive testing (no stdio hang)
# Based on FastMCP documentation: https://github.com/jlowin/fastmcp

set -e

echo "🚀 Launching MCP Inspector..."
echo ""
echo "This will open a web interface for testing MCP tools interactively."
echo "URL: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

cd "$(dirname "$0")"

# Export environment variables
export GEMINI_API_KEY="${GEMINI_API_KEY:-}"

if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  WARNING: GEMINI_API_KEY not set"
    echo "   Embeddings will fail. Set with: export GEMINI_API_KEY=your_key"
    echo ""
fi

# Run FastMCP dev server
exec uv run fastmcp dev repo_indexer_mcp.py

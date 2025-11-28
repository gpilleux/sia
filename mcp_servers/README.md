# MCP Servers for SIA Framework

MCP (Model Context Protocol) server wrappers for SIA capabilities, enabling AI agents (VS Code Copilot, Claude Desktop) to access semantic code search and analysis tools.

## Overview

This directory contains MCP server implementations that expose SIA's capabilities:

- **repo_indexer_mcp.py**: Semantic code search via pgvector + Google Gemini embeddings
- Delegates to `repo_indexer` Application layer (DDD architecture)
- Supports stdio transport (Claude Desktop, VS Code) and HTTP transport (MCP Inspector)

## Quick Start

### For VS Code Copilot (Recommended)

```bash
cd /Users/gpilleux/apps/meineapps/sia/mcp_servers
./setup_vscode.sh
```

This will:
1. Build Docker image for MCP server
2. Verify database is running
3. Create `.vscode/mcp.json` configuration
4. Test the setup

Then reload VS Code and use MCP tools in Copilot Chat.

### For Claude Desktop

Copy configuration to Claude Desktop:

```bash
# macOS
cp claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Set API key
echo 'export GEMINI_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc

# Restart Claude Desktop
```

## Deployment Options

### Option 1: Docker (Production)

**Best for**: Team distribution, reproducible builds, isolation

```bash
# Build image
docker build -t sia/repo-indexer-mcp:latest .

# Run with docker compose
docker compose up -d

# VS Code will auto-connect via .vscode/mcp.json
```

See `VSCODE_SETUP.md` for detailed Docker configuration.

### Option 2: Local Python (Development)

**Best for**: Fast iteration, debugging, hot reload

Edit `.vscode/mcp.json`:

```json
{
  "mcp": {
    "servers": {
      "repo-indexer": {
        "command": "uv",
        "args": ["run", "--with", "fastmcp", "python", "repo_indexer_mcp.py"],
        "env": {
          "DATABASE_URL": "postgresql+asyncpg://indexer:indexer123@localhost:5436/repo_indexer",
          "GEMINI_API_KEY": "${env:GEMINI_API_KEY}"
        }
      }
    }
  }
}
```

### Option 3: MCP Inspector (Interactive Testing)

**Best for**: Tool validation, debugging, development

```bash
./run_mcp_inspector.sh
# Opens http://localhost:5173 with interactive UI
```

## Configuration Files

- **`fastmcp.json`**: FastMCP deployment configuration (Docker-friendly)
- **`Dockerfile`**: Multi-stage build for production deployment
- **`docker-compose.yml`**: Full stack (MCP server + database)
- **`.vscode/mcp.json`**: VS Code integration config (auto-created by setup script)
- **`claude_desktop_config.json`**: Claude Desktop template
- **`VSCODE_SETUP.md`**: Complete VS Code setup guide
- **`VALIDATION_GUIDE.md`**: Testing strategies and troubleshooting
      "args": [
        "/Users/gpilleux/apps/meineapps/sia/mcp_servers/repo_indexer_mcp.py"
      ],
      "env": {
        "GEMINI_API_KEY": "YOUR_ACTUAL_KEY",
        "DATABASE_URL": "postgresql+asyncpg://indexer:indexer123@localhost:5436/repo_indexer",
        "PYTHONPATH": "/Users/gpilleux/apps/meineapps/repo_indexer"
      }
    }
  }
}
```

**Testing**:
1. Restart Claude Desktop
2. In chat: "Use search_code to find vector store implementations in repo_indexer"
3. Verify: Results returned in <2s, similarity scores >0.5

**Troubleshooting**:
- `ImportError`: Check PYTHONPATH includes repo_indexer directory
- `Database connection failed`: Verify PostgreSQL is running on port 5436
- `GEMINI_API_KEY not set`: Check environment variable in claude_desktop_config.json
- `No results found`: Ensure repository was indexed (run `uv run repo-indexer index`)

**Performance**:
- Indexing: ~0.25 files/sec (Gemini API rate limited)
- Search latency: <2s P95 (embedding generation + pgvector KNN)
- Memory: <500MB for 1000 chunks

**Next Steps**:
- Add `index_repository` tool (Phase 2A implementation)
- Add `get_file_metadata` tool
- Implement progress reporting via Context
- Add unit tests with mocked use cases

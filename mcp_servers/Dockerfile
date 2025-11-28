# Multi-stage build for FastMCP repo_indexer server
# Stage 1: Build environment with dependencies

FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy FastMCP configuration and server code
COPY fastmcp.json .
COPY repo_indexer_mcp.py .

# Note: repo_indexer is expected to be accessible via PYTHONPATH
# In this build, we'll install dependencies but repo_indexer will be 
# mounted or accessed at runtime via network/import path
# For now, skip copying repo_indexer source and install only MCP dependencies

# Install FastMCP and prepare minimal environment
RUN pip install --no-cache-dir \
    fastmcp \
    sqlalchemy \
    asyncpg \
    pydantic-settings \
    python-dotenv \
    google-generativeai \
    pgvector

# Stage 2: Minimal runtime image

FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy application files from builder
COPY --from=builder /app/repo_indexer_mcp.py .
COPY --from=builder /app/fastmcp.json .

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set PYTHONPATH to find repo_indexer (will be mounted via volume or network)
ENV PYTHONPATH="/app/repo_indexer:${PYTHONPATH}"

# Run MCP server directly with Python
CMD ["python", "repo_indexer_mcp.py"]

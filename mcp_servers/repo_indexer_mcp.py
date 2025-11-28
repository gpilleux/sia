#!/usr/bin/env python3
"""MCP Server wrapper for repo_indexer capabilities.

Exposes semantic search and code indexing as MCP tools for AI agents.
Delegates to repo_indexer Application layer use cases.

Architecture:
    Claude Desktop/VS Code Copilot
        ↓ (MCP stdio transport)
    FastMCP Server (this file)
        ↓ (method calls)
    Application Use Cases (repo_indexer)
        ↓ (repository interfaces)
    Infrastructure (PostgreSQL + pgvector)
"""

import asyncio
import json
import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError

# Add repo_indexer to Python path
REPO_INDEXER_PATH = Path(__file__).parent.parent / "external" / "repo_indexer"
if not REPO_INDEXER_PATH.exists():
    # Fallback: Try relative to sia root
    REPO_INDEXER_PATH = Path(__file__).parent.parent.parent / "repo_indexer"

sys.path.insert(0, str(REPO_INDEXER_PATH))

# Import repo_indexer components
try:
    from application.query_codebase import QueryCodebaseUseCase, SearchResult
    from infrastructure.config import get_settings
    from infrastructure.database.config import AsyncSessionLocal, engine
    from infrastructure.database.vector_store import PostgresVectorStore
    from infrastructure.services.embedding_service import EmbeddingService
except ImportError as e:
    print(f"ERROR: Cannot import repo_indexer modules: {e}", file=sys.stderr)
    print(f"PYTHONPATH: {sys.path}", file=sys.stderr)
    print(f"Looking in: {REPO_INDEXER_PATH}", file=sys.stderr)
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global dependencies (initialized in lifespan, NOT at import time)
_settings: Optional[object] = None
_vector_store: Optional[PostgresVectorStore] = None
_embedding_service: Optional[EmbeddingService] = None
_session = None


@asynccontextmanager
async def lifespan(server: FastMCP):
    """Server lifespan manager for lazy initialization.
    
    This prevents blocking on database connections during module import,
    which causes hangs when using stdio transport.
    """
    global _settings, _vector_store, _embedding_service, _session
    
    logger.info("🚀 Initializing MCP server dependencies...")
    
    try:
        # Load settings
        _settings = get_settings()
        
        # Validate Gemini API key (EmbeddingService will use it from env)
        if not _settings.gemini_api_key:
            logger.warning("⚠️  GEMINI_API_KEY not set. Embeddings will fail.")
        
        # Create database session (lazy connection)
        try:
            _session = AsyncSessionLocal()
            logger.info(f"✅ Connected to database: {_settings.database_url}")
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
        
        # Initialize services (EmbeddingService reads GEMINI_API_KEY from environment)
        _embedding_service = EmbeddingService()
        _vector_store = PostgresVectorStore(
            session=_session,
            embedding_model="text-embedding-004"
        )
        
        logger.info("✅ MCP server initialized successfully")
        
        # Server is ready - yield control
        yield
        
    finally:
        # Cleanup on shutdown
        logger.info("🛑 Shutting down MCP server...")
        if _session:
            await _session.close()
            logger.info("✅ Database connection closed")


# Initialize MCP server with lifespan
mcp = FastMCP("Repository Indexer", lifespan=lifespan)


async def get_query_use_case() -> QueryCodebaseUseCase:
    """Factory for QueryCodebaseUseCase with dependencies."""
    if _vector_store is None or _embedding_service is None:
        raise ToolError("MCP server not initialized. Database connection required.")
    
    return QueryCodebaseUseCase(
        vector_store=_vector_store,
        embedding_service=_embedding_service,
    )


@mcp.tool
async def search_code(
    repo_name: str,
    query: str,
    top_k: int = 10,
    min_similarity: float = 0.5,
) -> str:
    """Semantic search across codebase using natural language.
    
    Uses vector embeddings (Google Gemini text-embedding-004) and pgvector
    to find code chunks similar to the query. Returns functions, classes,
    and modules ranked by semantic similarity.
    
    Args:
        repo_name: Repository identifier (e.g., "repo_indexer", "sia")
        query: Natural language query (e.g., "vector store implementation", "DDD repository pattern")
        top_k: Maximum number of results to return (1-50, default: 10)
        min_similarity: Minimum cosine similarity threshold 0-1 (default: 0.5)
    
    Returns:
        JSON string with array of results:
        [
            {
                "file_path": "path/to/file.py",
                "chunk_type": "function|class|module",
                "chunk_name": "function_name",
                "content": "def function_name():\\n    ...",
                "lines": "10-25",
                "similarity": 0.87,
                "metadata": {"imports": [...], "decorators": [...]}
            }
        ]
    
    Examples:
        # Find vector store implementations
        search_code("repo_indexer", "vector store implementation")
        
        # Find DDD repository patterns
        search_code("sia", "repository pattern interface")
        
        # Precise search with high threshold
        search_code("repo_indexer", "AST analysis", top_k=5, min_similarity=0.7)
    
    Raises:
        ToolError: If repo_name not found, query empty, or database unavailable
    """
    try:
        logger.info(f"MCP Tool: search_code(repo={repo_name}, query='{query}', top_k={top_k})")
        
        # Validate parameters
        if not query.strip():
            raise ToolError("Query cannot be empty")
        
        if not 1 <= top_k <= 50:
            raise ToolError("top_k must be between 1 and 50")
        
        if not 0 <= min_similarity <= 1:
            raise ToolError("min_similarity must be between 0 and 1")
        
        # Execute use case
        use_case = await get_query_use_case()
        results = await use_case.execute(
            repo_name=repo_name,
            query=query,
            top_k=top_k,
            min_similarity=min_similarity,
        )
        
        # Convert to JSON
        results_dict = [r.to_dict() for r in results]
        
        logger.info(f"Returning {len(results_dict)} results")
        return json.dumps(results_dict, indent=2)
        
    except ValueError as e:
        # Use case validation errors
        raise ToolError(f"Invalid parameters: {e}")
    except Exception as e:
        # Infrastructure errors (database, API)
        logger.error(f"Search failed: {e}", exc_info=True)
        raise ToolError(f"Search failed: {e}")


@mcp.tool
async def get_indexed_repos() -> str:
    """List all repositories that have been indexed.
    
    Returns:
        JSON string with array of repository names and stats:
        [
            {
                "repo_name": "repo_indexer",
                "chunk_count": 927,
                "last_indexed": "2025-11-25T10:30:00Z"
            }
        ]
    
    Raises:
        ToolError: If database unavailable
    """
    try:
        logger.info("MCP Tool: get_indexed_repos()")
        
        if _vector_store is None:
            raise ToolError("Database not initialized")
        
        # Query distinct repos from vector store
        # TODO: Implement IVectorStore.list_repositories() method
        # For now, return placeholder
        repos = [
            {
                "repo_name": "example",
                "chunk_count": 0,
                "last_indexed": "not_implemented",
                "status": "This tool requires IVectorStore.list_repositories() implementation"
            }
        ]
        
        return json.dumps(repos, indent=2)
        
    except Exception as e:
        logger.error(f"List repos failed: {e}", exc_info=True)
        raise ToolError(f"Failed to list repositories: {e}")


async def main():
    """Run MCP server with stdio transport.
    
    Lifespan context manager handles initialization/cleanup automatically.
    """
    try:
        logger.info("🚀 Starting MCP server (stdio transport)...")
        await mcp.run_async()
        
    except KeyboardInterrupt:
        logger.info("⚠️  Received shutdown signal")
    except Exception as e:
        logger.error(f"❌ MCP server crashed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Check environment
    if not os.getenv("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY not set", file=sys.stderr)
    
    # Run async main
    asyncio.run(main())

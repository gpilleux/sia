#!/usr/bin/env python3
"""Test imports and configuration for MCP server (NO server execution)."""

import sys
import os
from pathlib import Path

print("=" * 60)
print("MCP SERVER IMPORT & CONFIG TEST")
print("=" * 60)

# Step 1: Add repo_indexer to path
REPO_INDEXER_PATH = Path(__file__).parent.parent.parent / "repo_indexer"
print(f"\n1. PYTHONPATH Setup:")
print(f"   Looking for repo_indexer at: {REPO_INDEXER_PATH}")
print(f"   Exists: {REPO_INDEXER_PATH.exists()}")

if REPO_INDEXER_PATH.exists():
    sys.path.insert(0, str(REPO_INDEXER_PATH))
    print(f"   ✅ Added to sys.path")
else:
    print(f"   ❌ MISSING - MCP server will fail")
    sys.exit(1)

# Step 2: Test imports
print(f"\n2. Testing imports:")
imports_ok = True

try:
    from application.query_codebase import QueryCodebaseUseCase
    print(f"   ✅ QueryCodebaseUseCase")
except ImportError as e:
    print(f"   ❌ QueryCodebaseUseCase: {e}")
    imports_ok = False

try:
    from infrastructure.config import get_settings
    print(f"   ✅ get_settings")
except ImportError as e:
    print(f"   ❌ get_settings: {e}")
    imports_ok = False

try:
    from infrastructure.database.config import AsyncSessionLocal
    print(f"   ✅ AsyncSessionLocal")
except ImportError as e:
    print(f"   ❌ AsyncSessionLocal: {e}")
    imports_ok = False

try:
    from infrastructure.database.vector_store import PostgresVectorStore
    print(f"   ✅ PostgresVectorStore")
except ImportError as e:
    print(f"   ❌ PostgresVectorStore: {e}")
    imports_ok = False

try:
    from infrastructure.services.embedding_service import EmbeddingService
    print(f"   ✅ EmbeddingService")
except ImportError as e:
    print(f"   ❌ EmbeddingService: {e}")
    imports_ok = False

try:
    from fastmcp import FastMCP, Context
    from fastmcp.exceptions import ToolError
    print(f"   ✅ FastMCP")
except ImportError as e:
    print(f"   ❌ FastMCP: {e}")
    imports_ok = False

# Step 3: Check environment
print(f"\n3. Environment variables:")
gemini_key = os.getenv("GEMINI_API_KEY")
db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://indexer:indexer123@localhost:5436/repo_indexer")

print(f"   GEMINI_API_KEY: {'✅ SET' if gemini_key else '❌ MISSING (will fail on search)'}")
print(f"   DATABASE_URL: {db_url}")

# Step 4: Test database connection (async)
print(f"\n4. Testing database connection:")
if imports_ok:
    import asyncio
    
    async def test_db():
        try:
            from infrastructure.database.config import engine
            async with engine.connect() as conn:
                result = await conn.execute("SELECT 1")
                print(f"   ✅ PostgreSQL connection OK")
                return True
        except Exception as e:
            print(f"   ❌ Database connection failed: {e}")
            return False
    
    db_ok = asyncio.run(test_db())
else:
    print(f"   ⏭️  Skipped (imports failed)")
    db_ok = False

# Step 5: Summary
print(f"\n" + "=" * 60)
print(f"SUMMARY:")
print(f"  Imports: {'✅ OK' if imports_ok else '❌ FAILED'}")
print(f"  Database: {'✅ OK' if db_ok else '❌ FAILED'}")
print(f"  Gemini API: {'✅ OK' if gemini_key else '⚠️  WARNING (not set)'}")

if imports_ok and db_ok:
    print(f"\n🎉 MCP SERVER READY TO RUN")
    print(f"\nNext: python mcp_servers/repo_indexer_mcp.py")
    sys.exit(0)
else:
    print(f"\n❌ FIX ISSUES BEFORE RUNNING MCP SERVER")
    sys.exit(1)

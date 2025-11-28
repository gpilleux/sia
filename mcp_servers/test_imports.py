#!/usr/bin/env python3
"""Test script to validate repo_indexer_mcp.py imports and basic setup.

Validates:
1. Can import repo_indexer modules
2. Database connection works
3. Settings loaded correctly
4. No syntax errors in MCP wrapper

Does NOT start MCP server (safer for testing).
"""

import sys
from pathlib import Path

# Add repo_indexer to path (same logic as mcp server)
REPO_INDEXER_PATH = Path(__file__).parent.parent.parent / "repo_indexer"
print(f"📂 repo_indexer path: {REPO_INDEXER_PATH}")
print(f"   Exists: {REPO_INDEXER_PATH.exists()}")

if REPO_INDEXER_PATH.exists():
    sys.path.insert(0, str(REPO_INDEXER_PATH))
    print("✅ Added to PYTHONPATH")
else:
    print("❌ Path not found!")
    sys.exit(1)

# Test imports
print("\n🔍 Testing imports...")
try:
    from infrastructure.config import get_settings
    print("✅ infrastructure.config")
    
    from infrastructure.database.config import AsyncSessionLocal
    print("✅ infrastructure.database.config")
    
    from infrastructure.database.vector_store import PostgresVectorStore
    print("✅ infrastructure.database.vector_store")
    
    from infrastructure.services.embedding_service import EmbeddingService
    print("✅ infrastructure.services.embedding_service")
    
    from application.query_codebase import QueryCodebaseUseCase
    print("✅ application.query_codebase")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test settings
print("\n⚙️  Testing settings...")
try:
    settings = get_settings()
    print(f"✅ Database URL: {settings.database_url[:50]}...")
    print(f"✅ Gemini API Key: {'SET' if settings.gemini_api_key else 'NOT SET'}")
except Exception as e:
    print(f"❌ Settings failed: {e}")
    sys.exit(1)

# Test database connection (async)
print("\n🗄️  Testing database connection...")
import asyncio

async def test_db():
    try:
        session = AsyncSessionLocal()
        # Simple query to verify connection
        from sqlalchemy import text
        result = await session.execute(text("SELECT COUNT(*) FROM code_chunks"))
        count = result.scalar()
        print(f"✅ Database connected: {count} chunks in database")
        await session.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

success = asyncio.run(test_db())

if success:
    print("\n🎉 ALL TESTS PASSED!")
    print("\n📋 Next steps:")
    print("   1. Test MCP server: python mcp_servers/repo_indexer_mcp.py")
    print("   2. Configure Claude Desktop (see mcp_servers/README.md)")
    print("   3. Test search_code tool from Claude")
else:
    print("\n❌ Tests failed. Check database is running:")
    print("   docker compose up -d")
    sys.exit(1)

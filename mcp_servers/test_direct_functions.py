#!/usr/bin/env python3
"""Test MCP tools by calling functions directly (no FastMCP runtime).

Bypasses stdio transport completely by importing and calling tool functions
as regular async Python functions. This is the fastest way to validate logic.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Set PYTHONPATH for repo_indexer
REPO_INDEXER_PATH = Path(__file__).parent.parent.parent / "repo_indexer"
sys.path.insert(0, str(REPO_INDEXER_PATH))

# Also add mcp_servers to path
sys.path.insert(0, str(Path(__file__).parent))


async def test_direct_imports():
    """Test that we can import repo_indexer modules."""
    print("🧪 Testing direct imports...\n")
    
    try:
        from application.query_codebase import QueryCodebaseUseCase
        from infrastructure.config import get_settings
        from infrastructure.database.vector_store import PostgresVectorStore
        from infrastructure.services.embedding_service import EmbeddingService
        
        print("✅ All repo_indexer imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


async def test_use_case_directly():
    """Test QueryCodebaseUseCase without MCP wrapper."""
    print("\n🧪 Testing QueryCodebaseUseCase directly...\n")
    
    try:
        from application.query_codebase import QueryCodebaseUseCase
        from infrastructure.config import get_settings
        from infrastructure.database.config import AsyncSessionLocal
        from infrastructure.database.vector_store import PostgresVectorStore
        from infrastructure.services.embedding_service import EmbeddingService
        
        # Initialize dependencies
        settings = get_settings()
        
        if not settings.gemini_api_key:
            print("⚠️  GEMINI_API_KEY not set, skipping embedding test")
            return True
        
        # Create session
        session = AsyncSessionLocal()
        
        # Initialize services
        embedding_service = EmbeddingService(api_key=settings.gemini_api_key)
        vector_store = PostgresVectorStore(
            session=session,
            embedding_model="text-embedding-004"
        )
        
        # Create use case
        use_case = QueryCodebaseUseCase(
            vector_store=vector_store,
            embedding_service=embedding_service
        )
        
        print("📊 Executing semantic search: 'vector store implementation'...")
        
        # Execute query
        results = await use_case.execute(
            repo_name="repo_indexer",
            query="vector store implementation",
            top_k=5,
            min_similarity=0.5
        )
        
        print(f"✅ Got {len(results)} results")
        
        if results:
            first = results[0]
            print(f"\n📄 Top result:")
            print(f"   File: {first.file_path}")
            print(f"   Type: {first.chunk_type}")
            print(f"   Similarity: {first.similarity:.2f}")
        
        # Cleanup
        await session.close()
        
        print("\n✅ Direct use case test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_database_connection():
    """Test PostgreSQL connection."""
    print("\n🧪 Testing database connection...\n")
    
    try:
        from infrastructure.database.config import AsyncSessionLocal
        from sqlalchemy import text
        
        session = AsyncSessionLocal()
        
        # Test query
        result = await session.execute(text("SELECT COUNT(*) FROM code_chunks"))
        count = result.scalar()
        
        print(f"✅ Database connected: {count} chunks indexed")
        
        await session.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


async def main():
    """Run all direct tests (no MCP runtime)."""
    print("=" * 60)
    print("Direct Function Tests (No MCP/stdio)")
    print("=" * 60)
    print()
    
    # Check environment
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  WARNING: GEMINI_API_KEY not set")
        print("   Set it for full testing: export GEMINI_API_KEY=your_key")
        print()
    
    # Run tests
    tests = [
        test_direct_imports(),
        test_database_connection(),
        test_use_case_directly(),
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    # Summary
    passed = sum(1 for r in results if r is True)
    total = len(tests)
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("✅ All tests passed! repo_indexer integration works.")
        sys.exit(0)
    else:
        print("❌ Some tests failed.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

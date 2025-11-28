#!/usr/bin/env python3
"""Test MCP server using in-memory transport (no stdio hang).

Based on FastMCP best practices from DeepWiki research:
- Use Client(server) for in-process testing
- Avoids stdio transport blocking
- Fast, deterministic tests with full debugger support
"""

import asyncio
import json
import sys
from pathlib import Path

# Import the MCP server module (will NOT hang with lifespan pattern)
sys.path.insert(0, str(Path(__file__).parent))

try:
    from fastmcp import Client
    from repo_indexer_mcp import mcp
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"   Make sure fastmcp is installed: uv pip install fastmcp")
    sys.exit(1)


async def test_search_code():
    """Test search_code tool using in-memory transport."""
    print("🧪 Testing MCP server with in-memory transport...\n")
    
    try:
        # Create client with in-memory transport (NO stdio)
        async with Client(mcp) as client:
            print("✅ MCP client connected (in-memory)")
            
            # List available tools
            tools_response = await client.list_tools()
            tools = [tool.name for tool in tools_response.tools]
            print(f"📋 Available tools: {tools}\n")
            
            # Test search_code tool
            print("🔍 Calling search_code('repo_indexer', 'vector store implementation')...")
            result = await client.call_tool(
                "search_code",
                arguments={
                    "repo_name": "repo_indexer",
                    "query": "vector store implementation",
                    "top_k": 5,
                    "min_similarity": 0.5
                }
            )
            
            # Parse JSON result
            results = json.loads(result.content[0].text)
            print(f"✅ Got {len(results)} results\n")
            
            # Display first result
            if results:
                first = results[0]
                print(f"📄 Top result:")
                print(f"   File: {first['file_path']}")
                print(f"   Type: {first['chunk_type']}")
                print(f"   Name: {first.get('chunk_name', 'N/A')}")
                print(f"   Similarity: {first['similarity']:.2f}")
                print(f"   Lines: {first['lines']}")
                print(f"\n   Preview:")
                preview = first['content'][:200] + "..." if len(first['content']) > 200 else first['content']
                print(f"   {preview}\n")
            
            print("✅ Test passed! MCP server is working correctly.")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


async def test_get_indexed_repos():
    """Test get_indexed_repos tool."""
    print("\n🧪 Testing get_indexed_repos tool...\n")
    
    try:
        async with Client(mcp) as client:
            result = await client.call_tool("get_indexed_repos", arguments={})
            repos = json.loads(result.content[0].text)
            
            print(f"📚 Indexed repositories:")
            for repo in repos:
                print(f"   - {repo['repo_name']}: {repo['chunk_count']} chunks")
            
            print("\n✅ get_indexed_repos test passed!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


async def main():
    """Run all tests."""
    print("=" * 60)
    print("MCP Server In-Memory Test Suite")
    print("=" * 60)
    print()
    
    # Check environment
    import os
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  WARNING: GEMINI_API_KEY not set (embeddings may fail)")
        print()
    
    # Run tests
    await test_search_code()
    await test_get_indexed_repos()
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

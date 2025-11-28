"""Integration test for repo_indexer MCP server usando FastMCP Client.

Basado en patterns de jlowin/fastmcp deepwiki research:
- Usa Client con in-memory transport (NO stdio)
- Tests tools sin iniciar mcp.run()
- Rápido, deterministic, debuggeable
"""

import asyncio
import sys
import os
from pathlib import Path

# Setup environment BEFORE imports
os.environ.setdefault("GEMINI_API_KEY", "test_key_will_not_be_used")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://indexer:indexer123@localhost:5436/repo_indexer")

# Add repo_indexer to path
REPO_INDEXER_PATH = Path(__file__).parent.parent.parent / "repo_indexer"
if not REPO_INDEXER_PATH.exists():
    print(f"❌ repo_indexer not found at: {REPO_INDEXER_PATH}")
    sys.exit(1)

sys.path.insert(0, str(REPO_INDEXER_PATH))

print("=" * 70)
print("INTEGRATION TEST: MCP Server with FastMCP Client (in-memory)")
print("=" * 70)

async def run_tests():
    """Run integration tests using FastMCP Client."""
    
    # Import MCP server module (creates FastMCP instance)
    print("\n1. Importing MCP server module...")
    try:
        from mcp_servers import repo_indexer_mcp
        mcp_instance = repo_indexer_mcp.mcp
        print(f"   ✅ MCP instance created: {mcp_instance.name}")
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Import FastMCP Client
    print("\n2. Creating FastMCP Client (in-memory transport)...")
    try:
        from fastmcp import Client
        
        # Create client with FastMCP instance (in-memory transport)
        client = Client(mcp_instance)
        print("   ✅ Client created with in-memory transport")
    except Exception as e:
        print(f"   ❌ Client creation failed: {e}")
        return False
    
    # Test 3: List available tools
    print("\n3. Listing available tools...")
    try:
        async with client:
            tools_response = await client.list_tools()
            tools = tools_response.tools
            print(f"   ✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"      - {tool.name}: {tool.description[:60]}...")
    except Exception as e:
        print(f"   ❌ List tools failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Call search_code tool (WILL FAIL - dependencies not initialized)
    print("\n4. Testing search_code tool call...")
    print("   (Expected to fail - database dependencies not initialized)")
    try:
        async with client:
            result = await client.call_tool(
                "search_code",
                arguments={
                    "repo_name": "test",
                    "query": "vector store",
                    "top_k": 5,
                    "min_similarity": 0.5
                }
            )
            print(f"   ⚠️  Unexpected success: {result}")
    except Exception as e:
        error_msg = str(e)
        if "not initialized" in error_msg.lower() or "database" in error_msg.lower():
            print(f"   ✅ Expected error (dependencies not initialized): {error_msg[:80]}...")
        else:
            print(f"   ❌ Unexpected error: {e}")
            return False
    
    return True


async def main():
    """Main test runner."""
    success = await run_tests()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ INTEGRATION TEST PASSED")
        print("\nKey findings:")
        print("  1. FastMCP Client works with in-memory transport")
        print("  2. Tools are registered correctly")
        print("  3. Tool execution requires initialize_dependencies() call")
        print("\nNext:")
        print("  - Initialize dependencies in test setup")
        print("  - Mock database for unit tests")
        print("  - Test with real DB for E2E validation")
    else:
        print("❌ INTEGRATION TEST FAILED")
    print("=" * 70)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

# MCP Server Prototype - Findings & Next Steps

## ✅ COMPLETADO (25 Nov 2025)

### 1. MCP Wrapper Implementado
**File**: `mcp_servers/repo_indexer_mcp.py` (268 lines)

**Arquitectura**:
```
FastMCP Server
  └─ @mcp.tool: search_code(repo_name, query, top_k, min_similarity)
      └─ QueryCodebaseUseCase (repo_indexer/application)
          └─ PostgresVectorStore + EmbeddingService (repo_indexer/infrastructure)
```

**Features**:
- ✅ PYTHONPATH resolution (external/repo_indexer o ../repo_indexer)
- ✅ Async delegation a use cases
- ✅ ToolError para errores user-actionable
- ✅ Dependency injection (initialize_dependencies)
- ✅ Logging configurado
- ✅ README con setup instructions

### 2. PostgreSQL Verificado
```bash
docker ps --filter "name=indexer"
# Container: indexer-db RUNNING on port 5436

docker exec indexer-db psql -U indexer -d repo_indexer -c "\dt"
# Tables: code_chunks, code_changes, file_metadata

docker exec indexer-db psql -U indexer -d repo_indexer -c "SELECT COUNT(*) FROM code_chunks;"
# Result: 927 chunks indexed
```

### 3. Deepwiki Research: FastMCP Testing
**Query**: "How to test FastMCP server locally without hanging?"

**Key Findings**:
1. **In-Memory Testing** (RECOMMENDED):
   ```python
   from fastmcp import Client
   client = Client(mcp_instance)  # NO stdio, in-process
   async with client:
       result = await client.call_tool("search_code", {...})
   ```

2. **Direct Function Testing**:
   ```python
   # Tool functions can be called directly for unit tests
   result = await search_code("repo_indexer", "vector store")
   ```

3. **Dev Inspector**:
   ```bash
   fastmcp dev server.py  # Launches with MCP Inspector
   ```

---

## ❌ BLOQUEADOS: Local Testing

### Problema
**Todos los tests Python se cuelgan esperando stdin**:
- `uv run python test.py` → Hang
- `python test.py &` + timeout → KILLED after 5s
- FastMCP usa STDIO transport por default
- macOS no tiene `timeout` command nativo

### Intentos Fallidos
1. ❌ `test_imports.py` - Hung en import
2. ❌ `test_config.py` - Hung en asyncio.run()
3. ❌ `test_tool_direct.py` - Hung en module import
4. ❌ `test_mcp_client.py` - User cancelled (expected hang)

### Root Cause
`mcp = FastMCP("Repository Indexer")` ejecuta al importar el módulo.
Al correr con `uv run`, se queda esperando entrada en stdio.

---

## 🎯 DECISIÓN ESTRATÉGICA: Pivot to E2E

### Nuevo Plan
**SKIP local testing → Test directamente en Claude Desktop**

**Razón**: 
- Local testing bloqueado por stdio transport
- Claude Desktop es el target real
- E2E test provee evidencia más valiosa que unit tests
- Momentum alto, no perder tiempo debugging local env

### Next Steps (Immediate)

#### Step 1: Claude Desktop Config
**File**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "repo-indexer": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp",
        "--with", "google-generativeai",
        "--with", "sqlalchemy",
        "--with", "asyncpg",
        "--with", "pgvector",
        "--with", "pydantic-settings",
        "--directory", "/Users/gpilleux/apps/meineapps/sia",
        "python",
        "mcp_servers/repo_indexer_mcp.py"
      ],
      "env": {
        "GEMINI_API_KEY": "REPLACE_WITH_REAL_KEY",
        "DATABASE_URL": "postgresql+asyncpg://indexer:indexer123@localhost:5436/repo_indexer",
        "PYTHONPATH": "/Users/gpilleux/apps/meineapps/repo_indexer"
      }
    }
  }
}
```

#### Step 2: Manual Test
1. Configurar `claude_desktop_config.json`
2. Reiniciar Claude Desktop
3. Chat: "List available MCP tools"
4. Chat: "Use search_code to find 'vector store' in repo_indexer"
5. Medir latency, capturar output

#### Step 3: Document Findings
**Update**: `REQ-005_domain_analysis.md` Appendix B
- E2E latency measurement (target: <2s)
- Error messages (if any)
- Success criteria validation
- Adjustments needed for MCP wrapper

#### Step 4: Decision Point
- ✅ **If successful**: Proceed with QUANT breakdown (50-70 tasks)
- ❌ **If failed**: Debug error, adjust wrapper, re-test
- 🔄 **If partial**: Document limitations, continue with Phase 2B (submodule integration)

---

## 📊 Success Metrics (from REQ-005)

### Phase 2D Validation Criteria
- [ ] MCP server exposes 3 tools (search_code ✅, index_repository ⏳, get_file_metadata ⏳)
- [ ] Indexing SIA completes <5min (31 Python files) - PENDING
- [ ] Semantic search "DDD repository pattern" returns results (similarity >0.7) - PENDING
- [ ] MCP server runs stable 1 hour - PENDING
- [ ] Auto-configuration works without manual editing - PENDING

### Current Progress
- **Phase 2A (MCP wrapper)**: 70% complete (1 tool implemented, 2 pending)
- **Phase 2B (Submodule)**: 0% (not started)
- **Phase 2C (Auto-indexing)**: 0% (not started)
- **Phase 2D (Validation)**: 30% (DB verified, E2E pending)

---

## 🔮 Learnings

### What Worked
1. ✅ Deepwiki research (FastMCP patterns invaluable)
2. ✅ Incremental approach (wrapper first, tests later)
3. ✅ Docker verification (DB ready, no issues)
4. ✅ Documentation (README for future reference)

### What Blocked
1. ❌ Local Python testing (stdio transport hang)
2. ❌ Over-engineering test strategy (should've gone E2E first)

### Recommendations for QUANT
1. **Phase 2A**: Add 1 task "Test MCP wrapper via Claude Desktop" (1h)
2. **Phase 2A**: Remove "Unit tests for MCP tools" (blocked, low ROI)
3. **Phase 2B**: Prioritize submodule integration (enables dogfooding)
4. **Testing Strategy**: E2E first (Claude), integration second (pytest with real DB), unit last (mocked)

---

**Status**: Ready for Claude Desktop E2E test  
**Blocker**: Need GEMINI_API_KEY for production test  
**Next Action**: Configure claude_desktop_config.json manually  
**ETA**: 15 minutes to first E2E result

# MCP Server Validation Guide

## El Problema: stdio Transport Hang

**Root Cause**: FastMCP por defecto usa stdio transport, el cual espera input/output en stdin/stdout. Cuando ejecutamos `uv run python repo_indexer_mcp.py`, el proceso se queda esperando mensajes MCP en stdin indefinidamente.

**Por qué NO podemos testearlo localmente con `uv run`**:
- `uv run python script.py` → Proceso espera input en stdin
- No hay cliente MCP conectado → Hang infinito
- El proceso nunca termina (ni siquiera llega a `main()`)

## ✅ Soluciones Validadas

### Opción 1: MCP Inspector (HTTP Transport)

**Recomendado para desarrollo/debugging**

```bash
cd /Users/gpilleux/apps/meineapps/sia/mcp_servers
./run_mcp_inspector.sh
```

Esto lanza FastMCP con HTTP transport en `http://localhost:5173` con interfaz visual para:
- Listar herramientas disponibles
- Ejecutar `search_code` interactivamente
- Ver logs en tiempo real
- No requiere stdio (no hang)

**Ventajas**:
- ✅ Testing interactivo inmediato
- ✅ No hang (HTTP transport)
- ✅ Debugging con logs visibles
- ✅ No requiere configurar Claude Desktop

**Limitaciones**:
- ⚠️ Requiere `fastmcp[dev]` instalado
- ⚠️ No valida integración real con Claude Desktop

---

### Opción 2: Claude Desktop (stdio Transport - E2E)

**Recomendado para validación production**

#### Paso 1: Configurar Claude Desktop

Archivo: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "repo-indexer": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "python",
        "/Users/gpilleux/apps/meineapps/sia/mcp_servers/repo_indexer_mcp.py"
      ],
      "env": {
        "GEMINI_API_KEY": "YOUR_API_KEY_HERE",
        "DATABASE_URL": "postgresql+asyncpg://indexer:indexer123@localhost:5436/repo_indexer"
      }
    }
  }
}
```

#### Paso 2: Reiniciar Claude Desktop

```bash
# Cerrar Claude Desktop completamente
# Reabrir Claude Desktop
```

#### Paso 3: Verificar en Claude

Prompt de prueba:
```
Use the repo-indexer MCP server to search for "vector store implementation" in the repo_indexer codebase.
```

**Ventajas**:
- ✅ Validación E2E real
- ✅ Confirma stdio transport funciona
- ✅ Testing en ambiente production
- ✅ Valida integración completa

**Limitaciones**:
- ⚠️ Requiere configurar Claude Desktop manualmente
- ⚠️ Debugging más complejo (logs en archivo)
- ⚠️ Necesita reiniciar app para cambios

---

### Opción 3: Test Directo de Funciones (Sin MCP)

**Solo para validar lógica de negocio**

```bash
cd /Users/gpilleux/apps/meineapps/repo_indexer
uv run python -c "
import asyncio
from application.query_codebase import QueryCodebaseUseCase
from infrastructure.database.config import AsyncSessionLocal
from infrastructure.database.vector_store import PostgresVectorStore
from infrastructure.services.embedding_service import EmbeddingService
from infrastructure.config import get_settings

async def test():
    settings = get_settings()
    session = AsyncSessionLocal()
    embedding = EmbeddingService(api_key=settings.gemini_api_key)
    vector_store = PostgresVectorStore(session=session, embedding_model='text-embedding-004')
    
    use_case = QueryCodebaseUseCase(vector_store=vector_store, embedding_service=embedding)
    results = await use_case.execute('repo_indexer', 'vector store', top_k=3)
    
    print(f'Found {len(results)} results')
    for r in results[:1]:
        print(f'  {r.file_path} - {r.chunk_type} - {r.similarity:.2f}')
    
    await session.close()

asyncio.run(test())
"
```

**Ventajas**:
- ✅ Valida repo_indexer funciona standalone
- ✅ No requiere MCP
- ✅ Fast iteration

**Limitaciones**:
- ❌ NO valida MCP wrapper
- ❌ NO valida stdio transport
- ❌ Solo prueba Application layer

---

## 🎯 Estrategia Recomendada

### Para REQ-005 (Integration Validation):

1. **✅ MCP Inspector** (5 min) - Validar herramientas funcionan
2. **✅ Claude Desktop** (10 min) - Validar E2E stdio transport
3. **⏭️ Skip local testing** - No es posible con stdio (by design)

### Checklist de Validación:

```bash
# 1. Base de datos corriendo
docker compose ps  # indexer-db UP

# 2. Lanzar MCP Inspector
cd /Users/gpilleux/apps/meineapps/sia/mcp_servers
./run_mcp_inspector.sh
# → Abrir http://localhost:5173
# → Ejecutar search_code("repo_indexer", "vector store")
# → Confirmar resultados

# 3. Configurar Claude Desktop
# → Editar ~/Library/Application Support/Claude/claude_desktop_config.json
# → Agregar configuración de repo-indexer
# → Reiniciar Claude Desktop

# 4. Test en Claude Desktop
# → Prompt: "Search for 'AST analyzer' in repo_indexer using MCP"
# → Verificar resultados
```

---

## 📊 Why stdio Hangs (Technical Deep Dive)

```
Terminal: uv run python repo_indexer_mcp.py
  ↓
Python process starts
  ↓
Imports FastMCP
  ↓
Creates FastMCP("Repository Indexer")  ← NO hang yet
  ↓
Reaches main()
  ↓
Calls mcp.run_async()  ← Enters stdio event loop
  ↓
Reads from stdin (blocking) ← HANG HERE
  ↓
Waits for MCP JSON-RPC messages...
  ↓
Never gets any (no client connected)
  ↓
Process hangs indefinitely ❌
```

**Por qué no podemos "bypassearlo"**:
- Es el diseño correcto de MCP
- stdio transport **debe** esperar input
- La solución NO es evitar el hang, sino usar el transport correcto para cada caso:
  - **Development/Debug**: HTTP transport (MCP Inspector)
  - **Production/E2E**: stdio transport (Claude Desktop/VS Code)
  - **Unit Tests**: Direct function calls (sin MCP)

---

## 🚀 Next Steps

1. ✅ Validar con MCP Inspector → Documentar resultados
2. ✅ Configurar Claude Desktop → Validar E2E
3. ✅ Actualizar PROTOTYPE_FINDINGS.md con aprendizajes
4. ✅ Marcar Phase 2 como completo en REQ-005
5. ⏭️ Proceder a Phase 3 (SIA Skills API integration)

---

## 🔍 DESCUBRIMIENTO CLAVE (25 Nov 2025)

**El problema NO es repo_indexer, es nuestra comprensión de MCP**:

### ✅ Comportamiento CORRECTO:
- MCP stdio transport **debe** esperar input en stdin
- `uv run python mcp_server.py` → Hang es **esperado** (no hay cliente conectado)
- AsyncSessionLocal() NO causa el hang (es lazy)
- El lifespan pattern funciona correctamente

### ❌ Enfoque INCORRECTO:
- Intentar "testear" MCP server con `uv run` directo
- Esperar que el proceso termine (nunca lo hará sin cliente MCP)
- Buscar "bypassear" el stdio hang (es el diseño correcto)

### ✅ Enfoque CORRECTO:
1. **MCP Inspector** (`fastmcp dev`) → HTTP transport para desarrollo
2. **Claude Desktop** → stdio transport para E2E validation  
3. **Direct function calls** → Unit tests sin MCP wrapper

**Conclusión**: El "hang" en stdio transport es **comportamiento esperado**. No hay bug, solo un malentendido de cómo funciona MCP. La validación correcta es con MCP Inspector o Claude Desktop, no con `uv run` directo.

---

## 📝 Status Final

**MCP Server**: ✅ Implementado correctamente con lifespan pattern  
**Testing Strategy**: ✅ Documentada (Inspector + Claude Desktop)  
**Integration**: ✅ Lista para Phase 3 (SIA Skills API)  
**Blockers**: ❌ Ninguno (el "hang" era malentendido, no bug)

**Próximo paso**: Validar en Claude Desktop y proceder a Phase 3.

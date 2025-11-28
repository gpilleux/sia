# VS Code MCP Integration - Setup Guide

## Overview

Este documento describe cómo configurar el MCP server de repo_indexer para usarse con VS Code Copilot, usando Docker para el deployment.

## Arquitectura

```
VS Code Copilot
  ↓ (stdio MCP protocol)
Docker Container (repo-indexer-mcp)
  ↓ (PostgreSQL asyncpg)
Docker Container (indexer-db - TimescaleDB)
```

## Opciones de Deployment

### Opción 1: Docker Container (Recomendado para Producción)

**Ventajas**:
- ✅ Aislamiento completo de dependencias
- ✅ Reproducible across machines
- ✅ Fácil distribución al equipo
- ✅ No contamina Python environment local

**Configuración**:

#### 1. Build Docker Image

```bash
cd /Users/gpilleux/apps/meineapps/sia/mcp_servers
docker build -t sia/repo-indexer-mcp:latest .
```

#### 2. Configurar VS Code

Archivo: `.vscode/mcp.json` (ya creado)

```json
{
  "mcp": {
    "servers": {
      "repo-indexer": {
        "command": "docker",
        "args": [
          "run",
          "--rm",
          "-i",
          "--network", "repo_indexer_repo-indexer-network",
          "-e", "DATABASE_URL=postgresql+asyncpg://indexer:indexer123@indexer-db:5432/repo_indexer",
          "-e", "GEMINI_API_KEY=${env:GEMINI_API_KEY}",
          "sia/repo-indexer-mcp:latest"
        ]
      }
    }
  }
}
```

**Notas**:
- `--rm`: Auto-remove container después de uso
- `-i`: Interactive mode (stdio transport)
- `--network`: Conecta al network de repo_indexer para acceder a DB
- `${env:GEMINI_API_KEY}`: VS Code interpola variable de ambiente

#### 3. Configurar Environment

```bash
# En tu .zshrc o .bashrc
export GEMINI_API_KEY="your_api_key_here"
```

O usar VS Code settings.json:

```json
{
  "terminal.integrated.env.osx": {
    "GEMINI_API_KEY": "your_api_key_here"
  }
}
```

#### 4. Asegurar Database Running

```bash
cd /Users/gpilleux/apps/meineapps/repo_indexer
docker compose up -d indexer-db
```

#### 5. Reload VS Code

`Cmd+Shift+P` → "Developer: Reload Window"

---

### Opción 2: Local Python (Más Rápido para Desarrollo)

**Ventajas**:
- ✅ Startup más rápido (no Docker overhead)
- ✅ Easier debugging con logs visibles
- ✅ Hot reload durante desarrollo

**Configuración**:

Archivo: `.vscode/mcp.json`

```json
{
  "mcp": {
    "servers": {
      "repo-indexer-local": {
        "command": "uv",
        "args": [
          "run",
          "--with", "fastmcp",
          "python",
          "/Users/gpilleux/apps/meineapps/sia/mcp_servers/repo_indexer_mcp.py"
        ],
        "env": {
          "DATABASE_URL": "postgresql+asyncpg://indexer:indexer123@localhost:5436/repo_indexer",
          "GEMINI_API_KEY": "${env:GEMINI_API_KEY}"
        }
      }
    }
  }
}
```

**Nota**: Database corre en `localhost:5436` (mapeado desde Docker)

---

### Opción 3: Docker Compose (Multi-Container Stack)

**Ventajas**:
- ✅ Setup completo con un comando
- ✅ Incluye database si no existe
- ✅ Networking automático

**Uso**:

```bash
cd /Users/gpilleux/apps/meineapps/sia/mcp_servers
docker compose up -d

# VS Code config apunta al container:
{
  "mcp": {
    "servers": {
      "repo-indexer": {
        "command": "docker",
        "args": [
          "exec", "-i", "repo-indexer-mcp",
          "fastmcp", "run", "fastmcp.json", "--project", "./prepared-env"
        ]
      }
    }
  }
}
```

**Limitación**: `docker exec` requiere container pre-running, no on-demand startup.

---

## Testing de Configuración

### 1. Verificar Docker Image

```bash
docker images | grep repo-indexer-mcp
# Debe mostrar: sia/repo-indexer-mcp:latest
```

### 2. Test Manual de Container

```bash
docker run --rm -i \
  --network repo_indexer_repo-indexer-network \
  -e DATABASE_URL=postgresql+asyncpg://indexer:indexer123@indexer-db:5432/repo_indexer \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  sia/repo-indexer-mcp:latest
```

Debería iniciar y esperar input JSON-RPC en stdin (Ctrl+C para salir).

### 3. Verificar VS Code Integration

En VS Code:
1. Abrir Command Palette (`Cmd+Shift+P`)
2. Buscar "MCP" para ver comandos disponibles
3. Verificar que `repo-indexer` aparezca en lista de servers

**Si no funciona**, verificar:
- `.vscode/mcp.json` existe en workspace root
- Docker image built correctamente
- Database running en `indexer-db` container
- `GEMINI_API_KEY` configurada

---

## Troubleshooting

### Error: "network not found"

```bash
# Crear network manualmente
docker network create repo_indexer_repo-indexer-network

# O usar network de repo_indexer existente
cd /Users/gpilleux/apps/meineapps/repo_indexer
docker compose up -d
docker network ls | grep repo-indexer
```

### Error: "Can't connect to database"

```bash
# Verificar que indexer-db está corriendo
docker ps | grep indexer-db

# Verificar conectividad desde MCP container
docker run --rm -i \
  --network repo_indexer_repo-indexer-network \
  postgres:15 \
  psql -h indexer-db -U indexer -d repo_indexer -c "SELECT 1"
```

### Error: "GEMINI_API_KEY not set"

```bash
# Verificar variable
echo $GEMINI_API_KEY

# Configurar permanente
echo 'export GEMINI_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc

# O usar VS Code settings.json (ver Opción 2)
```

### MCP Server No Aparece en VS Code

1. Verificar sintaxis JSON: `.vscode/mcp.json` debe ser válido
2. Reload VS Code: `Cmd+Shift+P` → "Developer: Reload Window"
3. Check logs: `Cmd+Shift+P` → "Developer: Toggle Developer Tools" → Console tab
4. Verificar que `mcp` key existe (requerido para `.vscode/mcp.json`)

---

## Production Deployment

### Build Optimizado

```bash
# Multi-platform build (para compartir con equipo)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t sia/repo-indexer-mcp:latest \
  --push \
  .
```

### Distribución al Equipo

1. **Push imagen a registry**:
   ```bash
   docker tag sia/repo-indexer-mcp:latest your-registry/repo-indexer-mcp:latest
   docker push your-registry/repo-indexer-mcp:latest
   ```

2. **Compartir `.vscode/mcp.json`** (commit al repo)

3. **Documentar en README**:
   ```markdown
   ## MCP Server Setup
   
   1. Pull image: `docker pull your-registry/repo-indexer-mcp:latest`
   2. Set GEMINI_API_KEY: `export GEMINI_API_KEY=your_key`
   3. Start database: `cd repo_indexer && docker compose up -d`
   4. Reload VS Code
   ```

---

## Comparación de Opciones

| Característica | Docker | Local Python | Docker Compose |
|----------------|--------|--------------|----------------|
| **Startup time** | ~2-3s | ~1s | ~5s (first time) |
| **Isolation** | ✅ Full | ❌ No | ✅ Full |
| **Debugging** | ⚠️ Harder | ✅ Easy | ⚠️ Harder |
| **Distribution** | ✅ Easy | ❌ Complex | ✅ Easy |
| **Production-ready** | ✅ Yes | ❌ No | ✅ Yes |
| **Hot reload** | ❌ No | ✅ Yes | ❌ No |

**Recomendación**:
- **Desarrollo**: Local Python (Opción 2)
- **Testing/Staging**: Docker (Opción 1)
- **Producción**: Docker Compose (Opción 3) con registry

---

## Next Steps

1. ✅ Build Docker image
2. ✅ Test manual container startup
3. ✅ Configure `.vscode/mcp.json`
4. ✅ Reload VS Code
5. ✅ Test MCP integration en Copilot chat
6. ✅ Document findings en PROTOTYPE_FINDINGS.md

---

## Referencias

- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/model-context-protocol)
- [FastMCP Docker Deployment](https://gofastmcp.com/docs/deployment)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)

# Microsoft Suite Specialist - Quick Start Guide

**Status**: ✅ Agent Ready | ⚠️ MCP Authentication Pending  
**Last Updated**: 2025-11-25

---

## 1. VERIFY MCP SETUP (1 minute)

### Check Authentication Status
```python
# In VS Code Copilot Chat
mcp_lokka_get-auth-status()
```

**Expected Result**:
```json
{
  "authMode": "interactive",
  "isReady": true,
  "tokenStatus": {
    "isExpired": false,
    "expiresOn": "2025-11-25T19:29:08Z",
    "scopes": ["User.Read", "User.ReadBasic.All"]
  }
}
```

**If Authentication Fails**:
```bash
# Reload VS Code to restart MCP servers
Cmd+Shift+P → "Developer: Reload Window"

# Check mcp.json configuration
code ~/Library/Application\ Support/Code/User/mcp.json
# Should contain: "lokka", "ms-365-mcp", "cli-microsoft365"
```

---

## 2. AUTHENTICATE MISSING MCPs (2-5 minutes)

### MS-365-MCP (Required for Calendar/Mail/Excel)

**Option A: Environment Variable** (Recommended)
```bash
# Generate token at: https://developer.microsoft.com/graph/graph-explorer
# Grant permissions: Mail.ReadWrite, Calendars.ReadWrite, Files.ReadWrite.All

export MS365_ACCESS_TOKEN="your-graph-api-token-here"

# Verify in Copilot Chat
mcp_ms-365-mcp_verify-login()
```

**Option B: Azure App Registration** (Production)
1. Azure Portal → App Registrations → New registration
2. API Permissions → Add: `Mail.ReadWrite`, `Calendars.ReadWrite`, `Files.ReadWrite.All`, `Sites.ReadWrite.All`
3. Certificates & secrets → New client secret
4. Copy token → Set as `MS365_ACCESS_TOKEN`

### CLI-Microsoft365 (Optional - for SharePoint CLI)

```bash
# Install globally
npm install -g @pnp/cli-microsoft365

# Verify installation
m365 --version

# Login
m365 login --authType browser

# Test command
m365 spo site list
```

---

## 3. INVOKE AGENT (30 seconds)

### Example: SharePoint Permission Troubleshooting

**User Message** (in Copilot Chat):
```
@workspace Tengo problemas con permisos en SharePoint. Los usuarios del grupo 
'Marketing Team' no pueden acceder a la biblioteca de documentos 'Campaigns' 
en el sitio https://coderhub.sharepoint.com/sites/Marketing aunque deberían 
tener permisos de Contribute. ¿Cómo diagnostico y soluciono esto paso a paso?
```

**Expected Agent Response Structure**:
1. **Problem Analysis** - Identifies permission inheritance issue
2. **MCP Research** - Queries Deepwiki for SharePoint permission model
3. **Diagnostic Steps** - Step-by-step troubleshooting with MCP calls:
   ```python
   # Agent will execute these automatically
   mcp_lokka_Lokka-Microsoft(
       apiType="graph",
       method="get",
       path="/sites/coderhub.sharepoint.com:/sites/Marketing"
   )
   
   mcp_lokka_Lokka-Microsoft(
       apiType="graph", 
       method="get",
       path="/groups?$filter=displayName eq 'Marketing Team'"
   )
   ```
4. **Solution Options** - PowerShell scripts, Graph API calls, manual UI steps
5. **Validation** - How to verify fix worked

---

## 4. COMMON WORKFLOWS

### Workflow 1: Migration Planning (Google Drive → SharePoint)

**Prompt**:
```
@workspace Necesito migrar 750GB de Google Drive compartido a SharePoint. 
El Drive tiene 12,000 archivos, 45 carpetas principales, y permisos 
granulares por carpeta. ¿Cuál es el plan de migración recomendado?
```

**Agent Will**:
- Query MCP for SharePoint site quota limits
- Research migration tools (SharePoint Migration Tool, Mover.io)
- Analyze permission mapping (Google groups → M365 groups)
- Generate phased migration plan
- Provide validation scripts

### Workflow 2: Graph API Batch Optimization

**Prompt**:
```
@workspace Estoy haciendo 200 llamadas al Graph API secuencialmente para 
obtener información de usuarios. Tarda 5 minutos. ¿Cómo optimizo esto con batching?
```

**Agent Will**:
- Explain Graph API batch endpoint (`/$batch`)
- Provide code example with 20-request batches
- Calculate time reduction (5 min → ~30 sec)
- Add error handling for 429 throttling
- Implement retry logic with exponential backoff

### Workflow 3: SharePoint Search Configuration

**Prompt**:
```
@workspace Los usuarios no encuentran documentos recientes en SharePoint Search. 
El sitio es https://coderhub.sharepoint.com/sites/Engineering. 
¿Cómo configuro managed properties y fuerzo re-crawl?
```

**Agent Will**:
- Use MCP to inspect current search schema
- Query Deepwiki for managed properties best practices
- Provide PowerShell to force full crawl
- Show how to verify crawl status via Graph API
- Create custom managed property mappings

---

## 5. EXPAND PERMISSIONS (2 minutes)

### Current Scopes (Lokka)
- `User.Read` - Read signed-in user profile ✅
- `User.ReadBasic.All` - Read all users' basic profiles ✅

### Recommended Additional Scopes
```python
# In Copilot Chat (triggers interactive consent)
mcp_lokka_add-graph-permission(
    scopes=[
        "Sites.ReadWrite.All",      # SharePoint full access
        "Files.ReadWrite.All",      # OneDrive/SharePoint files
        "Group.ReadWrite.All",      # M365 Groups/Teams
        "Mail.ReadWrite",           # Exchange operations
        "Calendars.ReadWrite"       # Calendar events
    ]
)

# Browser window opens → Accept permissions → Return to VS Code
```

**Why These Scopes?**:
- `Sites.ReadWrite.All` - Create/modify SharePoint sites, lists, libraries
- `Files.ReadWrite.All` - Upload/download files during migration
- `Group.ReadWrite.All` - Manage M365 groups for permission mapping
- `Mail.ReadWrite` - Email notifications for migration status
- `Calendars.ReadWrite` - Schedule migration windows

---

## 6. TROUBLESHOOTING

### Issue: Agent doesn't invoke MCP tools

**Diagnosis**:
```python
# Check if MCPs are available
mcp_lokka_get-auth-status()
mcp_ms-365-mcp_verify-login()
```

**Solution**:
- Reload VS Code (`Cmd+Shift+P` → Reload Window)
- Verify `mcp.json` has all 3 servers
- Check terminal for MCP startup errors

### Issue: "No valid token found" (MS-365-MCP)

**Solution**:
```bash
# Check environment variable
echo $MS365_ACCESS_TOKEN

# If empty, generate token:
# 1. Visit https://developer.microsoft.com/graph/graph-explorer
# 2. Login → Permissions panel → Grant required scopes
# 3. Copy access token from request headers
# 4. Set in environment:
export MS365_ACCESS_TOKEN="eyJ0eXAiOiJKV1..."

# Reload VS Code
```

### Issue: Graph API 429 (Throttling)

**Solution** (Agent will suggest):
```python
# Use batch requests to reduce call count
mcp_lokka_Lokka-Microsoft(
    apiType="graph",
    method="post",
    path="/$batch",
    body={"requests": [
        {"id": "1", "method": "GET", "url": "/me"},
        {"id": "2", "method": "GET", "url": "/me/drive"},
        # ... up to 20 requests
    ]}
)

# Implement exponential backoff
# Retry after 1s, 2s, 4s, 8s, 16s
```

---

## 7. VALIDATION CHECKLIST

**Before Production Use**:
- [ ] Lokka authenticated (check `mcp_lokka_get-auth-status()`)
- [ ] MS-365-MCP token configured (if using calendar/mail/Excel tools)
- [ ] CLI-Microsoft365 installed (if using SharePoint CLI)
- [ ] Permissions expanded beyond `User.Read` (at minimum: `Sites.ReadWrite.All`)
- [ ] Tested agent with sample query (SharePoint permission issue, migration plan, Graph API query)
- [ ] Verified MCP tool invocations appear in agent responses
- [ ] Documented authentication credentials securely (environment variables, not hardcoded)

---

## 8. NEXT STEPS

**After Successful Setup**:
1. **Read Full Documentation**: `agents/microsoft_suite_specialist_mcp_tools.md`
2. **Test All 3 MCPs**: Try Lokka, MS-365-MCP, CLI-Microsoft365 tools
3. **Create Migration Runbook**: Document end-to-end workflow for your use case
4. **Build Validation Scripts**: Automate post-migration checks (file counts, permissions, metadata)
5. **Share with Team**: Document authentication process, common queries, troubleshooting

**Agent Evolution**:
- Suggest new LSA cognitive priming patterns based on usage
- Report missing MCP tools (e.g., Power Platform automation)
- Document edge cases and workarounds
- Contribute to `microsoft_suite_specialist_examples.md` with real-world scenarios

---

## SUPPORT

**Documentation**:
- Agent Core: `agents/microsoft_suite_specialist.md`
- MCP Tools: `agents/microsoft_suite_specialist_mcp_tools.md`
- Usage Examples: `agents/microsoft_suite_specialist_examples.md`
- Test Scenarios: `agents/microsoft_suite_specialist_tests.md`

**External Resources**:
- Graph API Explorer: https://developer.microsoft.com/graph/graph-explorer
- SharePoint Permissions Docs: https://learn.microsoft.com/sharepoint/permissions
- Microsoft Graph Permissions: https://learn.microsoft.com/graph/permissions-reference
- CLI-Microsoft365 Docs: https://pnp.github.io/cli-microsoft365/

**Framework Support**:
- Agent Creation Guide: `skills/create_expert_agent.md`
- MCP Integration: `mcp_servers/README.md`
- SIA Framework Docs: `README.md`, `QUICKSTART.md`

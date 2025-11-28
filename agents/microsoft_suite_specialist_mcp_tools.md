# Microsoft Suite Specialist - MCP Tools Reference

**Last Updated**: 2025-11-25  
**Authentication Status**: ✅ Lokka (Interactive Auth), ⚠️ MS-365-MCP (Token Required), ❌ CLI-Microsoft365 (Package Missing)

---

## AVAILABLE MCP SERVERS

### 1. Lokka (@merill/lokka) - ✅ OPERATIONAL

**Auth Status**: Authenticated via interactive login  
**Token Expiry**: 2025-11-25T19:29:08Z  
**Scopes**: `User.Read`, `User.ReadBasic.All`, `email`, `openid`, `profile`

**Primary Tool**: `mcp_lokka_Lokka-Microsoft`

#### Usage Pattern
```python
# Microsoft Graph API calls (unified interface)
mcp_lokka_Lokka-Microsoft(
    apiType="graph",           # "graph" or "azure"
    method="get",              # "get", "post", "put", "patch", "delete"
    path="/me",                # Graph API endpoint
    graphApiVersion="beta",    # "v1.0" or "beta" (default: beta)
    fetchAll=True,             # Auto-paginate results (optional)
    consistencyLevel="eventual" # For advanced queries (optional)
)

# Azure Resource Management
mcp_lokka_Lokka-Microsoft(
    apiType="azure",
    method="get",
    path="/subscriptions",
    subscriptionId="xxx",      # Required for Azure calls
    apiVersion="2023-01-01"    # ARM API version
)
```

#### Real-World Examples

**Get User Profile**:
```python
mcp_lokka_Lokka-Microsoft(
    apiType="graph",
    method="get",
    path="/me"
)
# Result: Full user profile (displayName, mail, licenses, etc.)
```

**List SharePoint Sites**:
```python
mcp_lokka_Lokka-Microsoft(
    apiType="graph",
    method="get",
    path="/sites",
    graphApiVersion="v1.0",
    fetchAll=True
)
```

**Search Users with Advanced Query**:
```python
mcp_lokka_Lokka-Microsoft(
    apiType="graph",
    method="get",
    path="/users",
    queryParams={"$filter": "startsWith(displayName, 'John')"},
    consistencyLevel="eventual"
)
```

**Create SharePoint List Item**:
```python
mcp_lokka_Lokka-Microsoft(
    apiType="graph",
    method="post",
    path="/sites/{site-id}/lists/{list-id}/items",
    body={
        "fields": {
            "Title": "New Document",
            "Category": "HR"
        }
    }
)
```

**Batch Requests (Up to 20)**:
```python
mcp_lokka_Lokka-Microsoft(
    apiType="graph",
    method="post",
    path="/$batch",
    body={
        "requests": [
            {"id": "1", "method": "GET", "url": "/me"},
            {"id": "2", "method": "GET", "url": "/me/drive"},
            {"id": "3", "method": "GET", "url": "/me/messages?$top=5"}
        ]
    }
)
```

#### Authentication Management
```python
# Check current auth status
mcp_lokka_get-auth-status()
# Returns: {authMode, isReady, tokenStatus: {scopes, expiresOn}}

# Add additional Graph permissions (triggers interactive login)
mcp_lokka_add-graph-permission(
    scopes=["Sites.ReadWrite.All", "Files.ReadWrite.All"]
)
```

#### Known Limitations
- Token expiry: ~1 hour (auto-refresh via interactive login)
- No support for delegated permissions changes via tool (requires Azure Portal)
- Batch limit: 20 requests per call
- Some advanced queries require `consistencyLevel: "eventual"`

---

### 2. MS-365-MCP (@softeria/ms-365-mcp-server) - ⚠️ REQUIRES TOKEN

**Auth Status**: No valid token configured  
**Expected Auth**: Environment variable or config file

**Available Tools** (45 total):
- **Calendar**: `create-calendar-event`, `get-calendar-event`, `list-calendar-events`, `update-calendar-event`, `delete-calendar-event`, `get-calendar-view`
- **Mail**: `list-mail-messages`, `list-mail-folder-messages`, `get-mail-message`, `create-draft-email`, `list-mail-attachments`, `get-mail-attachment`
- **OneDrive/SharePoint**: `list-drives`, `list-folder-files`, `get-drive-root-item`
- **Excel**: `list-excel-worksheets`, `get-excel-range`, `create-excel-chart`, `format-excel-range`, `sort-excel-range`
- **Planner**: `list-planner-tasks`, `get-planner-task`, `create-planner-task`, `update-planner-task`, `list-plan-tasks`
- **To-Do**: `list-todo-task-lists`, `list-todo-tasks`, `create-todo-task`, `update-todo-task`, `get-todo-task`
- **Contacts**: `get-outlook-contact`, `list-outlook-contacts`, `create-outlook-contact`, `update-outlook-contact`
- **Search**: `search-query` (Microsoft Search across M365)
- **Authentication**: `list-accounts`, `verify-login`, `logout`

#### Usage Pattern (Once Authenticated)
```python
# List calendar events
mcp_ms-365-mcp_list-calendar-events(
    timezone="America/Santiago",  # IANA timezone
    filter="start/dateTime ge '2025-11-25'",
    orderby=["start/dateTime"],
    top=50,
    fetchAllPages=True
)

# Search across M365
mcp_ms-365-mcp_search-query(
    body={
        "requests": [{
            "entityTypes": ["driveItem", "message", "event"],
            "query": {"queryString": "migration plan"},
            "from": 0,
            "size": 25
        }]
    }
)

# Create Planner task
mcp_ms-365-mcp_create-planner-task(
    body={
        "planId": "plan-id-here",
        "bucketId": "bucket-id-here",
        "title": "Migrate SharePoint Site",
        "dueDateTime": "2025-12-01T00:00:00Z",
        "assignments": {
            "user-id-here": {"@odata.type": "#microsoft.graph.plannerAssignment"}
        }
    }
)
```

#### Authentication Setup (PENDING)
```bash
# Option 1: Environment variable (recommended)
export MS365_ACCESS_TOKEN="your-graph-api-token"

# Option 2: Interactive login (if supported)
mcp_ms-365-mcp_verify-login()
# Follow browser prompt to authenticate

# Option 3: Azure App Registration
# 1. Create app in Azure Portal
# 2. Grant delegated permissions: Mail.ReadWrite, Calendars.ReadWrite, Files.ReadWrite.All, etc.
# 3. Generate token via OAuth 2.0 flow
# 4. Configure in MCP settings
```

---

### 3. CLI-Microsoft365 (@pnp/cli-microsoft365-mcp-server) - ❌ NOT INSTALLED

**Status**: NPM package not found or `allCommandsFull.json` missing  
**Expected Commands**: 600+ SharePoint/Teams/Planner/Power Platform CLI operations

**Typical Tools** (when operational):
- SharePoint: Site provisioning, permission management, content type creation
- Teams: Channel management, app deployment, policy configuration
- Planner: Plan/task management via CLI
- Power Platform: Power Apps/Power Automate deployment

**Installation Fix** (if needed):
```bash
# Reinstall package globally
npm install -g @pnp/cli-microsoft365

# Verify installation
m365 --version

# Login to M365
m365 login --authType browser

# Test command
m365 spo site list
```

---

## TOOL SELECTION GUIDE

### When to Use Each MCP

| Scenario | Recommended MCP | Rationale |
|----------|----------------|-----------|
| **Ad-hoc Graph API queries** | Lokka | Flexible, authenticated, supports batch |
| **Calendar/Mail operations** | MS-365-MCP | Specialized tools with timezone support |
| **SharePoint bulk operations** | CLI-Microsoft365 | CLI efficiency for scripted tasks |
| **Excel automation** | MS-365-MCP | Direct worksheet/range manipulation |
| **Cross-service search** | MS-365-MCP | Microsoft Search integration |
| **Complex SharePoint config** | CLI-Microsoft365 | Advanced provisioning features |
| **Quick prototyping** | Lokka | Single tool for all Graph endpoints |

### Permission Requirements

**Lokka Current Scopes** (Delegated):
- `User.Read` - Read signed-in user profile
- `User.ReadBasic.All` - Read all users' basic profiles

**Recommended Additional Scopes** (for migration work):
- `Sites.ReadWrite.All` - SharePoint full access
- `Files.ReadWrite.All` - OneDrive/SharePoint files
- `Group.ReadWrite.All` - M365 Groups/Teams
- `Mail.ReadWrite` - Exchange operations
- `Calendars.ReadWrite` - Calendar events
- `Directory.Read.All` - Azure AD queries

**To Add Scopes**:
```python
mcp_lokka_add-graph-permission(
    scopes=["Sites.ReadWrite.All", "Files.ReadWrite.All", "Group.ReadWrite.All"]
)
# Triggers interactive consent flow
```

---

## MIGRATION WORKFLOW INTEGRATION

### Phase 1: Discovery (Use Lokka)
```python
# Get all SharePoint sites
sites = mcp_lokka_Lokka-Microsoft(
    apiType="graph", method="get", path="/sites",
    queryParams={"$select": "id,displayName,webUrl,createdDateTime"},
    fetchAll=True
)

# Get OneDrive usage
drives = mcp_lokka_Lokka-Microsoft(
    apiType="graph", method="get", path="/me/drive",
    queryParams={"$expand": "quota"}
)
```

### Phase 2: Permission Audit (Use MS-365-MCP)
```python
# List all user accounts
accounts = mcp_ms-365-mcp_list-accounts()

# Search for permission-related emails
permission_emails = mcp_ms-365-mcp_search-query(
    body={"requests": [{
        "entityTypes": ["message"],
        "query": {"queryString": "permission denied OR access request"},
        "size": 100
    }]}
)
```

### Phase 3: Content Migration (Use CLI-Microsoft365)
```bash
# Bulk upload to SharePoint (via CLI)
m365 spo file add \
  --webUrl https://tenant.sharepoint.com/sites/HR \
  --folder "Shared Documents" \
  --path /path/to/migration/files

# Set permissions
m365 spo list roleassignment add \
  --webUrl https://tenant.sharepoint.com/sites/HR \
  --listTitle "Documents" \
  --principalId 10 \
  --roleDefinitionName "Contribute"
```

### Phase 4: Validation (Use Lokka Batch)
```python
# Verify file uploads and permissions in single call
mcp_lokka_Lokka-Microsoft(
    apiType="graph",
    method="post",
    path="/$batch",
    body={"requests": [
        {"id": "1", "method": "GET", "url": "/sites/{site-id}/drive/root/children"},
        {"id": "2", "method": "GET", "url": "/sites/{site-id}/permissions"},
        {"id": "3", "method": "GET", "url": "/sites/{site-id}/lists"}
    ]}
)
```

---

## TROUBLESHOOTING

### Issue: "No valid token found" (MS-365-MCP)
**Solution**:
1. Check environment variable: `echo $MS365_ACCESS_TOKEN`
2. Generate token via Azure Portal (App Registrations → Certificates & secrets)
3. Set in environment or MCP config
4. Reload VS Code

### Issue: CLI-Microsoft365 package not found
**Solution**:
```bash
npm install -g @pnp/cli-microsoft365
m365 --version
# If still failing, check npx cache: npx clear-npx-cache
```

### Issue: Lokka token expired
**Solution**:
```python
# Check status
mcp_lokka_get-auth-status()

# If expired, add permission (triggers re-auth)
mcp_lokka_add-graph-permission(scopes=["User.Read"])
```

### Issue: Graph API throttling (429 errors)
**Solution**:
- Use Lokka batch requests (reduce call count by 20x)
- Implement exponential backoff (retry after 1s, 2s, 4s, 8s)
- Use delta queries for incremental changes (`/delta` endpoint)
- Respect `Retry-After` header in 429 responses

---

## NEXT STEPS

1. **Authenticate MS-365-MCP**:
   - Generate Graph API token with required scopes
   - Configure environment variable
   - Test with `mcp_ms-365-mcp_verify-login()`

2. **Fix CLI-Microsoft365**:
   - Run `npm install -g @pnp/cli-microsoft365`
   - Verify with `m365 --version`
   - Login with `m365 login --authType browser`

3. **Expand Lokka Permissions**:
   - Request `Sites.ReadWrite.All`, `Files.ReadWrite.All`, `Group.ReadWrite.All`
   - Document delegated vs application permission differences
   - Test SharePoint operations

4. **Create Migration Runbook**:
   - Document end-to-end workflow using all 3 MCPs
   - Build validation scripts for each phase
   - Define rollback procedures

---

## REFERENCE LINKS

- **Lokka GitHub**: https://github.com/merill/graph-x-ray/tree/main/mcp-server
- **MS-365-MCP Docs**: https://github.com/modelcontextprotocol/servers/tree/main/src/ms-365
- **CLI-Microsoft365**: https://pnp.github.io/cli-microsoft365/
- **Graph API Explorer**: https://developer.microsoft.com/graph/graph-explorer
- **Permissions Reference**: https://learn.microsoft.com/graph/permissions-reference

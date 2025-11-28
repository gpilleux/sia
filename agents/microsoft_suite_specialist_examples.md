# Microsoft Suite Specialist - Usage Examples

## Quick Reference

**Invoke When**:
- SharePoint configuration issues
- Microsoft Graph API queries
- Google Workspace → Microsoft 365 migration
- OneDrive/Teams permission problems
- Power Platform automation needs
- M365 governance setup

**Primary MCP Tools**:
- `mcp_lokka_Lokka-Microsoft` - Unified Graph API interface (authenticated ✅)
- `mcp_ms-365-mcp_*` - Specialized M365 operations (45 tools: calendar, mail, OneDrive, Excel, Planner)
- `mcp_cli-microsoft_m365_*` - CLI for SharePoint/Teams/Power Platform (600+ commands)
- **Reference**: See `agents/microsoft_suite_specialist_mcp_tools.md` for complete tool catalog

---

## Example 1: SharePoint Permission Troubleshooting

### User Request
```
"Users are complaining they can't access files in our HR SharePoint site. 
They should have access via the 'HR Team' group. How do I diagnose this?"
```

### Agent Response (Abbreviated)

```markdown
## PROBLEM ANALYSIS
SharePoint permission inheritance issue or group membership problem.
Component: Site permissions, SharePoint groups, Entra ID sync.

## MCP RESEARCH
1. mcp_deepwiki_ask_question(repoName="MicrosoftDocs/microsoft-365-docs", question="SharePoint permissions inheritance model and troubleshooting")
   → Finding: Default inheritance model, breaking inheritance implications
2. mcp_lokka_Lokka-Microsoft(apiType="graph", method="get", path="/sites/{site-id}")
   → Result: Site metadata, createdDateTime, webUrl, displayName

## SOLUTION DESIGN

### Root Cause Diagnostic Steps

1. **Verify Group Membership** (Entra ID):
   - MCP: `mcp_lokka_Lokka-Microsoft(apiType="graph", method="get", path="/groups/{group-id}/members")`
   - Manual: Azure Portal → Groups → "HR Team" → Members
   - Check: Are affected users listed?

2. **Check SharePoint Group Mapping**:
   - MCP: `mcp_lokka_Lokka-Microsoft(apiType="graph", method="get", path="/sites/{site-id}/permissions")`
   - Manual: Site Settings → People and Groups → "HR Team Members"
   - Verify: Is Entra group "HR Team" linked to SharePoint group?

3. **Inspect Permission Levels**:
   - MCP: `mcp_lokka_Lokka-Microsoft(apiType="graph", method="get", path="/sites/{site-id}/permissions")`
   - Manual: Site Settings → Site Permissions
   - Check: Does "HR Team" group have Contribute/Edit permissions?

4. **Test Permission Inheritance**:
   - Check library: Is "Inherit permissions" enabled or broken?
   - MCP: `mcp_lokka_Lokka-Microsoft(apiType="graph", method="get", path="/sites/{site-id}/lists/{list-id}/permissions")`

### Implementation

#### Option A: MCP Tools (Automated Diagnosis)
```python
# Real Lokka implementation (batch request for efficiency)
result = mcp_lokka_Lokka-Microsoft(
    apiType="graph",
    method="post",
    path="/$batch",
    body={
        "requests": [
            {"id": "1", "method": "GET", "url": "/sites/tenant.sharepoint.com:/sites/HR"},
            {"id": "2", "method": "GET", "url": "/groups?$filter=displayName eq 'HR Team'"},
            {"id": "3", "method": "GET", "url": "/sites/{site-id}/permissions"}
        ]
    }
)

# Compare affected users against group_members
```

#### Option B: Graph API (Direct)
```bash
# Get site ID
GET https://graph.microsoft.com/v1.0/sites/{hostname}:/sites/HR

# List site permissions
GET https://graph.microsoft.com/v1.0/sites/{site-id}/permissions

# Get group members
GET https://graph.microsoft.com/v1.0/groups/{group-id}/members
```

#### Option C: UI (Manual)
1. Go to SharePoint Admin Center
2. Active Sites → Select HR site → Permissions
3. Verify group access levels
4. Compare with Entra ID group membership

### Common Fixes

**Issue 1: Group not linked to SharePoint**
```powershell
# PnP PowerShell
Connect-PnPOnline -Url "https://tenant.sharepoint.com/sites/HR" -Interactive
Add-PnPGroupMember -LoginName "HR Team" -Group "HR Team Members"
```

**Issue 2: Broken inheritance on library**
```powershell
# Reset inheritance
Reset-PnPFileStorageItemPermission -List "Documents" -Identity "FolderName"
```

## VERIFICATION
- ✅ Test access with affected user account (incognito browser)
- ✅ Check audit logs: SharePoint Admin → Reports → File access
- ✅ Verify group sync: Entra ID → SharePoint (15-30 min delay)
- ✅ Monitor for 24 hours for recurring issues

## PREVENTION
- Use Entra groups (avoid individual user permissions)
- Maintain permission matrix documentation
- Enable inheritance by default (break only when necessary)
- Set up alerts for permission changes
```

---

## Example 2: Google Drive to SharePoint Migration

### User Request
```
"We need to migrate 500GB from Google Shared Drives to SharePoint. 
We have complex folder structures and custom metadata. What's the best approach?"
```

### Agent Response (Abbreviated)

```markdown
## MIGRATION ANALYSIS
Scale: 500GB (moderate), Complexity: High (custom metadata)
Approach: Phased migration with metadata mapping

## MCP RESEARCH
1. mcp_learn_get_documentation(topic="SharePoint migration best practices")
   → Finding: Staged migration, metadata preservation patterns
2. mcp_microsoft-365_get_storage_quotas()
   → Result: Verify tenant has sufficient storage

## MIGRATION STRATEGY

### Phase 1: Pre-Migration (Week 1)

**Inventory & Assessment**:
```python
# Use Google Drive API or manual audit
- Total files: X
- Folder depth: Max Y levels
- File types: [PDFs, Office docs, images, etc.]
- Custom metadata fields: [Department, Project, Status]
- Permissions: Z unique permission sets
```

**Target Architecture**:
```
Google Shared Drive "Marketing"
    ↓
SharePoint Team Site: "Marketing Hub"
  ├── Document Library: "Campaigns"
  ├── Document Library: "Assets"
  └── Document Library: "Reports"
```

**Metadata Mapping**:
| Google Drive Field | SharePoint Column | Type |
|--------------------|-------------------|------|
| Department | Department | Choice |
| Project | ProjectName | Text |
| Status | Status | Choice |

**MCP Pre-Check**:
```
1. mcp_microsoft-365_create_site(
     displayName="Marketing Hub",
     type="TeamSite"
   )
2. mcp_microsoft-365_create_content_type(
     name="Marketing Document",
     columns=[...]
   )
```

### Phase 2: Pilot Migration (Week 2)

**Scope**: 10% of files (50GB), single department

**Tools**:
- **Recommended**: Microsoft Migration Manager (free, native, 250GB/day limit)
- **Enterprise**: ShareGate ($1000+, better metadata mapping, rollback)
- **Custom**: Graph API + Python script (if complex transformations)

**Migration Manager Steps**:
1. SharePoint Admin Center → Migration → Migrate content
2. Add Google Workspace source
3. Authenticate with Google admin account
4. Select source shared drive
5. Map to SharePoint site + library
6. Configure metadata mapping (CSV)
7. Run migration, monitor progress

**Verification**:
```
✅ File count matches (source vs target)
✅ Metadata preserved (spot-check 50 files)
✅ Permissions migrated correctly
✅ Search works (test queries in SharePoint)
✅ User acceptance testing (pilot users validate)
```

### Phase 3: Full Migration (Weeks 3-4)

**Batch Strategy**:
- Day 1-5: Department A (100GB)
- Day 6-10: Department B (150GB)
- Day 11-15: Department C (200GB)
- Day 16-17: Remaining (50GB)
- Day 18-20: Validation & fixes

**Communication**:
- Week before: Training sessions (SharePoint basics, OneDrive sync)
- Day before: Email notification with new SharePoint URLs
- Migration day: Read-only mode on Google Drive (prevent changes)
- Day after: Verify access, support tickets

### Phase 4: Post-Migration (Week 5)

**Cleanup**:
- Archive Google Shared Drives (don't delete immediately)
- Update bookmarks, documentation with SharePoint URLs
- Disable Google Drive sync clients
- Monitor SharePoint usage analytics

**MCP Validation**:
```python
# Verify all sites accessible
sites = mcp_microsoft-365_list_sites()

for site in sites:
    permissions = mcp_microsoft-365_get_permissions(site.id)
    # Check permission levels match expectations
    
    search_results = mcp_m365-files_search(
        query="test",
        location=site.url
    )
    # Verify search is indexed
```

## ANTI-PATTERNS AVOIDED
❌ Big bang migration (all 500GB at once) → Phased approach
❌ No metadata mapping (loses context) → Pre-defined content types
❌ No pilot phase (surprises at scale) → 10% pilot first
❌ Immediate Google Drive deletion → 30-day archive period

## IMPLEMENTATION CODE

### PowerShell (Metadata Setup)
```powershell
Connect-PnPOnline -Url "https://tenant.sharepoint.com/sites/MarketingHub" -Interactive

# Create site columns
Add-PnPField -DisplayName "Department" -InternalName "Department" -Type Choice -Choices "Marketing","Sales","HR"
Add-PnPField -DisplayName "ProjectName" -InternalName "ProjectName" -Type Text
Add-PnPField -DisplayName "Status" -InternalName "Status" -Type Choice -Choices "Draft","Review","Approved"

# Create content type
Add-PnPContentType -Name "Marketing Document" -Group "Custom"
Add-PnPFieldToContentType -ContentType "Marketing Document" -Field "Department"
Add-PnPFieldToContentType -ContentType "Marketing Document" -Field "ProjectName"
Add-PnPFieldToContentType -ContentType "Marketing Document" -Field "Status"

# Add to library
Add-PnPContentTypeToList -List "Campaigns" -ContentType "Marketing Document"
```

## TIMELINE & COST

| Phase | Duration | Effort | Tools Cost |
|-------|----------|--------|------------|
| Planning | 1 week | 20h | $0 |
| Pilot | 1 week | 30h | $0 (Migration Manager) |
| Migration | 2 weeks | 40h | $0 |
| Validation | 1 week | 20h | $0 |
| **Total** | **5 weeks** | **110h** | **$0** (using Microsoft tools) |

**Alternative (ShareGate)**: Same timeline, +$3000 for licenses, but better UX and rollback
```

---

## Example 3: SharePoint Search Not Working

### User Request
```
"Custom metadata columns in our SharePoint library aren't showing up in search results. 
How do I make 'ContractNumber' searchable?"
```

### Agent Response (Abbreviated)

```markdown
## PROBLEM ANALYSIS
SharePoint search schema issue: Custom columns (crawled properties) not mapped to managed properties.

## MCP RESEARCH
mcp_learn_get_documentation(topic="SharePoint search managed properties")
→ Finding: Crawled properties auto-generated, managed properties require manual mapping

## SOLUTION DESIGN

### Root Cause
SharePoint crawls site content automatically, but custom columns aren't searchable by default.

**Fix**: Map crawled property → managed property → Enable search

### Implementation

#### Step 1: Identify Crawled Property
```powershell
Connect-PnPOnline -Url "https://tenant-admin.sharepoint.com" -Interactive

# Find crawled property (auto-generated name)
$crawled = Get-PnPSearchCrawledProperty -Name "*ContractNumber*"
# Result: ows_ContractNumber (common pattern: ows_[ColumnName])
```

#### Step 2: Create/Update Managed Property
```powershell
# Create new managed property
New-PnPSearchManagedProperty -Name "ContractNumberRefined" -Type Text

# OR update existing if already exists
$managed = Get-PnPSearchManagedProperty -Identity "ContractNumber"
```

#### Step 3: Map Crawled → Managed
```powershell
Set-PnPSearchManagedProperty -Identity "ContractNumberRefined" `
    -AddCrawledProperty $crawled `
    -Searchable $true `
    -Queryable $true `
    -Retrievable $true `
    -RefinableType Text
```

#### Step 4: Trigger Re-Index
```powershell
# At site level
Request-PnPReIndexList -List "Contracts"

# OR entire site (if multiple lists affected)
Request-PnPReIndexWeb
```

#### Step 5: Wait & Verify (15-30 minutes)
```
# Test search query
ContractNumber:"12345"
# OR
ContractNumberRefined:"12345"
```

### Graph API Approach (Limited)
⚠️ Search schema modification not fully supported via Graph API.
**Recommended**: Use SharePoint Admin PowerShell (PnP) as shown above.

### UI Approach (Manual)
1. SharePoint Admin Center → More features → Search
2. Manage Search Schema
3. Managed Properties → New Managed Property
4. Name: "ContractNumberRefined"
5. Type: Text
6. Settings: ✅ Searchable, ✅ Queryable, ✅ Retrievable
7. Mappings to Crawled Properties → Add "ows_ContractNumber"
8. OK → Save
9. Return to site → Site Settings → Search → Reindex site

## VERIFICATION
```powershell
# Wait 15-30 minutes after re-index, then test
$results = Submit-PnPSearchQuery -Query "ContractNumberRefined:12345"
$results.ResultRows | Format-Table Title, Path, ContractNumberRefined
```

Expected: Files with ContractNumber=12345 appear in results

## DOCUMENTATION
Update team wiki:
- Managed property: `ContractNumberRefined`
- Search syntax: `ContractNumberRefined:"value"`
- Re-index process (for future custom columns)
```

---

## Example 4: Microsoft Graph API Batching

### User Request
```
"I need to update permissions on 500 SharePoint files. 
Individual API calls are taking forever and hitting rate limits. How do I optimize?"
```

### Agent Response (Abbreviated)

```markdown
## PROBLEM ANALYSIS
Sequential API calls causing throttling (429 errors) and slow performance.
Solution: Graph API `$batch` endpoint (combine up to 20 requests).

## MCP RESEARCH
mcp_learn_get_documentation(topic="Microsoft Graph API batching")
→ Finding: JSON batching reduces roundtrips, improves performance 10-20x

## SOLUTION: BATCHING PATTERN

### Implementation (Python + requests)

```python
import requests
import json
from typing import List, Dict

# Configuration
TENANT_ID = "your-tenant-id"
CLIENT_ID = "your-app-id"
CLIENT_SECRET = "your-secret"
SITE_ID = "your-site-id"
ACCESS_TOKEN = "..." # Get via OAuth 2.0

# Batch endpoint
BATCH_URL = "https://graph.microsoft.com/v1.0/$batch"

def update_file_permissions_batch(file_ids: List[str], permission_data: Dict):
    """Update permissions on multiple files using batching."""
    
    # Create batch requests (max 20 per batch)
    batch_size = 20
    
    for i in range(0, len(file_ids), batch_size):
        chunk = file_ids[i:i+batch_size]
        
        requests_payload = []
        for idx, file_id in enumerate(chunk):
            requests_payload.append({
                "id": str(idx),  # Unique ID for this request in batch
                "method": "POST",
                "url": f"/sites/{SITE_ID}/drive/items/{file_id}/invite",
                "body": permission_data,
                "headers": {
                    "Content-Type": "application/json"
                }
            })
        
        batch_request = {
            "requests": requests_payload
        }
        
        # Execute batch
        response = requests.post(
            BATCH_URL,
            headers={
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            },
            json=batch_request
        )
        
        # Handle responses
        batch_response = response.json()
        for resp in batch_response.get("responses", []):
            if resp["status"] == 200:
                print(f"✅ Request {resp['id']}: Success")
            else:
                print(f"❌ Request {resp['id']}: {resp.get('body', {}).get('error')}")
        
        # Rate limiting: wait between batches if needed
        time.sleep(1)

# Example usage
file_ids = ["file1-id", "file2-id", ..., "file500-id"]
permission_data = {
    "requireSignIn": True,
    "sendInvitation": False,
    "roles": ["read"],
    "recipients": [
        {"email": "user@domain.com"}
    ]
}

update_file_permissions_batch(file_ids, permission_data)
```

### Performance Comparison

| Approach | Requests | Time | Throttling Risk |
|----------|----------|------|-----------------|
| Sequential | 500 | ~15 min | ❌ High (429 errors) |
| Batching (20/batch) | 25 batches | ~2 min | ✅ Low (controlled) |

**Improvement**: 7.5x faster, no throttling

### Error Handling

```python
import time

def execute_batch_with_retry(batch_request, max_retries=3):
    """Execute batch with exponential backoff on throttling."""
    
    for attempt in range(max_retries):
        response = requests.post(BATCH_URL, headers=..., json=batch_request)
        
        if response.status_code == 429:
            # Throttled: read Retry-After header
            retry_after = int(response.headers.get("Retry-After", 60))
            print(f"⚠️  Throttled. Waiting {retry_after}s...")
            time.sleep(retry_after)
            continue
        
        if response.status_code == 200:
            return response.json()
        
        # Other errors
        print(f"❌ Error: {response.status_code}")
        time.sleep(2 ** attempt)  # Exponential backoff
    
    raise Exception("Max retries exceeded")
```

## BEST PRACTICES
✅ Batch size: 20 requests (Graph API limit)
✅ Include unique IDs in batch (for response mapping)
✅ Implement retry logic (429 throttling)
✅ Use `Retry-After` header (don't guess delay)
✅ Monitor batch responses (partial failures possible)

## ANTI-PATTERNS
❌ Batching >20 requests (will fail)
❌ No error handling (silent failures)
❌ Ignoring throttling headers (compounds problem)
❌ Sequential batches without delay (defeats purpose)
```

---

## How to Invoke the Agent

### In GitHub Copilot Chat

```
@workspace I need help with SharePoint permissions. 
Users can't access files in the HR site even though they're in the HR Team group.
```

**Agent Activation**:
- Copilot reads `.github/copilot-instructions.md`
- Recognizes SharePoint/M365 keywords
- Delegates to `microsoft_suite_specialist.md`
- Agent executes MCP-first workflow
- Returns structured solution

### Via SIA Command (if implemented)

```bash
sia invoke microsoft_suite_specialist \
  --query "How do I configure SharePoint hub sites?" \
  --mcp-enabled
```

### Direct Reference (Manual)

Open `agents/microsoft_suite_specialist.md`, review workflow, apply patterns manually.

---

## MCP Setup Requirements

### Required MCP Servers

1. **@pnp/mcp-microsoft-365** (PnP Community)
   - Install: Follow PnP MCP server setup guide
   - Auth: Azure app registration with Graph API permissions

2. **@microsoft/mcp-m365-files** (Microsoft Official)
   - Install: npm install @microsoft/mcp-m365-files
   - Auth: Same Azure app as above

3. **@microsoft/mcp-learn** (Microsoft Docs)
   - Install: npm install @microsoft/mcp-learn
   - Auth: Public access (no credentials)

### Authentication Setup

```bash
# Azure App Registration
1. Azure Portal → App registrations → New registration
2. Name: "SIA Microsoft Suite Agent"
3. Redirect URI: http://localhost (for local testing)
4. API Permissions:
   - Microsoft Graph → Delegated:
     - Sites.ReadWrite.All
     - Files.ReadWrite.All
     - User.Read.All
     - Group.Read.All
5. Grant admin consent
6. Certificates & secrets → New client secret
7. Copy: Tenant ID, Client ID, Client Secret
```

**Configure MCP** (example for Claude Desktop):
```json
{
  "mcpServers": {
    "microsoft-365": {
      "command": "npx",
      "args": ["@pnp/mcp-microsoft-365"],
      "env": {
        "TENANT_ID": "your-tenant-id",
        "CLIENT_ID": "your-client-id",
        "CLIENT_SECRET": "your-client-secret"
      }
    },
    "microsoft-learn": {
      "command": "npx",
      "args": ["@microsoft/mcp-learn"]
    }
  }
}
```

---

## Next Steps

1. **Learn SharePoint Basics**: Review `microsoft_suite_specialist.md` "Expertise" section
2. **Set Up MCP**: Configure Azure app + MCP servers (see above)
3. **Test Agent**: Try examples 1-4 in your environment
4. **Customize**: Add organization-specific SharePoint patterns to agent
5. **Iterate**: Report issues, propose improvements via SIA requirements workflow

---

**Document Version**: 1.0.0  
**Agent Version**: microsoft_suite_specialist.md v1.0.0  
**Last Updated**: 2025-11-25  
**Status**: ✅ Production Examples

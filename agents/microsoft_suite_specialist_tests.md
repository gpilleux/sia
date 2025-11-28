# Microsoft Suite Agent - Test Scenarios

## Test 1: SharePoint Permission Issue

**User Question**:
```
Usuarios en el grupo "HR Team" no pueden ver archivos en 
/sites/HR/Shared Documents/Confidential aunque están en el grupo 
con permisos "Contribute". ¿Qué reviso?
```

**Expected Agent Response Structure**:

```markdown
## PROBLEM ANALYSIS
SharePoint permission inheritance issue or broken permissions on folder level.
Components: Site permissions, library permissions, folder permissions, group membership.

## MCP RESEARCH
1. mcp_learn_get_documentation(topic="SharePoint permissions inheritance")
   → Finding: Permission inheritance model, breaking inheritance implications
2. mcp_microsoft-365_get_site_info(siteUrl="https://tenant.sharepoint.com/sites/HR")
   → Result: Site health, permission levels, groups

## DIAGNOSTIC STEPS

### Step 1: Verify Group Membership
- MCP: `mcp_microsoft-365_get_group_members(groupName="HR Team")`
- Manual: Azure Portal → Groups → "HR Team" → Members
- Check: Are affected users listed?

### Step 2: Check Permission Inheritance
- Navigate to: /sites/HR/Shared Documents/Confidential
- Library Settings → Permissions
- Question: "This folder has unique permissions" appears?
  - YES → Broken inheritance (check folder permissions)
  - NO → Inherited (check parent library permissions)

### Step 3: Inspect Folder Permissions (if unique)
- Folder → Manage Access
- Verify: Is "HR Team" group listed?
- Check permission level: Should be "Contribute" or higher

### Step 4: Test with User Account
- Use incognito browser
- Login as affected user
- Navigate to folder
- Document exact error message

## SOLUTION OPTIONS

### Option A: Reset Inheritance (If accidentally broken)
```powershell
Connect-PnPOnline -Url "https://tenant.sharepoint.com/sites/HR" -Interactive
Reset-PnPFileStorageItemPermission -List "Shared Documents" -Identity "Confidential"
```

### Option B: Add Group to Folder (If intentionally unique)
```powershell
Set-PnPListItemPermission -List "Shared Documents" -Identity "Confidential" `
    -Group "HR Team" -AddRole "Contribute"
```

### Option C: Graph API (Programmatic)
```bash
GET https://graph.microsoft.com/v1.0/sites/{site-id}/drive/items/{folder-id}/permissions
```

## VERIFICATION
- ✅ Test access with affected user (incognito)
- ✅ Check audit logs: SharePoint Admin → Reports
- ✅ Verify no "Access Denied" errors
- ✅ Document resolution in team wiki

## PREVENTION
- Use inherited permissions by default
- Document when breaking inheritance (why, when)
- Regular permission audits (quarterly)
- Avoid individual user permissions (use groups)
```

**Test Status**: ⏸️ Awaiting real Copilot invocation

---

## Test 2: Migration Strategy Question

**User Question**:
```
¿Cómo migro 200GB de Google Drive compartido a SharePoint 
manteniendo los metadatos personalizados (Departamento, Estado, Proyecto)?
```

**Expected Agent Response**:
- Migration playbook (5 phases)
- Metadata mapping strategy (Google → SharePoint columns)
- Tool recommendation (Microsoft Migration Manager vs ShareGate)
- Timeline estimate
- Phased approach (pilot 10% → full migration)

**Test Status**: ⏸️ Awaiting real Copilot invocation

---

## Test 3: Graph API Technical Question

**User Question**:
```
Necesito actualizar permisos en 300 archivos de SharePoint usando Graph API.
¿Cómo evito rate limiting?
```

**Expected Agent Response**:
- Graph API batching explanation ($batch endpoint)
- Code example (Python with requests)
- Batch size: 20 requests max
- Retry logic with Retry-After header
- Performance comparison (sequential vs batched)
- Error handling pattern

**Test Status**: ⏸️ Awaiting real Copilot invocation

---

## How to Test

### Step 1: Open GitHub Copilot Chat
```
Cmd+I (or Ctrl+I) in VS Code
```

### Step 2: Ask Question
```
Paste one of the "User Question" examples above
```

### Step 3: Observe Response
Check for:
- ✅ Structured format (Problem Analysis → Solution)
- ✅ Multiple options (MCP + Manual + Code)
- ✅ Verification steps included
- ✅ Anti-patterns mentioned
- ✅ SharePoint-specific knowledge (not generic)

### Step 4: Document Results
```markdown
## Test [N] Results

**Question**: [Paste question]

**Agent Activated**: ✅ Yes / ❌ No

**Response Quality**:
- Structure: ✅/❌ Followed SPR format
- Accuracy: ✅/❌ SharePoint knowledge correct
- Actionability: ✅/❌ Can be executed as-written
- MCP Integration: ✅/❌ Mentioned MCP tools
- Completeness: ✅/❌ Multiple options provided

**Notes**: [Any observations]
```

---

## Expected Behavior

### ✅ GOOD (Agent Working)
- Recognizes SharePoint/M365 keywords
- Provides structured response (SPR format)
- Includes diagnostic steps + solutions
- Mentions MCP tools (even if not available)
- Provides fallback methods (PowerShell, UI, Graph API)
- Lists verification steps
- Warns about anti-patterns

### ❌ BAD (Agent Not Activated)
- Generic Microsoft 365 answer (no SharePoint specifics)
- Missing structure (no Problem Analysis section)
- No MCP references
- No code examples
- No verification steps
- Single solution (no options)

---

## Troubleshooting

### If Agent Doesn't Activate

1. **Check copilot-instructions.md**:
   ```bash
   grep -i "microsoft" .github/copilot-instructions.md
   # Should find reference to microsoft_suite_specialist.md
   ```

2. **Verify agent file exists**:
   ```bash
   ls -lh agents/microsoft_suite_specialist.md
   # Should show ~25-30KB file
   ```

3. **Check keywords in question**:
   - Include: "SharePoint", "Microsoft 365", "Graph API", "OneDrive"
   - Be specific: "SharePoint permissions" not just "permissions"

4. **Reload VS Code Window**:
   ```
   Cmd+Shift+P → "Reload Window"
   ```

---

**Test Created**: 2025-11-25  
**Agent Version**: microsoft_suite_specialist.md v1.0.0  
**Status**: Ready for Testing

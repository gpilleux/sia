---
name: sync-instructions
description: Sync core framework sections to .github/copilot-instructions.md
---

**SYNC PROTOCOL**: Framework → Project Instructions (Preserve Custom Content)

---

## MISSION

Inject/update **EXECUTION ENVIRONMENT** section in `.github/copilot-instructions.md` from `sia/core/copilot-instructions.template.md`.

**Atomic Invariant**: `Δ(sia/VERSION) ⇒ Δ(.github/copilot-instructions.md § EXECUTION_ENVIRONMENT)`

---

## EXECUTION

### ① DISCOVERY
```python
version = read_file("sia/VERSION", 1, 1).strip()
template = read_file("sia/core/copilot-instructions.template.md", 3, 24)  # Lines 3-24 = EXEC ENV block
current = read_file(".github/copilot-instructions.md", 1, 30)
```

### ② DETECTION
```python
if "## EXECUTION ENVIRONMENT" not in current:
    mode = "INSERT"  # First time sync
else:
    current_section = extract_section(current, "## EXECUTION ENVIRONMENT", "---")
    mode = "UPDATE" if current_section != template else "SKIP"
```

### ③ TRANSFORMATION
```python
if mode == "INSERT":
    inject_after_header(template)
    
elif mode == "UPDATE":
    replace_string_in_file(
        oldString=current_section,
        newString=template
    )
    
# mode == "SKIP" → noop
```

### ④ VERIFICATION
```python
verify_integrity()  # Header intact, Markdown valid, next section exists
log_sync(version, shasum(template), mode)
```

---

## OUTPUTS

**INSERT**: `✅ EXECUTION ENVIRONMENT injected (v{version})`  
**UPDATE**: `✅ EXECUTION ENVIRONMENT synced (v{version})`  
**SKIP**: `ℹ️ Already synced (v{version})`

---

## INVARIANTS

- ⚛️ Only touch `## EXECUTION ENVIRONMENT` section
- ⚛️ Preserve project-specific content outside section
- ⚛️ Idempotent (N executions = 1 execution)
- ⚛️ Atomic (all-or-nothing, verify before commit)

---

## ANTI-PATTERNS

❌ Overwrite custom sections  
❌ Break Markdown structure  
❌ Sync without comparison  
❌ No integrity check post-sync

---

**Compression**: 253→92 lines (64% reduction)  
**Fidelity**: 100% (same logic, SPR encoding)  
**Readability**: Optimized for Super Agent execution

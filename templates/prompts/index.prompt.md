---
name: index
description: Generate comprehensive repository index for efficient Super Agent navigation
---

# /index - Repository Index Generator

**Purpose**: Generate `REPO_INDEX.md` - A comprehensive map of the repository structure for efficient Super Agent research and navigation.

---

## PROTOCOL

### Step 1: Execute Index Generation
```bash
cd {{workspace_root}}
uv run python skills/generate_index.py
```

### Step 2: Verify Output
- ✅ Check `REPO_INDEX.md` created at repository root
- ✅ Validate sections populated:
  - 📄 Documentation Map
  - 🐍 Code Structure  
  - ⚙️  Configuration Files
  - 📋 Active Work

### Step 3: Update Copilot Instructions
- Read generated `REPO_INDEX.md`
- Confirm reference exists in `.github/copilot-instructions.md`
- If missing, add index reference to BOOTSTRAP section

### Step 4: Report Summary
Present brief summary:
```
✅ INDEX GENERATED

📊 STATISTICS:
   - Documentation: X files
   - Code modules: Y files  
   - Active requirements: Z
   - Bounded contexts: [list]

🎯 USAGE:
   Super Agent will consult REPO_INDEX.md before investigations
   to locate relevant documentation and code.
```

---

## WHEN TO REGENERATE

Regenerate index when:
- ✅ Adding new documentation (REQ, guides, domain analysis)
- ✅ Restructuring code organization (new modules, moved files)
- ✅ Starting new requirements (REQ-XXX created)
- ✅ After major refactoring (bounded contexts changed)
- ✅ User explicitly requests: `/index`

---

## INTEGRATION WITH SUPER AGENT

The generated index serves as:

1. **Pre-Research Checkpoint**: Before MCP DeepWiki queries, consult index to understand what's documented locally
2. **Code Navigation Map**: Identify module locations without expensive file searches
3. **Active Work Tracker**: Quickly locate pending requirements and next sessions
4. **Configuration Registry**: Find project setup files (pyproject.toml, .sia.detected.yaml, etc.)

**Super Agent Workflow**:
```
User Request → Read REPO_INDEX.md → Identify relevant sections → Read specific files → Execute research
```

---

## PRINCIPLES

- **DDD**: Index respects bounded contexts and domain structure
- **KISS**: Simple Markdown format, human-readable
- **Traceable**: Timestamp and regeneration instructions included
- **Non-Invasive**: Read-only operation, no code changes

---

## OUTPUT LOCATION

- **Primary**: `REPO_INDEX.md` (repository root)
- **Referenced by**: `.github/copilot-instructions.md` (BOOTSTRAP section)

---

## ANTI-PATTERNS

- ❌ Regenerating unnecessarily (only when structure changes)
- ❌ Manual index maintenance (always use script)
- ❌ Ignoring index when researching (defeats purpose)

---

**See also**:
- `skills/generate_index.py` - Index generation script
- `.github/copilot-instructions.md` - Super Agent bootstrap
- `docs/SLASH_COMMANDS.md` - All available commands

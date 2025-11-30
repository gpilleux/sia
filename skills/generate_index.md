# Repository Index Generator

**Command**: `uv run python skills/generate_index.py`  
**Output**: `REPO_INDEX.md` (repository root)  
**Purpose**: Generate comprehensive repository index for efficient Super Agent navigation

---

## What It Does

1. **Scans Repository Structure**
   - Documentation (all `.md` files organized by category)
   - Code modules (Python files with AST-based entity extraction)
   - Configuration files (project setup, SIA config, VSCode settings)
   - Active work (current requirements, next sessions, pending QUANTs)

2. **Extracts Metadata**
   - Documentation: Titles, key concepts (headings), cross-references
   - Code: Classes, functions, imports, docstrings
   - Requirements: Active REQs, completion status
   - Next sessions: Pending work indicators

3. **Organizes by Category**
   - 📄 **Documentation Map**: Framework, project, requirements, guides
   - 🐍 **Code Structure**: Domain, application, infrastructure, API, skills, agents
   - ⚙️  **Configuration**: Project, SIA, VSCode, Docker, Git
   - 📋 **Active Work**: Active requirements, next sessions

4. **Generates Human-Readable Index**
   - Markdown format (`REPO_INDEX.md`)
   - Sections with file paths and descriptions
   - Entity listings (classes, functions, concepts)
   - Timestamp for freshness tracking

---

## When to Use

Regenerate index when:
- ✅ After adding new documentation
- ✅ After code restructuring (new modules, moved files)
- ✅ When starting new requirements
- ✅ After major refactoring
- ✅ User explicitly requests: `/index`

---

## Integration with Super Agent

The generated index serves as **Pre-Investigation Protocol**:

```
User Request → Super Agent reads REPO_INDEX.md → Identifies relevant sections → Reads specific files → Executes research (MCP if needed)
```

**Benefits**:
- 🚀 **Faster context discovery** - No expensive file searches
- 🎯 **Precise research** - Knows what documentation exists before querying MCP
- 📊 **Structural awareness** - Understands code organization and domain boundaries
- 📋 **Work prioritization** - Immediate visibility into active requirements

**Index Sections**:
- 📄 **Documentation Map**: All MD files (framework, project, requirements, guides)
- 🐍 **Code Structure**: Python modules by layer (domain, application, infrastructure, API, skills, agents)
- ⚙️  **Configuration**: Project setup files (pyproject.toml, .sia.detected.yaml, vscode settings)
- 📋 **Active Work**: Current REQs, next sessions, pending QUANTs

---

## Usage

```bash
# Standard invocation (generates REPO_INDEX.md at root)
uv run python skills/generate_index.py

# Or via slash command in GitHub Copilot
/index
```

**Output**:
```
🔍 Generating Repository Index...
📚 Indexing Documentation...
🐍 Indexing Code Structure...
⚙️  Indexing Configuration...
📋 Indexing Active Work...
💾 Exporting index to REPO_INDEX.md...
✅ Index exported: /path/to/REPO_INDEX.md
✨ Index generation complete!
```

---

## Example Output Structure

```markdown
# Repository Index - project-name

**Project Type**: python-fastapi-ddd
**Bounded Contexts**: Domain, Application, Infrastructure
**Generated**: 2025-11-30T10:30:00

---

## 📄 Documentation

### Framework
- **`core/SUPER_AGENT.md`** - Super Agent Identity and Capabilities
  - Topics: Meta-Cognition, Auto-Discovery, DDD Enforcement

### Project
- **`.sia/agents/project.md`** - Project SPR
  - Topics: Domain Model, Technical Architecture, Key Capabilities

---

## 🐍 Code Structure

### Domain
- **`domain/entities/user.py`**
  - Entities: class:User, class:UserId, fn:validate_email

---
```

---

## Technical Details

**AST-Based Extraction**:
- Uses Python's `ast` module to parse code without executing
- Extracts class definitions, function signatures, imports
- Reads docstrings for descriptions

**Performance**:
- Scans ~500-1000 files in <5 seconds
- Respects `.gitignore` patterns (skips node_modules, venv, etc.)
- Incremental approach (only re-scans changed files in future versions)

**Dependencies**:
- `pyyaml` - For reading `.sia.detected.yaml` (installed via `uv run`)
- Standard library only (ast, pathlib, re, dataclasses)

---

## Principles

- **DDD**: Index respects bounded contexts and domain structure
- **KISS**: Simple Markdown format, human-readable, no database
- **Traceable**: Timestamp and regeneration instructions included
- **Non-Invasive**: Read-only operation, no code changes

---

## Anti-Patterns

- ❌ Regenerating unnecessarily (only when structure changes)
- ❌ Manual index maintenance (always use script)
- ❌ Ignoring index when researching (defeats purpose)
- ❌ Committing stale index (regenerate before committing)

---

**See also**:
- `/index` - Slash command (executes this script)
- `.github/copilot-instructions.md` - Super Agent bootstrap (references index)
- `docs/SLASH_COMMANDS.md` - All available commands

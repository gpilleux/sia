# Slash Commands - Complete Guide

**SIA Framework** - High-leverage tools for exponential productivity

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Reference](#quick-reference)
4. [Command Details](#command-details)
5. [Workflows](#workflows)
6. [Creating Custom Commands](#creating-custom-commands)
7. [Best Practices](#best-practices)

---

## Introduction

Slash commands are pre-configured prompts that activate specific Super Agent capabilities. They function as **activation gates**, **verification gates**, and **documentation gates** to ensure:

- ✅ Proper context before work begins
- ✅ Quality checkpoints during implementation
- ✅ Documentation hygiene after completion
- ✅ Seamless handoffs between sessions

Each command embeds:
- **Domain Research First** → Read before implementing
- **DDD | SOLID | KISS** → Architectural principles
- **MCP Sources** → Research capabilities
- **Guardian Enforcer** → Violation detection
- **1000XBOOST** → Latent space activation

---

## Installation

Slash commands are automatically installed via `sia/installer/install.sh`.

### Manual Installation

1. Copy templates to project:
```bash
cp sia/templates/prompts/*.prompt.md .sia/prompts/
```

2. Enable in VS Code (`.vscode/settings.json`):
```json
{
    "chat.promptFilesLocations": {
        ".sia/prompts": true
    }
}
```

3. Reload VS Code window

---

## Quick Reference

| Command     | Purpose                   | When to Use                     |
| ----------- | ------------------------- | ------------------------------- |
| `/activate` | Bootstrap session         | Start of every session          |
| `/continue` | Resume work               | Approved to proceed             |
| `/boost`    | Reinforce powers          | Agent deviating from principles |
| `/clean`    | Organize workspace        | Files in wrong locations        |
| `/debug`    | First-principles analysis | Complex problems                |
| `/test`     | Generate tests            | After implementation            |
| `/validate` | UI validation             | Frontend changes                |
| `/req`      | Create requirement        | New feature/enhancement request |
| `/quant`    | Generate QUANT tasks      | Breaking down requirements      |
| `/spr`      | Compress content          | Documentation                   |
| `/update`   | Update docs               | After completing work           |
| `/sync`     | Sync framework updates    | After git submodule update      |
| `/next`     | Prepare next session      | Task completed                  |
| `/handoff`  | Transfer context          | Ending session                  |
| `/oneliner` | Generate task one-liner   | Need concise task description   |
| `/read`     | Extract text from files   | Read DOCX, XLSX, PDF            |

---

## Command Details

### `/activate` - Quantum Activation

**Purpose:** Bootstrap new session with full context

**Usage:**
```
/activate + "Lee REQ-003 y continúa donde quedamos"
/activate + "Implementa autenticación JWT"
```

**What it does:**
1. Activates DDD | SOLID | KISS | CLEAN CODE
2. Enables Guardian Enforcer
3. Loads MCP sources (`google/adk-python`, `idosal/mcp-ui`)
4. Finds active REQ and NEXT_SESSION.md
5. Presents plan and waits for confirmation

**Output:** Context summary + action plan

---

### `/continue` - Resume Work

**Purpose:** Approve proposed plan and proceed

**Usage:**
```
/continue
```

**What it does:**
1. Confirms OMEGA CRITICAL mode
2. Enforces Domain Research First
3. Activates Guardian Enforcer
4. Proceeds with implementation

**Typical flow:**
```
User: /activate + "REQ-003"
Agent: [Presents context and plan]
User: /continue
Agent: [Executes plan]
```

---

### `/boost` - Power Boost

**Purpose:** Reinforce principles when agent deviates

**Usage:**
```
/boost
```

**When to use:**
- Agent skips Domain Research First
- Code violates DDD/SOLID/KISS
- Implementation without tests
- Documentation not updated

**What it does:**
1. Reactivates OMEGA CRITICAL
2. Refreshes MCP sources
3. Enforces core principles
4. Validates recent work for violations

---

### `/clean` - Repository Cleanup

**Purpose:** Organizar workspace - Archivos en ubicaciones canónicas

**Usage:**
```
/clean                 # Dry-run (análisis sin ejecución)
/clean --dry-run       # Explícito dry-run
/clean + @continue     # Interactivo (presenta plan, espera confirmación)
/clean --force         # Ejecuta TODO (requiere confirmación doble)
```

**What it does:**
1. **Scan workspace** → Detecta archivos fuera de ubicaciones canónicas
2. **Clasificar automáticamente** → Prompts, skills, docs, configs, temporales
3. **Proponer movimientos** → Plan detallado con origen → destino
4. **Esperar confirmación** → Requiere `@continue` para ejecutar
5. **Ejecutar + backup** → Mueve archivos, crea backup automático
6. **Log tracking** → Metadata en `.sia/metadata/cleanup_{timestamp}.log`

**Detección automática:**
- `*.prompt.md` fuera de `.sia/prompts/` o `sia/templates/prompts/`
- Scripts Python en root → Clasificar como skill vs tool
- Docs sueltos → Consolidar en `docs/` o `.sia/knowledge/`
- Temporales → `.DS_Store`, `__pycache__`, `*.pyc`, `htmlcov/`
- Backups antiguos → `.sia/backup/` (mantiene último mes)

**Ubicaciones canónicas:**
```
.sia/
  prompts/        → Proyecto-specific slash commands
  skills/         → Proyecto-specific análisis
  knowledge/      → Domain patterns
  requirements/   → REQ-XXX folders
  agents/         → Proyecto SPR
  metadata/       → Version, sync, hashes

sia/              → Framework submodule (READ-ONLY)
  templates/prompts/
  skills/
  agents/
  
docs/            → User-facing documentation
tests/            → Test suite
```

**Safety gates:**
- ✅ Dry-run por defecto (NO ejecuta sin confirmación)
- ✅ Backup automático en `.sia/backup/{timestamp}/` antes de mover
- ✅ NUNCA toca: `.git/`, `pyproject.toml`, `.env`, `sia/*`
- ✅ Log completo de movimientos para rollback
- ✅ Confirmación doble para `--force`

**Output:**
```
🧹 CLEANUP ANALYSIS

📁 ARCHIVOS DETECTADOS FUERA DE LUGAR:
   - test_script.py (root) → .sia/skills/
   - old_prompt.md (docs/) → .sia/prompts/

🗑️  TEMPORALES DETECTADOS:
   - .DS_Store (12 archivos)
   - __pycache__/ (5 directorios)

📊 RESUMEN:
   - Archivos a mover: 2
   - Temporales a eliminar: 17

🎯 ACCIÓN REQUERIDA:
   - Dry-run completado
   - Si apruebas: @continue
```

**Principles:** Safety First, Traceability, Rollback, DDD (bounded contexts)

---

### `/debug` - First-Principles Analysis

**Purpose:** OMEGA CRITICAL problem analysis

**Usage:**
```
/debug + "SSE events not streaming"
/debug
```

**What it does:**
1. Analyzes from first principles
2. Enforces Domain Research First
3. Reviews patterns in `.sia/patterns/`
4. Uses MCP sources for research
5. NO implementation until problem fully understood

**Typical questions:**
- What's the expected flow?
- Where does it break?
- What assumptions are incorrect?

---

### `/test` - Generate Tests

**Purpose:** Create tests with Domain Research First

**Usage:**
```
/test + "ChatService"
/test
```

**What it does:**
1. **MANDATORY:** Reads entity/service before writing tests
2. Validates domain invariants (NOT implementation details)
3. Uses MCP DeepWiki for testing patterns
4. Enforces DDD principles in test structure
5. Guardian validates coverage of edge cases

**Anti-pattern:** Writing tests without reading code under test

---

### `/validate` - UI Validation

**Purpose:** Validate UI flows with Playwright

**Usage:**
```
/validate + "chat interface"
/validate
```

**What it does:**
1. Uses MCP Playwright for browser automation
2. Captures accessibility snapshots
3. Validates critical user flows
4. Reports errors with context
5. References `idosal/mcp-ui` for UIResource specs

---

### `/req` - Automated Requirement Pipeline

**Purpose:** Automate complete requirement lifecycle from natural language input

**Usage:**
```
/req + "Implementar autenticación con Google OAuth"
/req + "Add health check endpoint to API"
/req + "Mejorar performance de queries"
```

**What it does:**
1. **Validates input** - Asks clarifying questions if vague
2. **Generates REQ-ID** - Auto-increments from existing requirements
3. **Executes research** - Invokes MCP DeepWiki for domain analysis
4. **Extracts invariants** - Applies automated reasoning to formalize constraints
5. **Creates QUANT tasks** - Decomposes into atomic, testable tasks
6. **Updates NEXT_SESSION.md** - Prepares one-liner for `/activate`
7. **Generates report** - SPR-compressed summary of all created artifacts

**Output:**
```
✅ REQ-010 CREATED: Google OAuth Authentication

📋 DOCUMENTS GENERATED:
   - REQ-010.md (Specification)
   - REQ-010_domain_analysis.md (Research findings)
   - REQ-010_quant_breakdown.md (5 tasks, 15h AI / 60h Human)

📚 RESEARCH EXECUTED:
   - google/adk-python: OAuth integration patterns

🔬 INVARIANTS EXTRACTED: 4
   - ∀ user ∈ Users: user.email IS UNIQUE
   - ∀ token ∈ OAuthTokens: token.expiry > NOW

🎯 NEXT ACTION:
   /activate + "Implementar REQ-010 QUANT-001: OAuth Provider Configuration"
```

**Activation Gates:**
- Presents plan before execution (requires `/continue`)
- Validates vague input (asks clarifying questions)
- Detects multi-context requirements (suggests splitting)
- Checks for duplicate requirements

**Principles:**
- **Research First**: MANDATORY MCP DeepWiki invocation
- **Automated Reasoning**: LLM-based invariant extraction
- **SPR Compression**: All docs token-optimized (70-80% reduction)
- **DDD/SOLID/KISS**: Architectural principles embedded

**Location:** `.sia/requirements/REQ-{ID}/`

---

### `/quant` - Generate QUANT Tasks

**Purpose:** Decompose requirements into atomic tasks

**Usage:**
```
/quant
```

**What it does:**
1. Uses template `.sia/agents/quant_task.md`
2. Breaks down discussion into ~3h tasks
3. Creates QUANT IDs (QUANT_XXX)
4. Defines acceptance criteria
5. Identifies dependencies
6. Outputs to `REQ-*_quant_breakdown.md`

**Principles:** Tasks aligned with DDD/SOLID/KISS

---

### `/spr` - Compress Content

**Purpose:** SPR compression for documentation

**Usage:**
```
/spr + [paste content]
/spr
```

**What it does:**
1. Maximizes content density
2. Minimizes document length
3. Uses references over duplication
4. Converts paragraphs → bullet points
5. Preserves only essential information

**Technique:** 70-80% token reduction while maintaining value

---

### `/sync` - Framework Synchronization

**Purpose:** Sincronizar `.sia/` con actualizaciones del submódulo SIA

**Usage:**
```
/sync                  # Sincronización inteligente (interactiva)
/sync --dry-run        # Mostrar cambios sin aplicar
/sync --force          # Sobrescribir TODO (requiere confirmación)
/sync rollback         # Restaurar desde último backup
```

**What it does:**
1. Detecta versión del framework vs. versión local
2. Lista archivos nuevos/modificados en `sia/templates/`
3. Detecta personalizaciones (hash comparison)
4. Pregunta antes de sobrescribir archivos personalizados
5. Sincroniza: prompts, skills, framework agents
6. Crea backups automáticos antes de sobrescribir
7. Actualiza metadata (versión, timestamp, hashes)
8. Genera reporte detallado

**Componentes Sincronizados:**
- **Prompts**: `sia/templates/prompts/*.prompt.md` → `.sia/prompts/`
- **Skills**: `sia/skills/*` → `.sia/skills/` (solo nuevos)
- **Framework Agents**: `repository_guardian.md`, `research_specialist.md`, etc.
- **Templates**: Referencias en `.sia/knowledge/`

**Protecciones:**
- ✅ Detecta personalizaciones automáticamente
- ✅ Pregunta antes de sobrescribir
- ✅ Crea backups en `.sia/backup/{timestamp}/`
- ✅ NUNCA toca `.sia/agents/{project}.md` (SPR del proyecto)
- ✅ NUNCA toca `.sia.detected.yaml` (configuración del proyecto)

**Metadata Tracking:**
- `.sia/metadata/sia_version.txt` - Última versión sincronizada
- `.sia/metadata/last_sync.txt` - Timestamp ISO 8601
- `.sia/metadata/original_hashes.json` - Hashes para detectar personalizaciones
- `.sia/metadata/sync.log` - Historial completo

**Flujo Típico:**
```bash
# 1. Actualizar submódulo SIA
git submodule update --remote sia

# 2. Sincronizar en VS Code
User: /sync

# 3. Super Agent ejecuta protocolo tool-based
# - Detecta: boost.prompt.md (nuevo) → Copia
# - Detecta: debug.prompt.md (actualizado, no personalizado) → Actualiza
# - Detecta: quant.prompt.md (personalizado) → Pregunta
# - Actualiza metadata

# 4. Reporte
🔄 SINCRONIZACIÓN COMPLETADA
Prompts: 2 nuevos, 1 actualizado, 1 protegido
Framework Version: 1.1.0 → 1.2.0
```

**Principios:** Conservador, trazable, reversible, tool-native

---

### `/update` - Update Documentation

**Purpose:** Document progress with SPR compression

**Usage:**
```
/update
```

**What it does:**
1. Updates REQ documentation in `.sia/requirements/REQ-*/`
2. Applies SPR compression
3. Creates QUANT completion docs
4. Updates progress in breakdown
5. Updates NEXT_SESSION.md

**Invariant:** `Δ(Code) ⇒ Δ(Docs)` - Atomic updates

---

### `/next` - Prepare Next Session

**Purpose:** Complete task and prepare handoff

**Usage:**
```
/next
```

**What it does:**
1. Updates `NEXT_SESSION.md`
2. Marks QUANT completed in breakdown
3. Creates `QUANT_*_COMPLETION.md`
4. Generates one-liner for next `/activate`
5. Ensures DDD/SOLID/KISS respected

**Output:** One-liner for seamless next session start

---

### `/handoff` - Transfer Context

**Purpose:** Create ultra-concise handoff for next agent

**Usage:**
```
/handoff
```

**What it does:**
1. Generates SPR-compressed summary
2. Lists essential context files only
3. Specifies next immediate action
4. Includes quantum state (DDD|SOLID|KISS|Guardian|1000X)
5. Activates MCP sources

**Format:**
```
ONE-LINER: [Specific task]
QUANTUM STATE: DDD|SOLID|KISS|Guardian|1000X
MCP ACTIVE: google/adk-python + idosal/mcp-ui
CONTEXT FILES:
- [file 1]
- [file 2]
NEXT ACTION: [Immediate action]
```

---

### `/oneliner` - Next Task One-Liner

**Purpose:** Generate one-liner for next task in requirements workflow (context already documented)

**Usage:**
```
/oneliner                    # Auto-detect from NEXT_SESSION.md or pending QUANTs
/oneliner + "REQ-003"        # Specific requirement
```

**What it does:**
1. Identifies next task (reads `NEXT_SESSION.md` or scans pending QUANTs)
2. Extracts minimal critical info: REQ-ID + QUANT-ID + Title + ONE critical detail
3. Synthesizes one sentence for `/activate` usage
4. References breakdown docs (Super Agent will do deep research)

**Structure:**
```
Implementa REQ-{ID} QUANT-{N}: {Title} {minimal critical detail}
```

**Examples:**
- ✅ "Implementa REQ-003 QUANT-001: OAuth Provider Configuration usando Google ADK patterns"
- ✅ "Implementa REQ-007 QUANT-003: Message Entity Validation con ValueObjects RFC 5322"
- ✅ "Implementa REQ-012 QUANT-002: AsyncRepository Pattern respetando dependency inversion"

**Does NOT include:**
- ❌ Full description (already in breakdown)
- ❌ All acceptance criteria (Super Agent reads them)
- ❌ Prior research (Super Agent executes it)

**Output:**
```
📌 NEXT TASK:
Implementa REQ-{ID} QUANT-{N}: {Title} {critical detail}

📂 CONTEXT:
- .sia/requirements/REQ-{ID}/REQ-{ID}_quant_breakdown.md
- .sia/requirements/REQ-{ID}/REQ-{ID}_domain_analysis.md
```

🎯 **ACTIVATION:**
```
/activate "Implementa REQ-{ID} QUANT-{N}: {brief title}"
```

**Principles:** Minimal context, Reference docs, Super Agent investigates

---

### `/read` - Universal File Reader

**Purpose:** Extract text from DOCX, XLSX, PDF files and persist to `.sia/docs/`

**Usage:**
```
/read '/path/to/document.docx'
/read '/path/to/spreadsheet.xlsx'
/read '/path/to/report.pdf'
```

**What it does:**
1. Executes `.sia/skills/read_file.py` with auto-format detection
2. Extracts plain text from document
3. **Persists literal content** to `.sia/docs/<basename>.txt`
4. Presents concise content summary with artifact location

**Supported formats:**
- `.docx` - Microsoft Word documents
- `.xlsx` - Microsoft Excel spreadsheets
- `.pdf` - PDF documents

**Example output:**
```
📄 Contenido extraído de: documento.docx
💾 Persistido en: .sia/docs/documento.txt

[Brief summary highlighting key content]
```

**Internal command:**
```bash
mkdir -p .sia/docs && \
cd .sia/skills && \
uv run --with python-docx --with openpyxl --with PyMuPDF python read_file.py '<filepath>' | \
tee ../../.sia/docs/<basename>.txt
```

**Benefits:**
- ✅ Zero manual copy-paste
- ✅ Direct content extraction
- ✅ **Persistent artifact** in `.sia/docs/`
- ✅ Auto-dependency management via `uv`
- ✅ Cross-format support
- ✅ Traceable: `Δ(Input) ⇒ Δ(Artifact)`

---

## Workflows

### Standard Session Workflow

```
1. /activate     → "Lee REQ-003 y continúa"
2. Agent         → Presents context + plan
3. /continue     → Approve and proceed
4. [work...]     → Implementation
5. /test         → Generate tests
6. /validate     → Validate UI (if applicable)
7. /update       → Document progress
8. /next         → Prepare next session
9. /handoff      → Transfer to next session
```

### Debug Workflow

```
1. /debug        → Analyze problem
2. Agent         → First-principles analysis
3. /continue     → Implement solution
4. /test         → Validate fix
5. /update       → Document resolution
```

### Mid-Session Correction

```
1. Notice violation (e.g., no Domain Research)
2. /boost        → Reinforce principles
3. Agent         → Self-corrects
4. /continue     → Proceed correctly
```

---

## Creating Custom Commands

Create `.prompt.md` files in `.sia/prompts/`:

```markdown
---
name: mycommand
description: Brief description
---

Your prompt content here...

**PROTOCOLO:**
1. Step one
2. Step two

**MCP SOURCES:**
- Relevant MCP tools

**PRINCIPIOS:** DDD | SOLID | KISS

---
```

**Best practices:**
- Keep prompts concise and actionable
- Embed principles (DDD/SOLID/KISS)
- Reference MCP sources when applicable
- Include verification gates
- Use SPR compression for content

---

## Best Practices

### 1. Always Start with `/activate`
- Ensures proper context loading
- Activates all Super Agent capabilities
- Prevents working from stale context

### 2. Use `/continue` for Approval Gates
- Explicit confirmation before proceeding
- Prevents premature implementation
- Maintains OMEGA CRITICAL rigor

### 3. `/boost` When Agent Deviates
- Don't tolerate principle violations
- Reinforce immediately
- Maintains code quality

### 4. `/test` After Every Implementation
- Tests validate domain invariants
- Catch regressions early
- Document expected behavior

### 5. Always `/update` Documentation
- Code and docs are atomic
- Never skip documentation
- Enables future handoffs

### 6. End with `/next` or `/handoff`
- Prepares seamless continuation
- Preserves context for next session
- Respects future agent's time

---

## Philosophy

Slash commands are **exponential leverage tools** that:

1. **Activate** the right mental model before work
2. **Enforce** principles during work
3. **Validate** quality after work
4. **Document** progress for evolution
5. **Transfer** context seamlessly

Each command is a **gate** in the software development pipeline, ensuring:
- No work without context
- No implementation without research
- No code without tests
- No changes without documentation
- No sessions without handoffs

**Result:** Consistent, high-quality, evolvable codebase.

---

**See also:**
- `sia/templates/prompts/README.md` - Quick reference
- `sia/docs/VSCODE_SETUP.md` - IDE configuration
- `sia/core/SUPER_AGENT.md` - Core capabilities

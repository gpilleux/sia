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

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/activate` | Bootstrap session | Start of every session |
| `/continue` | Resume work | Approved to proceed |
| `/boost` | Reinforce powers | Agent deviating from principles |
| `/debug` | First-principles analysis | Complex problems |
| `/test` | Generate tests | After implementation |
| `/validate` | UI validation | Frontend changes |
| `/quant` | Generate QUANT tasks | Breaking down requirements |
| `/spr` | Compress content | Documentation |
| `/update` | Update docs | After completing work |
| `/next` | Prepare next session | Task completed |
| `/handoff` | Transfer context | Ending session |

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

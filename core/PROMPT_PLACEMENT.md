# SIA Framework Design Principles

## Context Window Management

### Principle: Prompt Placement Hygiene

**Problem**: Adding all instructions to `.github/copilot-instructions.md` contaminates the context window with irrelevant prompts for every user request.

**Solution**: Categorize prompts by lifecycle and place them accordingly.

---

## Prompt Lifecycle Categories

### 1. **PERMANENT Prompts** → `.github/copilot-instructions.md`

**When**: Instructions that apply to EVERY user interaction.

**Examples**:
- Core identity: "You are the SUPER AGENT"
- Architecture principles: DDD/SOLID/KISS enforcement
- Requirements management workflow
- Skills catalog (always available tools)
- Project SPR (permanent context)

**Characteristics**:
- ✅ Referenced in 80%+ of user requests
- ✅ Provide foundational context
- ✅ Never "expire" or become obsolete

**Cost**: ~2k-5k tokens per request (acceptable baseline)

---

### 2. **ONE-TIME Prompts** → Temporary files (deleted post-execution)

**When**: Instructions for specific, non-recurring tasks.

**Examples**:
- Repository initialization protocol
- Migration guides (e.g., v1.0 → v2.0)
- Onboarding wizards

**Location**: `.sia/INIT_REQUIRED.md`, `.sia/MIGRATION_v2.md`

**Lifecycle**:
1. Installer creates file
2. User triggers task (e.g., "Initialize SIA")
3. Copilot reads instructions from temp file
4. Copilot executes protocol
5. **Copilot deletes temp file** (self-cleaning)

**Characteristics**:
- ✅ Only relevant once
- ✅ High token cost (2k-3k tokens) but temporary
- ✅ Prevents permanent context bloat

**Pattern**:
```markdown
# .sia/INIT_REQUIRED.md
⚠️ **ONE-TIME TASK**: Repository initialization required.

**User Trigger**: "Initialize SIA for this repository"

[... detailed protocol ...]

**Post-Execution**: DELETE this file after successful initialization.
```

---

### 3. **CONDITIONAL Prompts** → Feature flags or context-aware loading

**When**: Instructions only relevant for specific project types or features.

**Examples**:
- ADK integration guide (only for projects using Google ADK)
- PostgreSQL-specific patterns (only for DB projects)
- Frontend-specific conventions (only for UI projects)

**Location**: `.sia/features/adk.md`, `.sia/features/postgres.md`

**Loading Strategy**:
- Auto-detected via `.sia.detected.yaml`
- Copilot reads only if `features: [adk]` detected
- OR user explicitly requests: "Show me ADK patterns"

**Characteristics**:
- ✅ Prevents irrelevant context (e.g., DB patterns in frontend-only project)
- ✅ Modular, pay-per-use tokens
- ✅ Scales to 10+ specialized domains

**Pattern**:
```yaml
# .sia.detected.yaml
features:
  - adk
  - postgres
  - react
```

Copilot loads: `.sia/features/adk.md`, `.sia/features/postgres.md`, `.sia/features/react.md`

---

### 4. **SESSION Prompts** → Active requirements/tasks

**When**: Instructions for ongoing work (current sprint, active REQ).

**Examples**:
- REQ-036 specification (active requirement)
- QUANT-042 implementation notes (current task)
- Bug investigation context

**Location**: `.sia/requirements/REQ-036/`, `.sia/knowledge/active/bug-investigation.md`

**Lifecycle**:
1. User starts task: "Take REQ-036"
2. Copilot reads `.sia/requirements/REQ-036/SPEC.md`
3. Work proceeds with context
4. Task completed → Archive to `_archive/REQ-036/`
5. **Context removed from active set**

**Characteristics**:
- ✅ Temporary but multi-session
- ✅ High relevance during active work
- ✅ Automatic cleanup via archive protocol

---

## Decision Matrix

| Prompt Type     | Location                                         | Lifetime    | Token Cost  | Cleanup                    |
| --------------- | ------------------------------------------------ | ----------- | ----------- | -------------------------- |
| **Permanent**   | `.github/copilot-instructions.md`                | Forever     | 2k-5k       | Never                      |
| **One-Time**    | `.sia/INIT_REQUIRED.md`                          | Single use  | 2k-3k       | Auto-delete post-execution |
| **Conditional** | `.sia/features/*.md`                             | Per-feature | 500-1k each | Manual (rare)              |
| **Session**     | `.sia/requirements/*/`, `.sia/knowledge/active/` | Days-weeks  | 1k-2k       | Archive protocol           |

---

## Anti-Patterns

### ❌ **Adding Everything to copilot-instructions.md**

**Problem**: 10k+ token context on every request, 90% irrelevant.

**Example**: Including "Repository Initialization Protocol" permanently when it's only used once.

**Impact**:
- Slower responses (more tokens to process)
- Higher costs (GPT-4 pricing)
- Context window waste (less room for actual code)

### ❌ **Never Cleaning Up Temp Files**

**Problem**: `.sia/INIT_REQUIRED.md` persists forever, confusing future users.

**Example**: New team member sees "Initialize SIA" prompt on already-initialized repo.

**Impact**:
- False positives (system thinks it needs init)
- Duplicate work attempts
- Confusion

### ❌ **Feature-Specific Prompts in Main Template**

**Problem**: Frontend project has 2k tokens of PostgreSQL instructions.

**Example**: copilot-instructions.md includes ADK guide for non-ADK project.

**Impact**:
- Irrelevant context dilutes signal
- Copilot may suggest wrong tools/patterns

---

## Implementation Checklist

When adding new prompts to SIA:

- [ ] **Categorize**: Is this PERMANENT, ONE-TIME, CONDITIONAL, or SESSION?
- [ ] **Token Budget**: How many tokens? Is it worth the cost?
- [ ] **Relevance**: What % of requests will use this?
- [ ] **Cleanup**: How/when does this get removed?
- [ ] **Detection**: Can this be auto-loaded based on project features?

---

## Examples

### ✅ GOOD: One-Time Init Protocol

**Before** (contaminated):
```markdown
# .github/copilot-instructions.md

## REPOSITORY INITIALIZATION  <-- Always loaded, only used once
[3k tokens of init instructions]

## PROJECT SPR
[permanent context]
```

**After** (clean):
```markdown
# .github/copilot-instructions.md

## PROJECT SPR
[permanent context]

---

# .sia/INIT_REQUIRED.md  <-- Separate file, auto-deleted
## REPOSITORY INITIALIZATION
[3k tokens, only loaded during init]
**POST-EXECUTION**: Delete this file.
```

### ✅ GOOD: Conditional ADK Feature

**Before** (bloated):
```markdown
# .github/copilot-instructions.md

## ADK INTEGRATION GUIDE  <-- 2k tokens, only relevant for ADK projects
[detailed ADK patterns]
```

**After** (modular):
```yaml
# .sia.detected.yaml
features: [adk]
```

```markdown
# .sia/features/adk.md  <-- Only loaded if detected
## ADK INTEGRATION GUIDE
[detailed ADK patterns]
```

---

## Self-Evolution Notes

**Learned From**: User feedback on context contamination (2025-11-23)

**Trigger**: Observing that init protocol in main template wastes tokens on every request.

**Principle**: "Pay-per-use context" - only load what's needed, when it's needed.

**Framework Impact**: This is FRAMEWORK learning (applies to all SIA projects).

---

**Last Updated**: 2025-11-23  
**SIA Version**: 1.1.0  
**Author**: Self-evolved from user observation

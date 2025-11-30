# SIA Core Concepts

**Date**: 2025-11-23  
**Context**: Architectural definitions and operational modes.

---

## 1. SPR: Two Distinct Meanings

### SPR Skill (Sparse Priming Representation)
- **What**: Compression technique for LLM documentation (70-80% token reduction).
- **Who**: `spr_pack.md` agent (specialized sub-agent).
- **Commands**:
  - `/spr compress [file]` - Compress documentation to max density.
  - `/spr extract-matrix --target backend/src --output matrix/` - Extract docs from code.
- **Example**: `CONTINUE_HERE.spr.md` is written in SPR format (bullets, symbols, tables).

### Project SPR (Project Specific Agent)
- **What**: Markdown file acting as the "architectural brain" of the project.
- **Location**: `.sia/agents/{project_name}.md` (e.g., `.sia/agents/erp.md`).
- **Content**: DDD/SOLID/KISS philosophy, project patterns, lookup tables, quick reference.
- **Format**: Written using **SPR skill** (compression applied).
- **Purpose**: Mental map for the Super Agent when working on that specific project.

**Relationship**: The **Project SPR** (project file) is written in **SPR format** (compression technique).

---

## 2. Default Stack: AI-Native Architecture

**Source**: `sia/agents/sia.md` (DDD/AI-Native specialist agent)

### Greenfield Stack (New Project)
```
Backend:     Python 3.10+ + FastAPI + DDD/SOLID/KISS + uv
Database:    PostgreSQL 15 + TimescaleDB + PostGIS
Frontend:    React 18 + Vite (HMR <1s)
AI Layer:    Google ADK (OPTIONAL - agents as services, NOT core logic)
DevOps:      Docker Compose (hot reload all services)
Testing:     pytest + Playwright MCP
```

### Critical Principles

1. **AI is Optional, Not Mandatory**:
   - App 100% functional without AI agents.
   - AI = "Assistant" layer (recommendations, analysis), not business logic.
   - Example: `OrderAssistant` suggests discounts, but `Order` entity calculates total (deterministic).

2. **Docker for Everything**:
   - Development = `docker-compose up` (postgis + backend + frontend).
   - Production = `docker-compose -f docker-compose.prod.yml up`.
   - Hot reload: Backend (uvicorn --reload, 1-2s), Frontend (Vite HMR, <1s).
   - Principle: No "works on my machine" - Dev/Prod parity.

3. **DDD/SOLID/KISS Enforced**:
   - Pure Domain layer (no infra dependencies).
   - Repositories = interfaces (domain) + implementations (infrastructure).
   - KISS: Postgres before hypertables, monolith before microservices.

---

## 3. First Principles: Epistemological Foundation

### Definition
**First Principles Reasoning** = Recursive decomposition of problems until reaching fundamental truths that are self-evident, irreducible, independent, and universal.

**Core Protocol**:
```
1. WHAT are we trying to achieve?
2. WHY is this the goal? (Recursive until axiom)
3. WHAT do we know is fundamentally true?
4. WHAT are we assuming? (Eliminate)
5. HOW do we rebuild from axioms?
```

### Contrast with Conventional Thinking

| Conventional                  | First Principles                           |
| ----------------------------- | ------------------------------------------ |
| "Use X because it's standard" | "What problem does X solve fundamentally?" |
| Copy existing patterns        | Derive solution from axioms                |
| Assume inherited constraints  | Question every assumption                  |
| Follow best practices blindly | Validate practices against fundamentals    |

### Application in SIA

#### Planning (Requirements → QUANT)
```markdown
Feature: "Add caching"

❌ Conventional: "Add Redis because it's standard"

✅ First Principles:
Q: What's the fundamental problem?
FACT: API response 2s (violates <200ms axiom)
MEASUREMENT: 1.8s database query

Q: What are we assuming?
❌ ASSUMPTION: Caching needed
❌ ASSUMPTION: Redis is solution

Q: What's fundamentally true?
AXIOM 1: Simplest solution that works (KISS)
AXIOM 2: Optimize before adding complexity

SOLUTION: Add database index (1.8s → 0.05s)
JUSTIFIED: ✅ (simplest, biggest impact, zero complexity)
```

#### Development (Implementation)
```python
# ❌ CONVENTIONAL (No justification)
def save_user(user_data):
    db.execute("INSERT INTO users ...")

# ✅ FIRST PRINCIPLES (Axiom-justified)
def save_user(user: UserAggregate) -> Result[UserId, DomainError]:
    """
    AXIOM 1: Domain logic must not depend on infrastructure (DDD)
    AXIOM 2: Invalid state must be unrepresentable
    AXIOM 3: Side effects must be explicit
    
    JUSTIFICATION:
    - UserAggregate type: Guarantees invariants (Axiom 2)
    - Return Result[T, E]: Makes failure explicit (Axiom 3)
    - Repository pattern: Decouples domain from DB (Axiom 1)
    """
    if not user.is_valid():
        return Err(InvalidUserError(user.validation_errors))
    
    return self.repository.save(user)
```

#### QA (Testing)
```python
# ❌ CONVENTIONAL (Tests implementation)
def test_user_service_calls_db():
    assert mock_db.execute.called  # ← Tests HOW

# ✅ FIRST PRINCIPLES (Tests axioms)
def test_user_invariants_enforced():
    """
    AXIOM: Invalid users must be unrepresentable
    INVARIANT: ∀ user ∈ Users: user.email.is_valid() ∧ user.age >= 18
    """
    result = UserAggregate.create(email="invalid", age=25)
    assert result.is_err()  # ← Tests WHAT (invariant)
```

### Integration with SIA Capabilities

**Meta-Cognition + First Principles**:
- Meta-Cognition: Reasoning about reasoning
- First Principles: Foundation for that reasoning
- Result: Architectural decisions justified by axioms

**Automated Reasoning + First Principles**:
- First Principles: Extract axioms from requirements
- Automated Reasoning: Derive mathematical invariants from axioms
- Result: Invariants trace back to fundamental truths

**Self-Discovery + First Principles**:
- Conventional: Guess project type from folder names
- First Principles: Base detection on observable facts
- Result: `pyproject.toml` exists → Python project (no guessing)

**Self-Evolution + First Principles**:
- Observation: "Skills take 30s to run"
- Axiom: Developer time > compute time
- Solution: Parallelize skills (justified by axiom)

### Anti-Patterns

```markdown
❌ Cargo Cult: "Use microservices because Netflix does"
✅ First Principles: Do we have Netflix-scale problems? (No → Monolith)

❌ Assumption: "We'll need Kafka for events"
✅ First Principles: What's the event volume? (10/min → PostgreSQL LISTEN/NOTIFY)

❌ Implementation Tests: "Test that method X calls method Y"
✅ First Principles: Test domain invariants (Input → Expected Output)
```

### Complete Documentation

See `core/FIRST_PRINCIPLES.md` for:
- Philosophical foundation
- Complete methodology (Planning, Development, QA)
- Integration with all SIA workflows
- Operational protocols
- Anti-patterns and examples

---

## 4. Two Phases of Initialization

### Phase 1: Installer Script (Mechanical, Safe)
**Execute**: `bash sia/installer/install.sh` or `smart_init.py`

**Actions**:
1. Create `.sia/` structure (agents, knowledge, requirements, skills).
2. Detect legacy structures (`requirements/`, `.agents/`) - **DO NOT move them**.
3. Install base skills (check_complexity.sh, audit_ddd.py, etc.).
4. Run auto-discovery (tech stack, bounded contexts).
5. Generate `.sia.detected.yaml` + `.github/copilot-instructions.md`.

**Result**: Skeleton ready, **without touching user code**.

### Phase 2: Super Agent Initialization (Cognitive, Contextual)
**Execute**: User in VS Code Copilot Chat

#### Scenario A: Brownfield (Existing Code)
**Prompt**: `"Initialize SIA for this repository"`

**Actions**:
1. Read `.sia.detected.yaml` (detected tech stack).
2. Analyze existing architecture (DDD compliance, bounded contexts).
3. Generate **Project SPR** (`.sia/agents/{project}.md`) - Project mental map.
4. Detect technical debt (complexity, SOLID violations).
5. Propose migrations (e.g., "Migrate `requirements/` to `.sia/requirements/`?").
6. Configure requirements workflow (`.sia/requirements/README.md`).

**Result**: Super Agent "understands" the repo and can work with existing architecture.

#### Scenario B: Greenfield (New Project)
**Prompt**: `"Initialize SIA. I want to build a SaaS for pet grooming."`

**Actions**:
1. Propose stack (default AI-Native: FastAPI+React+Docker, or custom if specified).
2. Scaffold folders (backend/src/{project}/domain|application|infrastructure|api).
3. Generate **Project SPR** with architectural vision.
4. Create `docker-compose.yml` (postgis + backend + frontend).

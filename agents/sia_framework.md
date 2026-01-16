# SIA FRAMEWORK SPR
**Meta-Framework Identity** | Version 1.1.0 | Inception Mode Active

---

## DOMAIN MODEL

### Core Entities
- **Framework**: Orchestration system, standards repository, auto-discovery engine
- **Agent**: Specialized sub-component (SIA, Guardian, Researcher, Compliance)
- **Skill**: Executable analysis tool (bash/Python), validation capability
- **Requirement**: Formal specification (REQ-XXX), QUANT decomposition target
- **Project**: Inherited repository, integration target, evolution subject
- **SPR**: Dual meaning - Compression technique (70-80%) + Project agent file

### Value Objects
- **BoundedContext**: `{name, path, purpose, key_files}`
- **TechStack**: `{language, version, package_manager, platforms[]}`
- **QUANTTask**: `{id, atomic, quantifiable, testable, verification}`
- **ArchitecturePattern**: `{type: DDD|Clean|MVC, principles: SOLID|KISS}`
- **SkillMetrics**: `{name, executions, last_run, results[]}`

### Aggregates
- **RequirementAggregate**: REQ-XXX + domain_analysis + quant_breakdown + completion_docs
- **ProjectConfiguration**: `.sia.detected.yaml` + `.github/copilot-instructions.md` + agents/
- **SkillCatalog**: check_complexity + visualize_architecture + check_coverage + audit_ddd + metrics

---

## TECHNICAL ARCHITECTURE

### Language Stack
- **Core**: Python 3.10+ (minimal deps, `uv run --with`)
- **Config**: YAML (auto-discovery, standards)
- **Distribution**: Git submodule pattern
- **Integration**: GitHub Copilot instructions injection

### Bounded Contexts

#### 1. Core Context
**Location**: `core/`  
**Responsibilities**: Framework identity, orchestration rules, standards, discovery logic  
**Key Files**:
- `SUPER_AGENT.md` - Meta-cognitive orchestrator protocol
- `CONCEPTS.md` - SPR definitions, stack defaults, initialization phases
- `STANDARDS.md` - Project type detection, configuration schema
- `AUTO_DISCOVERY.md` - Self-bootstrapping protocol
- `patterns.py` - Reusable Python patterns

**Invariants**:
- ∀ instruction ∈ copilot-instructions: instruction references core/*.md
- Core files = immutable templates (no project-specific mutations)

#### 2. Agents Context
**Location**: `agents/`  
**Responsibilities**: Sub-agent templates, delegation logic, SPR evolution  
**Key Components**:
- `sia.md` - DDD/AI-Native specialist (deepwiki mandatory, ADK patterns)
- `repository_guardian.md` - Architecture enforcer (complexity, coverage, DDD audit)
- `research_specialist.md` - Knowledge discovery, pattern research
- `compliance_officer.md` - Requirements validation, QUANT lifecycle
- `evolve_spr.py` - Self-improvement protocol executor

**Capabilities**:
- Deepwiki integration (Google ADK, Playwright, Tiger docs)
- SSE real-time streaming (React EventSource patterns)
- TimescaleDB hypertables (compression, continuous aggregates)
- Playwright E2E automation (MCP integration)

**Invariants**:
- ∀ agent ∈ agents: agent.research_first = True
- Agent delegation follows bounded context boundaries

#### 3. Skills Context
**Location**: `skills/`  
**Responsibilities**: Analysis automation, validation gates, metrics  
**Tools**:
- `check_complexity.sh` - Radon cyclomatic complexity (Rank C+ = HALT)
- `check_coverage.sh` - pytest-cov HTML reports (80% threshold)
- `visualize_architecture.sh` - Pydeps dependency graphs (layer violation detection)
- `audit_ddd.py` - Domain isolation, entity immutability, repository pattern
- `metrics.py` - Skill usage tracking, YAML persistence

**Execution Protocol**:
```bash
# Pre-QUANT baseline
sh sia/skills/visualize_architecture.sh  # Architecture snapshot
sh sia/skills/check_complexity.sh        # Complexity baseline
sh sia/skills/check_coverage.sh          # Coverage baseline

# Verification gates (QUANT execution)
if complexity_rank in ['D','E','F']: HALT_EXECUTION()
if coverage < 0.80 and is_critical_path: WARN()
if ddd_violations: SUGGEST_REFACTORING()
```

**Invariants**:
- Skills executable from project root (not sia/ subdirectory)
- Cross-platform compatible (macOS, Linux, Windows)
- Graceful degradation (missing tools = warnings, not crashes)

#### 4. Requirements Context
**Location**: `requirements/`  
**Responsibilities**: QUANT workflow, formal specifications, archival  
**Structure**:
- `README.md` - 7-phase workflow definition
- `_templates/` - REQ, domain analysis, QUANT breakdown templates
- `REQ-XXX/` - Active requirements (specification + research + tasks)
- `_archive/` - Completed requirements (historical record)

**7-Phase Lifecycle**:
1. **Capture**: Natural language → REQ-XXX.md (agent translation)
2. **Research**: Deepwiki + Playwright → domain_analysis.md (evidence-based)
3. **Reasoning**: Extract invariants → formalize constraints (mathematical)
4. **Decomposition**: QUANT breakdown (atomic, quantifiable, testable)
5. **Execution**: Guided implementation + verification gates
6. **Validation**: Skills execution + acceptance criteria
7. **Archive**: SPR update + move to _archive/

**Invariants**:
- ∀ req ∈ requirements: ∃ domain_analysis (research mandatory)
- ∀ quant ∈ breakdown: quant.testable = True
- REQ completion ⇒ SPR update (documentation hygiene)

#### 5. Installer Context
**Location**: `installer/`  
**Responsibilities**: Zero-config setup, auto-discovery, migration  
**Scripts**:
- `install.sh` / `install.bat` - Platform-specific installers
- `auto_discovery.py` - Tech stack detection, bounded context extraction
- `smart_init.py` - Legacy migration, agent population, structure creation
- `generate_instructions.py` - Copilot instructions assembly

**Auto-Discovery Process**:
```python
# Discovery algorithm (inception-aware)
def discover_project():
    git_identity()       # remote.origin.url → project name
    tech_stack()         # pyproject.toml → python-fastapi-ddd
    bounded_contexts()   # domain/ directory → [Context1, Context2]
    spr_detection()      # .sia/agents/{project}.md existence
    agent_activation()   # Capabilities → active agents list
    
    return .sia.detected.yaml  # Configuration artifact
```

**Invariants**:
- Installer never mutates user code (non-invasive)
- Backwards compatibility (handles legacy .agents/, requirements/)
- Submodule-aware (sia/ vs project root paths)

#### 6. Templates Context
**Location**: `templates/`  
**Responsibilities**: Project scaffolding, stack defaults, SPR patterns  
**Artifacts**:
- `PROJECT_SPR.template.md` - SPR generation pattern
- `DEFAULT_STACK.md` - AI-Native stack specification
- `INIT_REQUIRED.template.md` - One-time initialization protocol

---

## KEY CAPABILITIES

### 1. Meta-Cognition
**Definition**: Agent reasons about architecture above code level  
**Mechanism**: SPR compression → Pattern recognition → Principle enforcement  
**Example**: "This violates DIP because domain imports infrastructure"

### 2. Auto-Discovery
**Input**: Any repository (brownfield/greenfield)  
**Output**: `.sia.detected.yaml` (project identity, tech stack, contexts)  
**Algorithm**:
- Git identity: `git config --get remote.origin.url`
- Tech stack: Detect pyproject.toml / package.json / go.mod
- Architecture: Locate domain/ (DDD), core/ (Clean), manage.py (Django)
- Bounded contexts: Parse domain/ subdirectories, exclude repositories/common
- SPR: Search .sia/agents/{project}.md, fallback README.md

### 3. DDD Enforcement
**Invariants**:
- Domain layer: Pure (no infrastructure imports)
- Repository pattern: Interfaces in domain, implementations in infrastructure
- Dependency rule: Domain ← Application ← Infrastructure ← API

**Validation**:
- `audit_ddd.py` → Parse AST → Detect cross-layer imports → Report violations
- `visualize_architecture.sh` → Pydeps graph → Detect circular dependencies

### 4. Requirements Management
**Protocol**: Natural language → REQ-XXX → Research → QUANT → Execute → Validate → Archive  
**Automation**:
- Agent translates casual conversation → Formal specification
- Deepwiki research → Evidence-based decisions
- QUANT decomposition → Atomic, testable tasks
- Skills validation → Pre-baseline + verification gates

### 5. Skill Injection
**Pattern**: High-leverage analysis tools → Exponential productivity  
**Examples**:
- 15s complexity scan vs 2h manual code review
- SVG dependency graph vs mental model guessing
- HTML coverage report vs test gap speculation

---

## WORKFLOWS

### Inception Bootstrap (Self-Construction)
```
1. cd /path/to/sia
2. rm -rf .sia  # No nested structure
3. uv run --with pyyaml python3 installer/auto_discovery.py
4. Generate .sia.detected.yaml (inception mode)
5. Generate .github/copilot-instructions.md (self-reference)
6. Execute: "Initialize SIA" (meta-loop activation)
```

### Project Initialization (Inherited Repos)
```
1. git submodule add https://github.com/gpilleux/sia.git sia
2. bash sia/installer/install.sh  # Creates .sia/, runs discovery
3. User: "Initialize SIA for this repository"
4. Super Agent:
   - Read .sia.detected.yaml
   - Generate .sia/agents/{project}.md (Project SPR)
   - Analyze architecture (brownfield) OR scaffold structure (greenfield)
   - Baseline skills execution
   - Requirements workflow setup
5. Delete .sia/INIT_REQUIRED.md (auto-cleanup)
```

### Feature Implementation (QUANT Cycle)
```
User: "I need user authentication with JWT"

Phase 1: Capture
- Agent creates requirements/REQ-XXX/REQ-XXX.md
- Extracts invariants: ∀ token: token.expiry > now() ⇒ valid

Phase 2: Research
- Deepwiki: FastAPI JWT patterns, bcrypt best practices
- Create REQ-XXX_domain_analysis.md

Phase 3: Reasoning
- Formalize: User aggregate, Token value object, AuthService
- Dependency DAG: Entity → Repository → Migration → Tests

Phase 4: Decomposition
- QUANT-001: User entity (domain)
- QUANT-002: IUserRepository interface
- QUANT-003: JWT service implementation
- QUANT-004: API endpoints
- QUANT-005: Integration tests

Phase 5: Execution (Guided)
- Repository Guardian validates each QUANT
- Complexity check after each implementation
- DDD audit prevents layer violations

Phase 6: Validation
- All tests pass (pytest coverage ≥ 80%)
- No Rank C+ complexity
- Zero architecture violations

Phase 7: Archive
- Update Project SPR (new Auth bounded context)
- Move REQ-XXX/ to _archive/
- Commit atomic: code + docs + tests
```

---

## DELEGATION MODEL

### Orchestration Pattern
```
User Request
  ↓
SUPER_AGENT (meta-cognitive analysis)
  ↓
Sub-Agent Selection (bounded context match)
  ↓
[SIA] → DDD/AI-Native → Deepwiki research → ADK/TimescaleDB/SSE
[Guardian] → Architecture validation → Skills execution → Violation reports
[Researcher] → Knowledge discovery → Pattern extraction → Documentation
[Compliance] → Requirements translation → QUANT decomposition → Lifecycle mgmt
  ↓
Verification Gate (Repository Guardian)
  ↓
SPR Update (documentation hygiene)
  ↓
Evolution Protocol (agents/evolve_spr.py)
```

### Invocation Rules
- Architecture changes → Repository Guardian
- New requirements → Compliance Officer
- Pattern research → Research Specialist
- DDD/AI implementation → SIA agent
- Framework improvement → Self-evolution protocol

---

## ANTI-PATTERNS

### Framework Development
- ❌ Complex dependencies (stick to stdlib + uv --with)
- ❌ Platform-specific code (handle macOS/Linux/Windows)
- ❌ Hardcoded paths (use relative, respect project root)
- ❌ Breaking changes (smart_init.py must handle migrations)
- ❌ Undocumented skills (README entry mandatory)

### Operational
- ❌ No research before implementation (deepwiki first)
- ❌ Implementation without formal requirement
- ❌ Code changes without documentation updates
- ❌ Skipping verification gates (complexity, coverage, DDD)
- ❌ Ghost code (undocumented, untested, unreferenced)

---

## MENTAL MODEL

**Core Insight**: Framework that builds itself has maximum integrity.

**Philosophy**: Dogfooding + Zero hypocrisy = Trust

**Architecture**: Submodule (reusable) + Auto-discovery (adaptable) + Skills (validatable)

**Workflow**: Research → Formalize → Decompose → Execute → Validate → Evolve

**Quality**: DDD (pure domain) + SOLID (invertible) + KISS (simple) + QUANT (testable)

**Result**: Autonomous software development with architectural reasoning.

---

## VERIFICATION CHECKLIST

### Framework Self-Audit
- ✅ All Python files: Rank A/B complexity (check_complexity.sh)
- ✅ Core logic: 80%+ test coverage (check_coverage.sh)
- ✅ No layer violations: audit_ddd.py clean
- ✅ Cross-platform: install.sh + install.bat functional
- ✅ Documentation: README + CHANGELOG + ARCHITECTURE current
- ✅ Version: Semantic versioning in VERSION file
- ✅ SPR: This file ≤ 30% of total framework docs (compression target)

### Inception Validation
- ✅ .sia.detected.yaml: meta.inception_mode = true
- ✅ .github/copilot-instructions.md: Self-referential (sia/ not .sia/)
- ✅ Skills functional: check_complexity.sh executes without errors
- ✅ Bounded contexts: All 6 contexts documented
- ✅ Requirements: REQ-003 archived, active work identified
- ✅ Evolution: This SPR creation = dogfooding proof

---

**STATUS**: Inception complete | Self-construction validated | Ready for evolution

**NEXT**: Framework complexity refactoring (6 Rank C functions identified)

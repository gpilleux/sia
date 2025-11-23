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

## 3. Two Phases of Initialization

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

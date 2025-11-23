# SIA Default Stack - AI-Native Architecture

**Source**: `sia/agents/sia.md` (inside SIA submodule)  
**Philosophy**: AI-Native by design, robust without AI. Docker-first deployment.

**Note**: This document describes the stack that will be scaffolded in the **project root**, not inside the `sia/` submodule.

---

## Stack Specification

### Backend
- **Language**: Python 3.10+
- **Framework**: FastAPI (async, dependency injection, auto-docs)
- **Architecture**: DDD/SOLID/KISS (Domain → Application → Infrastructure → API)
- **Package Manager**: `uv` (fast, reproducible, pyproject.toml)

### Database
- **Core**: PostgreSQL 15+
- **Time-Series**: TimescaleDB (hypertables, compression, retention)
- **Geospatial**: PostGIS (spatial queries, routing)
- **Principle**: Relational first, hypertables only for time-series (>100K rows)

### Frontend
- **Framework**: React 18 (hooks, functional components)
- **Build Tool**: Vite (HMR <1s, ES modules)
- **Real-Time**: EventSource SSE (agent streaming, CORS configured)
- **UI**: Design tokens (CSS variables), Component composition

### AI Layer (Optional)
- **Framework**: Google ADK (Agent Development Kit)
- **Pattern**: Agents as DDD services (not core logic)
- **Models**: Gemini 2.5 Flash/Pro
- **Orchestration**: LlmAgent + sub_agents (Sequential/Parallel/Loop)
- **Streaming**: SSE + AsyncGenerator (real-time feedback)
- **Memory**: Sessions + State + MemoryService
- **Protocol**: A2A (Agent-to-Agent communication)

**Critical**: AI layer is **additive**, not **foundational**. App must work 100% without agents. AI = assistants, not business logic.

### DevOps
- **Containerization**: Docker Compose (all services)
- **Hot Reload**: 
  - Backend: `uvicorn --reload` (1-2s)
  - Frontend: Vite HMR (<1s)
  - Database: Volume persistence
- **Services**: `postgis`, `backend`, `frontend`, `solver` (if applicable)
- **Principle**: Development = Production parity. No "works on my machine".

### Testing
- **Unit**: pytest (domain layer, pure logic)
- **Integration**: pytest + real PostgreSQL (repositories)
- **E2E**: Playwright MCP (browser automation, SSE validation)
- **Coverage**: pytest-cov (>80% target)

---

## Directory Structure (Greenfield Scaffold)

**Important**: This structure is created in the **project root**, not inside the `sia/` submodule.

```
project-name/                   # Project root (NOT inside sia/ submodule)
├── docker-compose.yml          # All services (postgis, backend, frontend)
├── init.sql                    # Database schema + seed data
├── pyproject.toml              # Python dependencies (uv managed)
├── backend/
│   ├── Dockerfile              # Python 3.10 + uv
│   ├── src/
│   │   └── {project}/
│   │       ├── domain/         # Entities, VOs, Repository interfaces
│   │       │   ├── {context1}/
│   │       │   │   ├── entities.py
│   │       │   │   └── repositories.py (interfaces)
│   │       │   └── {context2}/
│   │       ├── application/    # Use cases (orchestration)
│   │       │   └── {context}/
│   │       │       └── use_cases.py
│   │       ├── infrastructure/ # Postgres repos, ORM models
│   │       │   ├── database/
│   │       │   │   └── models.py (SQLAlchemy)
│   │       │   └── postgres/
│   │       │       └── repositories.py (implementations)
│   │       ├── api/            # FastAPI routes, schemas
│   │       │   ├── routes/
│   │       │   │   └── {context}.py
│   │       │   ├── schemas/
│   │       │   │   └── {context}.py (Pydantic DTOs)
│   │       │   └── main.py
│   │       └── agents/         # ADK agents (optional)
│   │           └── {context}_assistant.py
│   └── tests/
│       ├── domain/             # Pure logic (mocked repos)
│       ├── application/        # Use case tests
│       ├── integration/        # Real DB tests
│       └── api/                # FastAPI TestClient
├── frontend/
│   ├── Dockerfile              # Node 18 + Vite
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── components/
│   │   │   └── {context}/
│   │   ├── hooks/              # TanStack Query hooks
│   │   ├── contexts/           # React Context (user, theme)
│   │   ├── styles/
│   │   │   └── tokens.css      # Design tokens (90 CSS variables)
│   │   └── App.jsx
│   └── e2e/                    # Playwright tests
├── sia/                        # SIA submodule (framework, not edited)
└── .sia/                       # Project-specific SIA data (created by installer)
    ├── agents/
    │   └── {project}.md        # Project SPR (architectural agent)
    ├── requirements/
    ├── skills/
    └── knowledge/
```

**Key Distinction**:
- `sia/` = SIA framework (git submodule, read-only for project)
- `.sia/` = Project-specific data (agents, requirements, knowledge)

---

## Deployment Flow

### Local Development
```bash
# 1. Clone/Scaffold project
git clone <repo> && cd <project>

# 2. Start all services (hot reload enabled)
docker-compose up --build

# 3. Services available:
# - Backend API: http://localhost:8000
# - Frontend: http://localhost:5173
# - Database: postgresql://localhost:5432
# - Docs: http://localhost:8000/docs

# 4. Code changes auto-reload (no restart needed)
```

### Production
```bash
# 1. Build production images
docker-compose -f docker-compose.prod.yml build

# 2. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 3. Nginx reverse proxy (production frontend)
# - Static build served
# - API proxied to backend container
```

---

## AI-Native Principles

### 1. Agents as Services (not Core Logic)
```python
# ❌ WRONG: Business logic in agent
class OrderAgent(LlmAgent):
    async def calculate_total(self, items):
        # AI calculating prices = non-deterministic = BAD
        pass

# ✅ CORRECT: Agent uses domain entity
class OrderAssistant(LlmAgent):
    async def suggest_discount(self, order: Order):
        # Domain entity calculates, agent suggests
        current_total = order.calculate_total()  # Deterministic
        suggestion = await self.generate_suggestion(current_total)
        return suggestion
```

### 2. Streaming for Long Operations (>2s)
```python
# Agent endpoint with SSE
@app.post("/agent/analyze/stream")
async def analyze_stream():
    async def event_generator():
        async for event in agent.run_async(prompt):
            yield f"data: {event.json()}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

### 3. Docker Compose for All Services
```yaml
# docker-compose.yml (AI-Native example)
services:
  postgis:
    image: timescale/timescaledb-ha:pg15-ts2.13
    volumes: ["./init.sql:/docker-entrypoint-initdb.d/init.sql"]
  
  backend:
    build: ./backend
    command: uvicorn src.{project}.api.main:app --reload --host 0.0.0.0
    volumes: ["./backend:/app"]  # Hot reload
    environment:
      - DATABASE_URL=postgresql://user:pass@postgis:5432/db
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}  # ADK agents
    depends_on: [postgis]
  
  frontend:
    build: ./frontend
    command: npm run dev -- --host
    volumes: ["./frontend:/app", "/app/node_modules"]
    ports: ["5173:5173"]
```

---

## When to Deviate from Default Stack

**Keep if**:
- Building web app (API + frontend)
- Need real-time features (SSE/WebSocket)
- Plan to integrate AI assistants (optional now, later)
- Want DDD architecture (bounded contexts)
- Require geospatial/time-series data

**Replace if**:
- Mobile-first → React Native (frontend)
- Static site → Next.js SSG
- CLI tool → Python + Typer (no FastAPI/React)
- Pure microservices → Drop monolith, add service mesh
- Enterprise Java shop → Spring Boot (backend), keep DDD
- .NET environment → ASP.NET Core (backend), keep React

**Override Stack**:
```
User: "Initialize SIA. I want a Java Spring Boot app for inventory management."

Agent: "Detected stack override: Java + Spring Boot
Will scaffold:
- Backend: Spring Boot + DDD
- Database: PostgreSQL
- Frontend: React + Vite
- Docker: Compose for all services
- Testing: JUnit (backend), Playwright (E2E)

Note: AI-Native layer (ADK) not available for Java. Manual agent integration required."
```

---

## Stack Validation Checklist

Before scaffolding, Super Agent validates:
- [ ] Docker installed (required for all services)
- [ ] Python 3.10+ / Node 18+ (if default stack)
- [ ] PostgreSQL client available (for migrations)
- [ ] Git repository initialized
- [ ] `.sia/` structure created
- [ ] No conflicting port bindings (5173, 8000, 5432)

**If validation fails** → Agent prompts installation instructions or suggests alternatives.

---

## Stack Evolution (Self-Improving)

The Super Agent tracks **stack decisions** in `.sia/knowledge/active/STACK_DECISIONS.md`:

```markdown
# Stack Decision Log

## 2025-11-23: Initial Scaffold
- Stack: Python + FastAPI + React + Docker
- Reason: AI-Native default, DDD support
- AI Layer: Deferred to Phase 2 (ADK)

## 2025-12-01: Added TimescaleDB
- Trigger: REQ-005 (metrics time-series)
- Decision: Hypertable for `metrics` table (1M+ rows expected)
- Compression: 7d policy, 90d retention

## 2026-01-15: Migrated to Next.js
- Trigger: REQ-020 (SEO requirement)
- Decision: React → Next.js 14 (SSG + SSR)
- Impact: Frontend rebuild (2 days)
```

**Principle**: Stack evolves based on **requirements**, not trends.

---

**Default Stack Summary**: Python + FastAPI + PostgreSQL + React + Docker. AI-Native ready (ADK optional). DDD/SOLID/KISS enforced. Hot reload <2s. Production-ready from day 1.

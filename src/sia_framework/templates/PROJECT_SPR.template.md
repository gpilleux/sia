# {{PROJECT_NAME}} - WORKSPACE NAVIGATION SPR

## CORE MISSION
[Concise 1-2 sentence mission statement. What problem does this project solve? For whom?]

**Example**:
> AI-Native Document Intelligence Platform for Chilean government PDFs. RAG pipeline: PDF → embeddings → pgvector → semantic search → LLM → frontend.

---

## ARCHITECTURE PARADIGM

**Pattern**: [DDD Clean Architecture | MVC | Microservices | Monolith]

**Key Principles**: [Domain-driven design, SOLID, KISS, etc.]

**Structure**:
```
[High-level directory tree showing layers/modules]
```

**Bounded Contexts** (if DDD):
1. **[Context 1]**: [Brief description]
2. **[Context 2]**: [Brief description]

---

## DOMAIN MODEL

### [Context 1] Context

**Aggregate Roots**:
- **[Entity]** (Aggregate Root): [Fields]. [Key invariants].
- **[Entity]** (Entity): [Relationship to aggregate]. [Fields].
- **[ValueObject]** (Value Object): [Immutable properties].

**Aggregate Pattern**: [Which entities are loaded together, transaction boundaries]

### [Context 2] Context

[Repeat for each bounded context]

---

## INFRASTRUCTURE LAYER

### [Subsystem 1]
- **[file.py]**: [Purpose, key functions]
- **[schema.sql]**: [Database schema, tables, indexes]
- **[repository.py]**: Implements I[Name]Repository
  - `method()`: [Description]

### [Subsystem 2]
[Repeat for each infrastructure component]

---

## SHARED KERNEL (Reusable Components)

- **[component.py]**: [Shared utility, cross-cutting concern]

---

## APPLICATION LAYER

- **[use_case.py]**: orchestrates [domain operation]
  - Workflow: [step 1] → [step 2] → [step 3]

---

## API/CLI LAYER

- **cli.py** (Click commands):
  - `command`: [Description]
- **api/main.py**: [FastAPI/Flask/etc] application
- **api/v1/[resource].py**: [Endpoints]

---

## TECH STACK

**Language**: Python 3.10+ | TypeScript | etc.

**Backend**: [Framework, database, key libraries]

**Frontend**: [Framework, UI library]

**Tools**: [Package manager, Docker, CI/CD]

---

## KEY WORKFLOWS

### [Workflow 1 Name]

**Flow**: [Step-by-step description with file references]

```
1. [Action] → [file.py:function()]
   ↓
2. [Processing] → [service.py:method()]
   ↓
3. [Output] → [Result]
```

**Key Files**: [List files involved in this workflow]

---

## FILE NAVIGATION PATTERNS

### Domain Logic
- `domain/entities.py`: [frozen dataclasses, enums]
- `domain/repositories/`: [abstract interfaces]

### Infrastructure Implementations
- `infrastructure/repositories/[impl].py`: [production implementations]
- `infrastructure/[subsystem]/`: [external integrations]

### Application Logic
- `application/[use_case].py`: [use case orchestrators]

### API Endpoints
- `api/v1/[resource].py`: [REST/GraphQL endpoints]

### Configuration
- `.env`: [Environment variables]
- `pyproject.toml`: [Dependencies]
- `docker-compose.yml`: [Services]

### Database
- `infrastructure/db/schema.sql`: [DDL]
- `infrastructure/db/migrations/`: [Alembic/etc migrations]

### Testing
- `test_[feature].py`: [Test descriptions]

### Documentation
- `docs/[category]/`: [Documentation structure]

---

## DATA FLOW

**[Primary Flow Name]**:
1. [Input] → `[function()]` → [intermediate data]
2. [Processing] → `[service.method()]` → [transformation]
3. [Storage] → `[repository.save()]` → [persistence]
4. [Output] → [Result format]

---

## MENTAL MODEL COMPRESSION

**Essence**: [Ultra-concise 2-3 sentence summary of the entire system. What goes in, what comes out, how it works.]

**Example**:
> PDF → text chunks → OpenAI embeddings (1536-dim) → pgvector → cosine similarity search → context injection → GPT streaming → frontend. DDD layers enforce dependency inversion. Repository factory swaps persistence.

**Critical Path**: 
1. **[Primary User Journey]**: [Step-by-step with file references]
2. **[Secondary Flow]**: [Alternative path]

**Architecture DNA**: [Core pattern in one sentence]

**Example**:
> Domain (pure logic) ← Application (use cases) ← Infrastructure (repositories, parsers, LLM) ← API/CLI (interfaces). No upward dependencies.

**Key Invariants**:
- [Invariant 1]: [Always true constraint]
- [Invariant 2]: [Business rule that never changes]
- [Invariant 3]: [Technical constraint]

---

## CURRENT STATUS

**Completed**:
- ✅ [Feature 1]
- ✅ [Feature 2]

**In Progress**:
- 🔄 [Feature 3]

**Planned**:
- 📋 [Feature 4]

---

## NOTES

[Any additional context, quirks, known issues, or important reminders]

---

**Last Updated**: {{DATE}}
**SIA Version**: {{SIA_VERSION}}

# templates/ - SIA Template Index

Template files for SIA framework initialization and usage.

---

## Available Templates

### `PROJECT_SPR.template.md`

**Purpose**: Structure for project System Personality Record (SPR)

**Usage**: Copied during "Initialize SIA" protocol to `.sia/agents/<project>.md`

**Compression Goal**: 10,000 lines of codebase → 2,000 tokens

**Sections**:
- Core Mission
- Architecture Paradigm (DDD, Clean Architecture, MVC, etc.)
- Domain Model (aggregates, entities, value objects)
- Infrastructure Layer
- Application Layer
- API/CLI Layer
- Tech Stack
- Key Workflows
- Mental Model Compression
- File Navigation Patterns
- Key Invariants

**Token Cost**: Template itself ~300 tokens, generated SPR ~2000 tokens

---

### `INIT_REQUIRED.template.md`

**Purpose**: One-time repository initialization instructions

**Usage**: Copied by installer to `.sia/INIT_REQUIRED.md`

**Lifecycle**: 
1. Installer creates `.sia/INIT_REQUIRED.md`
2. User triggers: "Initialize SIA for this repository"
3. SUPER AGENT reads instructions (~3k tokens)
4. SUPER AGENT executes 6-step protocol
5. **Auto-cleanup**: Deletes `.sia/INIT_REQUIRED.md`

**Why Separate**: Prevents 3k tokens of one-time context from contaminating permanent template

**Token Cost**: ~3000 tokens (one-time only)

**See**: `sia/core/PROMPT_PLACEMENT.md` for context hygiene principles

---

## Template Usage Pattern

```bash
# During installation
cp sia/templates/INIT_REQUIRED.template.md .sia/INIT_REQUIRED.md

# During initialization (user triggers via Copilot)
# SUPER AGENT reads .sia/INIT_REQUIRED.md
# SUPER AGENT uses PROJECT_SPR.template.md as guide
# SUPER AGENT generates .sia/agents/<project>.md
# SUPER AGENT deletes .sia/INIT_REQUIRED.md (cleanup)
```

---

## Token Efficiency

| Template | Permanent Context | One-Time Context |
|----------|-------------------|------------------|
| `PROJECT_SPR.template.md` | ✅ (~2k tokens in generated SPR) | - |
| `INIT_REQUIRED.template.md` | - | ✅ (~3k tokens, deleted after use) |

**Total Permanent**: ~2k tokens (only PROJECT SPR)  
**Total One-Time**: ~3k tokens (INIT protocol, auto-cleaned)

---

## Adding New Templates

1. Create template file in `sia/templates/`
2. Add entry to this README
3. Document token cost and lifecycle
4. Update installer if auto-copied
5. Test in fresh repository

**Guidelines**:
- Follow SPR format (high-density, no verbosity)
- Use `{{PLACEHOLDERS}}` for auto-replacement
- Include usage examples
- Document cleanup requirements (if temporary)

---

See `CONTRIBUTING.md` for template contribution standards.

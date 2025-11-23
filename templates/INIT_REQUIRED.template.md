# ⚠️ REPOSITORY INITIALIZATION REQUIRED

**ONE-TIME TASK**: This repository requires SIA framework initialization.

**User Trigger**: Say to GitHub Copilot: **"Initialize SIA for this repository"**

---

## Initialization Protocol

Execute the following steps to complete repository setup:

### 1. Analyze Repository Structure

- Read `.sia.detected.yaml` for auto-detected context
- Identify architecture pattern (DDD, Clean Architecture, MVC, etc.)
- Map bounded contexts and domain layers (if applicable)
- Detect tech stack and frameworks

### 2. Generate Project SPR

Create `.sia/agents/{{PROJECT_NAME}}.md` following `sia/templates/PROJECT_SPR.template.md`:

**Required Sections**:
- Core Mission (1-2 sentences)
- Architecture Paradigm (pattern + principles)
- Domain Model (aggregates, entities, value objects if DDD)
- Infrastructure Layer (repositories, external services)
- Application Layer (use cases)
- API/CLI Layer (interfaces)
- Tech Stack
- Key Workflows (critical paths)
- Mental Model Compression (10k lines → 2k tokens)
- File Navigation Patterns
- Key Invariants

**Compression Goal**: Reduce 10,000 lines of codebase into 2,000 tokens of essential context.

### 3. Detect Specialized Agents

Based on architecture, create agent files in `.sia/agents/`:

- **DDD/Clean Architecture detected** → `repository_guardian.md`
  - Enforces: Domain independence, aggregate boundaries, DDD patterns
  
- **Research-heavy project** → Research Specialist (already in framework)

- **Multi-module monorepo** → Module Coordinator
  - Manages: Cross-module dependencies, shared kernels

- **Legacy codebase** → Refactoring Advisor
  - Guides: Incremental modernization, technical debt reduction

**Template**: Use `sia/templates/AGENT.template.md` if exists, or create minimal SPR format.

### 4. Populate Knowledge Base

Create `.sia/knowledge/active/README.md` with:
- Project overview (high-level context)
- Domain glossary (if DDD: ubiquitous language terms)
- Key decisions (architecture decision records)
- Research cache (if research-heavy)

### 5. Initialize Skills Catalog

Create `.sia/skills/README.md` listing:
- Project-specific automation scripts
- Reference to framework skills (`sia/skills/check_complexity.sh`, etc.)
- Placeholder for future custom skills

### 6. Update Copilot Instructions

Verify `.github/copilot-instructions.md`:
- Replace `{{PROJECT_NAME}}` with actual project name
- Replace `{{PROJECT_TYPE}}` with detected type
- Replace `{{BOUNDED_CONTEXTS}}` with comma-separated list
- Replace `{{PROJECT_SPR_CONTENT}}` with full SPR from step 2
- Update `{{REQUIREMENTS_STATUS}}` to "System initialized. Ready for requirements."

---

## Expected Output

After successful initialization:

✅ `.sia/agents/{{PROJECT_NAME}}.md` (Project SPR)  
✅ `.sia/agents/repository_guardian.md` (if DDD detected)  
✅ `.sia/knowledge/active/README.md` (Project overview)  
✅ `.sia/skills/README.md` (Skills catalog)  
✅ Updated `.github/copilot-instructions.md` (All placeholders replaced)

---

## Post-Execution Cleanup

**CRITICAL**: After successful initialization, **DELETE THIS FILE**:

```bash
rm .sia/INIT_REQUIRED.md
git add .sia/
git commit -m "chore: Complete SIA initialization"
```

**Rationale**: This file is ONE-TIME context. Keeping it permanently would contaminate the context window on every future request. See `sia/core/PROMPT_PLACEMENT.md` for details.

---

## Troubleshooting

### "Cannot find .sia.detected.yaml"

```bash
# Re-run auto-discovery
cd sia && uv run installer/auto_discovery.py
```

### "Project type is 'generic'"

This means auto-discovery didn't detect a specific framework. Manually update:

```yaml
# .sia.detected.yaml
project:
  type: python-fastapi-ddd  # or react-nextjs, etc.
```

### "Don't know what to put in Project SPR"

Use `sia/templates/PROJECT_SPR.template.md` as guide. Fill what you can detect:
- Read `README.md`, `package.json`, `pyproject.toml` for tech stack
- Scan directory structure for architecture pattern
- Grep for "class", "interface", "entity" to find domain models
- Check imports to understand data flow

**Minimal viable SPR**: Core Mission + Tech Stack + Mental Model Compression

---

**Framework Version**: SIA 1.1.0  
**Installation Date**: {{INSTALLATION_DATE}}  
**Auto-Detected Type**: {{PROJECT_TYPE}}

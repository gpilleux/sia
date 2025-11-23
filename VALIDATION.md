# SIA Submodule - Self-Validation Checklist

**Purpose**: Ensure the `sia/` submodule is generic, reusable, and contains NO project-specific data.

**Last Validated**: 2025-11-23

---

## ✅ PASS Criteria

### 1. No Project-Specific Data
- [ ] NO `.sia/` directory inside submodule
- [ ] NO `.agents/` directory inside submodule
- [ ] NO `requirements/` with actual project requirements (only templates)
- [ ] NO references to specific projects (VRP, ERP, etc.) except as examples

### 2. Generic Content Only
- [ ] `agents/` contains only framework agents (sia.md, spr_pack.md, etc.)
- [ ] `skills/` contains only generic analysis tools
- [ ] `requirements/` contains only templates
- [ ] `templates/` contains scaffolding patterns (no concrete implementations)

### 3. Proper .gitignore
- [ ] Python artifacts ignored (`__pycache__/`, `*.pyc`, etc.)
- [ ] IDE files ignored (`.vscode/`, `.idea/`, etc.)
- [ ] Test artifacts ignored (`.pytest_cache/`, `.coverage`)
- [ ] NO need to ignore `.sia/` or `.agents/` (they never exist in submodule)

### 4. Documentation References
- [ ] References to `sia/` (submodule) use absolute paths from project root
- [ ] References to `.sia/` (project) use future tense ("will create")
- [ ] No hardcoded project names except as examples

---

## Validation Commands

Run from **inside the `sia/` submodule directory**:

```bash
# 1. Check for project-specific directories
ls -la | grep -E "^d.*\.sia$|^d.*\.agents$"
# Expected: NO output

# 2. Check for project-specific references
grep -r "VRP\|vrp" --include="*.md" --include="*.py" . | grep -v "example\|Example"
# Expected: NO output (or only generic examples)

# 3. Verify .gitignore (standard Python/IDE patterns)
grep -E "__pycache__|\.vscode|\.pytest_cache" .gitignore
# Expected: Standard development artifacts ignored

# 4. Check structure
ls -1
# Expected: agents/, core/, installer/, requirements/, skills/, templates/, *.md files
```

---

## Current Status (2025-11-23)

### ✅ PASSED
- [x] Removed `sia/.sia/` (redundant directory)
- [x] Removed VRP-specific context from `sia/agents/sia.md`
- [x] Generalized docker-compose examples (no hardcoded project names)
- [x] Generalized Playwright examples (placeholders instead of specifics)
- [x] Corrected `.gitignore` (only standard Python/IDE artifacts)
- [x] All references to project structures use future tense
- [x] `requirements/` contains only templates (not project requirements)

### ⚠️ MONITORED
- Template files in `templates/` describe project scaffolding (OK, this is their purpose)
- `ARCHITECTURE.md` has examples of `.sia/agents/erp.md` (OK, these are examples)

### ❌ PENDING
- None

---

## Installation Test (New Project)

To verify the submodule is truly generic, test installation in a **new empty project**:

```bash
# 1. Create test project
mkdir test-project && cd test-project
git init

# 2. Add SIA submodule
git submodule add https://github.com/gpilleux/sia.git sia

# 3. Run installer
bash sia/installer/install.sh

# 4. Verify created structure
ls -la .sia/  # Should exist (created by installer)
ls -la sia/.sia/  # Should NOT exist (never created in submodule)

# 5. Check detection
cat .sia.detected.yaml  # Should have generic detection (not project-specific)
```

**Expected Result**:
- `.sia/` created in project root (test-project/.sia/)
- NO `.sia/` inside submodule (test-project/sia/.sia/)
- Installer completes without errors
- No references to VRP, ERP, or other specific projects

---

## Common Violations (Anti-Patterns)

### ❌ Project Data in Submodule
```
sia/
└── .sia/  # WRONG: Project-specific data inside submodule
    └── agents/
        └── erp.md  # WRONG: Specific to ERP project
```

### ✅ Correct Structure
```
project-root/
├── sia/  # Submodule (generic framework)
│   ├── agents/  # Framework agents only
│   │   └── sia.md  # Generic DDD/AI-Native specialist
│   └── templates/  # Scaffolding templates
└── .sia/  # Project-specific data (created by installer)
    └── agents/
        └── erp.md  # Project SPR (created by Super Agent)
```

### ❌ Hardcoded Project References
```markdown
<!-- sia/README.md -->
Read your ERP domain model in `backend/src/erp/domain/`.
```

### ✅ Generic References
```markdown
<!-- sia/README.md -->
After initialization, the Super Agent will analyze your domain model
in the detected backend directory (e.g., `backend/src/{project}/domain/`).
```

---

## Maintenance Protocol

Before committing changes to the `sia/` submodule:

1. Run validation commands (above)
2. Check for project-specific references: `grep -r "erp\|vrp\|ERP\|VRP" --include="*.md" .`
3. Verify `.gitignore` blocks `.sia/`, `.agents/`, `requirements/`
4. Test installation in a fresh project
5. Update this checklist if new validation rules are needed

---

## Submodule Distribution

The `sia/` submodule is distributed as:
- **Git Submodule**: `git submodule add https://github.com/gpilleux/sia.git sia`
- **Standalone Clone**: `git clone https://github.com/gpilleux/sia.git sia`

**Principle**: Any user should be able to clone `sia/` into their project and have it "just work" without assumptions about project structure, tech stack, or domain.

---

**Status**: ✅ VALIDATED (2025-11-23)  
**Validator**: Super Agent  
**Next Review**: Before next submodule commit

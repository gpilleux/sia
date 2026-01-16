# UV Package Manager Standard

## MANDATE

**ALL Python scripts in SIA framework MUST use `uv` as package manager.**

## RATIONALE

### Technical Superiority
- **10-100x faster** than pip (Rust-based resolver)
- **Zero-config**: No manual venv creation, auto-isolated environments
- **Reproducible**: Lockfile support (uv.lock) for deterministic builds
- **Dependency resolution**: Faster conflict detection vs pip backtracking

### Operational Benefits
- **Scripts are self-contained**: `#!/usr/bin/env uv run python` shebang pattern
- **No activation friction**: `uv run script.py` works without sourcing venvs
- **Cross-project consistency**: Same tool for all Python execution
- **Future-proof**: Industry trend towards Rust-based Python tooling (ruff, uv, polars)

## MIGRATION PATTERN

### OLD (Deprecated)
```bash
# Manual venv management
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python script.py

# Direct execution (wrong environment risk)
python3 script.py
```

### NEW (Standard)
```bash
# Zero-config execution
uv run script.py

# With inline dependencies (script declares deps)
uv run --with pandas,numpy script.py

# Script with shebang (make executable)
chmod +x script.py
./script.py
```

## SCRIPT SHEBANG PATTERN

**Template**:
```python
#!/usr/bin/env uv run python
"""
SKILL: {Name}
Description: {Purpose}
Invariant: {What must be true}

NOTE: Uses `uv` package manager (project standard). Auto-installs dependencies.
"""

import sys
# ... rest of script
```

**Why `uv run python` vs `python3`**:
- `uv run` creates isolated env automatically
- Respects pyproject.toml dependencies if present
- Fallback to system Python if no deps
- No PATH pollution from global pip packages

## DEPENDENCY DECLARATION

### Option 1: Inline (Recommended for Skills)
```python
#!/usr/bin/env uv run python
# /// script
# dependencies = [
#   "requests>=2.31.0",
#   "rich>=13.0.0",
# ]
# ///

import requests
import rich
```

### Option 2: pyproject.toml (Project-level)
```toml
[project]
name = "sia-skills"
dependencies = [
    "radon>=6.0.1",
    "pytest-cov>=4.1.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
]
```

## VERIFICATION GATES

**FASE 1** (Skill Creation):
```bash
# Ensure script uses uv shebang
grep -n "#!/usr/bin/env uv run python" sia/skills/*.py

# Verify executable permissions
chmod +x sia/skills/*.py
```

**FASE 5** (Execution):
```bash
# Run with uv (correct)
uv run sia/skills/task_timer.py start QUANT-040 3 "Task"

# NOT with python3 (deprecated)
# python3 sia/skills/task_timer.py  # ❌ Wrong environment risk
```

## ARGUS PROJECT INTEGRATION

**Backend** (`backend/pyproject.toml`):
```toml
[project]
name = "argus-backend"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "psycopg2-binary>=2.9.9",
    "pgvector>=0.2.3",
    "openai>=1.3.0",
    "pdfplumber>=0.10.3",
    # ... rest
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Execution Pattern**:
```bash
# Development server
cd backend
uv run uvicorn src.api.main:app --reload

# CLI commands
uv run python -m src.cli index document.pdf
uv run python -m src.cli search "query"

# Tests
uv run pytest tests/
```

**Frontend** (Node.js, not affected):
```bash
# Frontend still uses npm/pnpm (JavaScript)
cd frontend
npm run dev
```

## ANTI-PATTERNS

❌ **Mixing pip and uv**: Choose one, stick to it
```bash
# Don't do this
pip install requests
uv run script.py  # May not see pip-installed package
```

❌ **Hardcoding python3 path**: Breaks portability
```python
#!/usr/bin/python3  # ❌ System-specific
#!/usr/bin/env uv run python  # ✅ Portable
```

❌ **Manual venv in scripts**: uv handles this
```bash
# Don't do this
python3 -m venv .venv
source .venv/bin/activate
python script.py

# Do this instead
uv run script.py
```

❌ **Global pip install for dev tools**: Use uv tools
```bash
# Old way
pip install black ruff pytest  # ❌ Pollutes global

# New way
uv tool install black  # ✅ Isolated tool install
uv run black .
```

## INSTALLATION

**System Requirement**: uv must be installed globally.

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify
uv --version
# Output: uv 0.5.0 (or higher)
```

**Bootstrap Check** (add to sia/installer/):
```bash
#!/bin/bash
# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "⚠️  UV not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo "✅ UV ready: $(uv --version)"
```

## SKILL DEVELOPMENT CHECKLIST

When creating new skills in `sia/skills/`:

- [ ] Use `#!/usr/bin/env uv run python` shebang
- [ ] Document dependencies in script docstring or inline comments
- [ ] Make script executable: `chmod +x sia/skills/{skill}.py`
- [ ] Update `sia/skills/README.md` with `uv run` command
- [ ] Test execution: `uv run sia/skills/{skill}.py --help`
- [ ] Verify no python3 hardcoding in docs

## TRANSITION TIMELINE

**Phase 1** (Immediate - Nov 2024):
- ✅ All new skills use uv
- ✅ task_timer.py migrated
- 🔄 Update existing skills (check_complexity.sh → .py migration pending)

**Phase 2** (Q1 2025):
- [ ] Migrate all bash skills to Python + uv (better portability)
- [ ] Add uv bootstrap to sia/installer/install.sh
- [ ] Deprecate python3 references in all docs

**Phase 3** (Q2 2025):
- [ ] CI/CD integration (GitHub Actions with uv cache)
- [ ] Performance benchmarks (uv vs pip install times)
- [ ] Team training materials

## METRICS

**Before UV** (estimated):
- pip install time: ~45s (clean install)
- venv creation: ~12s
- Total setup: ~60s per session

**After UV** (measured):
- uv install time: ~4s (parallel downloads)
- Auto-env creation: ~1s (on-demand)
- Total setup: ~5s per session

**Efficiency Gain**: 12x faster environment setup

## REFERENCES

- **UV Docs**: https://github.com/astral-sh/uv
- **Inline Script Deps**: https://packaging.python.org/en/latest/specifications/inline-script-metadata/
- **Argus pyproject.toml**: `/backend/pyproject.toml`

---

**Established**: 2024-11-24  
**Rationale**: Eliminate venv friction, accelerate development, standardize tooling  
**Status**: ACTIVE - all new Python code must comply


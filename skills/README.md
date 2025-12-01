# SIA Skills Catalog

High-leverage commands for verification gates and quality assurance.

## Token-Efficient Pattern

This README = **index only** (~50 tokens). Full docs = separate files (pay-per-use).

**When to read full docs**: Only when invoking specific skill.

---

## Available Skills

| Skill                       | Purpose                    | When                    | Docs                           |
| --------------------------- | -------------------------- | ----------------------- | ------------------------------ |
| `orchestrate_subagents.py`  | CLI-based agent delegation | Multi-agent orchestration | [→](delegate_subagent.md)    |
| `generate_index.py`         | Repository index map       | After structure changes | [→](generate_index.md)         |
| `check_complexity.sh`       | Radon complexity hunter    | Pre/Post-QUANT          | [→](check_complexity.md)       |
| `visualize_architecture.sh` | Pydeps dependency graph    | Pre/Post-implementation | [→](visualize_architecture.md) |
| `check_coverage.sh`         | pytest-cov HTML report     | Pre-archive, Post-QUANT | [→](check_coverage.md)         |
| `audit_ddd.py`              | DDD compliance checker     | Post-implementation     | [→](audit_ddd.md)              |
| `task_timer.py`             | QUANT task chronometer     | FASE 5 (start/stop)     | [→](task_timer.md)             |

**Token Budget**: Index (~50 tokens), Full doc (~200 tokens each). Total if all loaded: ~1000 tokens.

---

## Quick Reference

```bash
# Sub-agent orchestration (CLI-based delegation)
uv run python sia/skills/orchestrate_subagents.py  # Test mode
# Production: Use from Python code (see delegate_subagent.md)

# Repository index (structural navigation)
uv run python sia/skills/generate_index.py  # Outputs: REPO_INDEX.md

# Complexity check (detect technical debt)
sh sia/skills/check_complexity.sh

# Architecture validation (enforce DDD layers)
sh sia/skills/visualize_architecture.sh

# Coverage report (ensure >80%)
sh sia/skills/check_coverage.sh

# DDD audit (validate patterns)
python3 sia/skills/audit_ddd.py

# Task timer (track actual vs estimated time)
uv run sia/skills/task_timer.py start QUANT-XXX HOURS "Description"
uv run sia/skills/task_timer.py status
uv run sia/skills/task_timer.py stop
uv run sia/skills/task_timer.py metrics
```

---

## Integration with Requirements System

**FASE 4** (Pre-Decomposition):
```bash
sh sia/skills/check_complexity.sh > baseline_complexity.txt
sh sia/skills/visualize_architecture.sh  # Review SVG
```

**FASE 5** (Post-Task Verification):
```bash
# Start timer before implementation
uv run sia/skills/task_timer.py start QUANT-040 3 "Task description"

# ... execute task ...

# Verification gates
sh sia/skills/check_complexity.sh  # No regression
sh sia/skills/check_coverage.sh    # Coverage maintained

# Stop timer after completion
uv run sia/skills/task_timer.py stop
```

**FASE 7** (Pre-Archive):
```bash
python3 sia/skills/audit_ddd.py  # Final validation
```

---

## Pay-Per-Use Documentation

**Don't read all docs upfront**. Only read when invoking:

1. User requests task → SUPER AGENT identifies skill needed
2. Read specific skill doc (e.g., `check_complexity.md`)
3. Execute skill with proper flags
4. Return to main context

**Why**: Avoids loading 800 tokens of skill docs when only 1 skill is used.

---

See `sia/core/PROMPT_PLACEMENT.md` for token optimization principles.

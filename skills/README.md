# SIA Skills Catalog

High-leverage commands for verification gates and quality assurance.

## Token-Efficient Pattern

This README = **index only** (~50 tokens). Full docs = separate files (pay-per-use).

**When to read full docs**: Only when invoking specific skill.

---

## Available Skills

### Quality Assurance Skills

| Skill | Purpose | When | Docs |
|-------|---------|------|------|
| `check_complexity.sh` | Radon complexity hunter | Pre/Post-QUANT | [→](check_complexity.md) |
| `visualize_architecture.sh` | Pydeps dependency graph | Pre/Post-implementation | [→](visualize_architecture.md) |
| `check_coverage.sh` | pytest-cov HTML report | Pre-archive, Post-QUANT | [→](check_coverage.md) |
| `audit_ddd.py` | DDD compliance checker | Post-implementation | [→](audit_ddd.md) |

### Agent Development Skills

| Skill | Purpose | When | Docs |
|-------|---------|------|------|
| `scaffold_adk_agent.py` | ADK agent generator | Creating new ADK agents | TBD |
| `spawn_copilot_agent.sh` | Copilot CLI spawner | Single-task delegation | TBD |
| `delegate_to_copilot.sh` | Background task delegator | Long-running tasks | TBD |
| `setup_copilot_cli.sh` | Copilot CLI setup | Initial environment | TBD |
| `mcp_server.py` | MCP server integration | MCP protocol support | TBD |

**Token Budget**: Index (~100 tokens), Full doc (~200 tokens each). Total if all loaded: ~2000 tokens.

---

## Quick Reference

### Quality Assurance

```bash
# Complexity check (detect technical debt)
sh sia/skills/check_complexity.sh

# Architecture validation (enforce DDD layers)
sh sia/skills/visualize_architecture.sh

# Coverage report (ensure >80%)
sh sia/skills/check_coverage.sh

# DDD audit (validate patterns)
python3 sia/skills/audit_ddd.py
```

### Agent Development

```bash
# Generate new ADK agent
python3 sia/skills/scaffold_adk_agent.py <AgentName> [AgentType]

# Spawn single-task Copilot agent
sh sia/skills/spawn_copilot_agent.sh "<task>" [agent]

# Delegate long-running task
sh sia/skills/delegate_to_copilot.sh "<task>" [branch]

# Setup Copilot CLI environment
sh sia/skills/setup_copilot_cli.sh

# Run MCP server
python3 sia/skills/mcp_server.py
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
sh sia/skills/check_complexity.sh  # No regression
sh sia/skills/check_coverage.sh    # Coverage maintained
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

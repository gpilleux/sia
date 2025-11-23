# {{PROJECT_NAME}} - GitHub Copilot Instructions

## META-SYSTEM

**Identity**: SUPER AGENT (meta-cognitive AI orchestrator)  
**Core**: `sia/core/SUPER_AGENT.md`  
**Fundamentals**: `sia/core/CONCEPTS.md` (SPR definitions, Stack, Phases)
**Bootstrap**: Read SUPER_AGENT.md + CONCEPTS.md → Execute auto-discovery → Operate

---

## PROJECT CONTEXT

**Name**: {{PROJECT_NAME}}  
**Type**: {{PROJECT_TYPE}}  
**Contexts**: {{BOUNDED_CONTEXTS}}

---

## PROJECT SPR

{{PROJECT_SPR_CONTENT}}

---

## REQUIREMENTS

**Workflow**: `sia/requirements/README.md`  
**Status**: {{REQUIREMENTS_STATUS}}

---

## SKILLS

Available: `sia/skills/README.md`

Core skills:
- `sh sia/skills/check_complexity.sh` - Radon complexity
- `sh sia/skills/visualize_architecture.sh` - Pydeps graph
- `sh sia/skills/check_coverage.sh` - pytest-cov report
- `python3 sia/skills/audit_ddd.py` - DDD compliance

---

## OPERATIONAL MODE

**Default**: Research first → Delegate to sub-agents → Invoke skills → Update SPR → Evolve

**Anti-Patterns**: No research, no verification, no DDD/SOLID/KISS trace


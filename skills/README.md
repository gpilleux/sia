# SIA Skills - Task Performance Tracking

---

## ACTIVE SKILL

**`task_timer.py`** - QUANT task chronometer with AI vs Human comparison

**Purpose**: Track actual execution time vs AI estimates, measure Super Agent performance

**Usage**:
```bash
# Start timer (AI estimates 3h for task)
uv run skills/task_timer.py start QUANT-040 3 "Implement chat UI"

# Check progress
uv run skills/task_timer.py status

# Stop timer (Human team would need 12h)
uv run skills/task_timer.py stop --human-hours 12

# View performance report
uv run skills/task_timer.py metrics
```

**Metrics Tracked**:
- AI Estimated vs Actual (variance %)
- Human Team Estimated vs AI Actual (speedup factor)
- Historical correction factor for future predictions
- Task completion rate

**Integration**: QUANT workflow FASE 5 (execution tracking)

**Docs**: [task_timer.md](task_timer.md)

---

## EXPERT AGENT CREATION

**Tools for generating domain-specific agents**:

- `create_expert_agent.md` - Template and guidelines
- `create_agent_cli.py` - CLI scaffolding generator
- `EXPERT_AGENT_CREATION_QUICKSTART.md` - 5-min guide
- `EXPERT_AGENT_CREATION_SUMMARY.md` - Pattern reference

**Status**: Active (framework meta-tooling)

---

**Philosophy**: Minimal tooling, maximum leverage. Use platform capabilities over custom scripts.

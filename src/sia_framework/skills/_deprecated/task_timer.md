# Task Timer Skill

## Purpose

Track actual time spent on QUANT tasks vs LLM estimates, build prediction model for:
1. **AI Self-Prediction**: Correct future estimates based on historical variance
2. **Human Team Comparison**: Estimate human dev team duration (baseline: 4x AI speed)

## When to Use

**FASE 5 (Execution)** - Task Boundaries:
- **Start**: Immediately before beginning QUANT implementation
- **Stop**: After task completion (tests passing, docs written)
- **Status**: Check progress during long-running tasks
- **Metrics**: Review prediction accuracy, generate reports

## Commands

### Start Timer
```bash
uv run sia/skills/task_timer.py start TASK-ID HOURS [DESCRIPTION]

# Example:
uv run sia/skills/task_timer.py start QUANT-040 3 "Chat UIResourceRenderer integration"
```

**Output**:
```
⏱️  Timer started for QUANT-040
   Description: Chat UIResourceRenderer integration
   Estimated: 3h (180 min)
   Started: 2025-11-24 15:30:00

   Timer runs in background. Stop with: python3 sia/skills/task_timer.py stop
```

### Check Status
```bash
uv run sia/skills/task_timer.py status
```

**Output**:
```
⏱️  Timer running for QUANT-040
   Description: Chat UIResourceRenderer integration
   Estimated: 3h (180 min)
   Elapsed: 1.25h (75 min)
   Progress: 41.7% of estimate
   Duration: 1h 15m 23s
   Started: 2025-11-24T15:30:00
```

### Stop Timer
```bash
# Task completed
uv run sia/skills/task_timer.py stop

# Task abandoned (not counted in metrics)
uv run sia/skills/task_timer.py stop --abandoned
```

**Output**:
```
⏹️  Timer stopped for QUANT-040
   Status: ✅ COMPLETED
   Estimated: 3h (180 min)
   Actual: 2.75h (165 min)
   Variance: -8.3% (faster ⚡)
   Duration: 2h 45m 12s

💡 PREDICTION INSIGHTS:
   Historical Variance: -5.2%
   Next Task: Apply 0.95x to LLM estimate
```

### Metrics Report
```bash
uv run sia/skills/task_timer.py metrics
```

**Output**:
```
📊 Task Metrics Report
============================================================

📈 COMPLETED TASKS: 8
   Total Estimated (LLM): 24.0h
   Total Actual (AI): 22.3h
   Average Variance: -7.1%

🤖 AI PREDICTION ACCURACY:
   Correction Factor: 0.93x
   Next Task Prediction: EstimatedTime × 0.93

👥 HUMAN TEAM COMPARISON (Baseline):
   Estimated Human Time: 89.2h
   Speedup Factor: 4.0x faster
   Time Saved: 66.9h

📋 RECENT TASKS (Last 5):
   ⚡ QUANT-039: 4h → 3.75h (-6.3%)
   🎯 QUANT-038: 3h → 3.1h (+3.3%)
   ⚡ QUANT-037: 2h → 1.8h (-10.0%)
   🐌 QUANT-036: 3h → 3.5h (+16.7%)
   ⚡ QUANT-035: 4h → 3.5h (-12.5%)

🎯 PREDICTION QUALITY:
   Best: QUANT-038 (+3.3%)
   Worst: QUANT-036 (+16.7%)

💡 INSIGHTS:
   ✅ AI predictions are accurate (±20% tolerance)

============================================================
```

## Workflow Integration

### FASE 5 Pattern (QUANT Execution)

```bash
# 1. Super Agent starts timer (from QUANT breakdown: AI=3h, Human=12h)
uv run sia/skills/task_timer.py start QUANT-040 3 "Chat UIResourceRenderer"

# 2. Execute task (MCP research → code → tests → docs)
mcp_deepwiki_ask_question(...)
# ... implementation ...

# 3. Check progress periodically (optional)
uv run sia/skills/task_timer.py status

# 4. Stop timer with human estimate (from QUANT breakdown)
uv run sia/skills/task_timer.py stop --human-hours 12

# 5. Review accumulated metrics
uv run sia/skills/task_timer.py metrics
```

### Human Estimation (Super Agent Reasoning)

**NOT automated**. Super Agent provides estimate in QUANT breakdown based on:

1. **Task complexity** (research, integration, UI, testing, refactoring)
2. **Domain novelty** (ADK, new frameworks = higher learning curve)
3. **Human overhead** (meetings, code review, context switching, breaks)
4. **Team dynamics** (communication, handoffs, debugging without AI)

**Example QUANT Breakdown**:
```markdown
## QUANT-040: Chat UIResourceRenderer Integration

### Complexity Analysis
- **Research**: MCP-UI SSE patterns (humans: 2h docs reading vs AI: 15min targeted questions)
- **Integration**: 3 systems (SSE handler, ChatMessage, UIResourceRenderer) = context switching
- **Testing**: 10+ integration tests = comprehensive coverage
- **UI/UX**: Responsive layout + loading states = iterative design

### Estimates
- **AI (self)**: 3h (prior experience with similar tasks)
- **Human Team**: 12h
  - Research: 2h (manual doc reading)
  - Implementation: 4h (no AI autocomplete)
  - Testing: 3h (manual test writing + debugging)
  - Code Review: 1.5h (team review cycles)
  - Overhead: 1.5h (meetings, breaks, context switching)
```

## Persistence

**State File**: `~/.sia/timer_state.json`
- Contains running timer info (task_id, start_time, estimate)
- Survives terminal restarts
- Cleared when timer stopped

**Metrics File**: `~/.sia/task_metrics.json`
- Accumulates all completed task data
- Schema:
  ```json
  [
    {
      "task_id": "QUANT-040",
      "description": "Chat UIResourceRenderer",
      "ai_estimated_hours": 3.0,
      "ai_actual_hours": 2.75,
      "ai_variance_percent": -8.3,
      "human_estimated_hours": 12.0,
      "completed": true,
      "start_time": "2025-11-24T15:30:00",
      "end_time": "2025-11-24T18:15:12",
      "duration_formatted": "2h 45m 12s"
    }
  ]
  ```

## Anti-Patterns

❌ **Starting timer without QUANT ID**: Need traceability to requirements
❌ **Forgetting to stop timer**: Inflates actual time, corrupts metrics
❌ **Stopping with --abandoned for debug breaks**: Only use for truly abandoned tasks
❌ **Not providing --human-hours**: Loses human comparison data (most valuable metric)
❌ **Automating human prediction**: Super Agent must reason, not use formulas

## Metrics Interpretation

### Variance Icons
- ⚡ (faster): Actual < Estimated, negative variance
- 🎯 (exact): Within ±5% of estimate
- 🐌 (slower): Actual > Estimated (+10%+), possible scope creep

### Correction Factor
- `< 1.0`: AI overestimates (faster than expected), reduce future estimates
- `= 1.0`: Perfect accuracy (rare)
- `> 1.0`: AI underestimates (slower than expected), increase future estimates

### Human Comparison (Super Agent Reasoning)
- **NOT a formula**: Super Agent analyzes task complexity in QUANT breakdown
- **Factors**: Research depth, integration complexity, testing scope, human overhead
- **Purpose**: Quantify ROI of AI-driven development vs traditional teams

## Package Manager Standard

**UV Package Manager**: Project standard for all Python scripts.

**Why UV**:
- **Zero-config**: No virtual env setup needed, auto-creates isolated environments
- **Fast**: Rust-based, 10-100x faster than pip
- **Dependency resolution**: Built-in lockfile support
- **Shebang pattern**: `#!/usr/bin/env uv run python` for self-contained scripts

**Usage Pattern**:
```bash
# Direct execution (uv handles deps)
uv run sia/skills/task_timer.py start QUANT-040 3 "Task"

# Alternative: make script executable
chmod +x sia/skills/task_timer.py
./sia/skills/task_timer.py start QUANT-040 3 "Task"
```

**Migration from python3**:
- ❌ `python3 script.py` → ⚠️ Requires manual venv activation
- ✅ `uv run script.py` → ✅ Auto-isolated, reproducible

## Future Enhancements

**Planned**:
- [ ] Task type segmentation (research/integration/UI/testing/refactoring)
- [ ] Confidence intervals (±1σ prediction ranges)
- [ ] Integration with REQ breakdown (auto-read human estimates from markdown)
- [ ] Slack/Discord webhooks for timer reminders
- [ ] Export to CSV for external analysis
- [ ] Visualization dashboard (time series, speedup trends)

**Token Optimization**:
- Metrics stored locally (not in prompt)
- Report generation on-demand
- Minimal memory footprint (~200 tokens for full doc)

---

**Added**: 2024-11-24  
**Rationale**: Enable data-driven prediction vs LLM hallucinated estimates. Build historical baseline for human team comparisons.

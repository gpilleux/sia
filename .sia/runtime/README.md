# Runtime Session Management

## Purpose

Orchestration state for **CLI-spawned sub-agents** with file-based communication protocol.

---

## Directory Structure

```yaml
.sia/runtime/
  {session_id}/                    # UUID v4 (e.g., a1b2c3d4-e5f6-7890-abcd-ef1234567890)
    orchestrator.yaml              # SUPER_AGENT state
    research-specialist/
      status.yaml                  # Progress tracking (polled by orchestrator)
      output.md                    # Final SPR output
      progress.log                 # Timestamped event log
      logs/                        # Copilot CLI logs (--log-dir)
        copilot.log
    repository-guardian/
      status.yaml
      output.md
      progress.log
      logs/
```

---

## File Schemas

### 1. `orchestrator.yaml` (SUPER_AGENT State)

```yaml
session_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
created_at: "2025-11-30T10:00:00Z"
agents:
  - agent_name: "research-specialist"
    task: "Research pgvector integration with LangChain"
    status_file: ".sia/runtime/{session_id}/research-specialist/status.yaml"
    output_file: ".sia/runtime/{session_id}/research-specialist/output.md"
    pid: 12345
    started_at: "2025-11-30T10:00:05Z"
    timeout: 300  # 5 minutes
  - agent_name: "repository-guardian"
    task: "Audit DDD compliance in domain layer"
    status_file: ".sia/runtime/{session_id}/repository-guardian/status.yaml"
    output_file: ".sia/runtime/{session_id}/repository-guardian/output.md"
    pid: 12346
    started_at: "2025-11-30T10:00:06Z"
    timeout: 180  # 3 minutes
poll_interval: 2  # seconds
max_parallel: 5
```

### 2. `status.yaml` (Sub-Agent Progress)

**Schema**:
```yaml
state: "in_progress"  # Enum: initializing | in_progress | completed | failed
updated_at: "2025-11-30T10:01:30Z"
progress_percent: 45
current_task: "Executing MCP query: langchain-ai/langchain"
findings_count: 3
errors: []
```

**States**:
- `initializing` - Sub-agent started, preparing execution
- `in_progress` - Actively executing workflow
- `completed` - Finished successfully (output.md ready)
- `failed` - Error occurred (check errors list)

**Update Frequency**: Every 30 seconds (sub-agent responsibility)

### 3. `output.md` (SPR Final Output)

**Format**: Structured markdown following SPR compression principles

```markdown
# [Agent Name] - [Task Name]

**Session**: {session_id}
**Executed**: {timestamp}
**Duration**: {duration_seconds}s

---

## FINDINGS

### Finding 1: [Pattern/Discovery Name]

**Context**: [Where/when this applies]

**Pattern**:
\`\`\`python
# Code example
\`\`\`

**Rationale**: [Why this pattern works]

**Anti-Pattern**: ❌ [What NOT to do]

---

## PATTERNS EXTRACTED

1. **[Pattern Name]** - [One-line description]
2. **[Pattern Name]** - [One-line description]

---

## ANTI-PATTERNS IDENTIFIED

1. ❌ **[Anti-Pattern]** - [Why this fails]
2. ❌ **[Anti-Pattern]** - [Why this fails]

---

## CODE EXAMPLES

### Example 1: [Use Case]

\`\`\`python
# Idiomatic implementation
\`\`\`

---

## RECOMMENDATIONS

1. [Actionable recommendation]
2. [Actionable recommendation]

---

**Confidence**: High | Medium | Low
**References**: [repos queried, docs consulted]
**Next Steps**: [Suggested follow-up actions]
```

### 4. `progress.log` (Event Log)

**Format**: Timestamped text log

```
2025-11-30T10:00:05Z [INFO] Sub-agent initialized (session: a1b2c3d4)
2025-11-30T10:00:10Z [INFO] Phase 1: Analyzing user request
2025-11-30T10:00:35Z [INFO] Phase 2: Executing MCP query (repo: langchain-ai/langchain)
2025-11-30T10:01:05Z [INFO] Phase 2: Received 1,234 tokens from DeepWiki
2025-11-30T10:01:30Z [INFO] Phase 3: Synthesizing findings (3 patterns identified)
2025-11-30T10:02:00Z [INFO] Phase 4: Generating SPR output
2025-11-30T10:02:15Z [INFO] Completed successfully (duration: 130s)
```

---

## Lifecycle Management

### Session Creation

```python
import uuid
from pathlib import Path
from datetime import datetime, UTC

def create_session(agents: list[dict]) -> str:
    """Create runtime session directory structure"""
    session_id = str(uuid.uuid4())
    session_dir = Path(f".sia/runtime/{session_id}")
    
    # Create orchestrator state
    (session_dir).mkdir(parents=True, exist_ok=True)
    
    # Create agent directories
    for agent in agents:
        agent_dir = session_dir / agent['agent_name']
        agent_dir.mkdir(exist_ok=True)
        (agent_dir / "logs").mkdir(exist_ok=True)
        
        # Initialize status.yaml
        status = {
            'state': 'initializing',
            'updated_at': datetime.now(UTC).isoformat(),
            'progress_percent': 0,
            'current_task': 'Starting execution',
            'findings_count': 0,
            'errors': []
        }
        (agent_dir / "status.yaml").write_text(yaml.dump(status))
    
    return session_id
```

### Status Polling

```python
def poll_status(session_id: str, agents: list[str]) -> dict:
    """Poll status files for all agents in session"""
    session_dir = Path(f".sia/runtime/{session_id}")
    status = {}
    
    for agent_name in agents:
        status_file = session_dir / agent_name / "status.yaml"
        if status_file.exists():
            status[agent_name] = yaml.safe_load(status_file.read_text())
        else:
            status[agent_name] = {'state': 'unknown', 'error': 'Status file missing'}
    
    return status
```

### Session Cleanup

```python
def cleanup_old_sessions(max_age_days: int = 7):
    """Remove sessions older than max_age_days"""
    runtime_dir = Path(".sia/runtime")
    if not runtime_dir.exists():
        return
    
    cutoff = datetime.now(UTC) - timedelta(days=max_age_days)
    
    for session_dir in runtime_dir.iterdir():
        if not session_dir.is_dir() or session_dir.name == '.gitkeep':
            continue
        
        # Check orchestrator.yaml created_at
        orchestrator_file = session_dir / "orchestrator.yaml"
        if orchestrator_file.exists():
            data = yaml.safe_load(orchestrator_file.read_text())
            created = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            if created < cutoff:
                shutil.rmtree(session_dir)
```

---

## Integration with Sub-Agents

Sub-agents receive environment variable `SIA_STATUS_FILE` pointing to their `status.yaml`:

```bash
# Orchestrator spawns sub-agent
export SIA_STATUS_FILE=".sia/runtime/{session_id}/{agent_name}/status.yaml"
copilot --agent research-specialist -p "..." --allow-all-tools
```

Sub-agent instructions include status update snippet:

```python
import os
import yaml
from pathlib import Path
from datetime import datetime, UTC

def update_status(progress: int, task: str, findings_count: int = 0, errors: list = []):
    """Update orchestrator-visible status file"""
    status_file = Path(os.getenv('SIA_STATUS_FILE', '.sia/runtime/status.yaml'))
    if not status_file.exists():
        return  # Not running in orchestrated mode
    
    status = yaml.safe_load(status_file.read_text()) if status_file.exists() else {}
    status.update({
        'state': 'in_progress' if progress < 100 else 'completed',
        'updated_at': datetime.now(UTC).isoformat(),
        'progress_percent': progress,
        'current_task': task,
        'findings_count': findings_count,
        'errors': errors
    })
    status_file.write_text(yaml.dump(status, default_flow_style=False))
```

---

## Monitoring Example

```python
# Orchestrator monitors 2 parallel agents
import time

session_id = create_session([...])
agents = spawn_parallel(session_id, tasks)

print(f"Monitoring session {session_id}...\n")

while True:
    status = poll_status(session_id, [a['agent_name'] for a in agents])
    
    # Display progress
    for agent_name, agent_status in status.items():
        state = agent_status.get('state', 'unknown')
        progress = agent_status.get('progress_percent', 0)
        task = agent_status.get('current_task', 'N/A')
        print(f"[{agent_name}] {progress}% - {task}")
    
    # Check completion
    if all(s.get('state') in ['completed', 'failed'] for s in status.values()):
        break
    
    time.sleep(2)  # Poll every 2 seconds

print("\nAll agents completed. Consolidating results...")
```

**Output**:
```
Monitoring session a1b2c3d4-e5f6-7890-abcd-ef1234567890...

[research-specialist] 25% - Executing MCP query: langchain-ai/langchain
[repository-guardian] 40% - Running check_complexity.sh

[research-specialist] 60% - Synthesizing LangChain patterns
[repository-guardian] 80% - Analyzing DDD violations

[research-specialist] 100% - Completed
[repository-guardian] 100% - Completed

All agents completed. Consolidating results...
```

---

## Anti-Patterns

❌ **Committing runtime/** to git (transient state only)
❌ **Hardcoding session IDs** (use UUID generation)
❌ **Polling faster than 1s** (CPU spike, no value gain)
❌ **Ignoring errors list** in status.yaml (silent failures)
❌ **Not cleaning old sessions** (disk bloat over time)

---

## References

- **REQ-011**: Native Sub-Agent Delegation (CLI spawning architecture)
- **QUANT-001**: File-Based Protocol implementation
- **Orchestrator Skill**: `skills/orchestrate_subagents.py` (to be created in QUANT-002)

---

**Created**: 2025-11-30  
**Version**: 1.0.0  
**Status**: Schema defined, awaiting orchestrator implementation

# LESSON LEARNED: Copilot CLI Custom Agents ≠ Python Execution

**Date**: 2025-11-30  
**Context**: REQ-011 QUANT-001 End-to-End Validation

---

## DISCOVERY

**Assumption (WRONG)**:
> Custom agents in `.github/agents/*.agent.md` can execute Python code blocks directly

**Reality**:
> Copilot CLI custom agents are **markdown instruction sets** processed by the LLM.
> Code blocks in agents are **examples/templates**, NOT executable code.
> The agent can USE tools, but cannot RUN Python scripts embedded in the agent definition.

---

## EVIDENCE

### Test Setup
- Created `research-specialist.agent.md` with Python code for `update_status()`
- Set environment variable `SIA_STATUS_FILE` pointing to `status.yaml`
- Spawned agent via Copilot CLI with `--agent research-specialist`
- Expected: Agent would execute Python to update status

### Actual Behavior
- Agent executed successfully (57s runtime)
- Generated valid SPR output (10,516 chars, 3+ code examples)
- Completed MCP queries (Deepwiki calls visible in logs)
- **status.yaml NEVER updated** (remained in "initializing" state)

### Root Cause
- Copilot CLI agents are **LLM instruction contexts**, not script executors
- Python code in agent.md is **documentation**, not runtime code
- Agents CAN call MCP tools (deepwiki, repo-indexer) via LLM tool calling
- Agents CANNOT execute arbitrary Python within their definition

---

## IMPLICATIONS

### File-Based Protocol Needs Revision

**Current Design (INVALID)**:
```
Sub-Agent (research-specialist.agent.md)
  ↓ Executes Python snippet
  ↓ Updates status.yaml
  ↓ Writes progress.log
Orchestrator (orchestrate_subagents.py)
  ↓ Polls status.yaml every 2s
  ↓ Displays progress
```

**Required Design (VALID)**:
```
Orchestrator (orchestrate_subagents.py)
  ↓ Spawns Copilot CLI subprocess
  ↓ Captures stdout/stderr in real-time
  ↓ Parses output for progress indicators
  ↓ Updates status.yaml externally
  ↓ Displays progress to user
```

---

## ALTERNATIVE APPROACHES

### Option 1: Output Stream Parsing (Recommended)
- Orchestrator reads subprocess stdout line-by-line
- Parses markdown headers/sections as progress milestones
- Extracts findings count from code blocks
- Updates status.yaml based on parsing

**Pros**:
- No modification to agent definitions needed
- Works with ANY custom agent
- Real-time progress without agent cooperation

**Cons**:
- Parsing heuristics (not guaranteed accurate)
- Requires patterns like "## Phase 1", "Finding X of Y"

### Option 2: MCP Status Service (Complex)
- Create custom MCP server: `status-reporter`
- Agent calls `mcp_status-reporter_update_progress()`
- Orchestrator subscribes to MCP status stream

**Pros**:
- Agent explicitly reports progress (accurate)
- Standard MCP protocol (reusable)

**Cons**:
- Requires new MCP server development
- Agent definitions must be modified (add tool calls)
- More infrastructure complexity

### Option 3: Copilot CLI --json Mode (If Available)
- Check if Copilot CLI supports `--output json` or `--progress-file`
- Use built-in progress reporting

**Pros**:
- Official solution (if exists)
- Zero custom code

**Cons**:
- Unknown if feature exists (needs research)

---

## RECOMMENDED NEXT STEPS

1. **Investigate Copilot CLI Options**:
   ```bash
   copilot --help | grep -i progress
   copilot --help | grep -i output
   copilot --help | grep -i json
   ```

2. **Prototype Output Stream Parser**:
   - Modify `orchestrate_subagents.py`
   - Use `subprocess.PIPE` instead of file redirect
   - Parse stdout in real-time (asyncio + regex)
   - Update status.yaml from orchestrator side

3. **Simplify Status Tracking**:
   - Instead of 30s granular updates, track:
     - **Spawn** → state: in_progress
     - **Completion** → state: completed (when subprocess exits)
     - **Findings** → parse final output for sections/code blocks

4. **Update Documentation**:
   - Remove Python execution assumptions from agent docs
   - Clarify agent.md = "instruction context" not "script"
   - Document orchestrator's responsibility for status tracking

---

## VALIDATION OUTCOME

**QUANT-001 Status**: ❌ PARTIAL PASS

✅ **Working**:
- Copilot CLI spawn successful
- Agent executes correctly
- SPR output generated
- MCP queries functional

❌ **Failed**:
- Status updates (0%, never progressed)
- Real-time progress tracking
- Findings count tracking
- Error reporting via status.yaml

**Impact**: 
- Sub-agent **delegation works** (output quality good)
- Real-time **monitoring doesn't work** (needs orchestrator-side parsing)
- File-based protocol needs **architecture revision**

---

## REVISED PROTOCOL

### Phase 1: Minimal Viable Monitoring

**Track 3 states only**:
1. **Spawned** (state: in_progress, progress: 0%)
2. **Running** (state: in_progress, progress: 50% - estimated)
3. **Completed** (state: completed, progress: 100% - on subprocess exit)

**Implementation**:
```python
# Orchestrator monitors subprocess, not status.yaml
process = subprocess.Popen(...)
status_file.write('state: in_progress\nprogress: 0%')

while process.poll() is None:
    time.sleep(5)
    status_file.write('state: in_progress\nprogress: 50%')

# Process completed
output = output_file.read_text()
findings = output.count('##') - 1
status_file.write(f'state: completed\nprogress: 100%\nfindings: {findings}')
```

### Phase 2: Enhanced Parsing (Future)

**Parse output for phases**:
- Match `## Phase X` → Update progress
- Match `### Finding:` → Increment findings_count
- Match `ERROR`, `FAILURE` → Add to errors list

---

## OPEN QUESTIONS

1. Does Copilot CLI support structured output formats?
2. Can we hook into LLM streaming API for progress?
3. Should we build MCP status-reporter service?
4. Is there a Copilot SDK for programmatic control?

---

**Status**: Documented  
**Action Required**: Revise orchestrator implementation (QUANT-001.1)  
**Blocker Resolved**: Understanding of agent execution model ✅

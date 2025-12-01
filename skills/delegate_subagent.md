# Delegate Subagent Skill

**Purpose**: Enable SUPER AGENT to programmatically invoke custom agents via Copilot CLI background execution.

**Implementation**: `skills/orchestrate_subagents.py` - CLI-based subprocess orchestration

**Version**: 2.0.0 (Updated 2025-11-30)  
**Breaking Change**: Migrated from native `runSubagent` tool to CLI-based execution via `orchestrate_subagents.py`  
**Reason**: Custom agents are instruction contexts (not script executors), orchestrator handles monitoring

**When to use**: 
- Research needed (external knowledge) → `research-specialist`
- Architecture validation → `repository-guardian` 
- Requirements creation → `compliance-officer`
- AI-Native patterns → `sia-ddd`
- M365 expertise → `microsoft-suite-specialist`

---

## Prerequisites

**Copilot CLI** (GitHub CLI with Copilot extension):
```bash
# Verify installation
gh copilot --version
# Expected: gh version X.X.X (with copilot extension)
```

**Custom Agent Location**: `.github/agents/*.agent.md`

**Python Environment**: Python 3.10+ with optional PyYAML

**Verification**:
```bash
# Check custom agents exist
ls -la .github/agents/
# Expected: research-specialist.agent.md, repository-guardian.agent.md, etc.

# Test orchestrator
python skills/orchestrate_subagents.py
# Expected: Session creation successful
```

---

## Invocation Protocol

### Step 1: Analyze Bounded Context

**Decision Tree**:
```
User Request → SUPER_AGENT analyzes
    ↓
External knowledge needed? → research-specialist
Domain architecture? → repository-guardian
Requirements workflow? → compliance-officer
AI-Native implementation? → sia-ddd
M365 integration? → microsoft-suite-specialist
```

### Step 2: Formulate Delegation Prompt

**Template**:
```markdown
## TASK
[Specific action to perform - ONE sentence]

## CONTEXT
[Why this task is needed, what user is trying to achieve - 2-3 sentences]

## CONSTRAINTS
[Technical limits, architectural requirements, DDD rules - bullet list]

## EXPECTED OUTPUT
[Format: SPR markdown with patterns + anti-patterns + code examples]

## ADDITIONAL INFO
[Relevant files, previous findings, domain knowledge]
```

**Example** (Research Specialist):
```markdown
## TASK
Research pgvector integration patterns with LangChain for semantic code search.

## CONTEXT
Building MCP repo-indexer tool that uses pgvector for similarity search.
Need to understand async connection pooling and batch embedding patterns.

## CONSTRAINTS
- Must use async/await (no sync blocking)
- PostgreSQL database (pgvector extension)
- LangChain as orchestration layer
- Target: <5000 tokens total research

## EXPECTED OUTPUT
- Code examples showing PGVector.from_documents() with async engine
- Batch embedding pattern (optimal batch_size)
- Index configuration (HNSW vs IVFFlat trade-offs)
- Anti-patterns to avoid

## ADDITIONAL INFO
Repos to query: langchain-ai/langchain, pgvector/pgvector
Current context: MCP server using FastMCP + SQLAlchemy async
```

### Step 3: Invoke Subagent (CLI Execution)

**Method**: Execute `orchestrate_subagents.py` (Copilot CLI subprocess)

**Parameters**:
- `agent_name`: Custom agent identifier (e.g., "research-specialist")
- `prompt`: Delegation prompt (formatted per template above)
- `timeout`: Execution timeout in seconds (default: 300)

**Example invocation**:
```python
# Execute via run_in_terminal or direct Python call
from skills.orchestrate_subagents import SubAgentOrchestrator

tasks = [{
    'agent_name': 'research-specialist',
    'prompt': '[Full delegation prompt from Step 2]',
    'timeout': 300
}]

orchestrator = SubAgentOrchestrator()
agents = orchestrator.spawn_parallel(tasks)
status = orchestrator.monitor_progress(agents)
results = orchestrator.consolidate_results(agents)
```

### Step 4: Monitor Execution (Background Process)

**Execution model**:
- Copilot CLI spawns subagent as subprocess
- Subagent has access to specialized tools (MCP, semantic_search, etc.)
- Orchestrator monitors via output file polling
- Returns markdown SPR output when completed
- **Note**: Real-time status updates pending (QUANT-001.1), currently uses start/end states

**Expected response format**:
```markdown
## RESEARCH FINDINGS

### MCP Queries Executed
1. `repo/name` - "question" → Finding: [summary]

### Patterns Discovered
- **Pattern Name**: Description + use case

### Anti-Patterns
- ❌ Anti-pattern: Why it fails

### Code Examples
\```language
// Executable snippet
\```

### Token Efficiency
- Queries: X questions × ~Y tokens = Z total
- vs Full Wiki: ~W tokens
- Efficiency: V% context preserved
```

### Step 5: Validate & Integrate

**SUPER AGENT responsibilities**:
1. ✅ Verify output matches expected format
2. ✅ Extract patterns for Project SPR
3. ✅ Identify anti-patterns for guardrails
4. ✅ Store code examples in knowledge base
5. ✅ Update `.sia/agents/[project].md` with findings

**Validation checklist**:
- [ ] Output is markdown (not plain text)
- [ ] Contains patterns section
- [ ] Contains anti-patterns section
- [ ] Code examples are executable
- [ ] Token usage documented
- [ ] Findings directly answer delegation prompt

---

## Delegation Patterns by Agent

### Research Specialist

**When**: External knowledge needed (MCP Deepwiki, Repo-Indexer)

**Delegation template**:
```markdown
## TASK
Research [technology/pattern] implementation in [framework].

## CONTEXT
Implementing [feature] for [bounded context].
Need to understand [specific aspect].

## CONSTRAINTS
- Token budget: <5000 total
- Repos to query: [primary repo], [secondary repo if needed]
- Expected output: Code examples + patterns

## EXPECTED OUTPUT
- Implementation pattern showing [specific API/pattern]
- Anti-patterns to avoid
- Token efficiency metrics

## ADDITIONAL INFO
Current architecture: [relevant context]
```

**Tools available to subagent**:
- `mcp_deepwiki_ask_question`
- `mcp_deepwiki_read_wiki_contents`
- `mcp_repo-indexer_search_code`
- `semantic_search`
- `grep_search`

### Repository Guardian

**When**: Architecture validation, DDD compliance

**Delegation template**:
```markdown
## TASK
Validate [proposed change] against DDD clean architecture.

## CONTEXT
User wants to [action], proposed implementation involves [changes].

## CONSTRAINTS
- Strict DDD layer separation (domain → application → infrastructure)
- No domain dependencies on infrastructure
- Entities must be anemic (no business logic in constructors)

## EXPECTED OUTPUT
- ✅/❌ Validation result with specific violations
- Corrected implementation if violations found
- Architectural guidance

## ADDITIONAL INFO
Proposed files: [list]
Current architecture: [SPR reference]
```

**Tools available to subagent**:
- `run_in_terminal` (execute skills)
- `get_errors` (static analysis)
- `audit_ddd.py` (DDD validation)
- `check_complexity.sh` (complexity analysis)

### Compliance Officer

**When**: Requirements creation, QUANT breakdown

**Delegation template**:
```markdown
## TASK
Create formal requirement for [feature request].

## CONTEXT
User requested: "[original request]"
Bounded context: [domain area]

## CONSTRAINTS
- Follow QUANT 7-phase methodology
- Atomic tasks (2-4 hours each)
- DDD invariants documented
- Acceptance criteria testable

## EXPECTED OUTPUT
- REQ-XXX formal specification
- QUANT breakdown (5-10 tasks)
- Dependencies identified
- Estimated effort

## ADDITIONAL INFO
Related REQs: [if any]
Technical debt: [if any]
```

**Tools available to subagent**:
- `semantic_search` (find related requirements)
- `grep_search` (identify existing patterns)
- `read_file` (analyze current implementation)

---

## Anti-Patterns (What NOT to Do)

### ❌ Accidental CLI Invocation

**Problem**: Running orchestrator without proper task definition causes errors

**Example**:
```python
# BAD (incomplete task definition)
tasks = [{'agent_name': 'research-specialist'}]  # Missing prompt!
orchestrator.spawn_parallel(tasks)
→ CLI error: missing required argument 'prompt'
```

**Solution**:
```python
# GOOD (complete task definition)
tasks = [{
    'agent_name': 'research-specialist',
    'prompt': '[Complete delegation prompt with TASK/CONTEXT/etc]',
    'timeout': 300
}]
orchestrator.spawn_parallel(tasks)
→ Successful spawn with proper configuration
```

### ❌ Incomplete Delegation Prompt

**Problem**: Subagent lacks context, produces generic output

**Example**:
```markdown
# BAD
prompt: "Research LangChain"
→ Result: 30,000 token dump, no actionable info
```

**Solution**:
```markdown
# GOOD
prompt: """
## TASK
Research ConversationBufferMemory persistence with PostgreSQL in LangChain.

## CONTEXT
Building multi-turn chat with session persistence.
Need async pattern with SQLAlchemy.

## CONSTRAINTS
- Token budget: <2000
- Expected output: Code example + anti-patterns

## ADDITIONAL INFO
Repo: langchain-ai/langchain
Current stack: FastAPI + asyncpg
"""
→ Result: 800 tokens, specific implementation pattern
```

### ❌ Wrong Agent Selection

**Problem**: Delegating to agent without appropriate tools

**Example**:
```markdown
# BAD
User: "Research FastAPI patterns"
→ Delegate to repository-guardian (has no MCP Deepwiki access)
```

**Solution**:
```markdown
# GOOD
User: "Research FastAPI patterns"
→ Delegate to research-specialist (has mcp_deepwiki_ask_question)
```

### ❌ No Validation of Output

**Problem**: Blindly accepting subagent output without verification

**Example**:
```python
# BAD
results = orchestrator.consolidate_results(agents)
return results['research-specialist']  # No validation
```

**Solution**:
```python
# GOOD
results = orchestrator.consolidate_results(agents)
output = results['research-specialist']

# Validate structure
assert "## RESEARCH FINDINGS" in output
assert "### Patterns Discovered" in output
assert "### Anti-Patterns" in output

# Extract key learnings
patterns = extract_patterns(output)
update_project_spr(patterns)

return output
```

---

## Token Efficiency

### Delegation Overhead

**Baseline** (no delegation):
- SUPER AGENT executes research manually
- Loads full wiki → 30,000 tokens
- Limited context for implementation

**With delegation**:
- SUPER AGENT formulates prompt → 500 tokens
- Subagent executes → 2,000 tokens (targeted questions)
- SUPER AGENT validates → 100 tokens
- **Total**: 2,600 tokens vs 30,000 (91% reduction)

### When NOT to Delegate

**Don't delegate if**:
- Answer is in project code (use `semantic_search` directly)
- Simple question (< 100 tokens to answer inline)
- Repeated delegation (cache previous results)
- Token budget exhausted (< 10,000 remaining)

**Example**:
```markdown
# User: "What's the current Python version?"
# BAD: Delegate to research-specialist
# GOOD: Read pyproject.toml directly (10 tokens)
```

---

## Execution Example (REQ-011 QUANT-001)

### Scenario
User: "Investiga cómo implementar vector search con pgvector en LangChain"

### SUPER AGENT Analysis
```python
bounded_context = "External Knowledge Discovery"
complexity = "Medium (requires Deepwiki queries)"
decision = "Delegate to research-specialist"
```

### Step 1: Formulate Delegation Prompt
```markdown
## TASK
Research pgvector integration patterns with LangChain for semantic code search.

## CONTEXT
Building MCP repo-indexer tool using pgvector for similarity search.
Need async connection pooling and batch embedding patterns.

## CONSTRAINTS
- Async/await required (no sync blocking)
- PostgreSQL with pgvector extension
- LangChain orchestration layer
- Token budget: <5000 total

## EXPECTED OUTPUT
- Code example: PGVector.from_documents() with async engine
- Batch embedding pattern (optimal batch_size)
- Index configuration (HNSW vs IVFFlat)
- Anti-patterns to avoid

## ADDITIONAL INFO
Repos: langchain-ai/langchain, pgvector/pgvector
Current: FastMCP + SQLAlchemy async
```

### Step 2: Invoke Subagent (CLI Execution)
```python
from skills.orchestrate_subagents import SubAgentOrchestrator

tasks = [{
    'agent_name': 'research-specialist',
    'prompt': '[prompt from Step 1]',
    'timeout': 300
}]

orchestrator = SubAgentOrchestrator()
agents = orchestrator.spawn_parallel(tasks)
# Returns: [AgentProcess(agent_name='research-specialist', process=<Popen>, ...)]
```

### Step 3: Monitor Execution (Background)
```python
# Monitor progress (polls output files every 2s)
status = orchestrator.monitor_progress(agents, verbose=True)
# Output:
# ⚙️ [research-specialist] 50% - Executing research (estimated)
# ✅ [research-specialist] 100% - Completed
```

- Research Specialist executes in background
- Copilot CLI runs MCP Deepwiki queries:
  1. `langchain-ai/langchain` - "How to configure PGVector as vector store..."
  2. `pgvector/pgvector` - "Best practices for index optimization..."
- Writes findings to `.sia/runtime/{session_id}/research-specialist/output.md`

### Step 4: Consolidate Results
```python
# Read output files from all agents
results = orchestrator.consolidate_results(agents)
output = results['research-specialist']
```

**Output Structure**:
```markdown
## RESEARCH FINDINGS

### MCP Queries Executed
1. `langchain-ai/langchain` - "How to configure PGVector as vector store..." 
   → Finding: Use PGVector.from_documents() with async connection string

2. `pgvector/pgvector` - "Best practices for index optimization..." 
   → Finding: HNSW for <1M vectors, IVFFlat for >1M

### Patterns Discovered
- **Async Connection Pooling**: SQLAlchemy async engine with pool_size=10
- **Batch Embedding**: embed_documents() with batch_size=100
- **Index Selection**: HNSW (m=16, ef_construction=64) for precision

### Anti-Patterns
- ❌ Sync connection in async context (blocks event loop)
- ❌ Single embedding per query (batch for 10x speedup)

### Code Examples
\```python
from langchain.vectorstores.pgvector import PGVector
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@host/db",
    pool_size=10, max_overflow=20
)

vectorstore = await PGVector.afrom_documents(
    documents=docs,
    embedding=embeddings,
    connection_string=connection_string,
    collection_name="code_chunks",
    index_params={"method": "hnsw", "m": 16, "ef_construction": 64}
)
\```

### Token Efficiency
- Queries: 2 questions × ~600 tokens = 1,200 total
- vs Full Wiki: ~35,000 tokens
- Efficiency: 96.6% context preserved
```

### Step 5: SUPER AGENT Validates & Integrates
```python
# Validate output from orchestrator
output = results['research-specialist']

validation_checklist = {
    "has_markdown_format": True,  # ✅
    "has_patterns_section": True,  # ✅
    "has_antipatterns_section": True,  # ✅
    "has_code_examples": True,  # ✅
    "code_is_executable": True,  # ✅
    "answers_original_question": True  # ✅
}

if all(validation_checklist.values()):
    # Extract patterns for Project SPR
    patterns = extract_patterns(output)
    # → Pattern 1: Async pooling (SQLAlchemy async engine)
    # → Pattern 2: Batch embedding (batch_size=100)
    # → Pattern 3: HNSW indexing (m=16, ef_construction=64)
    
    # Document anti-patterns
    antipatterns = extract_antipatterns(output)
    # → Sync in async context
    # → Single embeddings
    
    # Update knowledge cache
    update_cache(
        topic="pgvector_langchain_async_pattern",
        content=output,
        req="REQ-015",
        tokens_used=587
    )
    
    # Update Project SPR (.sia/agents/repo_indexer.md)
    update_project_spr(
        section="Infrastructure.PGVector",
        patterns=patterns,
        antipatterns=antipatterns,
        code_examples=extract_code_examples(output)
    )

# Total execution time: ~57s (QUANT-001 validated)
# Output quality: 10,516 chars, 5 patterns, 5 anti-patterns, 3+ code examples
```

---

## Verification Checklist

**Before delegation**:
- [ ] Identified correct custom agent (has required tools)
- [ ] Formulated complete delegation prompt (TASK, CONTEXT, CONSTRAINTS, EXPECTED OUTPUT)
- [ ] Verified agent exists (`.github/agents/[agent-name].agent.md`)
- [ ] Copilot CLI installed (`gh copilot --version`)
- [ ] Python environment ready (Python 3.10+)

**During delegation**:
- [ ] Orchestrator spawned successfully (no CLI errors)
- [ ] Subagent process running (PID visible in logs)
- [ ] Output file being written (`.sia/runtime/{session_id}/{agent}/output.md`)

**After delegation**:
- [ ] Output validated (matches SPR structure)
- [ ] Patterns extracted for Project SPR
- [ ] Anti-patterns documented
- [ ] Code examples stored
- [ ] Knowledge cached (avoid redundant research)
- [ ] Execution metrics captured (time, token efficiency)
- [ ] Anti-patterns documented
- [ ] Code examples stored
- [ ] Knowledge cached (avoid redundant research)
- [ ] Token efficiency calculated

---

## Integration with SUPER AGENT

**Modify `.github/copilot-instructions.md`**:
```markdown
## DELEGATION MODEL

**Primary Agent**: SUPER_AGENT  
**Sub-Agents**: research-specialist, repository-guardian, compliance-officer, sia-ddd

**Invocation Pattern**:
User Request → SUPER_AGENT analyzes bounded context
    ↓
Match expertise?
    ├─ Research needed → research-specialist
    ├─ Architecture validation → repository-guardian
    ├─ Requirements creation → compliance-officer
    └─ AI-Native patterns → sia-ddd
    ↓
Execute via orchestrate_subagents.py (CLI subprocess)
    ↓
Validate & integrate findings
    ↓
Update Project SPR
```

**See**: `skills/delegate_subagent.md` for full protocol  
**Implementation**: `skills/orchestrate_subagents.py` for CLI orchestration

---

## Self-Evolution

**This skill evolves via**:
- Documented delegation patterns (successful invocations)
- Anti-patterns discovered (failed delegations)
- Token efficiency metrics (optimize prompt templates)

**Feedback loop**:
1. Execute delegation
2. Measure token efficiency
3. Document outcome (`.sia/knowledge/delegation_patterns.md`)
4. Refine templates for future use

---

**Status**: ✅ ACTIVE (REQ-011 QUANT-001)  
**Version**: 2.0.0  
**Last Updated**: 2025-11-30  
**Dependencies**: Copilot CLI (gh copilot), Python 3.10+, orchestrate_subagents.py  
**Integration**: SUPER_AGENT orchestration protocol via CLI subprocess execution  
**Known Limitations**: Real-time status monitoring pending (QUANT-001.1), currently uses start/complete states

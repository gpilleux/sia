# SPR Output Template for Sub-Agents

**Purpose**: Standardized markdown format for sub-agent execution results.

**Location**: `{session_id}/{agent_name}/output.md`

**Principles**: SPR compression (Sparse Priming Representation) - maximize information density, minimize tokens.

---

## Template Structure

```markdown
# [Agent Name] - [Task Name]

**Session**: {session_id}
**Agent**: {agent_name}
**Executed**: {ISO 8601 timestamp}
**Duration**: {duration_seconds}s
**Status**: ✅ Completed | ⚠️ Partial | ❌ Failed

---

## FINDINGS

### Finding 1: [Pattern/Discovery Name]

**Context**: [Where/when this applies - 1 sentence]

**Pattern**:
\`\`\`python
# Idiomatic implementation (minimal, runnable)
\`\`\`

**Rationale**: [Why this works - 2-3 sentences max]

**Trade-offs**:
- ✅ [Advantage 1]
- ❌ [Disadvantage 1]

**Anti-Pattern**: 
\`\`\`python
# What NOT to do (common mistake)
\`\`\`

**Why it fails**: [1 sentence]

---

### Finding 2: [Pattern/Discovery Name]

[Repeat structure]

---

## SYNTHESIS

### Patterns Extracted

1. **[Pattern Name]** - [One-line description]
   - Use when: [Context]
   - Complexity: Low | Medium | High
   
2. **[Pattern Name]** - [One-line description]
   - Use when: [Context]
   - Complexity: Low | Medium | High

### Anti-Patterns Identified

1. ❌ **[Anti-Pattern]** - [Why this fails] → Use [correct pattern] instead
2. ❌ **[Anti-Pattern]** - [Why this fails] → Use [correct pattern] instead

### Key Insights

- [Insight 1: Non-obvious truth discovered during research]
- [Insight 2: Cross-cutting concern or architectural implication]

---

## CODE EXAMPLES

### Example 1: [Use Case Name]

**Scenario**: [Brief context - 1 sentence]

\`\`\`python
# Complete, runnable example (DRY, idiomatic)
from typing import Protocol

class VectorStore(Protocol):
    async def add_embeddings(self, texts: list[str]) -> None: ...

# Usage
async def main():
    store = PGVectorStore(connection_string=...)
    await store.add_embeddings(["doc1", "doc2"])
\`\`\`

**Complexity**: Low (< 10 LOC) | Medium (10-30 LOC) | High (> 30 LOC)

---

### Example 2: [Use Case Name]

[Repeat structure]

---

## RECOMMENDATIONS

### Immediate Actions

1. **[Action]** - [Rationale - 1 sentence]
2. **[Action]** - [Rationale - 1 sentence]

### Follow-Up Research

1. **[Topic]** - [Why worth investigating]
2. **[Topic]** - [Why worth investigating]

### Integration Strategy

[How to apply findings to current project - 2-3 steps]

---

## METADATA

**Confidence**: High | Medium | Low
- High: Multiple authoritative sources confirm pattern
- Medium: Single source or experimental validation
- Low: Inferred from limited data

**Sources**:
- Repositories: [org/repo1, org/repo2]
- Documentation: [URLs or tool calls executed]
- Code samples: [Files analyzed via repo-indexer]

**Token Budget**:
- Input: {prompt_tokens} tokens
- MCP queries: {mcp_tokens} tokens
- Output: {output_tokens} tokens
- Total: {total_tokens} tokens

**Execution Log**:
- Phase 1 (Analysis): {duration}s
- Phase 2 (Research): {duration}s
- Phase 3 (Synthesis): {duration}s
- Phase 4 (Output): {duration}s

---

## ERRORS & LIMITATIONS

### Errors Encountered

\`\`\`yaml
- timestamp: "2025-11-30T10:05:23Z"
  phase: "MCP Query"
  error: "Rate limit exceeded (429)"
  mitigation: "Retried after 60s delay"
  impact: "Low (added 60s to execution time)"
\`\`\`

### Known Limitations

1. **[Limitation]** - [Impact on findings accuracy]
2. **[Limitation]** - [Scope constraint]

### Assumptions Made

1. **[Assumption]** - [Validation status: confirmed | unconfirmed]
2. **[Assumption]** - [Validation status: confirmed | unconfirmed]

---

## NEXT STEPS

**For SUPER_AGENT**:
1. Extract patterns → Update Project SPR (`.sia/agents/[project].md`)
2. Validate anti-patterns against current codebase
3. Delegate follow-up research if needed: `[topic]`

**For User**:
1. Review code examples (prioritize Example 1, 2)
2. Validate assumptions in [assumptions section]
3. Confirm integration strategy aligns with project goals

---

**Agent Version**: [version from agent frontmatter]
**Protocol Version**: File-Based v1.0.0
**SPR Compliance**: ✅ Compressed, structured, actionable
```

---

## Compression Principles

### 1. Information Density
- **Code > Prose**: Prefer runnable examples over explanations
- **DRY**: Don't repeat context (frontmatter covers session metadata)
- **Atomic Findings**: Each finding = 1 pattern + 1 anti-pattern max

### 2. Actionability
- Every finding must have: Pattern (what to do) + Anti-Pattern (what NOT to do)
- Recommendations must be concrete (not "consider X" but "implement X because Y")
- Integration strategy in 2-3 steps (not abstract guidance)

### 3. Token Efficiency
- **Target**: < 5,000 tokens per output
- **Strategy**: 
  - Code blocks compressed (no comments beyond essentials)
  - Findings: 2-4 max (prioritize high-impact)
  - Examples: 2-3 max (prioritize common use cases)

### 4. Verifiability
- Sources traceable (repo names, MCP tool calls logged)
- Confidence explicit (High/Medium/Low with criteria)
- Errors transparent (logged with mitigation)

---

## Anti-Patterns (Output Generation)

❌ **Novel-Length Output** (> 5,000 tokens)
- Problem: Context overflow, low signal-to-noise
- Fix: Prioritize top 2-4 findings, compress examples

❌ **Abstract Recommendations** ("Consider using async patterns")
- Problem: Not actionable
- Fix: Concrete steps ("Replace sync client with AsyncClient: `client = AsyncPGVectorStore(...)`")

❌ **Unvalidated Code** (syntax errors, missing imports)
- Problem: User wastes time debugging examples
- Fix: Test snippets before including (mental simulation or validation)

❌ **Missing Anti-Patterns**
- Problem: User doesn't know what to avoid
- Fix: Every pattern needs paired anti-pattern

❌ **Undocumented Assumptions**
- Problem: Findings invalid in user's context
- Fix: Explicit assumptions section with validation status

---

## Validation Checklist

Before finalizing `output.md`, sub-agent verifies:

- [ ] **Token count** < 5,000 (use `len(output.split())` × 1.3 as estimate)
- [ ] **Code examples** syntax-valid (Python: no missing imports, runnable)
- [ ] **Findings** prioritized (top 2-4 high-impact patterns)
- [ ] **Anti-patterns** documented (1 per finding minimum)
- [ ] **Sources** traceable (repo names, URLs, tool calls listed)
- [ ] **Recommendations** actionable (concrete steps, not vague guidance)
- [ ] **Metadata** complete (confidence, token budget, execution log)
- [ ] **Errors** logged (if any occurred during execution)
- [ ] **SPR compliance** verified (compressed, structured, actionable)

---

## Example: Minimal Valid Output

```markdown
# Research Specialist - PGVector Async Patterns

**Session**: a1b2c3d4-e5f6-7890-abcd-ef1234567890
**Agent**: research-specialist
**Executed**: 2025-11-30T10:05:00Z
**Duration**: 89s
**Status**: ✅ Completed

---

## FINDINGS

### Finding 1: Async Connection Pooling

**Context**: LangChain PGVector with high concurrent load

**Pattern**:
\`\`\`python
from langchain_postgres import PGVector
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=10,
    max_overflow=20
)
store = PGVector(connection=engine, ...)
\`\`\`

**Rationale**: Async engine with connection pool prevents connection exhaustion under load (10-100x throughput gain).

**Trade-offs**:
- ✅ High concurrency support
- ❌ Requires asyncpg dependency

**Anti-Pattern**:
\`\`\`python
# Synchronous client (blocks event loop)
engine = create_engine("postgresql://...")  # ❌ BAD
\`\`\`

**Why it fails**: Blocks async event loop, nullifies concurrency gains.

---

## SYNTHESIS

### Patterns Extracted
1. **Async Connection Pooling** - Use asyncpg + pool_size=10 for concurrent workloads
   - Use when: > 10 concurrent operations
   - Complexity: Low

### Anti-Patterns Identified
1. ❌ **Sync clients in async context** - Blocks event loop → Use AsyncPGVectorStore

### Key Insights
- LangChain PGVector supports both sync/async - choose based on workload
- Connection pooling essential at scale (> 50 QPS)

---

## CODE EXAMPLES

### Example 1: Batch Embedding Insert

**Scenario**: Insert 1,000 embeddings efficiently

\`\`\`python
async def batch_insert(store: PGVector, texts: list[str], batch_size=100):
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        await store.aadd_texts(batch)
\`\`\`

**Complexity**: Low

---

## RECOMMENDATIONS

### Immediate Actions
1. **Replace sync client** - Migrate to `create_async_engine` for async workloads
2. **Set pool_size=10** - Handle concurrent connections efficiently

### Integration Strategy
1. Update `infrastructure/vectorstore.py` with async engine
2. Add asyncpg to pyproject.toml dependencies
3. Test with 50+ concurrent inserts

---

## METADATA

**Confidence**: High
**Sources**: langchain-ai/langchain, pgvector/pgvector
**Token Budget**: ~2,300 tokens total
**Execution Log**: Analysis (10s), Research (60s), Synthesis (15s), Output (4s)

---

**Agent Version**: 2.0.0
**Protocol Version**: File-Based v1.0.0
**SPR Compliance**: ✅
```

**Token Count**: ~600 tokens (efficient, complete)

---

## Integration with Status Updates

Sub-agent updates progress while generating output:

```python
# Phase 1: Research
update_status(25, "Executing MCP query: langchain-ai/langchain")

# Phase 2: Synthesis
findings = [...]  # Extract patterns
update_status(60, f"Synthesizing findings ({len(findings)} patterns identified)", findings_count=len(findings))

# Phase 3: Output Generation
output = generate_spr_output(findings)
update_status(90, "Generating SPR output")

# Phase 4: Finalize
Path(output_file).write_text(output)
update_status(100, "Completed", findings_count=len(findings))
```

---

**Created**: 2025-11-30  
**Version**: 1.0.0  
**Template Type**: SPR Output Format  
**Target Users**: CLI-spawned sub-agents (research-specialist, repository-guardian, etc.)

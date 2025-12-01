# REQ-011 NEXT SESSION - QUANT-001 End-to-End Validation

**Objective**: Validate file-based protocol with live CLI sub-agent execution

**Status**: QUANT-001 implemented ✅ → Needs runtime validation

---

## CONTEXT

**Completed**:
- File-based protocol (status.yaml, output.md, progress.log)
- Orchestrator skill (spawn_parallel, poll_status, monitor_progress)
- Research Specialist (progress tracking integrated)
- Validation script (8/8 static checks passed)

**Pending**:
- **Live execution test** (copilot CLI spawn + real MCP queries)
- End-to-end flow validation (spawn → poll → consolidate → integrate)
- Performance metrics (latency, token usage, progress accuracy)

---

## TASK

**Primary**: Execute live sub-agent orchestration with Research Specialist

**Test Scenario**:
```
User: "Investiga patrones de async connection pooling con pgvector en LangChain"
→ SUPER_AGENT spawns research-specialist via orchestrator
→ Monitor real-time progress (status.yaml polling every 2s)
→ Validate MCP queries executed (DeepWiki calls to langchain-ai/langchain)
→ Verify SPR output generated (findings, patterns, anti-patterns, code)
→ Consolidate results (extract patterns for integration)
```

---

## VALIDATION CHECKLIST

### Pre-Execution
- [ ] Copilot CLI installed (`which copilot` returns path)
- [ ] Custom agent detected (`research-specialist.agent.md` visible)
- [ ] VS Code settings enabled (`useIntentDetection: true`)
- [ ] MCP servers active (deepwiki, repo-indexer)

### Execution
- [ ] Session created (`.sia/runtime/{UUID}/` directory exists)
- [ ] Agent spawned (subprocess PID captured, no immediate crash)
- [ ] Status updates (status.yaml modified at ~30s intervals)
- [ ] Progress visible (`[research-specialist] X% - Current task`)
- [ ] MCP queries executed (DeepWiki logs show repo queries)
- [ ] Timeout enforced (agent completes or kills after 300s)

### Post-Execution
- [ ] Status final (`state: completed`, `progress_percent: 100`)
- [ ] Output generated (`output.md` exists, SPR format valid)
- [ ] Findings extracted (3+ patterns OR 1+ code example)
- [ ] Token efficiency (<5000 total, no context explosion)
- [ ] No errors (`errors: []` in status.yaml)
- [ ] Progress log complete (phases logged with timestamps)

### Integration
- [ ] Results consolidated (orchestrator.consolidate_results() returns SPR)
- [ ] Patterns extracted (code examples, anti-patterns identified)
- [ ] Project SPR updated (findings integrated into `.sia/agents/[project].md`)

---

## COMMANDS

**Execute orchestrator**:
```bash
uv run --with pyyaml python -c "
from skills.orchestrate_subagents import SubAgentOrchestrator

orchestrator = SubAgentOrchestrator()
tasks = [{
    'agent_name': 'research-specialist',
    'prompt': '''Research async connection pooling with pgvector in LangChain.

CONTEXT: Building semantic code search with high concurrent load.
QUESTIONS:
1. How to configure PGVector with async engine + connection pooling?
2. Batch embedding patterns (optimal batch_size for throughput)?
3. Index optimization (IVFFlat vs HNSW for 100k+ vectors)?

EXPECTED OUTPUT: SPR markdown (code examples + patterns + anti-patterns)
REPOS: langchain-ai/langchain, pgvector/pgvector''',
    'timeout': 300
}]

agents = orchestrator.spawn_parallel(tasks)
orchestrator.monitor_progress(agents, verbose=True)
results = orchestrator.consolidate_results(agents)

print('\n' + '='*80)
print('RESULTS:')
print('='*80)
for agent_name, spr in results.items():
    print(f'\n## {agent_name.upper()}\n')
    print(spr[:500] + '...' if len(spr) > 500 else spr)
"
```

**Inspect session**:
```bash
SESSION_ID=$(ls -t .sia/runtime/ | head -1)
cat .sia/runtime/$SESSION_ID/orchestrator.yaml
cat .sia/runtime/$SESSION_ID/research-specialist/status.yaml
head -50 .sia/runtime/$SESSION_ID/research-specialist/output.md
tail -20 .sia/runtime/$SESSION_ID/research-specialist/progress.log
```

---

## SUCCESS CRITERIA

**Minimum (MVP)**:
1. Agent spawns without crash
2. Status updates at least once (progress > 0%)
3. Output file created (even if incomplete)

**Target (Production-Ready)**:
1. Status updates every 30s (5+ updates during 150s execution)
2. Progress reaches 100% (state: completed)
3. SPR output valid (<5000 tokens, 2+ findings)
4. MCP queries logged (DeepWiki execution confirmed)
5. No errors in status.yaml

**Stretch (Optimal)**:
1. Latency <120s (spawn → completion)
2. Token efficiency >95% (vs full wiki context)
3. Code examples runnable (syntax-valid Python)
4. Anti-patterns identified (3+ documented)
5. Handoff ready (can delegate to repository-guardian)

---

## FAILURE SCENARIOS + MITIGATION

**Scenario 1**: Agent crashes on spawn
- **Check**: Copilot CLI version (`copilot --version`)
- **Mitigation**: Update CLI or fallback to manual MCP queries

**Scenario 2**: Status never updates (stuck at 0%)
- **Check**: `SIA_STATUS_FILE` env var set correctly
- **Mitigation**: Debug snippet in research-specialist.agent.md

**Scenario 3**: MCP queries fail (rate limit, auth)
- **Check**: MCP server logs, API keys
- **Mitigation**: Increase timeout, add retry logic

**Scenario 4**: Output incomplete (progress 60%, then hang)
- **Check**: Copilot CLI logs in `logs/copilot.log`
- **Mitigation**: Adjust timeout, simplify prompt

---

## PERFORMANCE METRICS TO CAPTURE

**Timing**:
- Spawn latency (create_session → agent PID captured)
- First status update (PID → first status.yaml modification)
- MCP query latency (status update → DeepWiki response)
- Completion time (spawn → state: completed)

**Resource Usage**:
- Memory (subprocess RSS during execution)
- Disk (session directory size after completion)
- Network (MCP query count × avg response size)

**Quality**:
- Token count (prompt + MCP responses + output)
- Findings quality (patterns useful? code runnable?)
- SPR compliance (structure matches template?)

---

## NEXT STEPS POST-VALIDATION

**If PASS**:
1. Mark QUANT-001 as production-ready
2. Update SESSION_SUMMARY.md with live metrics
3. Move to QUANT-002 (Repository Guardian conversion)

**If PARTIAL PASS** (works but has issues):
1. Document issues in LESSONS_LEARNED.md
2. Create QUANT-001.1 (refinements/bugfixes)
3. Re-validate before QUANT-002

**If FAIL** (agent doesn't execute):
1. Debug root cause (CLI, MCP, protocol)
2. Fix blockers in hotfix commit
3. Re-run validation before proceeding

---

## PROMPT FOR NEXT SESSION

```
@activate

"Valida QUANT-001 end-to-end: ejecuta research-specialist via orchestrator con prompt pgvector async patterns. 

Verifica:
- Spawn exitoso (PID capturado)
- Status updates cada 30s (5+ durante ejecución)
- Output.md SPR válido (<5000 tokens, 2+ findings)
- MCP queries ejecutadas (DeepWiki logs)
- No errors en status.yaml

Captura métricas: latency spawn→completion, token count, findings quality.

Si PASS → Update SESSION_SUMMARY + QUANT-002.
Si FAIL → Debug + hotfix antes de continuar."
```

---

**Created**: 2025-11-30  
**REQ**: REQ-011 QUANT-001  
**Type**: Validation Protocol  
**Format**: SPR (Sparse Priming Representation)  
**Status**: Ready for execution

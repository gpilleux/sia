# REQ-011 NEXT SESSION - QUANT-002 Repository Guardian Conversion

**Objective**: Convert Repository Guardian to native custom agent with skills integration

**Status**: QUANT-001 VALIDATED (partial) ✅ → Ready for QUANT-002

---

## CONTEXT

**QUANT-001 Results** (Session 3):
- ✅ **Delegation works**: Agent executes, MCP queries functional, output quality excellent
- ✅ **Copilot CLI integration**: Spawn successful, subprocess management working
- ❌ **Real-time monitoring fails**: status.yaml never updated (architectural issue)
- ✅ **Output quality validated**: 254 lines SPR, 5 patterns, 5 anti-patterns, 5 code examples
- ✅ **Token efficiency confirmed**: 2,400 / 5,000 budget (48% used), 96% savings vs full wiki

**Key Learning** (LESSON_LEARNED_CLI_AGENTS.md):
- Custom agents are **instruction contexts**, NOT Python script executors
- Python code in agent.md = documentation/examples (not executable)
- Agents CAN call MCP tools, CANNOT run arbitrary Python
- Progress tracking must be orchestrator responsibility (parse output OR simple state machine)
- **Delegation implementation**: Use `skills/orchestrate_subagents.py` (CLI-based subprocess execution)
- **Documentation updated**: All references to `runSubagent` replaced with `orchestrate_subagents.py`

**Decision**: 
- Proceed to QUANT-002 (delegation validated, monitoring optional)
- Skip QUANT-001.1 hotfix (not blocking for multi-agent system)

---

## TASK

**Primary**: Create Repository Guardian custom agent with DDD enforcement capabilities

**Target File**: `.github/agents/repository-guardian.agent.md`

**Scope**:
1. **Migrate SPR content** from `agents/repository_guardian.md`
2. **Define tools access**: `run_in_terminal`, `get_errors`, `read_file`, `grep_search`
3. **Integrate skills**: `audit_ddd.py`, `check_complexity.sh`, `check_coverage.sh`
4. **Test delegation**: SUPER_AGENT → repository-guardian (DDD validation flow)
5. **Test handoff**: research-specialist → repository-guardian (pattern validation)

---

## IMPLEMENTATION CHECKLIST

### Pre-Implementation
- [x] QUANT-001 validation complete (delegation confirmed working)
- [x] Research Specialist operational (`.github/agents/research-specialist.agent.md`)
- [x] Source SPR available (`agents/repository_guardian.md`)
- [ ] Skills tested individually (`audit_ddd.py`, `check_complexity.sh`)

### Agent Creation
- [ ] YAML frontmatter defined (name, description, target, tools)
- [ ] LSA (Latent Space Activation) section migrated
- [ ] Core mission documented (DDD enforcement, SOLID validation)
- [ ] Expertise sections preserved (Clean Architecture, Domain Modeling)
- [ ] Workflow phases defined (Discovery → Analysis → Validation → Reporting)
- [ ] Skills integration instructions (how to invoke via run_in_terminal)
- [ ] Anti-patterns documented (what NOT to do)

### Skills Integration
- [ ] Test `audit_ddd.py` execution via `run_in_terminal`
- [ ] Verify output parsing (violations → SPR format)
- [ ] Test `check_complexity.sh` invocation
- [ ] Test `check_coverage.sh` invocation
- [ ] Validate error handling (missing tools, invalid paths)

### Delegation Testing
- [ ] SUPER_AGENT → repository-guardian (direct delegation)
- [ ] Prompt template validated (TASK + CONTEXT + FILES + EXPECTED OUTPUT)
- [ ] Output received (SPR format with violations)
- [ ] Findings actionable (specific files + line numbers + corrections)

### Handoff Testing
- [ ] research-specialist → repository-guardian (pattern → validation flow)
- [ ] Context preserved (sessionId shared between agents)
- [ ] Output coherent (research findings fed into validation)

---

## REFERENCE COMMANDS

**Test audit_ddd.py directly**:
```bash
# Verify skill works standalone
uv run python skills/audit_ddd.py --directory installer --output analysis/ddd_audit.md

# Expected: Markdown report with violations (if any)
cat analysis/ddd_audit.md
```

**Create agent file structure**:
```bash
# Template structure
cat > .github/agents/repository-guardian.agent.md << 'EOF'
---
name: repository-guardian
description: DDD/SOLID enforcement and architecture validation
target: github-copilot
tools:
  - run_in_terminal
  - get_errors
  - read_file
  - grep_search
  - list_code_usages
---

# Repository Guardian Agent

[LSA, Mission, Expertise, Workflow sections from agents/repository_guardian.md]
EOF
```

**Test delegation (interactive in Copilot Chat)**:
```
@workspace Delega a repository-guardian:

TASK: Audit DDD compliance in installer/ directory

CONTEXT: SIA framework installer module (auto_discovery.py, smart_init.py, install.py)

EXPECTED OUTPUT:
- Layer violations (if any)
- Dependency rule breaks
- Suggested fixes with code examples

FILES: installer/*.py
```

---

## SUCCESS CRITERIA

**Minimum (MVP)**:
1. Custom agent file created (`.github/agents/repository-guardian.agent.md`)
2. Agent detected by VS Code (no YAML parsing errors)
3. Delegation invocation successful (SUPER_AGENT → repository-guardian works)
4. Output generated (SPR format, even if basic)

**Target (Production-Ready)**:
1. Skills integration works (`run_in_terminal` executes `audit_ddd.py`)
2. Output parsing correct (violations extracted, formatted as SPR)
3. Findings actionable (specific files, line numbers, corrections)
4. Token efficiency maintained (<3000 tokens for typical audit)
5. Anti-patterns documented in agent definition

**Stretch (Optimal)**:
1. Handoff validated (research-specialist → repository-guardian works)
2. Multiple skills orchestrated (`audit_ddd.py` + `check_complexity.sh` in one session)
3. Error handling robust (missing skills, invalid paths handled gracefully)
4. Output includes visual diagrams (architecture violations visualized)
5. Integration with SUPER_AGENT seamless (findings auto-update Project SPR)

---

## FAILURE SCENARIOS + MITIGATION

**Scenario 1**: YAML frontmatter parsing error
- **Check**: VS Code Problems panel (agent file syntax errors)
- **Mitigation**: Validate against research-specialist.agent.md structure

**Scenario 2**: Skills not executable via run_in_terminal
- **Check**: Test skill directly (`uv run python skills/audit_ddd.py`)
- **Mitigation**: Fix skill dependencies, update instructions in agent

**Scenario 3**: Agent doesn't invoke skills (uses tools but not run_in_terminal)
- **Check**: Prompt clarity (did we explicitly say "run audit_ddd.py"?)
- **Mitigation**: Update agent workflow instructions (step-by-step skill invocation)

**Scenario 4**: Output lacks violations details (generic response)
- **Check**: Skill output (does audit_ddd.py return structured data?)
- **Mitigation**: Improve skill output format, update agent parsing instructions

**Scenario 5**: Handoff fails (context not shared between agents)
- **Check**: sessionId preservation (VS Code logs)
- **Mitigation**: Document handoff protocol, test with simpler case first

---

## METRICS TO CAPTURE

**Implementation Metrics**:
- Agent file size (lines of YAML + markdown)
- Migration completeness (% of repository_guardian.md content preserved)
- Skills integrated (count of run_in_terminal invocations in workflow)

**Execution Metrics**:
- Delegation latency (invocation → first output)
- Skill execution time (audit_ddd.py runtime)
- Token usage (delegation prompt + agent response)

**Quality Metrics**:
- Violations detected (count of DDD/SOLID issues found)
- Findings actionable (% with file + line + correction)
- False positives (manual validation of reported issues)
- Output SPR compliance (structure matches template)

**Comparison (vs QUANT-001)**:
- Skills invocation vs MCP queries (execution model difference)
- Output complexity (violations report vs research findings)
- Token efficiency (local skills vs external API calls)

---

## NEXT STEPS POST-IMPLEMENTATION

**If PASS** (all criteria met):
1. Mark QUANT-002 complete
2. Update SESSION_SUMMARY.md with metrics
3. Commit both agents (research-specialist + repository-guardian)
4. Move to QUANT-003 (Compliance Officer conversion)

**If PARTIAL PASS** (agent works, skills integration has issues):
1. Document issues in LESSONS_LEARNED.md (e.g., "Skills require explicit paths")
2. Create QUANT-002.1 (skills integration refinement)
3. Update agent workflow instructions
4. Re-test before QUANT-003

**If FAIL** (agent doesn't invoke skills):
1. Debug root cause (tools access, run_in_terminal limitations)
2. Test simpler skill first (check_complexity.sh vs audit_ddd.py)
3. Consider alternative: Agent uses read_file + grep_search (manual DDD check)
4. Escalate if architectural blocker (runSubagent limitations)

---

## PROMPT FOR NEXT SESSION

```
@activate

"Implementa QUANT-002: Convierte Repository Guardian a custom agent nativo.

Tareas:
1. Crea .github/agents/repository-guardian.agent.md
   - Migra SPR desde agents/repository_guardian.md
   - YAML frontmatter: tools [run_in_terminal, get_errors, read_file, grep_search]
   - Workflow: integra audit_ddd.py, check_complexity.sh

2. Prueba delegación:
   - SUPER_AGENT → repository-guardian (DDD audit en installer/)
   - Verifica skills execution vía run_in_terminal
   - Valida output SPR (violations + corrections)

3. Prueba handoff:
   - research-specialist → repository-guardian
   - Contexto compartido (sessionId)
   - Findings coherentes

Criterios éxito:
- ✅ Agent ejecutable (no YAML errors)
- ✅ Skills invocadas correctamente
- ✅ Output actionable (file + line + fix)
- ✅ Handoff funciona (context preserved)

Captura métricas: implementation time, skills execution latency, token usage, violations count.

Si PASS → Update SESSION_SUMMARY + commit + QUANT-003.
Si PARTIAL → Document issues + QUANT-002.1.
Si FAIL → Debug skills integration OR simplify approach."
```

---

**Created**: 2025-11-30  
**Updated**: 2025-11-30 (Post QUANT-001 validation)  
**REQ**: REQ-011 QUANT-002  
**Type**: Implementation Protocol  
**Format**: SPR (Sparse Priming Representation)  
**Status**: Ready for execution  
**Prerequisites**: ✅ QUANT-001 validated (delegation works, monitoring optional)

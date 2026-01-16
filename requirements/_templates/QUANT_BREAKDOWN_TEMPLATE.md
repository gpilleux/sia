# REQ-{ID}: QUANT TASK DECOMPOSITION

**Requirement**: {Requirement Title}  
**Decomposition Date**: {YYYY-MM-DD}  
**Domain Analysis**: `REQ-{ID}_domain_analysis.md`

---

## OBJECTIVE

{Concise description of the final objective in 1-2 sentences}

---

## CENTRAL INVARIANT TO SATISFY

```
{Mathematical/logical constraint that MUST be met when all tasks are complete}

Example: purchase_order.total <= budget.limit
Example: embedding.dimensions == 1536
Example: ∀ message ∈ session: message.session_id == session.id
```

---

## QUANT TASK DEPENDENCY GRAPH

```mermaid
graph TD
  Q001[QUANT-{ID}-001: {Title}]
  Q002[QUANT-{ID}-002: {Title}]
  Q003[QUANT-{ID}-003: {Title}]
  Q004[QUANT-{ID}-004: {Title}]
  
  Q001 --> Q002
  Q001 --> Q003
  Q002 --> Q004
  Q003 --> Q004
```

---

## EXECUTION SEQUENCE

**Critical Path**: QUANT-{ID}-001 → QUANT-{ID}-002 → QUANT-{ID}-004 ({X}h)

**Parallel Opportunities**:
- QUANT-{ID}-003 can run in parallel with QUANT-{ID}-002

### Sequential Order
1. ✅ QUANT-{ID}-001 ({X}h, {RISK} risk) - {Short Title}
2. ⏳ QUANT-{ID}-002 ({X}h, {RISK} risk) - {Short Title}
3. ⏳ QUANT-{ID}-003 ({X}h, {RISK} risk) - {Short Title} [PARALLEL]
4. ⏳ QUANT-{ID}-004 ({X}h, {RISK} risk) - {Short Title}

---

## DETAILED QUANT TASKS

### QUANT-{ID}-001: {Verb} {Noun} {Constraint}

**Type**: [INFRA|DOMAIN|TEST|DEPLOY]  
**Layer**: [Domain|Application|Infrastructure|API]  
**Bounded Context**: {Bounded Context Name}

**Invariant**:
```
{Specific mathematical/logical constraint for this task}
```

**Description**:
{Detailed description of what must be done in this atomic task}

**Acceptance Criteria**:
- [ ] **AC1**: {Executable/observable criterion}
  - Verification: `{Command or test that verifies}`
- [ ] **AC2**: {Executable/observable criterion}
  - Verification: `{Command or test that verifies}`
- [ ] **AC3**: {Executable/observable criterion}
  - Verification: `{Command or test that verifies}`

**Dependencies**: `[{Previous QUANT-IDs}]`

**Files Affected**:
- `{path/to/file.py}`: {CREATE|MODIFY|DELETE} - {Reason}

**Implementation Notes**:
```python
# Expected code example (pseudocode if necessary)
class {ClassName}:
    def {method_name}(self) -> {ReturnType}:
        # {Logic description}
        pass
```

**Test Strategy**:
{How this specific task will be tested}

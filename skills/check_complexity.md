# check_complexity.sh - Radon Complexity Hunter

**Purpose**: Identify code with high Cyclomatic Complexity (Rank C or worse).

**Token Cost**: ~200 tokens (only load when invoking this skill)

---

## When to Invoke

- **Pre-QUANT** (FASE 4): Baseline complexity before implementing REQ
- **Post-Task** (FASE 5): Verify no complexity regression introduced
- **Pre-PR**: Ensure code meets quality standards

---

## Usage

```bash
sh sia/skills/check_complexity.sh
```

**Scans**: All `.py` files excluding `venv/`, `tests/`, `node_modules/`

**Output**:
```
Cyclomatic Complexity Report (Only C, D, E, F)
---------------------------------------------------
infrastructure/adk/openai_adapter.py
  M 15:4 OpenAILlm.stream_chat - C (12)
  
backend/src/domain/services/invoice.py
  M 42:8 InvoiceService.calculate_total - D (18)
```

---

## Complexity Ranks

| Rank | CC Score | Action Required |
|------|----------|----------------|
| A | 1-5 | ✅ Excellent |
| B | 6-10 | ✅ Good |
| C | 11-20 | ⚠️ Monitor, consider refactor |
| D | 21-30 | ❌ **Refactor immediately** |
| E | 31-40 | ❌ **Critical - create QUANT task** |
| F | 41+ | ❌ **Blocker - halt feature work** |

---

## Integration with Requirements

**Pre-QUANT Baseline** (FASE 4):
```bash
# Before starting REQ-042
sh sia/skills/check_complexity.sh > .sia/requirements/REQ-042/baseline_complexity.txt

# Identify high-complexity areas
# If Rank D+ detected → Add refactoring tasks to QUANT breakdown
```

**Post-Task Verification** (FASE 5):
```bash
# After completing QUANT-042-003
sh sia/skills/check_complexity.sh

# Compare with baseline
# ASSERT: No new C/D/E/F ranks introduced
```

---

## Action Matrix

| Detected Rank | Action |
|---------------|--------|
| **C (11-20)** | Log warning, continue. Schedule refactor for next sprint. |
| **D (21-30)** | **HALT**. Create refactoring QUANT task before proceeding. |
| **E/F (31+)** | **BLOCKER**. Cannot merge until refactored to Rank B or better. |

---

## Example Output

```bash
$ sh sia/skills/check_complexity.sh

Cyclomatic Complexity Report (Only C, D, E, F)
---------------------------------------------------
backend/src/application/use_cases/process_invoice.py
  M 28:4 ProcessInvoiceUseCase.execute - D (22)
  
  RECOMMENDATION: Extract validation logic to separate method.
  
backend/src/infrastructure/repositories/postgres_invoice.py
  M 145:8 PostgresInvoiceRepository.complex_query - C (15)
  
  RECOMMENDATION: Use query builder pattern.
  
---------------------------------------------------
Summary:
  Rank C: 1 function
  Rank D: 1 function
  Total violations: 2

ACTION REQUIRED: Refactor Rank D before proceeding.
```

---

## Dependencies

- **Radon**: Installed via `pip install radon` (auto-installed by skill)
- **Python**: 3.7+

---

## See Also

- `visualize_architecture.sh` - Validate DDD layer separation
- `audit_ddd.py` - Check domain purity (no infrastructure deps)
- `sia/core/STANDARDS.md` - Code quality standards

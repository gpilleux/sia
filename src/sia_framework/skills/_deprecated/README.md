# Deprecated Skills

## Purpose

This directory contains skills that have been deprecated from active use but preserved for reference.

## Deprecation Reason

**Date**: 2025-11-30  
**Reason**: Simplification of workflow - removed time estimation and AI vs Human comparison metrics

### Context

The initial framework included detailed time tracking to measure:
1. AI self-prediction accuracy (estimated vs actual time)
2. Human team comparison (AI speedup metrics)
3. Historical variance analysis

**Decision**: These metrics added complexity without sufficient value for the current workflow:
- Time estimation is inherently imprecise for creative/research work
- AI vs Human comparisons are valuable but better tracked at project level, not task level
- Focus shifted to **quality of output** rather than **speed metrics**

### Preserved Files

- `task_timer.md`: Documentation for task timer skill
- `task_timer.py`: Python script for time tracking

### Migration Path

If time tracking is needed in the future:
1. Review these files for implementation patterns
2. Consider simpler approach (start/stop only, no dual estimation)
3. Track at requirement level (REQ-XXX) not individual QUANT tasks

---

**Preservation Principle**: Never delete domain knowledge, archive it.

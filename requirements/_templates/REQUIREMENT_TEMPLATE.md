# REQ-{ID}: {Descriptive Title}

**Request Date**: {YYYY-MM-DD}  
**Requester**: {Name/Role}  
**Priority**: [CRITICAL|HIGH|MEDIUM|LOW]  
**Bounded Context**: {Context Name}

---

## REQUIREMENT DESCRIPTION

{Clear and concise description in natural language. Explain WHAT is needed, not how to implement it.}

### Problem to Solve
{What user/business problem does this requirement solve?}

### Expected Value
{What value does it generate for the system or end users?}

---

## INVARIANTS TO SATISFY

{List of mathematical/logical constraints that MUST be met when the requirement is complete. Example: "message_count >= 0", "embedding.dimensions == 1536"}

- [ ] Invariant 1: {Formal constraint}
- [ ] Invariant 2: {Formal constraint}

---

## ACCEPTANCE CRITERIA

{Verifiable conditions that determine if the requirement is DONE. Must be executable/observable.}

- [ ] Criteria 1: {Verifiable condition}
- [ ] Criteria 2: {Verifiable condition}
- [ ] Criteria 3: {Verifiable condition}

---

## TECHNICAL CONTEXT

### Affected Components
{List of modules/files/services that might be affected}

- `{path/to/file.py}`: {Reason for impact}

### Technical Dependencies
{APIs, libraries, external services needed}

- {Dependency 1}
- {Dependency 2}

### Architectural Constraints
{DDD/SOLID/KISS principles to respect, patterns to follow}

- **DDD**: {Affected Aggregate, Bounded Context}
- **SOLID**: {Relevant Principle}
- **Clean Architecture**: {Layer involved}

---

## RESEARCH NEEDED

### Domain Questions
{Questions requiring research via deepwiki/playwright/documentation}

1. {Technical question about libraries/APIs}
2. {Question about implementation patterns}

### Repositories/Docs to Consult
{Links or repo names to investigate with deepwiki}

- `{owner/repo}`: {What to investigate}

---

## ADDITIONAL NOTES

{Any relevant info: usage examples, edge cases, performance considerations, etc.}

---

## STATUS

- [ ] Requirement received
- [ ] Domain analysis completed (see `{ID}_domain_analysis.md`)
- [ ] QUANT decomposition completed (see `{ID}_quant_breakdown.md`)
- [ ] Implementation in progress
- [ ] Tests passing
- [ ] Documentation updated
- [ ] DONE (invariants verified)

---

## REFERENCES

- **Domain Analysis**: `requirements/{ID}_domain_analysis.md`
- **QUANT Decomposition**: `requirements/{ID}_quant_breakdown.md`
- **Related Issues**: {Links if applicable}

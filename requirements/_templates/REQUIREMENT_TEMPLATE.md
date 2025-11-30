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

## FIRST PRINCIPLES ANALYSIS

### Fundamental Question
**What are we fundamentally trying to achieve?**  
{Strip away assumptions. Get to the core problem without inherited beliefs.}

### Axioms (Fundamental Truths)
{List self-evident truths that require no proof and cannot be broken down further.}

1. **Axiom 1**: {Fundamental truth - example: "Users tolerate <200ms latency"}
2. **Axiom 2**: {Fundamental truth - example: "Invalid state must be unrepresentable"}
3. **Axiom 3**: {Fundamental truth - example: "Domain logic independent of infrastructure"}

### Inherited Assumptions (To Eliminate)
{List beliefs we're assuming without validation. Mark for elimination.}

- ❌ **Assumption 1**: {Example: "We need Redis because it's standard"}
- ❌ **Assumption 2**: {Example: "Must use microservices"}
- ❌ **Assumption 3**: {Example: "GraphQL required for flexible queries"}

### Observable Facts
{Measurements and verifiable data - not opinions.}

- **Fact 1**: {Example: "API response time: 2s (measured via /metrics)"}
- **Fact 2**: {Example: "Database query: 1.8s (EXPLAIN ANALYZE)"}
- **Fact 3**: {Example: "Current user count: 500 concurrent"}

### Reconstructed Solution (From Axioms)
{How do we rebuild the solution starting only from axioms and facts?}

**Option 1**: {Solution derived from first principles}
- **Cost**: {Implementation time/complexity}
- **Impact**: {Measurable improvement}
- **Complexity**: {Zero/Low/Medium/High}
- **Justified**: {✅/❌} {Reasoning from axioms}

**Option 2**: {Alternative solution}
- **Cost**: {Implementation time/complexity}
- **Impact**: {Measurable improvement}
- **Complexity**: {Zero/Low/Medium/High}
- **Justified**: {✅/❌} {Reasoning from axioms}

**Selected Solution**: {Chosen option}  
**Justification**: {Why this solution best satisfies axioms with minimal unjustified complexity}

### Re-evaluation Triggers
{Conditions under which this decision should be revisited}

- IF {condition} THEN re-evaluate {aspect}
- Example: "IF concurrent users > 10K THEN re-evaluate database index vs distributed cache"

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

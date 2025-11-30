# REQ-{ID}: DOMAIN RESEARCH & ANALYSIS

**Requirement**: {Requirement Title}  
**Analysis Date**: {YYYY-MM-DD}  
**Analyst**: SIA (Super Intelligence Agency)

---

## RESEARCH PROTOCOL

### 0. FIRST PRINCIPLES BREAKDOWN (Execute BEFORE research)

#### Core Question
**What are we fundamentally trying to achieve?**  
{Eliminate assumptions. Get to irreducible truth.}

#### Question Protocol
```
1. WHAT is the actual problem?
   → {Strip inherited beliefs}

2. WHY is this the goal? (Recursive)
   → {Keep asking "why" until you reach an axiom}

3. WHAT is fundamentally true?
   → {List axioms: self-evident, irreducible, independent}

4. WHAT are we assuming?
   → {Identify inherited beliefs to eliminate}

5. HOW do we rebuild from axioms?
   → {Derive solution from fundamental truths}
```

#### Axioms (Before Research)
{What do we know is fundamentally true WITHOUT external research?}

1. **Axiom 1**: {Example: "Users expect data permanence across sessions"}
2. **Axiom 2**: {Example: "Invalid state must be unrepresentable"}
3. **Axiom 3**: {Example: "Domain logic must not depend on infrastructure"}

#### Inherited Assumptions (To Validate)
{What are we assuming that needs research validation?}

- ❌ **Assumption 1**: {Example: "We need WebSockets for real-time"}
  - **Validation Needed**: Research alternative protocols, latency requirements
- ❌ **Assumption 2**: {Example: "Redis required for caching"}
  - **Validation Needed**: Research PostgreSQL caching capabilities
- ❌ **Assumption 3**: {Example: "GraphQL needed for flexible queries"}
  - **Validation Needed**: Research REST limitations for our use case

#### Observable Facts (Baseline)
{Measure current system BEFORE proposing solutions}

- **Fact 1**: {Example: "Current API latency: 2s (measured)"}
- **Fact 2**: {Example: "Database query time: 1.8s (EXPLAIN ANALYZE)"}
- **Fact 3**: {Example: "Concurrent users: 500 (analytics)"}

### 1. CENTRAL QUESTION
{What do I need to understand about the technical domain to correctly implement this requirement?}

### 2. INITIAL HYPOTHESIS
{Before researching: How do I think it should be implemented? What patterns/libraries do I assume I should use?}

---

## DEEPWIKI RESEARCH

### Repositories Consulted

#### {owner/repo-1}
**Question**: {Specific query asked}

**Findings**:
```
{Relevant documentation/code extract}
```

**Conclusions**:
- {Insight 1}
- {Insight 2}

---

#### {owner/repo-2}
**Question**: {Specific query asked}

**Findings**:
```
{Relevant documentation/code extract}
```

**Conclusions**:
- {Insight 1}

---

## PLAYWRIGHT RESEARCH (If applicable)

### Site/Documentation Consulted
**URL**: {Official documentation URL}

**Navigation**:
1. {Step 1: Click on section X}
2. {Step 2: Read subsection Y}

**Findings**:
```
{Official documentation extract}
```

**Conclusions**:
- {Technical insight}

---

## CURRENT TECH STACK ANALYSIS

### Relevant Existing Components

#### {Component 1}
**Location**: `{path/file.py}`  
**Current Pattern**: {Description of used pattern}  
**Reusable**: [YES|NO]  
**Modification Needed**: {Description if applicable}

#### {Component 2}
**Location**: `{path/file.py}`  
**Current Pattern**: {Description of used pattern}  
**Reusable**: [YES|NO]  

---

## ARCHITECTURAL DECISIONS

### Chosen Implementation Pattern
{Description of the pattern/strategy to be used}

**Justification**:
- **DDD**: {How it respects bounded contexts, aggregates, value objects}
- **SOLID**: {Which principles apply}
- **KISS**: {Why it is the simplest solution that works}
- **Clean Code**: {How it improves readability/maintainability}

### Alternatives Considered and Discarded

#### Alternative 1: {Name}
**Discarded because**: {Reason based on principles}

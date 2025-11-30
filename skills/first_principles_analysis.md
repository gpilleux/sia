# First Principles Analysis - Guided Decomposition Skill

**Type**: Prompt Skill  
**Purpose**: Guide systematic decomposition of problems to fundamental truths  
**When to Use**: Before planning, development, or architectural decisions  
**Reference**: `core/FIRST_PRINCIPLES.md` (complete methodology)

---

## SKILL INVOCATION

**Trigger**: User says "Analyze from first principles" OR before any major decision/implementation

**Protocol**: Execute this analysis BEFORE researching solutions or writing code

---

## THE QUESTION PROTOCOL

### Level 1: WHAT are we fundamentally trying to achieve?
```
Question Template:
"What is the actual problem we're solving, stripped of all assumptions?"

Anti-Patterns to Avoid:
❌ "Implement feature X" (describes solution, not problem)
❌ "Use technology Y" (inherited assumption)
❌ "Follow pattern Z" (cargo cult)

First Principles Answer:
✅ "Users need to {fundamental need} without {fundamental constraint}"
✅ Example: "Users need to verify identity without transmitting password on every request"
```

---

### Level 2: WHY is this the goal? (Recursive)
```
Recursive Questioning:
Q: "Why do users need {goal}?"
A: {Because X}

Q: "Why is {X} important?"
A: {Because Y}

Q: "Why is {Y} fundamental?"
A: {AXIOM - cannot be broken down further}

Example Chain:
Q: "Why add caching?"
A: "To improve performance"

Q: "Why improve performance?"
A: "Users complain about slow response"

Q: "Why do users care about response time?"
A: "Humans perceive >200ms as sluggish (cognitive limit)" ← AXIOM
```

**Stop Condition**: When you reach a statement that is:
- Self-evident (doesn't need proof)
- Irreducible (can't be broken down)
- Universal (true regardless of context)

---

### Level 3: WHAT do we know is fundamentally true?
```
Axiom Checklist:
For each claimed axiom, verify:

1. ✅ Self-Evident: True without requiring external proof?
2. ✅ Irreducible: Cannot be decomposed further?
3. ✅ Independent: Stands alone without dependencies?
4. ✅ Universal: Applies beyond current context?

Examples of VALID Axioms:
✅ "Process memory is volatile (OS kills processes)"
✅ "Invalid state must be unrepresentable (type safety)"
✅ "Users tolerate <200ms latency (cognitive threshold)"
✅ "Domain logic must not depend on infrastructure (DDD)"

Examples of INVALID Axioms (Actually Assumptions):
❌ "We need a database" (Could be files, API, memory)
❌ "REST is required" (Could be GraphQL, WebSocket, gRPC)
❌ "Microservices are necessary" (Could be monolith, modular monolith)
```

---

### Level 4: WHAT are we assuming?
```
Assumption Detection Protocol:

1. List all "shoulds" and "musts" in requirement
2. For each, ask: "Is this fundamentally true or inherited belief?"
3. Challenge inherited beliefs

Assumption Categories:

A) TECHNOLOGY ASSUMPTIONS:
   ❌ "We should use Redis"
   ✅ Question: "What problem does Redis solve that simpler tools don't?"
   
B) ARCHITECTURAL ASSUMPTIONS:
   ❌ "We need microservices"
   ✅ Question: "What scale/team problems justify microservice complexity?"
   
C) PATTERN ASSUMPTIONS:
   ❌ "Everyone uses X pattern"
   ✅ Question: "Does our context justify this pattern's complexity?"

D) CONSTRAINT ASSUMPTIONS:
   ❌ "We can't change the database schema"
   ✅ Question: "Is this a real constraint or perceived constraint?"

Elimination Test:
- Can we achieve the goal without this assumption?
- If YES → Eliminate it, rebuild from axioms
- If NO → Convert to verified requirement (research)
```

---

### Level 5: HOW do we rebuild from axioms?
```
Reconstruction Protocol:

1. Start with ONLY axioms (fundamental truths)
2. Derive requirements from axioms (logical deduction)
3. Evaluate solution options against axioms
4. Choose simplest solution that satisfies axioms

Evaluation Template:

OPTION 1: {Solution Name}
├─ Cost: {Time/Complexity}
├─ Impact: {Measurable Improvement}
├─ Complexity: {Zero/Low/Medium/High}
├─ Axioms Satisfied: {List}
├─ Axioms Violated: {List}
└─ Justified: {✅/❌} {Reasoning}

OPTION 2: {Alternative Solution}
├─ Cost: {Time/Complexity}
├─ Impact: {Measurable Improvement}
├─ Complexity: {Zero/Low/Medium/High}
├─ Axioms Satisfied: {List}
├─ Axioms Violated: {List}
└─ Justified: {✅/❌} {Reasoning}

Selection Criteria:
1. Satisfies ALL axioms
2. Minimal unjustified complexity
3. Measurable improvement
4. KISS principle (simplest that works)
```

---

## COMPLETE WORKFLOW EXAMPLE

### Scenario: "Add real-time notifications to app"

#### Step 1: WHAT are we fundamentally trying to achieve?
```
❌ Conventional: "Implement WebSocket server for push notifications"
✅ First Principles: "Users need to receive updates without manual refresh"
```

#### Step 2: WHY is this the goal? (Recursive)
```
Q: "Why do users need updates without refresh?"
A: "To know about new messages immediately"

Q: "Why do they need to know immediately?"
A: "Delayed notifications hurt UX (users expect real-time communication)"

Q: "Why do users expect real-time?"
A: "Cognitive expectation from messaging apps (WhatsApp, Slack)" ← AXIOM

Q: "What's the measurable threshold?"
A: "Users perceive <1s as real-time" ← MEASURABLE AXIOM
```

**Axioms Identified**:
1. Users expect notification latency <1s (cognitive threshold)
2. Manual refresh violates UX expectations (proven pattern)
3. Server must initiate communication (HTTP request-response insufficient)

#### Step 3: WHAT do we know is fundamentally true?
```
AXIOM 1: Notification latency <1s required (user perception)
AXIOM 2: Server-to-client push needed (client polling insufficient)
AXIOM 3: Connection must persist (stateless HTTP breaks requirement)
AXIOM 4: Simplest solution that works (KISS principle)
```

#### Step 4: WHAT are we assuming?
```
❌ ASSUMPTION 1: "WebSocket is the only solution"
   → Alternatives: Server-Sent Events (SSE), Long Polling, WebTransport
   
❌ ASSUMPTION 2: "Need external message broker (Redis, RabbitMQ)"
   → Alternatives: PostgreSQL LISTEN/NOTIFY, in-memory queue
   
❌ ASSUMPTION 3: "Horizontal scaling required immediately"
   → Reality Check: Current users = 500, concurrent = 50
```

#### Step 5: HOW do we rebuild from axioms?
```
OPTION 1: Server-Sent Events (SSE)
├─ Cost: 2h implementation (native browser API)
├─ Impact: <500ms latency (satisfies <1s axiom)
├─ Complexity: LOW (unidirectional, no handshake)
├─ Axioms Satisfied: ✅ Latency, ✅ Server push, ✅ Persistent connection
├─ Axioms Violated: ❌ None
├─ Limitations: Unidirectional only
└─ Justified: ✅ IF bidirectional not needed (check requirements)

OPTION 2: WebSocket
├─ Cost: 4h implementation (bidirectional protocol)
├─ Impact: <500ms latency (satisfies <1s axiom)
├─ Complexity: MEDIUM (handshake, connection management)
├─ Axioms Satisfied: ✅ Latency, ✅ Server push, ✅ Persistent connection
├─ Axioms Violated: ❌ None
├─ Justification: ✅ IF bidirectional needed (chat, collaborative editing)
└─ Justified: {CONDITIONAL - validate bidirectional requirement}

OPTION 3: Long Polling
├─ Cost: 3h implementation
├─ Impact: 1-5s latency (violates <1s axiom)
├─ Complexity: MEDIUM (connection management, timeout handling)
├─ Axioms Satisfied: ✅ Server push (simulated)
├─ Axioms Violated: ❌ Latency requirement
└─ Justified: ❌ (violates core axiom)

OPTION 4: PostgreSQL LISTEN/NOTIFY + SSE
├─ Cost: 3h implementation (DB events + SSE)
├─ Impact: <500ms latency
├─ Complexity: LOW (uses existing DB)
├─ Axioms Satisfied: ✅ All + KISS (no new infrastructure)
├─ Axioms Violated: ❌ None
├─ Limitation: Single-server (revisit at scale)
└─ Justified: ✅ (simplest, satisfies axioms, scales to 10K users)

DECISION: PostgreSQL LISTEN/NOTIFY + SSE
REASONING:
1. Satisfies latency axiom (<500ms measured)
2. No new infrastructure (KISS)
3. Leverages existing PostgreSQL
4. Scales to 10K concurrent users (tested)
5. Upgrade path: Redis pub/sub when >10K concurrent

RE-EVALUATION TRIGGER:
IF concurrent_users > 10K THEN re-evaluate distributed pub/sub
```

---

## INTEGRATION WITH SIA WORKFLOWS

### Planning Phase (Requirements)
```
BEFORE creating REQ-XXX:
1. Execute First Principles Analysis
2. Document axioms in requirements/_templates/REQUIREMENT_TEMPLATE.md
3. Eliminate unjustified assumptions
4. Proceed to domain research (validate remaining assumptions)
```

### Development Phase (Implementation)
```
BEFORE writing code:
1. Review axioms from requirement
2. Validate implementation satisfies axioms
3. Document justification in docstrings

Example:
def notify_user(user_id: UUID, message: str) -> Result[None, Error]:
    """
    AXIOM: Notification latency <1s (user perception threshold)
    AXIOM: Server-initiated push (HTTP pull insufficient)
    
    IMPLEMENTATION: PostgreSQL NOTIFY + SSE
    JUSTIFIED: Simplest solution satisfying both axioms
    """
```

### QA Phase (Testing)
```
Tests MUST validate axioms, not implementation:

❌ def test_uses_websocket():
    assert isinstance(transport, WebSocketTransport)

✅ def test_notification_latency_axiom():
    """AXIOM: Notification latency <1s"""
    start = time.time()
    notify_user(user_id, "test")
    # Verify user receives notification
    latency = wait_for_notification(user_id)
    assert latency < 1.0, f"Violated latency axiom: {latency}s"
```

---

## AXIOM LIBRARY (SIA Domain)

### Architectural Axioms
```
1. Domain Independence (DDD)
   - Domain logic must not depend on infrastructure
   - Enables testing without DB, easier refactoring

2. Dependency Inversion (SOLID)
   - High-level modules must not depend on low-level modules
   - Both depend on abstractions

3. Single Responsibility (SOLID)
   - Each module has one reason to change
   - Reduces coupling, improves cohesion

4. KISS Principle
   - Simplest solution that works
   - Complexity justified only by demonstrated need
```

### Performance Axioms
```
1. Human Cognitive Limits
   - <200ms: Instant response perception
   - <1s: Flow state maintained
   - >10s: Context switch occurs

2. Developer Time > Compute Time
   - Optimize developer experience before compute performance
   - Premature optimization is evil

3. Measure Before Optimizing
   - Speculation violates evidence-based principle
   - Profile → Identify bottleneck → Fix → Verify
```

### Testing Axioms
```
1. Tests Protect Invariants
   - NOT implementation details
   - Input → Expected Output (black box)

2. Test Pyramid
   - Many unit tests (fast, isolated)
   - Some integration tests (realistic)
   - Few E2E tests (expensive, brittle)

3. Coverage = Axioms Tested
   - 100% axiom coverage > 100% line coverage
   - Uncovered axiom = potential bug
```

---

## ANTI-PATTERNS (Common Violations)

### 1. Cargo Cult Programming
```
❌ VIOLATION: "Use microservices because Netflix does"

FIRST PRINCIPLES CHALLENGE:
Q: What problem does microservices solve?
A: Independent scaling, team autonomy, failure isolation

Q: Do we have those problems?
FACTS: 3 developers, 500 users, monolith deploys in 2 min
AXIOM: Complexity justified only by demonstrated need

CONCLUSION: Monolith justified (KISS)
DEFER: Microservices when team >20 OR scaling bottleneck proven
```

### 2. Technology-First Thinking
```
❌ VIOLATION: "Let's use GraphQL for this API"

FIRST PRINCIPLES CHALLENGE:
Q: What problem are we solving?
PROBLEM: Need flexible queries from mobile app

Q: What's fundamentally needed?
AXIOM: Client-specific data fetching (avoid over-fetching)

Q: What are the alternatives?
- REST with query params: Complexity LOW, satisfies requirement
- GraphQL: Complexity MEDIUM, satisfies requirement + future flexibility

DECISION: REST with query params (KISS)
RE-EVALUATE: When multiple clients with divergent needs emerge
```

### 3. Assumption-Based Architecture
```
❌ VIOLATION: "We'll need Kafka for event streaming"

FIRST PRINCIPLES CHALLENGE:
Q: What events? What volume?
FACTS: 10 events/min, single service, no external consumers

Q: What's fundamentally needed?
AXIOM: Async event processing with delivery guarantee

Q: What's the simplest solution?
- PostgreSQL queue table: Complexity ZERO (existing DB)
- Redis pub/sub: Complexity LOW (new service)
- Kafka: Complexity HIGH (cluster management)

MEASUREMENT: 10 events/min = 14K events/day
THRESHOLD: Kafka justified at >1K events/min (proven bottleneck)

DECISION: PostgreSQL queue table
RE-EVALUATE: IF events/min > 1000 THEN consider Redis/Kafka
```

---

## VALIDATION CHECKLIST

After completing First Principles Analysis, verify:

- [ ] **Axioms Identified**: At least 2-3 fundamental truths listed
- [ ] **Axiom Quality**: Each axiom passes 4-criteria test (self-evident, irreducible, independent, universal)
- [ ] **Assumptions Eliminated**: All inherited beliefs questioned and validated or removed
- [ ] **Facts Measured**: Observable data collected (not speculation)
- [ ] **Options Evaluated**: At least 2 alternatives compared against axioms
- [ ] **Decision Justified**: Selected solution traces back to axioms with clear reasoning
- [ ] **Re-evaluation Triggers**: Conditions for revisiting decision documented
- [ ] **KISS Validated**: Simplest solution that satisfies axioms chosen

---

## SKILL MAINTENANCE

### When to Update This Skill
- New anti-patterns discovered in project retrospectives
- Axiom library grows with domain-specific truths
- Improved templates emerge from repeated usage
- Integration with new SIA capabilities (e.g., MCP tools for fact-gathering)

### Evolution Protocol
```
OBSERVATION: First Principles analysis repetitive for common patterns
SOLUTION: Expand axiom library with project-specific fundamentals
VALIDATION: Analysis time reduction (target: <5 min for common scenarios)
```

---

## REFERENCES

- **Complete Methodology**: `core/FIRST_PRINCIPLES.md`
- **Requirements Integration**: `requirements/README.md` (PHASE 3)
- **Template**: `requirements/_templates/REQUIREMENT_TEMPLATE.md` (First Principles section)
- **Domain Analysis**: `requirements/_templates/DOMAIN_ANALYSIS_TEMPLATE.md` (Step 0)

---

**Status**: ✅ Active Skill  
**Invocation**: Manual OR auto-triggered before major decisions  
**Next**: Integrate with `/req` and `/debug` slash commands

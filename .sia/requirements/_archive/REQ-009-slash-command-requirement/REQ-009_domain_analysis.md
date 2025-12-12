# REQ-009: DOMAIN RESEARCH & ANALYSIS

**Requirement**: Slash Command para Automatización de Requirements  
**Analysis Date**: 2025-11-29  
**Analyst**: SIA (Super Intelligence Agency)

---

## RESEARCH PROTOCOL

### 1. CENTRAL QUESTION
How do VS Code `.prompt.md` files work, and what patterns should be used to create a robust `/req` command that automates the complete requirement lifecycle (capture → research → reasoning → decomposition)?

### 2. INITIAL HYPOTHESIS
The `/req` command should be implemented as a `.prompt.md` file that:
- Uses frontmatter properties (`name`, `description`, `argumentHint`) to define the command
- Accepts natural language input via argument passing
- Orchestrates sequential phases (Capture, Research, Reasoning, QUANT)
- Delegates to MCP tools (DeepWiki) for domain research
- Generates structured documents using templates from `requirements/_templates/`

**Assumed Pattern**: Sequential prompt-driven workflow with explicit activation gates.

---

## DEEPWIKI RESEARCH

### Repositories Consulted

#### microsoft/vscode
**Question**: How do VS Code chat participants and slash commands work? What is the .prompt.md file format, how are arguments passed from chat to prompts, and how do frontmatter properties like 'name' and 'description' work?

**Findings**:
```
VS Code chat participants (agents) are registered via vscode.chat.createChatParticipant(id, handler).
Slash commands can be global or participant-specific, registered via IChatSlashCommandService.

.prompt.md File Format:
- Frontmatter (YAML): name, description, argumentHint, agent, tools, model
- Body: Markdown instructions with variable references (e.g., {{<topic>}})

Argument Passing:
- Text after slash command is passed as argument
- ChatRequestParser identifies ChatRequestSlashPromptPart
- Variable references like {{<argumentHint>}} are replaced with user input

Key Properties:
- name: Defines slash command (e.g., /myprompt)
- description: Explains what the prompt does (shown in autocomplete)
- argumentHint: Describes expected input (e.g., "<topic>")
- agent: Specifies which agent processes the prompt (e.g., "ask")
```

**Conclusions**:
- ✅ `.prompt.md` files are the correct approach for custom slash commands
- ✅ Frontmatter `name` property defines the command invocation (`/req`)
- ✅ Arguments are passed via variable references in prompt body
- ✅ `description` is shown in VS Code autocomplete (must be clear and actionable)
- ✅ No programmatic registration needed (declarative approach via file)

---

#### google/adk-python
**Question**: What are best practices for extracting invariants and constraints from natural language requirements?

**Findings**:
```
ADK doesn't provide formal methods (Alloy/TLA+) for invariant extraction.
However, it demonstrates constraint application patterns:

1. Natural Language Instructions: LlmAgent.instruction defines constraints
2. Tool Parameter Constraints: Enum constraints on tool parameters (e.g., TransferToAgentTool)
3. Guardrails: before_model_callback for policy enforcement
4. Evaluation Criteria: Post-hoc invariant checking (HallucinationsCriterion, ToolTrajectoryCriterion)

Approach: Constraints expressed via natural language instructions + programmatic validation,
not formal mathematical logic transformation.
```

**Conclusions**:
- ✅ LLM-based constraint extraction via structured prompting (not formal methods)
- ✅ Use natural language patterns to identify domain entities and their relationships
- ✅ Extract invariants through:
  1. Entity identification (nouns → domain objects)
  2. Relationship mapping (verbs → associations, constraints)
  3. Quantifier detection (always, never, at least → ∀, ∄, ≥)
  4. State validation (conditions → logical predicates)
- ✅ Apply guardrails via prompt instructions (e.g., "MUST identify at least 2 invariants")

---

## CURRENT TECH STACK ANALYSIS

### Relevant Existing Components

#### Slash Commands System
**Location**: `.sia/prompts/*.prompt.md`, `templates/prompts/*.prompt.md`  
**Current Pattern**: Declarative `.prompt.md` files with frontmatter + markdown instructions  
**Reusable**: YES  
**Modification Needed**: None - `/req` follows existing pattern

**Examples Analyzed**:
- `activate.prompt.md`: Multi-step bootstrap sequence, activation gate
- `quant.prompt.md`: Template-based document generation
- `sync.prompt.md`: Complex protocol with tool invocation

**Pattern Observed**:
```markdown
---
name: commandname
description: "Clear description for autocomplete"
---

**PROTOCOL:**
1. Step 1
2. Step 2

**MCP SOURCES:** {relevant tools}
**PRINCIPLES:** DDD | SOLID | KISS
```

#### Requirements Management System
**Location**: `requirements/README.md`, `requirements/_templates/`  
**Current Pattern**: Phase-based workflow (Capture → Research → Reasoning → QUANT → Execution)  
**Reusable**: YES  
**Modification Needed**: `/req` automates what is currently manual

**Templates Available**:
- `REQUIREMENT_TEMPLATE.md`: Initial capture structure
- `DOMAIN_ANALYSIS_TEMPLATE.md`: Research documentation
- `QUANT_BREAKDOWN_TEMPLATE.md`: Task decomposition

#### MCP Integration
**Location**: `mcp_servers/`, copilot-instructions.md  
**Current Pattern**: DeepWiki for GitHub repo research, Playwright for docs  
**Reusable**: YES  
**Tools to Invoke**:
- `mcp_deepwiki_ask_question(repoName, question)`
- `mcp_deepwiki_read_wiki_structure(repoName)`

---

## ARCHITECTURAL DECISIONS

### Chosen Implementation Pattern
**Pattern**: Declarative `.prompt.md` file with embedded multi-phase protocol

**Structure**:
```markdown
---
name: req
description: "Create and decompose requirement with automated domain research"
argumentHint: "<requirement description>"
---

# SLASH COMMAND: /req

## MISSION
Automate requirement lifecycle from natural language input.

## PROTOCOL
1. Validate input (ask clarifying questions if vague)
2. Generate REQ-ID (auto-increment)
3. Execute Phase 1: Capture (use REQUIREMENT_TEMPLATE.md)
4. Execute Phase 2: Domain Research (invoke MCP DeepWiki)
5. Execute Phase 3: Automated Reasoning (extract invariants)
6. Execute Phase 4: QUANT Decomposition (use QUANT_BREAKDOWN_TEMPLATE.md)
7. Update NEXT_SESSION.md
8. Generate SPR report

## MCP SOURCES
- mcp_deepwiki_ask_question (domain research)

## PRINCIPLES
- Research First: ALWAYS invoke MCP before implementation decisions
- DDD: Requirements are meta-system entities
- SOLID: Single Responsibility (orchestrate, don't implement)
- KISS: Use existing templates, no custom tooling
```

**Justification**:
- **DDD**: 
  - Bounded Context: SIA Meta-Framework (not target project domain)
  - Aggregate: Requirement (REQ-ID) with child documents (domain_analysis, quant_breakdown)
  - Value Objects: Invariants, Acceptance Criteria
  - Repository: File system (`.sia/requirements/REQ-{ID}/`)
  
- **SOLID**:
  - **Single Responsibility**: Command orchestrates phases, delegates to templates and MCP tools
  - **Open/Closed**: Extensible (add new phases without modifying command structure)
  - **Dependency Inversion**: Depends on abstractions (templates, MCP interface), not concrete implementations
  
- **KISS**:
  - Reuses existing templates (no duplication)
  - Leverages MCP tools (no custom web scraping)
  - File-based approach (no database, no complex state)
  - Sequential execution (no complex orchestration logic)
  
- **Clean Code**:
  - Self-documenting structure (protocol steps are explicit)
  - Separation of concerns (each phase has clear responsibility)
  - Traceable (user input → REQ-ID → documents → NEXT_SESSION)

### Alternatives Considered and Discarded

#### Alternative 1: Programmatic VS Code Extension
**Discarded because**:
- ❌ Violates KISS (adds complexity: TypeScript build, extension packaging)
- ❌ Violates Zero-Config philosophy (users must install extension)
- ❌ Breaks distribution model (requires npm publish, version management)
- ❌ Maintenance burden (API changes in VS Code require updates)
- ✅ `.prompt.md` is declarative, zero-install, version-controlled

#### Alternative 2: External Python Script (e.g., `create_req.py`)
**Discarded because**:
- ❌ Breaks user flow (must exit VS Code chat, run CLI, return to chat)
- ❌ No integration with MCP tools (would need separate MCP client)
- ❌ Duplicates slash command pattern (SIA already uses prompts)
- ✅ `.prompt.md` keeps workflow in VS Code Copilot Chat

#### Alternative 3: Interactive Multi-Turn Conversation (No Templates)
**Discarded because**:
- ❌ Violates DRY (prompt would duplicate template structure)
- ❌ Inconsistent output (no schema enforcement)
- ❌ Hard to maintain (changes require updating monolithic prompt)
- ✅ Templates provide versioning, schema validation, reusability

---

## AUTOMATED REASONING STRATEGY

### Invariant Extraction Pattern
**Approach**: Structured prompt template with linguistic analysis

**Heuristics for LLM-Based Invariant Extraction**:

1. **Entity Identification**:
   - Nouns → Domain objects (e.g., "user session" → `Session` entity)
   - Proper nouns → External systems (e.g., "Google OAuth" → `GoogleAuthProvider`)

2. **Relationship Detection**:
   - Verbs → Associations (e.g., "user creates session" → `User --creates--> Session`)
   - Ownership words (has, owns, contains) → Composition

3. **Quantifier Mapping**:
   - "always", "must", "required" → `∀` (universal quantifier)
   - "never", "cannot", "forbidden" → `∄` (negation)
   - "at least", "minimum" → `≥` (inequality)
   - "exactly", "only" → `==` (equality)
   - "unique" → `UNIQUE` constraint

4. **State Constraints**:
   - "before X, Y must be true" → Precondition (`Y ⇒ X`)
   - "after X, Y is guaranteed" → Postcondition (`X ⇒ Y`)
   - "while X, Y holds" → Invariant (`X → Y`)

**Example Application**:
```
User Input: "Implementar autenticación con Google OAuth para login"

Extracted Invariants:
- ∀ user ∈ Users: user.email IS UNIQUE
- ∀ token ∈ OAuthTokens: token.expiry > NOW
- ∀ session ∈ ActiveSessions: session.user_id ∈ AuthenticatedUsers
- GoogleOAuthProvider.client_id ≠ NULL
- Token refresh MUST occur before expiry - 5min
```

**Validation Guardrails** (Embedded in Prompt):
- "If input does not specify entities, ASK for clarification"
- "Extract AT LEAST 2 invariants (or explain why none exist)"
- "Express invariants using mathematical notation (∀, ∃, ⇒, ==, ≠)"

---

## TECHNICAL IMPLEMENTATION DETAILS

### File Locations
```
templates/prompts/req.prompt.md         # Source of truth (framework)
.sia/prompts/req.prompt.md              # Installed copy (project)
```

### Auto-Increment Logic for REQ-ID
**Pattern**: Scan `.sia/requirements/` directory, extract numeric IDs, increment max

**Pseudo-code in Prompt**:
```
1. List directories matching pattern "REQ-\d+"
2. Extract numeric IDs: [1, 2, 3, 5, 9] (assuming REQ-001, REQ-002, etc.)
3. Compute max: 9
4. New ID: 9 + 1 = 10
5. Format: REQ-010 (zero-padded to 3 digits)
```

**Edge Case**: First requirement → Use REQ-001

### SPR Compression Application
**When**: After generating domain_analysis.md and quant_breakdown.md  
**How**: Invoke `/spr` internally or apply compression heuristics:
- Convert paragraphs → bullet points
- Remove redundant phrases
- Use abbreviations for repeated terms
- Inline references instead of duplicating content
- Target: 70-80% token reduction

### Activation Gate Implementation
**Pattern**: Present plan, wait for `/continue`

**Protocol**:
```
1. Validate user input (ask questions if vague)
2. Present plan:
   ```
   📋 PLAN FOR REQ-{ID}:
   1. Research: {repos to consult}
   2. Invariants: {expected count}
   3. QUANT Tasks: {estimated count, estimated hours}
   
   Confirm with /continue to proceed.
   ```
3. HALT execution until user approves
4. On /continue → Execute full pipeline
```

---

## RISKS AND MITIGATIONS

### Risk 1: User Provides Vague Input
**Example**: "/req + 'Mejorar sistema'"  
**Mitigation**: Embedded clarification protocol in prompt
```
IF input lacks:
  - Specific component/feature → ASK "What component?"
  - Success criteria → ASK "What defines 'improved'?"
  - Bounded context → ASK "Which part of the system?"
```

### Risk 2: MCP DeepWiki Failure
**Example**: Rate limit, network error  
**Mitigation**: 
- Catch error, document in domain_analysis.md
- Mark section with `⚠️ RESEARCH INCOMPLETE - {error reason}`
- Continue with best-effort analysis
- Suggest manual research steps

### Risk 3: Duplicate Requirement Title
**Example**: User creates "Google OAuth" twice  
**Mitigation**:
- Before creating REQ-ID, scan existing requirements for similar titles
- Use semantic similarity (if available) or keyword matching
- If match found → ASK: "REQ-005 already covers 'Google OAuth'. Create new requirement, or update existing?"

### Risk 4: Complex Multi-Context Requirement
**Example**: "Implement auth + dashboard + notifications"  
**Mitigation**:
- Detect multiple bounded contexts via entity analysis
- SUGGEST splitting: "This requirement spans 3 bounded contexts. Recommended: Create REQ-010 (Auth), REQ-011 (Dashboard), REQ-012 (Notifications)"
- Await user decision before proceeding

---

## VALIDATION STRATEGY

### Pre-Implementation Validation
- ✅ Read `sia/docs/SLASH_COMMANDS.md` (understand VS Code prompts API)
- ✅ Analyze existing commands (`activate.prompt.md`, `quant.prompt.md`)
- ✅ Research VS Code chat prompts with MCP DeepWiki (`microsoft/vscode`)

### Post-Implementation Validation
**Manual Testing Scenarios**:

1. **Simple Clear Input**:
   ```
   /req + "Add health check endpoint to API"
   
   Expected Output:
   ✅ REQ-010 created
   📚 Research: fastapi/fastapi (health check patterns)
   📋 3 invariants extracted
   📝 3 QUANT tasks generated
   🎯 Next: /activate + "Implementar REQ-010 QUANT-001"
   ```

2. **Vague Input**:
   ```
   /req + "Improve performance"
   
   Expected Output:
   ❓ CLARIFICATION NEEDED:
   1. Which component? (API, DB, Frontend)
   2. What metric? (latency, throughput, memory)
   3. Current vs target threshold?
   ```

3. **Multi-Context Input**:
   ```
   /req + "Add auth and dashboard"
   
   Expected Output:
   ⚠️ MULTI-CONTEXT DETECTED
   Suggested split:
   - REQ-010: Authentication system
   - REQ-011: Dashboard implementation
   Proceed with split or single requirement?
   ```

4. **MCP Failure Simulation**:
   ```
   [Simulate DeepWiki error]
   
   Expected Output:
   ⚠️ RESEARCH INCOMPLETE
   MCP DeepWiki error: [reason]
   Domain analysis created with best-effort approach
   Manual research recommended: [suggested repos/docs]
   ```

### Verification Checklist
- [ ] `/req` appears in VS Code autocomplete
- [ ] Description shown in autocomplete is clear
- [ ] Argument hint (`<requirement description>`) visible
- [ ] REQ-ID auto-increments correctly
- [ ] All 3 files generated (REQ-{ID}.md, domain_analysis, quant_breakdown)
- [ ] MCP DeepWiki invoked at least once
- [ ] Invariants use mathematical notation (∀, ∃, ⇒)
- [ ] NEXT_SESSION.md updated with one-liner
- [ ] SPR compression applied (token count reduced)
- [ ] Error handling graceful (vague input, MCP failure, duplicates)

---

## FINAL RECOMMENDATIONS

### Implementation Checklist
1. ✅ Create `templates/prompts/req.prompt.md` (source of truth)
2. ✅ Copy to `.sia/prompts/req.prompt.md` (installed version)
3. ✅ Embed complete protocol (Capture → Research → Reasoning → QUANT)
4. ✅ Include activation gate ("Present plan, wait for /continue")
5. ✅ Add MCP DeepWiki invocation (mandatory research step)
6. ✅ Embed invariant extraction heuristics (entity, relationship, quantifier detection)
7. ✅ Add error handling (vague input, MCP failure, duplicates, multi-context)
8. ✅ Update `sia/docs/SLASH_COMMANDS.md` with `/req` entry
9. ✅ Update `.sia/NEXT_SESSION.md` with completion status

### Documentation Updates Required
- `sia/docs/SLASH_COMMANDS.md`: Add `/req` to command table + detailed section
- `requirements/README.md`: Add note about `/req` automation (optional manual workflow still supported)
- `CHANGELOG.md`: Document new feature in next version

### Future Enhancements (Out of Scope)
- `/req --edit REQ-{ID}`: Edit existing requirement
- `/req --archive REQ-{ID}`: Archive completed requirement
- `/req --merge REQ-{ID1} REQ-{ID2}`: Merge related requirements
- `/req --export`: Export all requirements to PDF/Markdown

---

**Analysis Status**: ✅ COMPLETED  
**Next Step**: Implement `req.prompt.md` with findings from this analysis  
**Estimated Implementation Time**: 2-3h (prompt creation + testing + documentation)

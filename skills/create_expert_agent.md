# Skill: Expert Agent Creation

## Overview

**Purpose**: Systematically create domain-specialist agents using empirical evidence from MCP Deepwiki research

**Input**: User request for expert agent (e.g., "Create agent for Microsoft Suite migration from Google Drive")

**Output**: Production-ready SPR agent with LSA, MCP integrations, workflows, examples, and documentation

**Methodology**: Evidence-based knowledge synthesis → SPR compression → LSA cognitive priming

---

## Workflow: 7-Phase Agent Creation

### Phase 0: Request Analysis (5 min)

**Goal**: Extract domain, specialization, and user pain points

**Steps**:
1. **Parse User Request**:
   ```markdown
   Input: "Create expert agent for [DOMAIN] to solve [PROBLEM]"
   
   Extract:
   - Domain: [e.g., Microsoft 365, Kubernetes, AWS, Django]
   - Specialization: [e.g., SharePoint, networking, IAM, ORM]
   - Problem: [e.g., migration from X, configuration issues, optimization]
   - Context: [e.g., team size, existing tools, constraints]
   ```

2. **Identify Knowledge Gaps**:
   - What do we NOT know about this domain?
   - What are the current best practices?
   - What tools/MCPs exist for this domain?

3. **Formulate Research Questions**:
   ```markdown
   Example (Microsoft Suite):
   Q1: What MCP servers exist for Microsoft 365 / Graph API / SharePoint?
   Q2: What are the core SharePoint configuration patterns?
   Q3: What are common migration strategies from Google Workspace?
   Q4: What are the anti-patterns and pitfalls?
   ```

**Output**: Research brief (domain + questions + expected MCP sources)

---

### Phase 1: MCP Research (15-20 min)

**Goal**: Gather empirical evidence from authoritative sources via Deepwiki

**Protocol**:

#### Step 1.1: Identify Target Repositories
```markdown
Domain: Microsoft 365
Potential Repos:
- modelcontextprotocol/servers (MCP ecosystem)
- microsoft/microsoft-graph-docs (Graph API)
- SharePoint/sp-dev-docs (SharePoint patterns)
- pnp/pnpjs (Community patterns)
```

#### Step 1.2: Execute Deepwiki Queries

**Query Template**:
```markdown
## Question Formulation (Specific + Contextual)

**Context**: Creating agent for [DOMAIN] with focus on [SPECIALIZATION]
**Need**: Understand [SPECIFIC_ASPECT] to provide actionable guidance
**Question**: [PRECISE_QUERY with constraints and expected output format]
**Expected Output**: [Code snippets | Patterns | Configuration examples | Tool list]

## Example ✅ GOOD
Context: Creating Microsoft 365 migration agent
Need: Identify available MCP servers for automation
Question: What MCP servers are available for Microsoft documentation, 
          Microsoft Graph API, SharePoint, or Office 365 integration? 
          Include authentication requirements and tool capabilities.
Expected Output: List of MCPs with provider, capabilities, setup instructions

## Example ❌ BAD
Question: Tell me about Microsoft 365
Expected Output: Everything
→ Result: Too broad, unusable context dump
```

**Execution**:
```python
# Query 1: MCP Ecosystem Discovery
mcp_deepwiki_ask_question(
    repoName="modelcontextprotocol/servers",
    question="What MCP servers are available for [DOMAIN]? Include capabilities, authentication, and setup."
)

# Query 2: Domain Best Practices
mcp_deepwiki_ask_question(
    repoName="[domain-specific-repo]",
    question="What are the recommended patterns for [SPECIFIC_TASK]? Include code examples and anti-patterns."
)

# Query 3: Common Problems & Solutions
mcp_deepwiki_ask_question(
    repoName="[community-repo]",
    question="What are common [PROBLEM] issues and their solutions? Include diagnostic steps."
)
```

#### Step 1.3: Synthesize Research Findings

**Template**:
```markdown
## Research Summary

### MCP Servers Identified
| Server | Provider | Capabilities | Priority | Setup Complexity |
|--------|----------|--------------|----------|------------------|
| [name] | [org]    | [features]   | ⭐⭐⭐    | Low/Medium/High  |

### Core Patterns Discovered
1. [Pattern Name]: [Brief description + use case]
2. [Pattern Name]: [Brief description + use case]

### Anti-Patterns (What NOT to do)
- ❌ [Anti-pattern 1]: [Why it fails]
- ❌ [Anti-pattern 2]: [Why it fails]

### Common Problem Categories
1. [Problem Type]: [Diagnostic approach + solution template]
2. [Problem Type]: [Diagnostic approach + solution template]

### Code Examples Extracted
- [Scenario 1]: [Language/tool + code snippet reference]
- [Scenario 2]: [Language/tool + code snippet reference]
```

**Validation**:
- ✅ At least 3 MCP servers identified (or explicit "none available")
- ✅ Minimum 5 patterns documented
- ✅ Minimum 3 anti-patterns identified
- ✅ At least 2 code examples per major use case

**Output**: Research synthesis document (markdown, ~2k tokens)

---

### Phase 2: Agent Architecture Design (10 min)

**Goal**: Structure agent knowledge using SPR + LSA

#### Step 2.1: Latent Space Activation (LSA) Design

**Purpose**: Pre-prime LLM cognitive patterns for instant domain expertise

**Template**:
```yaml
## LATENT SPACE ACTIVATION (LSA)

**Cognitive Priming Vectors**:
- [Key domain concept 1] (e.g., SharePoint architecture)
- [Key domain concept 2] (e.g., Microsoft Graph API patterns)
- [Key domain concept 3] (e.g., Migration workflows)
- [Problem-solving pattern] (e.g., Permission troubleshooting logic)

**Domain Expertise Activation**:
```yaml
[domain_category]:
  core_concepts: [list_of_fundamentals]
  advanced_topics: [list_of_specialized_knowledge]
  tools_ecosystem: [list_of_relevant_tools]
  
[specialization_category]:
  architecture: [architectural_patterns]
  workflows: [common_workflows]
  configuration: [key_configurations]
  
[problem_category]:
  common_issues: [issue_types]
  diagnostic_patterns: [troubleshooting_flows]
  solutions: [solution_templates]
```

**Mental Models**:
- [Core analogy 1]: [Simple explanation of complex system]
- [Core analogy 2]: [Framework understanding]

**Problem-Solving Patterns**:
- [Issue Type] → [Diagnostic Step 1] → [Diagnostic Step 2] → [Solution Template]
```

**Guidelines**:
- Use research findings to populate LSA sections
- Extract mental models from documentation (analogies, comparisons)
- Identify problem-solving patterns from issue trackers, forums, docs

#### Step 2.2: SPR Structure Definition

**Sections** (based on `templates/PROJECT_SPR.template.md` adapted for agents):

```markdown
## LATENT SPACE ACTIVATION (LSA)
[Cognitive priming - see above]

## CORE MISSION
[One-sentence agent identity + primary value proposition]

## EXPERTISE
[Bullet-point knowledge areas - high density, no fluff]

### [Category 1]
- [Subconcept 1]: [Tools/patterns]
- [Subconcept 2]: [Tools/patterns]

### [Category 2]
...

## MCP INTEGRATION
[Available MCP servers, tools, usage protocol]

### Available MCP Servers
[Table from research]

### MCP Tool Usage Protocol
[When to use each MCP, fallback strategies]

## WORKFLOW: [PRIMARY_USE_CASE]
[Step-by-step problem-solving process]

### Phase 1: [Analysis]
### Phase 2: [Research]
### Phase 3: [Solution Design]
### Phase 4: [Implementation]
### Phase 5: [Verification]

## [DOMAIN-SPECIFIC SECTIONS]
[e.g., Migration Playbook, Configuration Patterns, API Integration]

## ANTI-PATTERNS
[What NOT to do - from research]

## MENTAL MODEL COMPRESSION
**Essence**: [2-3 sentence ultra-compressed system understanding]

**Critical Path**: [Step-by-step primary workflow]

**Architecture DNA**: [Core pattern in one sentence]

**Key Invariants**:
- [Always-true constraint 1]
- [Always-true constraint 2]

## OUTPUT FORMAT (SPR)
[Structured response template for agent answers]

## DELEGATION PROTOCOL
[When to escalate to other agents]

## VERIFICATION CHECKLIST
[Quality gates before providing response]

---

**Agent Version**: 1.0.0
**Specialization**: [Domain]
**MCP Dependencies**: [List]
**Last Updated**: [Date]
**Status**: ✅ Production Ready
```

**Token Budget**:
- LSA: ~500 tokens
- Core Mission: ~50 tokens
- Expertise: ~1200 tokens
- MCP Integration: ~400 tokens
- Workflows: ~800 tokens
- Domain-Specific: ~600 tokens
- Anti-Patterns: ~300 tokens
- Mental Model: ~200 tokens
- Output Format: ~250 tokens
- Misc: ~200 tokens
- **Total**: ~4500-5000 tokens (MAX)

**Output**: Agent structure outline with token allocation

---

### Phase 3: Knowledge Compression (15 min)

**Goal**: Transform research into high-density SPR content

#### Step 3.1: Expertise Section

**Rule**: 1 concept = 1 line. No explanatory paragraphs.

**Process**:
```markdown
Research Finding:
"SharePoint uses a hierarchical permission model where sites inherit 
from site collections, and libraries can break inheritance to create 
unique permissions. Best practice is to use SharePoint groups mapped 
to Azure AD groups rather than individual user permissions."

SPR Compression ✅:
- **Permissions**: Inheritance (site→library), SharePoint groups→Entra groups, avoid individual users

Research Finding:
"Microsoft Graph API supports batching up to 20 requests in a single 
call to the /$batch endpoint, which significantly reduces network 
overhead and improves performance for bulk operations."

SPR Compression ✅:
- **Graph API**: $batch endpoint (max 20 requests), reduces latency, use for bulk ops
```

**Technique**: Extract **actionable keywords** + **constraints** + **use cases**

#### Step 3.2: Workflow Section

**Rule**: Step-by-step, file/tool references, decision points

**Template**:
```markdown
## WORKFLOW: [Use Case Name]

### Phase 1: [Name]

**Questions to Ask**:
1. [Clarifying question 1]
2. [Clarifying question 2]

**Diagnostic Steps**:
```markdown
1. **[Action]**:
   - MCP: `mcp_[server]_[tool](...)`
   - Manual: [UI/CLI steps]
   - Check: [What to verify]

2. **[Action]**:
   ...
```

### Phase 2: Research (MCP-First)

**Template**:
```markdown
## Problem Context
[1 sentence]

## MCP Query Strategy
1. mcp_[tool]_get_documentation(...)
2. mcp_deepwiki_ask_question(...)

## Expected Insights
- [Type of information needed]
```

### Phase 3: Solution Design

**Output Format**:
```markdown
## Root Cause
[Technical explanation]

## Solution Strategy
1. [Step with verification]
2. [Step with rollback plan]

## Implementation

### Option A: MCP Tools (Automated)
[Commands]

### Option B: [Alternative Method]
[Steps]

## Verification
- ✅ [Check 1]
- ✅ [Check 2]
```
```

#### Step 3.3: Anti-Patterns Extraction

**Source**: Research findings + documentation warnings

**Format**:
```markdown
## ANTI-PATTERNS

### [Category] Anti-Patterns

❌ **[Bad Practice]** → [Why it fails]  
✅ [Correct approach]

❌ **[Bad Practice]** → [Consequence]  
✅ [Best practice]
```

**Example**:
```markdown
### SharePoint Anti-Patterns

❌ **Unique permissions on every file** → Unmaintainable, security risk  
✅ Use folders with inherited permissions + SharePoint groups

❌ **Overly complex folder hierarchies (>5 levels)** → Poor UX, search inefficiency  
✅ Flatten structure, use metadata + views for organization
```

#### Step 3.4: Mental Model Compression

**Goal**: Compress entire domain into 2-3 sentences

**Technique**: Identify **core flow** + **key relationships** + **invariants**

**Template**:
```markdown
## MENTAL MODEL COMPRESSION

**Essence**: [Input] → [Transformation 1] → [Transformation 2] → [Output]. 
[Architecture pattern]. [Key constraint].

**Example (Microsoft 365)**:
> Entra ID (identity) → SharePoint (structured content) + OneDrive (personal) 
> + Teams (conversations) → Graph API (unified access). 
> Permissions flow from Entra groups → SharePoint groups → resources.

**Critical Path**: 
1. **[Primary Journey]**: [Step 1] → [Step 2] → [Step 3]
2. **[Secondary Flow]**: [Alternative path]

**Architecture DNA**: [Core pattern in one sentence]

**Example**:
> Domain (pure logic) ← Application (use cases) ← Infrastructure (external) 
> ← API (interface). No upward dependencies.

**Key Invariants**:
- [Invariant 1]: [Always true]
- [Invariant 2]: [Never changes]
- [Invariant 3]: [Technical constraint]
```

**Output**: Complete agent file (`agents/[domain]_specialist.md`)

---

### Phase 4: Usage Examples Creation (20 min)

**Goal**: Demonstrate agent capabilities with real-world scenarios

#### Step 4.1: Scenario Identification

**Criteria**:
- Cover 4-6 common use cases from research
- Range from simple (troubleshooting) to complex (migration)
- Include MCP tool usage where applicable
- Provide code examples in multiple approaches

**Template**:
```markdown
# [Agent Name] - Usage Examples

## Example 1: [Simple Troubleshooting]

### User Request
```
"[User's actual question]"
```

### Agent Response (Abbreviated)

```markdown
## PROBLEM ANALYSIS
[Root cause + affected component]

## MCP RESEARCH
1. mcp_[tool](...) → [Finding]

## SOLUTION DESIGN
[Step-by-step with verification]

### Implementation

#### Option A: MCP Tools
[Code/commands]

#### Option B: Manual
[UI steps]

## VERIFICATION
- ✅ [Check 1]
```

## Example 2: [Complex Use Case]
...
```

#### Step 4.2: Code Examples

**Requirements**:
- Multiple languages/tools where applicable
- Include error handling
- Add comments for clarity
- Provide both automated and manual approaches

**Example Structure**:
```markdown
### Implementation (Python + Graph API)

```python
import requests
from typing import List, Dict

def solve_problem(params: Dict):
    """
    [Brief description]
    
    Args:
        params: [Parameter description]
    
    Returns:
        [Return value description]
    """
    # Step 1: [Action]
    result = api_call(...)
    
    # Step 2: [Processing]
    processed = transform(result)
    
    # Step 3: [Verification]
    if verify(processed):
        return processed
    else:
        raise Exception("Validation failed")
```

### Implementation (PowerShell + PnP)

```powershell
# [Brief description]
Connect-PnPOnline -Url "..." -Interactive

# Step 1: [Action]
$result = Get-PnP...

# Step 2: [Verification]
if ($result) {
    Write-Host "✅ Success"
}
```
```

#### Step 4.3: MCP Setup Guide

**Include**:
```markdown
## MCP Setup Requirements

### Required MCP Servers

1. **[Server Name]** ([Provider])
   - Install: [Command or link]
   - Auth: [Authentication method]
   - Permissions: [Required permissions]

### Authentication Setup

```bash
# Step-by-step configuration
1. [Platform setup - e.g., Azure app registration]
2. [Obtain credentials]
3. [Configure MCP server]
```

**Configure MCP** (example for Claude Desktop):
```json
{
  "mcpServers": {
    "[server-name]": {
      "command": "npx",
      "args": ["[package]"],
      "env": {
        "KEY": "value"
      }
    }
  }
}
```
```

**Output**: Examples file (`agents/[domain]_specialist_examples.md`)

---

### Phase 5: Catalog Integration (5 min)

**Goal**: Update `agents/README.md` with new agent entry

#### Step 5.1: Add Catalog Entry

**Template**:
```markdown
### `[domain]_specialist.md` - [Title] ✨ NEW
**Domain**: [Primary domain]  
**Specialization**: [Specific expertise areas]  
**MCP Dependencies**: [List of MCP servers]  
**Use When**: [Triggering conditions]

**Key Capabilities**:
- **[Capability 1]**: [Description]
- **[Capability 2]**: [Description]
- **[Capability 3]**: [Description]
- **MCP Integration**: [How MCP is used]

**Latent Space Activation (LSA)**: [Brief description of cognitive priming]

**Output Format**: [Response structure]
```

#### Step 5.2: Update Selection Guide

**Add to decision matrix**:
```markdown
| User Request | Primary Agent | Secondary Agent |
|--------------|---------------|-----------------|
| "[Trigger phrase]" | `[domain]_specialist.md` | `research_specialist.md` |
```

**Output**: Updated `agents/README.md`

---

### Phase 6: Documentation Updates (5 min)

**Goal**: Maintain traceability and versioning

#### Step 6.1: Update CHANGELOG.md

**Template**:
```markdown
## [Unreleased]

### Added
- **[Domain] Specialist Agent** (`agents/[domain]_specialist.md`)
  - [Key feature 1]
  - [Key feature 2]
  - [Key feature 3]
  - MCP integrations: [List]
  - Latent Space Activation (LSA) - [Brief description]
  - SPR-compressed format (<5k tokens)
- **Agent [Domain] Examples** (`agents/[domain]_specialist_examples.md`)
  - [Number] practical scenarios
  - [Tools/languages] code examples
  - MCP setup guide
```

#### Step 6.2: Create Summary Document (Optional)

**For complex agents, create**:
```markdown
# [Domain] Agent - Executive Summary

## Overview
[Brief description]

## Deliverables
1. Core Agent
2. Usage Examples
3. Documentation Updates

## Research Highlights
- MCP servers identified
- Patterns documented
- Anti-patterns discovered

## Business Value
[ROI estimate, problem solved]
```

**Output**: Updated CHANGELOG.md + optional summary

---

### Phase 7: Quality Validation (10 min)

**Goal**: Ensure agent meets production standards

#### Validation Checklist

**Agent File** (`[domain]_specialist.md`):
- ✅ LSA section present (cognitive priming vectors + domain activation)
- ✅ Core Mission (<100 words, clear value proposition)
- ✅ Expertise section (high-density bullets, no paragraphs)
- ✅ MCP Integration section (servers + usage protocol + fallback)
- ✅ Primary workflow documented (step-by-step)
- ✅ Anti-patterns section (minimum 3 entries)
- ✅ Mental Model Compression (essence + critical path + invariants)
- ✅ Output Format template (structured response)
- ✅ Verification checklist (quality gates)
- ✅ Token count <5000 tokens
- ✅ Version number and date present

**Examples File** (`[domain]_specialist_examples.md`):
- ✅ 4+ real-world scenarios
- ✅ Code examples in multiple languages/tools
- ✅ MCP tool invocations demonstrated
- ✅ Manual fallback approaches included
- ✅ Verification steps for each scenario
- ✅ MCP setup guide with authentication
- ✅ How to invoke section

**Documentation**:
- ✅ `agents/README.md` updated (catalog entry + selection guide)
- ✅ `CHANGELOG.md` updated ([Unreleased] section)
- ✅ Summary document created (if complex agent)

**Testing** (Manual):
1. Read agent file → Does LSA make sense for domain?
2. Check expertise → Is it actionable and high-density?
3. Review workflow → Can it be followed step-by-step?
4. Validate examples → Can they be executed as-written?
5. Test MCP references → Do servers exist and are accessible?

**Output**: Production-ready agent ✅

---

## Success Criteria

**Quantitative**:
- ✅ Agent file: 4500-5000 tokens (SPR compression)
- ✅ Examples file: 4+ scenarios with executable code
- ✅ MCP research: 3+ servers identified or "none available" documented
- ✅ Patterns: 5+ documented, 3+ anti-patterns
- ✅ Time: Total creation <90 minutes

**Qualitative**:
- ✅ Agent provides immediate value (answers domain questions accurately)
- ✅ LSA activates relevant cognitive patterns (feels "expert-like")
- ✅ MCP integration is practical (tools are accessible and useful)
- ✅ Examples are executable (copy-paste-run works)
- ✅ Documentation is discoverable (catalog entry is clear)

---

## Anti-Patterns (Agent Creation)

❌ **No MCP research** → Agent lacks automation capabilities  
✅ Execute Deepwiki queries, identify MCP ecosystem

❌ **Verbose expertise section** → Token bloat, low density  
✅ Use bullets, 1 concept = 1 line, actionable keywords only

❌ **Generic workflows** → Not domain-specific  
✅ Extract from research, include tool/file references

❌ **No LSA section** → Missed cognitive priming opportunity  
✅ Always include LSA with domain expertise activation

❌ **Untested examples** → Broken code, frustrated users  
✅ Validate examples are executable (at least conceptually)

❌ **Token count >6000** → Excessive context, violates SPR  
✅ Compress ruthlessly, target 4500-5000 tokens

❌ **No anti-patterns** → Users repeat mistakes  
✅ Extract from research, documentation, issue trackers

❌ **Missing MCP fallback** → Agent fails if MCP unavailable  
✅ Always provide manual alternatives (UI, CLI, API)

---

## Example: Microsoft Suite Agent Creation

### Phase 0: Request Analysis
```
Input: "Create agent for Microsoft Suite migration from Google Drive, 
        focus on SharePoint configuration issues"

Extract:
- Domain: Microsoft 365
- Specialization: SharePoint configuration, migrations
- Problem: Google Workspace → M365 migration + SharePoint troubleshooting
- Context: Team unfamiliar with SharePoint architecture
```

### Phase 1: MCP Research
```python
# Query 1: MCP Ecosystem
mcp_deepwiki_ask_question(
    repoName="modelcontextprotocol/servers",
    question="What MCP servers are available for Microsoft 365, SharePoint, Graph API?"
)
# Result: 11 MCPs found, 3 prioritized

# Query 2: SharePoint Patterns
mcp_deepwiki_ask_question(
    repoName="SharePoint/sp-dev-docs",
    question="What are best practices for SharePoint permissions and content types?"
)
# Result: Inheritance patterns, group-based permissions, content type hub

# Query 3: Migration Strategies
mcp_deepwiki_ask_question(
    repoName="microsoft/microsoft-graph-docs",
    question="What are recommended patterns for migrating from Google Drive to SharePoint?"
)
# Result: Phased approach, metadata mapping, Microsoft Migration Manager
```

### Phase 2: Architecture Design
```yaml
LSA:
  cognitive_priming:
    - SharePoint architecture (hub sites, permissions, content types)
    - Microsoft Graph API (batching, delta queries)
    - Migration workflows (Google → M365)
    
  domain_expertise:
    microsoft_365:
      core: [SharePoint, OneDrive, Teams, Graph API]
      governance: [retention, DLP, sensitivity labels]
    
  mental_models:
    - SharePoint = structured collaboration (sites + metadata + workflows)
    - Graph = unified API gateway
```

### Phase 3: Knowledge Compression
```markdown
## EXPERTISE

### SharePoint Core
- **Architecture**: Hub sites, site collections, modern sites, libraries, lists
- **Permissions**: Inheritance (site→library), SharePoint groups→Entra groups
- **Content Types**: Custom types, site columns, metadata, term store
- **Search**: Managed properties, crawled properties, search schema
```

### Phase 4: Examples
```markdown
## Example 1: SharePoint Permission Troubleshooting
[4 scenarios created with MCP tools, PowerShell, Graph API]

## Example 2: Google Drive → SharePoint Migration
[500GB phased migration playbook with code]
```

### Phase 5-7: Integration & Validation
- Updated `agents/README.md` with catalog entry
- Updated `CHANGELOG.md` with [Unreleased] section
- Validated all checklists ✅
- **Result**: Production-ready agent in 75 minutes

---

## Tools & Resources

### Required Tools
- **MCP Deepwiki**: Primary research tool
- **Text Editor**: Markdown editing
- **Token Counter**: Verify SPR compression (<5k tokens)

### Recommended Reading
- `core/CONCEPTS.md` - SPR definition, LSA patterns
- `templates/PROJECT_SPR.template.md` - SPR structure
- `agents/README.md` - Agent standards, selection guide
- `CONTRIBUTING.md` - SPR coding standards

### Validation Scripts
```bash
# Token count
wc -w agents/[domain]_specialist.md
# Target: ~1000 words = ~4500 tokens

# Checklist automation (future)
uv run python skills/validate_agent.py agents/[domain]_specialist.md
```

---

## Continuous Improvement

**After Each Agent Creation**:
1. Document time spent per phase (optimize bottlenecks)
2. Note MCP servers discovered (expand ecosystem knowledge)
3. Identify reusable patterns (add to this skill)
4. Update anti-patterns (learn from mistakes)

**Agent Evolution**:
- **Minor updates** (v1.1): Add MCP servers, new examples, bug fixes
- **Major updates** (v2.0): Domain paradigm shift, breaking LSA changes

**Skill Evolution**:
- Update this document with discovered patterns
- Add automation scripts (e.g., `create_agent.py` CLI tool)
- Create agent templates for common domains (cloud, databases, frontend)

---

## Appendix: LSA Design Patterns

### Pattern 1: Hierarchical Expertise Activation

```yaml
domain:
  fundamentals: [core_concepts]
  intermediate: [common_patterns]
  advanced: [edge_cases, optimizations]
```

**Use When**: Domain has clear skill progression (e.g., Kubernetes beginner → expert)

### Pattern 2: Problem-Category Activation

```yaml
problem_types:
  performance: [diagnostic_tools, optimization_patterns]
  security: [threat_models, mitigation_strategies]
  configuration: [setup_patterns, validation_methods]
```

**Use When**: Domain is problem-focused (e.g., database optimization, cloud security)

### Pattern 3: Tool-Ecosystem Activation

```yaml
tools:
  cli: [commands, flags, workflows]
  api: [endpoints, authentication, patterns]
  ui: [navigation, configuration, shortcuts]
```

**Use When**: Domain has multiple tool interfaces (e.g., AWS, Docker, Git)

### Pattern 4: Workflow-Based Activation

```yaml
workflows:
  setup: [initialization, configuration, validation]
  operation: [monitoring, maintenance, troubleshooting]
  migration: [assessment, planning, execution, validation]
```

**Use When**: Domain is process-heavy (e.g., DevOps, migrations, compliance)

---

**Skill Version**: 1.0.0  
**Created**: 2025-11-25  
**Evidence Source**: Microsoft Suite Agent creation (REF: `agents/microsoft_suite_specialist.md`)  
**Time Estimate**: 60-90 minutes (experienced), 120 minutes (first time)  
**Success Rate**: 100% (1/1 agents created using this methodology)  
**Status**: ✅ Production Ready

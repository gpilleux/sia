# SIA Agents Catalog

## Overview

This directory contains **specialized sub-agents** for the SIA framework. Each agent is a domain expert with specific capabilities, MCP integrations, and SPR-compressed knowledge.

**Invocation Pattern**: User request → SUPER_AGENT analyzes → Delegates to specialist → Specialist executes → SUPER_AGENT validates

---

## Framework Agents (Core SIA)

### `sia.md` - SIA Orchestrator
**Domain**: AI-Native architecture (DDD + ADK + TimescaleDB + Playwright)  
**Specialization**: Google ADK implementation, real-time systems, E2E testing  
**MCP Dependencies**: `mcp_deepwiki` (google/adk-python), `mcp_tiger-docs`, `mcp_playwright`  
**Use When**: Building AI agents with Google ADK, TimescaleDB integration, SSE frontends

**Key Capabilities**:
- ADK agent design (LlmAgent, Sequential, Parallel, Loop)
- TimescaleDB schema design (hypertables, aggregates, retention)
- SSE real-time communication patterns
- Playwright E2E test automation
- Docker hot-reload development workflows

---

### `repository_guardian.md` - Architecture Enforcer
**Domain**: DDD, SOLID, Clean Architecture compliance  
**Specialization**: Code quality, architectural patterns, dependency rule enforcement  
**Use When**: Architecture reviews, refactoring guidance, DDD violations detection

**Key Capabilities**:
- DDD layer separation validation
- SOLID principles enforcement
- Dependency injection patterns
- Repository pattern implementation
- Anti-corruption layer design

---

### `research_specialist.md` - Knowledge Discovery
**Domain**: Technical research, pattern discovery, documentation analysis  
**Specialization**: MCP Deepwiki queries, documentation synthesis, best practice extraction  
**MCP Dependencies**: `mcp_deepwiki`, `mcp_playwright`  
**Use When**: Investigating new frameworks, comparing solutions, gathering implementation examples

**Key Capabilities**:
- Targeted Deepwiki research protocol
- Multi-source knowledge synthesis
- Pattern extraction from documentation
- Technology comparison matrices
- Implementation example discovery

---

### `compliance_officer.md` - Requirements Manager
**Domain**: Requirements engineering, QUANT lifecycle, validation protocols  
**Specialization**: REQ-XXX tracking, acceptance criteria, phase validation  
**Use When**: Managing formal requirements, tracking project specifications

**Key Capabilities**:
- QUANT 7-phase workflow management
- Requirement decomposition
- Acceptance criteria definition
- Validation script creation
- Requirements traceability

---

### `sia_framework.md` - Framework SPR
**Domain**: SIA meta-framework knowledge (self-documentation)  
**Specialization**: Framework architecture, installer logic, auto-discovery patterns  
**Use When**: Framework development, SIA self-improvement, inception mode operations

**Key Capabilities**:
- Framework architecture understanding
- Auto-discovery protocol knowledge
- Installer behavior patterns
- Template system comprehension
- Self-evolution protocols

---

### `evolve_spr.py` - Self-Evolution Engine
**Type**: Python executable (not markdown agent)  
**Domain**: SPR generation, documentation compression, framework improvement  
**Use When**: Generating project SPRs, compressing documentation, framework meta-updates

**Key Capabilities**:
- Automated SPR generation from codebase
- 70-80% token compression
- Domain model extraction
- Architecture pattern detection
- Mental model synthesis

---

## Domain Specialist Agents (External Expertise)

### `microsoft_suite_specialist.md` - Microsoft 365 Expert ✨ NEW
**Domain**: Microsoft 365 ecosystem (SharePoint, OneDrive, Teams, Graph API)  
**Specialization**: SharePoint configuration, Google Workspace migration, Graph API integration  
**MCP Dependencies**: Lokka (authenticated ✅), MS-365-MCP (45 tools), CLI-Microsoft365 (600+ commands)  
**MCP Tools Reference**: See `microsoft_suite_specialist_mcp_tools.md` for complete catalog  
**Use When**: SharePoint troubleshooting, M365 migrations, Graph API queries, permission issues

**Key Capabilities**:
- **SharePoint Mastery**: Sites, libraries, permissions, content types, search schema
- **Migration Expertise**: Google Workspace → Microsoft 365 (Drive→OneDrive/SharePoint, permissions, metadata)
- **Microsoft Graph API**: Authentication, batching, delta queries, throttling management
- **Power Platform**: Power Automate workflows, Power Apps integration
- **Governance**: Retention policies, DLP, sensitivity labels, eDiscovery
- **MCP Integration**: Direct M365 operations via MCP tools, documentation queries via Microsoft Learn MCP

**Latent Space Activation (LSA)**: Pre-primed with SharePoint architecture, migration patterns, Graph API expertise

**Output Format**: Problem analysis → MCP research → Multi-option solution (Graph API + MCP + UI) → Verification steps

---

## Agent Selection Guide

| User Request | Primary Agent | Secondary Agent |
|--------------|---------------|-----------------|
| "Build AI agent with ADK" | `sia.md` | `repository_guardian.md` (architecture) |
| "Fix DDD violations" | `repository_guardian.md` | - |
| "Research LangChain patterns" | `research_specialist.md` | - |
| "Create new requirement REQ-007" | `compliance_officer.md` | - |
| "Improve SIA framework" | `sia_framework.md` | `evolve_spr.py` (generation) |
| "SharePoint permissions broken" | `microsoft_suite_specialist.md` | `research_specialist.md` (if docs needed) |
| "Migrate from Google Drive" | `microsoft_suite_specialist.md` | - |
| "Query Microsoft Graph API" | `microsoft_suite_specialist.md` | - |
| "Configure M365 governance" | `microsoft_suite_specialist.md` | - |

---

## Adding New Agents

### Checklist

1. **Create Agent File**: `agents/<domain>_specialist.md`
2. **Follow SPR Format**:
   - Latent Space Activation (LSA) - cognitive priming
   - Core Mission - one-sentence identity
   - Expertise - bullet-point knowledge areas
   - MCP Integration - available tools and usage protocol
   - Workflow - step-by-step problem-solving process
   - Anti-Patterns - what NOT to do
   - Mental Model Compression - essence extraction
   - Key Invariants - always-true constraints
   - Output Format - structured response template
   - Verification Checklist - quality gates

3. **Document MCP Dependencies**: List required MCP servers
4. **Update This README**: Add to catalog with selection criteria
5. **Test Agent**: Verify with real-world scenarios
6. **Version Control**: Tag agent version, update date

### SPR Standards

**✅ GOOD** (High-density):
```markdown
## EXPERTISE
- SharePoint: Sites, libraries, permissions, content types
- Graph API: /sites, /drives, batching, delta queries
```

**❌ BAD** (Verbose):
```markdown
## EXPERTISE
You are an expert in Microsoft SharePoint with extensive knowledge of...
[100 tokens of fluff]
```

**Rule**: 1 concept = 1 line. No explanatory paragraphs in expertise sections.

### Latent Space Activation (LSA)

**Purpose**: Pre-prime LLM with domain-specific cognitive patterns before processing requests

**Structure**:
```yaml
cognitive_priming_vectors:
  - [Key concept 1]
  - [Key concept 2]
  
domain_expertise_activation:
  category_1: [subconcepts]
  category_2: [patterns]
  
mental_models:
  - [Core analogy or framework understanding]
  
problem_solving_patterns:
  - [Common issue] → [Diagnostic approach] → [Solution template]
```

**Example** (Microsoft Suite Agent):
- Activates SharePoint architecture knowledge
- Primes Graph API patterns
- Loads migration workflow templates
- Pre-configures permission troubleshooting logic

**Benefit**: Faster, more accurate responses by activating relevant knowledge before inference

---

## Agent Communication Protocol

### Inter-Agent Delegation

**Pattern**:
```markdown
## DELEGATION PROTOCOL

**Escalate to [Agent Name]** when:
- [Condition 1]
- [Condition 2]

**Invoke [Agent Name]** when:
- [Scenario requiring collaboration]
```

**Example** (Microsoft Suite Agent):
- Escalates to `research_specialist.md` for deep Microsoft Graph changelog analysis
- Escalates to `repository_guardian.md` for SPFx code architecture review
- Invokes `sia.md` for M365 + AI agent integration

### MCP-First Workflow

**All agents MUST follow**:
1. Check MCP availability for domain
2. Query official documentation via MCP (if available)
3. Execute operations via MCP tools (if available)
4. Fallback to manual methods if MCP unavailable
5. Document MCP usage in response

**Example** (Microsoft Suite Agent):
```
Before answering SharePoint question:
1. mcp_learn_get_documentation(topic="SharePoint permissions")
2. mcp_microsoft-365_get_site_info(siteUrl="...")
3. Analyze results, provide solution
4. Include both MCP and manual approaches
```

---

## Framework Evolution

### Self-Improvement Cycle

```
User Request
    ↓
SUPER_AGENT (meta-orchestrator)
    ↓
Delegates to Specialist Agent
    ↓
Specialist executes with MCP integration
    ↓
SUPER_AGENT validates response
    ↓
[If new pattern discovered]
    ↓
Update Agent or Create New Agent
    ↓
Run evolve_spr.py (compress new knowledge)
    ↓
Commit to framework
```

### Agent Versioning

**Format**: `[Agent Name] v[MAJOR].[MINOR].[PATCH]`

**Rules**:
- **MAJOR**: Breaking changes (protocol changes, MCP dependency overhaul)
- **MINOR**: New capabilities, MCP integrations, workflow improvements
- **PATCH**: Bug fixes, documentation updates, minor refinements

**Example**: `microsoft_suite_specialist.md v1.0.0` (initial production release)

---

## Quality Standards

### Pre-Release Checklist

- ✅ SPR format compliance (LSA, Mission, Expertise, MCP, Workflow, Output Format)
- ✅ MCP dependencies documented (servers, tools, authentication)
- ✅ Workflow section with step-by-step process
- ✅ Anti-patterns section (what NOT to do)
- ✅ Mental Model Compression (essence in 2-3 sentences)
- ✅ Verification checklist (quality gates before response)
- ✅ Real-world testing with domain-specific scenarios
- ✅ Token efficiency (<5k tokens for agent file)
- ✅ README catalog entry with selection criteria
- ✅ Version number and last updated date

### Maintenance

- Review agents quarterly for outdated MCP servers
- Update when new MCP integrations become available
- Compress if agent file exceeds 5k tokens
- Archive deprecated agents to `agents/archive/`
- Document major changes in agent file header

---

**Catalog Version**: 1.1.0  
**Total Agents**: 7 (5 framework + 2 domain specialists)  
**Last Updated**: 2025-11-25  
**Status**: ✅ Production Ready

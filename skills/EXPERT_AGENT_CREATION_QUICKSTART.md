# Expert Agent Creation - Quick Start

## Overview

Complete methodology for creating domain-specialist agents using evidence-based research via MCP Deepwiki.

**Files**:
- `create_expert_agent.md` - Full 7-phase methodology documentation
- `create_agent_cli.py` - Interactive workflow assistant (automates templates, validation)

---

## Quick Start (CLI Assistant)

### Usage

```bash
# Navigate to SIA skills directory
cd /path/to/sia/skills

# Run workflow assistant
python create_agent_cli.py \
  --domain "Microsoft 365" \
  --specialization "SharePoint" \
  --problem "Google migration"
```

### What it Does

1. ✅ Generates research questions based on domain
2. ✅ Creates research synthesis template
3. ✅ Scaffolds agent file with SPR structure + LSA
4. ✅ Creates usage examples template
5. ✅ Guides through 7-phase workflow interactively
6. ✅ Validates agent structure automatically
7. ✅ Estimates token count

### What You Do (Manual Steps)

1. **Phase 1**: Execute MCP Deepwiki queries, document findings
2. **Phase 3**: Compress knowledge into SPR format (<5k tokens)
3. **Phase 4**: Write 4-6 real-world examples with code
4. **Phase 5**: Update `agents/README.md` catalog
5. **Phase 6**: Update `CHANGELOG.md` [Unreleased]
6. **Phase 7**: Manual validation (test with real questions)

---

## Full Methodology (Manual)

### When to Use

- **CLI Assistant**: First-time agent creation, want guided workflow
- **Full Methodology**: Experienced, need reference, custom workflow

### Read Full Docs

```bash
# Open methodology documentation
cat skills/create_expert_agent.md

# Or view in VS Code
code skills/create_expert_agent.md
```

### Key Sections

1. **Phase 0-1**: Request analysis + MCP research (20 min)
2. **Phase 2-3**: Architecture design + knowledge compression (25 min)
3. **Phase 4**: Usage examples creation (20 min)
4. **Phase 5-6**: Documentation updates (10 min)
5. **Phase 7**: Quality validation (10 min)

**Total Time**: 60-90 minutes (experienced), 120 minutes (first-time)

---

## Examples

### Example 1: Microsoft 365 Agent (Completed)

**Input**:
```bash
python create_agent_cli.py \
  --domain "Microsoft 365" \
  --specialization "SharePoint" \
  --problem "Google Workspace migration"
```

**Output**:
- `agents/microsoft_suite_specialist.md` (4900 tokens)
- `agents/microsoft_suite_specialist_examples.md` (4 scenarios)
- `agents/microsoft_suite_specialist_research.md` (synthesis)

**Time**: 75 minutes

**MCP Servers Discovered**: 3 (`@pnp/mcp-microsoft-365`, `@microsoft/mcp-m365-files`, `@microsoft/mcp-learn`)

### Example 2: Kubernetes Agent (Hypothetical)

**Input**:
```bash
python create_agent_cli.py \
  --domain "Kubernetes" \
  --specialization "Networking" \
  --problem "Multi-cluster service mesh setup"
```

**Expected Research**:
- MCP servers: `kubernetes` MCP (if available)
- Repos: `kubernetes/kubernetes`, `istio/istio`, `linkerd/linkerd2`
- Patterns: CNI plugins, service mesh comparison, multi-cluster federation

**Estimated Time**: 80-100 minutes (complex domain)

---

## Success Criteria

### Quantitative
- ✅ Agent file: 4500-5000 tokens
- ✅ Examples: 4+ scenarios
- ✅ MCP research: 3+ servers identified
- ✅ Patterns: 5+ documented
- ✅ Anti-patterns: 3+
- ✅ Time: <90 minutes

### Qualitative
- ✅ Agent answers domain questions accurately
- ✅ LSA activates relevant cognitive patterns
- ✅ MCP integration is practical
- ✅ Examples are executable
- ✅ Documentation is discoverable

---

## Troubleshooting

### CLI Script Errors

**Issue**: `FileNotFoundError: agents/`
```bash
# Ensure you're in SIA root or provide absolute paths
cd /path/to/sia
python skills/create_agent_cli.py --domain "..." ...
```

**Issue**: Permission denied
```bash
chmod +x skills/create_agent_cli.py
```

### MCP Research Issues

**Issue**: No MCP servers found
- ✅ Document "No MCP servers available" in research
- ✅ Provide manual alternatives (API, CLI, UI)
- ✅ Note in agent: "MCP integration pending"

**Issue**: Deepwiki returns too much content
- ✅ Refine query (more specific + contextual)
- ✅ Use multiple narrow queries instead of one broad query
- ✅ See `agents/research_specialist.md` for query formulation

### Token Budget Exceeded

**Issue**: Agent file >6000 tokens
- ✅ Review expertise section - compress to bullets
- ✅ Extract verbose workflows to examples file
- ✅ Remove explanatory paragraphs (only actionable content)
- ✅ Use tables instead of prose where possible

---

## Advanced Usage

### Custom Workflow (Skip CLI)

```bash
# 1. Manual research (Deepwiki)
# Document in agents/[domain]_research.md

# 2. Create agent file manually
# Follow templates/PROJECT_SPR.template.md adapted for agents

# 3. Validate
python -c "
import sys
content = open('agents/my_agent.md').read()
tokens = len(content.split()) * 1.3
print(f'Tokens: {int(tokens)}')
sys.exit(0 if tokens < 5000 else 1)
"
```

### Batch Agent Creation

```bash
# Create multiple agents in sequence
domains=("AWS IAM" "Azure Networking" "Django ORM")
specs=("Least privilege" "VNet peering" "QuerySet optimization")
problems=("Permission policies" "Multi-region setup" "N+1 queries")

for i in {0..2}; do
  python skills/create_agent_cli.py \
    --domain "${domains[$i]}" \
    --specialization "${specs[$i]}" \
    --problem "${problems[$i]}"
done
```

---

## Integration with SIA Workflow

### As a Skill

**Invoke when**: User requests expert agent creation

**Pattern**:
```
User: "Create agent for Kubernetes networking"
  ↓
SUPER_AGENT: Reads skills/create_expert_agent.md
  ↓
SUPER_AGENT: Executes 7-phase workflow
  ↓
Result: Production-ready agent in agents/
```

### As a Requirement

**Create formal requirement**:
```bash
# Create REQ-XXX for agent creation project
mkdir requirements/REQ-008-kubernetes-agent
cp requirements/_templates/REQUIREMENT_TEMPLATE.md requirements/REQ-008/REQ-008.md

# Follow QUANT breakdown
# Phase 0-1: Research
# Phase 2-3: Agent creation
# Phase 4-6: Documentation
# Phase 7: Validation
```

---

## References

- **Methodology**: `skills/create_expert_agent.md` (full 7-phase workflow)
- **Example Agent**: `agents/microsoft_suite_specialist.md` (reference implementation)
- **SPR Standards**: `CONTRIBUTING.md` (compression techniques)
- **LSA Patterns**: `skills/create_expert_agent.md` → Appendix
- **MCP Research**: `agents/research_specialist.md` (query formulation)

---

**Skill Version**: 1.0.0  
**CLI Version**: 1.0.0  
**Last Updated**: 2025-11-25  
**Success Rate**: 100% (1/1 agents created using methodology)  
**Status**: ✅ Production Ready

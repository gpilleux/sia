#!/usr/bin/env python3
"""
Expert Agent Creation Assistant

Usage:
    python create_agent_cli.py --domain "Microsoft 365" --specialization "SharePoint" --problem "Google migration"
    
This script guides you through the 7-phase expert agent creation workflow.
It doesn't replace the methodology but provides structure and validation.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class AgentCreationWorkflow:
    """7-phase expert agent creation workflow automation"""
    
    def __init__(self, domain: str, specialization: str, problem: str):
        self.domain = domain
        self.specialization = specialization
        self.problem = problem
        self.agent_name = self._generate_agent_name()
        self.timestamp = datetime.now().strftime("%Y-%m-%d")
        
        # Paths
        self.root = Path(__file__).parent.parent
        self.agents_dir = self.root / "agents"
        self.skills_dir = self.root / "skills"
        
    def _generate_agent_name(self) -> str:
        """Generate agent filename from domain"""
        # Convert "Microsoft 365" -> "microsoft_365_specialist"
        normalized = self.domain.lower().replace(" ", "_").replace("-", "_")
        return f"{normalized}_specialist"
    
    def run(self):
        """Execute 7-phase workflow interactively"""
        print("=" * 80)
        print("SIA EXPERT AGENT CREATION WORKFLOW")
        print("=" * 80)
        print()
        print(f"Domain: {self.domain}")
        print(f"Specialization: {self.specialization}")
        print(f"Problem Focus: {self.problem}")
        print(f"Agent Name: {self.agent_name}.md")
        print()
        
        phases = [
            self.phase_0_request_analysis,
            self.phase_1_mcp_research,
            self.phase_2_architecture_design,
            self.phase_3_knowledge_compression,
            self.phase_4_examples_creation,
            self.phase_5_catalog_integration,
            self.phase_6_documentation_updates,
            self.phase_7_quality_validation
        ]
        
        for idx, phase in enumerate(phases):
            print(f"\n{'=' * 80}")
            print(f"PHASE {idx}: {phase.__name__.replace('_', ' ').upper()}")
            print(f"{'=' * 80}\n")
            
            try:
                phase()
            except KeyboardInterrupt:
                print("\n\n⚠️  Workflow interrupted. Progress not saved.")
                sys.exit(1)
            except Exception as e:
                print(f"\n❌ Error in {phase.__name__}: {e}")
                print("Continuing to next phase...\n")
    
    def phase_0_request_analysis(self):
        """Phase 0: Request Analysis (5 min)"""
        print("📋 Extract domain, specialization, and user pain points\n")
        
        # Generate research questions
        questions = self._generate_research_questions()
        
        print("Generated Research Questions:")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q}")
        
        print("\n✅ Research brief created.")
        print("   📝 Review questions before proceeding to MCP research.")
        
        input("\nPress Enter to continue...")
    
    def _generate_research_questions(self) -> List[str]:
        """Generate domain-specific research questions"""
        return [
            f"What MCP servers exist for {self.domain}?",
            f"What are the core {self.specialization} configuration patterns?",
            f"What are common strategies for {self.problem}?",
            f"What are the anti-patterns and pitfalls in {self.domain}?"
        ]
    
    def phase_1_mcp_research(self):
        """Phase 1: MCP Research (15-20 min)"""
        print("🔍 Gather empirical evidence from MCP Deepwiki\n")
        
        print("MANUAL STEPS REQUIRED:")
        print("1. Open VS Code with MCP Deepwiki enabled")
        print("2. Execute queries (from Phase 0) using:")
        print("   mcp_deepwiki_ask_question(repoName='...', question='...')")
        print("3. Document findings in research synthesis file")
        print()
        print(f"Suggested repos:")
        print(f"  - modelcontextprotocol/servers (MCP ecosystem)")
        print(f"  - [domain-specific repos]")
        print()
        
        # Create research template
        research_file = self.agents_dir / f"{self.agent_name}_research.md"
        if not research_file.exists():
            template = self._generate_research_template()
            research_file.write_text(template)
            print(f"✅ Created research template: {research_file}")
        else:
            print(f"⚠️  Research file already exists: {research_file}")
        
        print("\n⏸️  Pausing for manual MCP research...")
        input("Press Enter when research is complete...")
    
    def _generate_research_template(self) -> str:
        """Generate research synthesis template"""
        return f"""# {self.domain} Agent - Research Synthesis

## MCP Servers Identified

| Server | Provider | Capabilities | Priority | Setup Complexity |
|--------|----------|--------------|----------|------------------|
| [name] | [org]    | [features]   | ⭐⭐⭐    | Low/Medium/High  |

## Core Patterns Discovered

1. **[Pattern Name]**: [Brief description + use case]
2. **[Pattern Name]**: [Brief description + use case]

## Anti-Patterns (What NOT to do)

- ❌ [Anti-pattern 1]: [Why it fails]
- ❌ [Anti-pattern 2]: [Why it fails]

## Common Problem Categories

1. **[Problem Type]**: [Diagnostic approach + solution template]
2. **[Problem Type]**: [Diagnostic approach + solution template]

## Code Examples Extracted

- **[Scenario 1]**: [Language/tool + code snippet reference]
- **[Scenario 2]**: [Language/tool + code snippet reference]

---

**Research Date**: {self.timestamp}
**Domain**: {self.domain}
**Specialization**: {self.specialization}
"""
    
    def phase_2_architecture_design(self):
        """Phase 2: Agent Architecture Design (10 min)"""
        print("🏗️  Structure agent knowledge using SPR + LSA\n")
        
        # Create agent skeleton
        agent_file = self.agents_dir / f"{self.agent_name}.md"
        if not agent_file.exists():
            skeleton = self._generate_agent_skeleton()
            agent_file.write_text(skeleton)
            print(f"✅ Created agent skeleton: {agent_file}")
            print()
            print("NEXT STEPS:")
            print("1. Review LSA section - add cognitive priming vectors")
            print("2. Fill in domain expertise from research synthesis")
            print("3. Define MCP integration protocol")
        else:
            print(f"⚠️  Agent file already exists: {agent_file}")
        
        input("\nPress Enter to continue...")
    
    def _generate_agent_skeleton(self) -> str:
        """Generate agent file skeleton with SPR structure"""
        return f"""# {self.domain} Specialist

## LATENT SPACE ACTIVATION (LSA)

**Cognitive Priming Vectors**:
- [Key domain concept 1] (e.g., {self.specialization} architecture)
- [Key domain concept 2] (e.g., API patterns)
- [Key domain concept 3] (e.g., {self.problem} workflows)

**Domain Expertise Activation**:
```yaml
{self.domain.lower().replace(' ', '_')}:
  core_services: [list_of_fundamentals]
  advanced_topics: [specialized_knowledge]
  
{self.specialization.lower().replace(' ', '_')}_mastery:
  architecture: [patterns]
  configuration: [key_settings]
  
problem_patterns:
  {self.problem.lower().replace(' ', '_')}: [solution_templates]
```

**Mental Models**:
- [Core analogy 1]: [Simple explanation]
- [Core analogy 2]: [Framework understanding]

**Problem-Solving Patterns**:
- [Issue Type] → [Diagnostic] → [Solution]

---

## CORE MISSION

Expert in {self.domain} with **deep {self.specialization} specialization**. 
Guide {self.problem}. Solve configuration challenges. 
Leverage MCP integrations for automated solutions.

---

## EXPERTISE

### {self.domain} Core
- **[Category 1]**: [Capabilities]
- **[Category 2]**: [Capabilities]

### {self.specialization} Deep Dive
- **[Aspect 1]**: [Details]
- **[Aspect 2]**: [Details]

### MCP Integration
- **[Tool 1]**: [Usage]
- **[Tool 2]**: [Usage]

---

## MCP INTEGRATION

### Available MCP Servers

**Priority MCPs**:

1. **[Server Name]** - `[package]`
   - Capabilities: [List]
   - Tools: [List]
   - Authentication: [Method]
   - **Best for**: [Use case]

### MCP Tool Usage Protocol

**Before answering ANY {self.domain} question**:

1. Check MCP Availability
2. Query Official Docs
3. Execute Operations
4. Fallback Strategy (if MCP unavailable)

---

## WORKFLOW: {self.problem.upper()}

### Phase 1: Problem Analysis

**Questions to Ask**:
1. [Clarifying question]
2. [Clarifying question]

**Diagnostic Steps**:
[Step-by-step with MCP/manual options]

### Phase 2: Research (MCP-First)

[Query protocol]

### Phase 3: Solution Design

[Multi-option approach]

---

## ANTI-PATTERNS

### {self.domain} Anti-Patterns

❌ **[Bad Practice]** → [Why it fails]  
✅ [Correct approach]

---

## MENTAL MODEL COMPRESSION

**Essence**: [2-3 sentence ultra-compressed understanding]

**Critical Path**: 
1. **[Primary Journey]**: [Step 1] → [Step 2] → [Step 3]

**Architecture DNA**: [Core pattern in one sentence]

**Key Invariants**:
- [Always-true constraint 1]
- [Always-true constraint 2]

---

## OUTPUT FORMAT (SPR)

```markdown
## PROBLEM ANALYSIS
[Root cause + component]

## MCP RESEARCH
Queries: 
1. mcp_[tool](...) → [Finding]

## SOLUTION DESIGN
[Multi-option approach]

## VERIFICATION
- ✅ [Check 1]
```

---

## VERIFICATION CHECKLIST

Before providing solution:
- ✅ Queried MCP for official documentation
- ✅ Verified tools/APIs exist
- ✅ Included verification steps
- ✅ Provided both automated and manual options
- ✅ Addressed anti-patterns

---

**Agent Version**: 1.0.0  
**Specialization**: {self.domain} ({self.specialization}-focused)  
**MCP Dependencies**: [List after research]  
**Last Updated**: {self.timestamp}  
**Status**: 🚧 In Development
"""
    
    def phase_3_knowledge_compression(self):
        """Phase 3: Knowledge Compression (15 min)"""
        print("🗜️  Transform research into high-density SPR content\n")
        print("MANUAL STEPS:")
        print("1. Open agent file in editor")
        print("2. Fill expertise section (1 concept = 1 line)")
        print("3. Write workflows with tool references")
        print("4. Extract anti-patterns from research")
        print("5. Compress mental model (2-3 sentences)")
        print()
        print("TARGET: <5000 tokens total")
        
        input("\nPress Enter when compression is complete...")
    
    def phase_4_examples_creation(self):
        """Phase 4: Usage Examples Creation (20 min)"""
        print("📚 Demonstrate agent capabilities with real-world scenarios\n")
        
        examples_file = self.agents_dir / f"{self.agent_name}_examples.md"
        if not examples_file.exists():
            template = self._generate_examples_template()
            examples_file.write_text(template)
            print(f"✅ Created examples template: {examples_file}")
        else:
            print(f"⚠️  Examples file already exists: {examples_file}")
        
        print("\nMANUAL STEPS:")
        print("1. Create 4-6 real-world scenarios")
        print("2. Add code examples (multiple languages)")
        print("3. Include MCP tool invocations")
        print("4. Provide verification steps")
        print("5. Add MCP setup guide")
        
        input("\nPress Enter to continue...")
    
    def _generate_examples_template(self) -> str:
        """Generate usage examples template"""
        return f"""# {self.domain} Specialist - Usage Examples

## Quick Reference

**Invoke When**:
- {self.specialization} configuration issues
- {self.problem}
- [Other scenarios]

**Primary MCP Tools**:
- `mcp_[server]_*` - [Capabilities]

---

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

### Implementation

#### Option A: MCP Tools
[Code]

#### Option B: Manual
[Steps]

## VERIFICATION
- ✅ [Check 1]
```

---

## Example 2: [Complex Use Case]

[Repeat structure]

---

## MCP Setup Requirements

### Required MCP Servers

1. **[Server Name]** ([Provider])
   - Install: [Command]
   - Auth: [Method]

### Authentication Setup

```bash
# Configuration steps
```

---

**Document Version**: 1.0.0  
**Agent Version**: {self.agent_name}.md v1.0.0  
**Last Updated**: {self.timestamp}
"""
    
    def phase_5_catalog_integration(self):
        """Phase 5: Catalog Integration (5 min)"""
        print("📇 Update agents/README.md with new agent entry\n")
        print("MANUAL STEPS:")
        print("1. Open agents/README.md")
        print("2. Add catalog entry in 'Domain Specialist Agents' section")
        print("3. Update selection guide table")
        print("4. Increment agent count in footer")
        
        input("\nPress Enter when catalog is updated...")
    
    def phase_6_documentation_updates(self):
        """Phase 6: Documentation Updates (5 min)"""
        print("📝 Maintain traceability and versioning\n")
        print("MANUAL STEPS:")
        print("1. Open CHANGELOG.md")
        print("2. Add entry to [Unreleased] section")
        print("3. Document key features and MCP integrations")
        print("4. (Optional) Create executive summary document")
        
        input("\nPress Enter when documentation is updated...")
    
    def phase_7_quality_validation(self):
        """Phase 7: Quality Validation (10 min)"""
        print("✅ Ensure agent meets production standards\n")
        
        # Run automated checks
        agent_file = self.agents_dir / f"{self.agent_name}.md"
        
        if agent_file.exists():
            content = agent_file.read_text()
            
            checks = {
                "LSA section present": "## LATENT SPACE ACTIVATION" in content,
                "Core Mission present": "## CORE MISSION" in content,
                "Expertise section present": "## EXPERTISE" in content,
                "MCP Integration present": "## MCP INTEGRATION" in content,
                "Workflow present": "## WORKFLOW" in content,
                "Anti-patterns present": "## ANTI-PATTERNS" in content,
                "Mental Model present": "## MENTAL MODEL COMPRESSION" in content,
                "Output Format present": "## OUTPUT FORMAT" in content,
                "Verification Checklist present": "## VERIFICATION CHECKLIST" in content,
                "Version number present": "**Agent Version**:" in content,
            }
            
            print("Automated Checks:")
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"{status} {check}")
            
            # Token estimate (rough)
            word_count = len(content.split())
            token_estimate = int(word_count * 1.3)  # Rough multiplier
            
            print(f"\n📊 Token Estimate: ~{token_estimate} tokens")
            if token_estimate > 5000:
                print("   ⚠️  Exceeds 5000 token target - consider compression")
            else:
                print("   ✅ Within token budget")
        else:
            print(f"❌ Agent file not found: {agent_file}")
        
        print("\nMANUAL VALIDATION:")
        print("1. Read agent file → Does LSA make sense?")
        print("2. Check expertise → Actionable and high-density?")
        print("3. Review workflow → Can it be followed?")
        print("4. Validate examples → Executable as-written?")
        print("5. Test MCP references → Servers exist?")
        
        print("\n" + "=" * 80)
        print("🎉 WORKFLOW COMPLETE!")
        print("=" * 80)
        print(f"\nGenerated Files:")
        print(f"  - {self.agents_dir / (self.agent_name + '.md')}")
        print(f"  - {self.agents_dir / (self.agent_name + '_examples.md')}")
        print(f"  - {self.agents_dir / (self.agent_name + '_research.md')}")
        print()
        print("Next Steps:")
        print("  1. Review all files for completeness")
        print("  2. Test agent with real questions")
        print("  3. Update CHANGELOG.md [Unreleased] → version bump")
        print("  4. Commit to repository")


def main():
    parser = argparse.ArgumentParser(
        description="Expert Agent Creation Workflow Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_agent_cli.py --domain "Microsoft 365" --specialization "SharePoint" --problem "Google migration"
  python create_agent_cli.py --domain "Kubernetes" --specialization "Networking" --problem "Multi-cluster setup"
  python create_agent_cli.py --domain "AWS" --specialization "IAM" --problem "Least privilege policies"
        """
    )
    
    parser.add_argument(
        "--domain",
        required=True,
        help="Primary domain (e.g., 'Microsoft 365', 'Kubernetes', 'AWS')"
    )
    
    parser.add_argument(
        "--specialization",
        required=True,
        help="Specific expertise area (e.g., 'SharePoint', 'Networking', 'IAM')"
    )
    
    parser.add_argument(
        "--problem",
        required=True,
        help="Problem focus (e.g., 'Google migration', 'Multi-cluster setup', 'Least privilege')"
    )
    
    args = parser.parse_args()
    
    workflow = AgentCreationWorkflow(
        domain=args.domain,
        specialization=args.specialization,
        problem=args.problem
    )
    
    workflow.run()


if __name__ == "__main__":
    main()

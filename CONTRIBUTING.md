# Contributing to SIA Framework

Thank you for your interest in improving the SIA (Super Intelligence Agency) framework!

## Table of Contents

- [Contribution Philosophy](#contribution-philosophy)
- [Framework vs Project Learning](#framework-vs-project-learning)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)

---

## Contribution Philosophy

SIA follows **DDD/SOLID/KISS** principles, even though it's a prompt-based framework:

- **DDD (Domain-Driven Design)**: Clear bounded contexts (agents, skills, requirements)
- **SOLID**: Single Responsibility (one agent = one bounded context), Open/Closed (extend via new agents, not modify core)
- **KISS (Keep It Simple, Stupid)**: Minimal complexity, maximum clarity

**SPR-First**: All contributions must be SPR-friendly (high-density, concise, no jargon).

---

## Framework vs Project Learning

### Framework Learning (Contributes to `sia/` submodule)

**What**: Reusable improvements applicable to **ALL** SIA projects.

**Examples**:
- New sub-agent (e.g., `agents/performance_optimizer.md`)
- New skill (e.g., `skills/check_security.sh`)
- Core prompt improvements (e.g., `core/PROMPT_PLACEMENT.md`)
- Installer enhancements (e.g., new platform support)

**Process**:
1. Fork https://github.com/gpilleux/sia
2. Create feature branch: `git checkout -b feat/your-feature`
3. Make changes in `sia/` directory
4. Test in at least 2 different projects
5. Submit PR to `gpilleux/sia:main`

**PR Title Format**:
```
feat(agents): Add performance optimizer sub-agent
fix(installer): Handle missing git remote gracefully
docs(skills): Add README with token-efficient catalog
```

---

### Project Learning (Stays in `.sia/` of specific project)

**What**: Project-specific knowledge not reusable elsewhere.

**Examples**:
- Project SPR (`.sia/agents/argus.md`)
- Domain-specific agents (`.sia/agents/invoice_validator.md`)
- Business rules (`.sia/knowledge/active/tax_calculations.md`)
- Project requirements (`.sia/requirements/REQ-042/`)

**Process**:
1. Make changes in `.sia/` directory of your project
2. Commit to your project repository
3. **Do NOT submit PR to sia/ submodule**

**Detection Logic**:
```python
if applies_to_all_projects:
    target = "sia/"  # Framework learning
else:
    target = ".sia/"  # Project learning
```

---

## Pull Request Process

### Before Submitting

- [ ] **Test**: Validate in 2+ different projects (Python/Node, DDD/MVC, etc.)
- [ ] **Documentation**: Update relevant README/docs
- [ ] **Changelog**: Add entry to `CHANGELOG.md` under `[Unreleased]`
- [ ] **SPR Compliance**: Ensure high-density, no verbosity
- [ ] **Token Budget**: If adding prompts, estimate token cost

### PR Template

```markdown
## Description
[What does this change? Why is it needed?]

## Type of Change
- [ ] Framework Learning (applies to all projects)
- [ ] Bug Fix (non-breaking)
- [ ] New Feature (non-breaking)
- [ ] Breaking Change (requires version bump)

## Testing
Tested in:
- [ ] Python + FastAPI + DDD project
- [ ] TypeScript + Next.js + MVC project
- [ ] [Other architecture]

## Token Impact
- **Before**: X tokens
- **After**: Y tokens
- **Change**: ±Z tokens (justify if increase)

## Checklist
- [ ] Follows DDD/SOLID/KISS principles
- [ ] SPR-friendly (concise, no jargon)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Self-tested in multiple projects
```

### Review Process

1. **Automated Checks** (when available):
   - Markdown linting
   - YAML validation
   - Token count analysis

2. **Manual Review**:
   - SPR compliance (maintainer checks density)
   - DDD/SOLID/KISS adherence
   - Token efficiency
   - Cross-project applicability

3. **Merge Criteria**:
   - ✅ Tested in 2+ projects
   - ✅ Documentation complete
   - ✅ No token bloat (or justified)
   - ✅ SPR-friendly format

---

## Coding Standards

### Prompt Standards (SPR Format)

**✅ GOOD** (High-Density):
```markdown
## MISSION
DDD architect. Analyze → SPR guidance. Build with ADK. Query Deepwiki FIRST.

## EXPERTISE
- AI-Native (ADK): LlmAgent, tools, Gemini, SSE
- Database: Postgres 15+, PostGIS, hypertables
- Testing: Playwright E2E, SSE validation
```

**❌ BAD** (Verbose):
```markdown
## MISSION
You are a highly sophisticated Domain-Driven Design architect with extensive 
experience in AI-Native development. Your role is to carefully analyze the 
architecture and provide comprehensive guidance...
[200 tokens of fluff]
```

**Rule**: 1 concept = 1 line. No explanatory paragraphs.

---

### Bash Script Standards

**✅ GOOD** (KISS):
```bash
#!/bin/bash
set -e  # Fail fast

# Check prerequisites
command -v python3 &> /dev/null || { echo "Python required"; exit 1; }

# Single responsibility
radon cc . --min C --exclude "venv/*,tests/*"
```

**❌ BAD** (Complex):
```bash
# No set -e
# Multiple nested if/else
# Unclear error messages
```

---

### Python Script Standards

**✅ GOOD** (DDD-Inspired):
```python
class AutoDiscovery:  # Single Responsibility
    def discover(self):  # Clear interface
        self.detect_git()
        self.detect_tech_stack()
        return self.config  # Immutable return
```

**❌ BAD**:
```python
def do_everything():  # God function
    # 500 lines of mixed concerns
```

---

## Testing Requirements

### Manual Testing Checklist

Since SIA is prompt-based, testing = validation in real projects:

- [ ] **Fresh Install**: Test installer in new empty repo
- [ ] **Python Project**: Validate auto-discovery detects FastAPI/Django
- [ ] **Node Project**: Validate auto-discovery detects Next.js/Express
- [ ] **DDD Project**: Verify Repository Guardian activates
- [ ] **MVC Project**: Verify generic patterns work
- [ ] **Skills Invocation**: Run each skill script successfully
- [ ] **Init Protocol**: Verify `.sia/INIT_REQUIRED.md` gets deleted post-init

### Automated Tests (Future)

When available:
```bash
pytest sia/installer/test_auto_discovery.py
bash sia/skills/test_all_skills.sh
```

---

## Documentation Standards

### README Structure

Every new component needs a README:

```markdown
# [Component Name]

**Purpose**: [1-sentence description]

**When to Use**: [Trigger condition]

**Token Cost**: ~X tokens

## Usage

[Minimal example]

## See Also

- [Related doc]
```

**Token Efficiency Rule**: README = index only, full docs = separate file (pay-per-use).

---

### Changelog Format

```markdown
## [Unreleased]

### Added
- New feature X with Y benefit

### Changed
- Improved Z for better performance

### Fixed
- Bug in W causing incorrect behavior

### Removed
- Deprecated feature V (breaking change)
```

---

## Development Workflow

### Local Development

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/sia.git
cd sia

# Create feature branch
git checkout -b feat/my-improvement

# Make changes
vim agents/my_new_agent.md

# Test in real project
cd ../my-test-project
git submodule update --remote sia  # Pull your changes
# Test initialization, skills, etc.

# Document
vim sia/CHANGELOG.md
vim sia/README.md

# Commit
git add -A
git commit -m "feat(agents): Add my new agent

FRAMEWORK LEARNING:
- Applies to all projects with X pattern
- Tested in Python + Node projects
- Token cost: +500 tokens (justified by Y benefit)

See: agents/my_new_agent.md"

# Push and PR
git push origin feat/my-improvement
# Open PR on GitHub
```

---

## Questions?

- **GitHub Issues**: https://github.com/gpilleux/sia/issues
- **Discussions**: https://github.com/gpilleux/sia/discussions

---

## Code of Conduct

- **Be respectful**: Constructive criticism only
- **Be concise**: Respect token budgets (SPR philosophy)
- **Be evidence-based**: Test before submitting
- **Be collaborative**: Framework learning benefits everyone

---

**Thank you for contributing to SIA!** 🚀

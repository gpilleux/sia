# SIA (Super Intelligence Agency)

**The Meta-Cognitive Framework for Autonomous Software Development**

SIA is a reusable framework that injects high-level architectural reasoning, domain-driven design enforcement, and autonomous capabilities into any software project. It operates as a "Super Agent" that orchestrates sub-agents, manages requirements, and ensures code quality.

**Version**: 1.0.0  
**License**: MIT  
**Repository**: https://github.com/gpilleux/sia

## Core Capabilities

1. **Meta-Cognition**: Operates above the code, reasoning about architecture and design patterns.
2. **Auto-Discovery**: Automatically detects project identity, technology stack, and domain boundaries.
3. **DDD Enforcement**: Strictly enforces Domain-Driven Design principles (Layer separation, Dependency Rule).
4. **Requirements Management**: Implements a rigorous 7-phase requirement lifecycle (QUANT).
5. **Skill Injection**: Provides high-leverage tools for complexity analysis, visualization, and auditing.

## Installation (Git Submodule)

SIA is designed to be installed as a git submodule in your project:

\`\`\`bash
# In your project root
git submodule add https://github.com/gpilleux/sia.git sia
cd sia && bash installer/install.sh
\`\`\`

The installer will:
1. Auto-discover your project structure
2. Generate \`.sia.detected.yaml\` configuration
3. Create \`.github/copilot-instructions.md\` with SIA integration
4. Initialize \`.agents/\` directory for project-specific agents

## Directory Structure

\`\`\`
sia/
├── core/              # Framework identity and orchestration
│   ├── SUPER_AGENT.md           # Core identity and capabilities
│   ├── STANDARDS.md             # SIA configuration standards
│   ├── AUTO_DISCOVERY.md        # Project detection logic
│   └── copilot-instructions.template.md
│
├── agents/            # Reusable agent templates
│   ├── repository_guardian.md   # DDD/SOLID enforcement
│   ├── research_specialist.md   # Knowledge discovery
│   └── sia.md                   # SIA orchestrator
│
├── skills/            # Automated analysis tools
│   ├── check_complexity.sh      # Radon complexity analysis
│   ├── check_coverage.sh        # Test coverage gaps
│   ├── visualize_architecture.sh # Pydeps dependency graphs
│   └── audit_ddd.py             # DDD compliance checker
│
├── requirements/      # Requirement lifecycle templates
│   ├── README.md                # 7-phase QUANT workflow
│   └── _templates/
│       ├── REQUIREMENT_TEMPLATE.md
│       ├── DOMAIN_ANALYSIS_TEMPLATE.md
│       └── QUANT_BREAKDOWN_TEMPLATE.md
│
└── installer/         # Zero-config installation
    ├── install.sh               # Main installer
    ├── auto_discovery.py        # Project detection
    └── generate_instructions.py # Copilot instructions generator
\`\`\`

## Usage in Your Project

After installation, your project will have:

\`\`\`
your-project/
├── .sia.detected.yaml          # Auto-generated config
├── .github/
│   └── copilot-instructions.md # SIA-enhanced instructions
├── .agents/                    # Project-specific agents
│   ├── product.md             # Your product SPR
│   └── knowledge/             # Research cache
├── sia/                        # Git submodule (this framework)
├── requirements/              # Your project requirements
│   ├── REQ-001/
│   └── ...
└── skills/                    # Project-specific skills
\`\`\`

## Framework Philosophy

SIA follows these principles:

1. **Zero Configuration**: Auto-discovers project context
2. **Non-Invasive**: Works alongside existing workflows
3. **Reusable**: Same framework across multiple projects
4. **Evolvable**: Learns and adapts from each project
5. **Traceable**: Every decision has a requirement trace

## Requirements Management (QUANT)

SIA implements a 7-phase lifecycle for every requirement:

1. **FASE 1**: User natural language → Formal requirement
2. **FASE 2**: Domain analysis (DDD bounded contexts)
3. **FASE 3**: Acceptance criteria definition
4. **FASE 4**: QUANT task decomposition
5. **FASE 5**: Implementation with verification gates
6. **FASE 6**: Knowledge evolution and SPR updates
7. **FASE 7**: Archive and completion report

See \`requirements/README.md\` for details.

## Skills System

High-leverage automation scripts:

- **check_complexity.sh**: Detects cyclomatic complexity violations (Rank C+)
- **visualize_architecture.sh**: Generates DDD layer dependency graphs
- **check_coverage.sh**: Identifies test coverage gaps (<80%)
- **audit_ddd.py**: Validates domain/infrastructure separation

Invoke at verification gates (pre-QUANT, post-implementation).

## Integration with GitHub Copilot

SIA enhances GitHub Copilot by:

1. Injecting architectural reasoning via \`.github/copilot-instructions.md\`
2. Providing specialized sub-agents (Repository Guardian, Research Specialist)
3. Enforcing DDD/SOLID principles through active validation
4. Managing requirements with formal traceability

## Contributing

SIA is an evolving framework. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Implement improvements
4. Submit PR with rationale

## License

MIT License - See LICENSE file

## Support

- **Issues**: https://github.com/gpilleux/sia/issues
- **Discussions**: https://github.com/gpilleux/sia/discussions
- **Documentation**: https://github.com/gpilleux/sia/wiki

---

**Built with SIA**: Projects using this framework maintain higher code quality, faster onboarding, and better architectural consistency.

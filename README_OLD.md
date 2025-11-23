# Super Intelligence Agency (SIA)

<div align="center">

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/gpilleux/sia/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](QUICKSTART.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Required-purple.svg)](https://github.com/features/copilot)

**The Meta-Cognitive Framework for Autonomous Software Development**

Transform GitHub Copilot into a "Super Agent" with architectural reasoning, DDD enforcement, and autonomous capabilities.

[Quick Start](#-quick-installation) • [Documentation](QUICKSTART.md) • [Distribution Guide](DISTRIBUTION.md) • [Examples](#-example-projects)

</div>

---

## 🚀 Quick Installation

**One-liner for each platform** – copy and paste in your project root:

### macOS / Linux
```bash
git submodule add https://github.com/gpilleux/sia.git sia && cd sia && bash installer/install.sh
```

### Windows (PowerShell/CMD)
```cmd
git submodule add https://github.com/gpilleux/sia.git sia && cd sia && installer\install.bat
```

**That's it!** SIA will auto-discover your project and configure itself in ~30 seconds.

---

## ✨ What You Get

After installation, SIA provides:

🤖 **AI Orchestration**
- GitHub Copilot becomes a "Super Agent"
- Auto-discovers project architecture
- Enforces DDD/SOLID principles
- Manages 7-phase QUANT requirements

🔍 **Auto-Discovery**
- Detects tech stack (Python, FastAPI, Next.js, etc.)
- Extracts bounded contexts from domain layer
- Identifies architecture patterns (DDD, MVC)
- Generates `.sia.detected.yaml` configuration

🛠️ **Analysis Skills**
- `check_complexity.sh` - Radon cyclomatic complexity
- `visualize_architecture.sh` - Pydeps dependency graphs
- `check_coverage.sh` - pytest-cov HTML reports

📋 **Requirements Management**
- Formal REQ-XXX tracking
- Domain analysis templates
- QUANT task decomposition
- Archive completed work

🧠 **Specialized Sub-Agents**
- Repository Guardian (DDD enforcement)
- Research Specialist (knowledge discovery)
- Requirement Translator (natural → formal)

---

## 📦 Prerequisites

- **Git** 2.0+
- **Python** 3.10+
- **GitHub Copilot** subscription

<details>
<summary><b>Platform-specific installation</b></summary>

### macOS (Homebrew)
```bash
brew install python@3.10 git
pip3 install uv
```

### Linux (Debian/Ubuntu)
```bash
sudo apt install python3 python3-pip git
pip3 install uv
```

### Linux (RHEL/CentOS)
```bash
sudo yum install python3 python3-pip git
pip3 install uv
```

### Windows
1. Install [Python 3.10+](https://www.python.org/downloads/) (✅ Check "Add to PATH")
2. Install [Git](https://git-scm.com/download/win)
3. Run: `pip install uv`

</details>

---

## 🎯 Core Capabilities

| Capability                    | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| 🧠 **Meta-Cognition**          | Reasons about architecture and design patterns above the code              |
| 🔍 **Auto-Discovery**          | Detects project identity, tech stack, and domain boundaries automatically  |
| 🏛️ **DDD Enforcement**         | Strictly enforces Domain-Driven Design (Layer separation, Dependency Rule) |
| 📋 **Requirements Management** | Implements rigorous 7-phase QUANT lifecycle                                |
| 🛠️ **Skill Injection**         | High-leverage tools for complexity analysis, visualization, auditing       |

---

## 📖 How It Works

```bash
# In your project root
git submodule add https://github.com/gpilleux/sia.git sia
cd sia && bash installer/install.sh  # macOS/Linux
# or
cd sia && installer\install.bat      # Windows
```

**What happens:**
1. ✅ Auto-detects your project structure (backend/, domain/, api/)
2. ✅ Identifies tech stack (Python, FastAPI, Next.js, etc.)
3. ✅ Extracts bounded contexts from domain layer
4. ✅ Generates `.sia.detected.yaml` configuration
5. ✅ Creates `.github/copilot-instructions.md` with SIA integration

**Prerequisites:**
- Git 2.0+
- Python 3.10+
- GitHub Copilot subscription (for AI orchestration)

**Platform Support:**
- ✅ macOS (Homebrew recommended)
- ✅ Linux (Debian/Ubuntu, RHEL/CentOS)
- ✅ Windows (PowerShell/Command Prompt)

**Quick Start:** See [QUICKSTART.md](./QUICKSTART.md) for detailed step-by-step guide.

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

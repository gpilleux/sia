<div align="center">

# Super Intelligence Agency (SIA)

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/gpilleux/sia/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](docs/QUICKSTART.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Required-purple.svg)](https://github.com/features/copilot)

**The Meta-Cognitive Framework for Autonomous Software Development**

Transform GitHub Copilot into a "Super Agent" with architectural reasoning, DDD enforcement, and autonomous capabilities.

[Quick Start](#-quick-installation) • [Documentation](docs/QUICKSTART.md) • [Architecture](docs/ARCHITECTURE.md) • [Contributing](docs/CONTRIBUTING.md) • [Distribution](docs/DISTRIBUTION.md) • [Uninstall](docs/UNINSTALL.md)

</div>

---

## 🚀 Quick Installation

**Universal cross-platform installer** – works on macOS, Linux, and Windows:

### Option 1: Git Submodule (Recommended)

Keeps SIA updated across projects, tracks framework version.

```bash
# git init
git submodule add https://github.com/gpilleux/sia.git sia
uv run sia/installer/install.py  # Recommended: Cross-platform Python installer
```

**Alternative platform-specific installers (legacy):**
```bash
bash sia/installer/install.sh      # macOS/Linux only
sia\installer\install.bat          # Windows only
```

> **💡 Tip**: Use `install.py` for all platforms. Shell scripts maintained for backwards compatibility.

### Option 2: Standalone Clone

Single project, no submodule. Add `sia/` to `.gitignore`.

```bash
git clone https://github.com/gpilleux/sia.git sia
python3 sia/installer/install.py   # Recommended: Cross-platform installer
echo "sia/" >> .gitignore
```

---

### ⚡ **NEXT STEP - ACTIVATION REQUIRED**

<div align="center">

### 🎯 Open VS Code and tell GitHub Copilot:

```
"Initialize SIA for this repository"
```

> 👆 **This activates the Super Agent and generates your project's AI architecture**

</div>

---

## 💡 Usage Scenarios

### Scenario A: Existing Codebase (Brownfield)

**Goal**: Analyze existing code, map architecture, and enforce standards.

```
You: "Initialize SIA for this repository"

SIA Actions:
1. ✅ Reads .sia.detected.yaml (tech stack, bounded contexts)
2. ✅ Generates Project SPR mapping your architecture
3. ✅ Identifies technical debt and refactoring opportunities
4. ✅ Sets up requirements/ workflow for future changes
5. ✅ Baseline analysis (complexity, coverage, dependencies)

Result: Complete architectural understanding + quality metrics
```

---

### Scenario B: New Project (Greenfield)

**Goal**: Scaffold a new application from scratch using best practices.

```
You: "Initialize SIA. I want to build a SaaS for pet grooming."

SIA Actions:
1. ✅ Proposes AI-Native Stack:
   - Backend: Python + FastAPI + DDD/SOLID/KISS
   - Database: PostgreSQL 15 + TimescaleDB + PostGIS
   - Frontend: React 18 + Vite + SSE (real-time)
   - AI Layer: Google ADK (optional, agents-as-services)
   - DevOps: Docker Compose (hot reload, all services)
   - Testing: Playwright MCP (E2E automation)

2. ✅ Scaffolds DDD directory structure:
   - Domain (entities, value objects, aggregates)
   - Application (use cases, DTOs)
   - Infrastructure (repositories, external services)
   - API (FastAPI endpoints, dependency injection)

3. ✅ Generates Project SPR (.sia/agents/pet_grooming.md)
4. ✅ Creates first REQ-001 for MVP
5. ✅ Note: AI is optional. App is 100% functional without agents.
         AI = Additional layer (assistants, not core logic).

Result: Production-ready structure + clean architecture + MVP roadmap
```

---

### Scenario C: Feature Implementation

**Natural language to implementation:**

```
You: "I need user authentication with JWT tokens"

SIA Workflow:
1. ✅ Creates REQ-XXX with formal specification
2. ✅ Analyzes impacted bounded contexts (Users, Auth)
3. ✅ Decomposes into QUANT tasks:
   - QUANT-001: Domain entities (User, Token)
   - QUANT-002: Repository interfaces
   - QUANT-003: JWT service implementation
   - QUANT-004: API endpoints
   - QUANT-005: Integration tests
4. ✅ Guides DDD-compliant implementation
5. ✅ Validates architecture with skills
6. ✅ Archives completed requirement

Result: Clean architecture + tests + documentation
```

---

## 📖 How It Works

**1. Install SIA as submodule** → Installer runs auto-discovery  
**2. SIA detects your project** → Generates `.sia.detected.yaml`  
**3. Copilot enhanced** → Reads `.github/copilot-instructions.md`  
**4. You interact naturally** → SIA orchestrates specialized agents  

```
You: "I need user authentication with JWT"
      ↓
SIA: Translates to REQ-XXX → Analyzes domain → Decomposes QUANT → Guides implementation
      ↓
Result: Clean architecture + tests + documentation
```

---

## 🎯 Core Capabilities

| Capability                    | Description                                                   | Features                                                                           |
| ----------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 🧠 **Meta-Cognition**          | Reasons about architecture and design patterns above the code | AI Orchestration, DDD enforcement, SOLID principles                                |
| 🔍 **Auto-Discovery**          | Detects project identity automatically                        | Tech stack detection, bounded contexts extraction, `.sia.detected.yaml` generation |
| 📝 **SPR Skills**              | Sparse Priming Representation (70-80% compression)            | Extract domain knowledge, generate Project SPR, compress docs                      |
| 🛠️ **Analysis Tools**          | High-leverage code quality tools                              | Complexity analysis, dependency graphs, coverage reports                           |
| 📋 **Requirements Management** | Rigorous 7-phase QUANT lifecycle                              | REQ-XXX tracking, domain analysis, QUANT decomposition, archival                   |
| 🧠 **Specialized Agents**      | Sub-agents for specific tasks                                 | Repository Guardian, Research Specialist, Requirement Translator                   |

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

## 📂 Directory Structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```
sia/
├── core/                        # Framework identity
│   ├── SUPER_AGENT.md          # Orchestration rules
│   ├── STANDARDS.md            # Configuration standards
│   └── AUTO_DISCOVERY.md       # Project detection logic
│
├── agents/                      # Reusable sub-agents
│   ├── repository_guardian.md  # DDD/SOLID enforcement
│   ├── research_specialist.md  # Knowledge discovery
│   └── sia.md                  # SIA orchestrator
│
├── skills/                      # Analysis tools
│   ├── check_complexity.sh     # Radon complexity
│   ├── check_coverage.sh       # Test coverage
│   └── visualize_architecture.sh # Dependency graphs
│
├── requirements/                # QUANT templates
│   ├── README.md               # 7-phase workflow
│   └── _templates/             # REQ, domain, QUANT templates
│
└── installer/                   # Zero-config setup
    ├── install.sh              # Unix installer
    ├── install.bat             # Windows installer
    └── auto_discovery.py       # Project detection
```

</details>

---

## 🏗️ Your Project After Installation

```
your-project/
├── .sia.detected.yaml          # ✅ Auto-generated config
├── .github/
│   └── copilot-instructions.md # ✅ SIA-enhanced instructions
├── sia/                        # ✅ Git submodule (framework)
└── ... (your existing code)
```

**Example `.sia.detected.yaml`:**

```yaml
sia_version: 1.1.0
project:
  name: my-awesome-app
  type: python-fastapi-ddd
  
domain:
  bounded_contexts:
    - Users
    - Products
    - Orders
```

---

## 🌟 Example Projects

### [Argus](https://github.com/gpilleux/argus) - AI Document Intelligence Platform
[![Stack](https://img.shields.io/badge/stack-Python%20%7C%20FastAPI%20%7C%20PostgreSQL-blue)](https://github.com/gpilleux/argus)
[![Architecture](https://img.shields.io/badge/architecture-DDD%20%7C%20Clean-green)](https://github.com/gpilleux/argus)

- **Tech**: Python + FastAPI + PostgreSQL + pgvector + Google ADK
- **Architecture**: Clean Architecture (DDD)
- **Bounded Contexts**: Documents, Chat, Visualization
- **SIA Features**: Full requirements management + self-evolution protocol

*Your project here? Submit a PR!*

---

## 📚 Documentation

- 📖 **[QUICKSTART.md](docs/QUICKSTART.md)** - 5-minute setup guide
- 🏗️ **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Framework architecture deep-dive
- 🚀 **[DISTRIBUTION.md](docs/DISTRIBUTION.md)** - Share with your team
- 🔧 **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Contribution guidelines
- 📝 **[CHANGELOG.md](docs/CHANGELOG.md)** - Version history
- 🗑️ **[UNINSTALL.md](docs/UNINSTALL.md)** - Clean removal guide
- ✅ **[VALIDATION.md](docs/VALIDATION.md)** - Installation verification
- 🧠 **[core/SUPER_AGENT.md](core/SUPER_AGENT.md)** - Core capabilities
- 🎯 **[requirements/README.md](requirements/README.md)** - QUANT workflow
- 💬 **[docs/SLASH_COMMANDS.md](docs/SLASH_COMMANDS.md)** - Slash commands guide
- ⚙️ **[docs/VSCODE_SETUP.md](docs/VSCODE_SETUP.md)** - VS Code configuration

---

## 🤝 Contributing

SIA evolves with every project. Contributions welcome:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-skill`)
3. Commit changes (`git commit -m 'feat: Add amazing skill'`)
4. Push to branch (`git push origin feature/amazing-skill`)
5. Open Pull Request

**Types of contributions:**
- ✅ New generic skills (analysis tools)
- ✅ Improved agent templates
- ✅ Platform support (installers)
- ✅ Documentation improvements

---

## 📊 Framework Philosophy

SIA follows these principles:

| Principle              | Description                             |
| ---------------------- | --------------------------------------- |
| **Zero Configuration** | Auto-discovers project context          |
| **Non-Invasive**       | Works alongside existing workflows      |
| **Reusable**           | Same framework across multiple projects |
| **Evolvable**          | Learns and adapts from each project     |
| **Traceable**          | Every decision has a requirement trace  |

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 💬 Support & Community

- 🐛 **Report Issues**: [GitHub Issues](https://github.com/gpilleux/sia/issues)
- 💡 **Discussions**: [GitHub Discussions](https://github.com/gpilleux/sia/discussions)
- 📖 **Wiki**: [Documentation](https://github.com/gpilleux/sia/wiki)

---

<div align="center">

**Built with SIA**

Projects using this framework maintain higher code quality, faster onboarding, and better architectural consistency.

[![Made with ❤️](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F-red.svg)](https://github.com/gpilleux/sia)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](docs/CONTRIBUTING.md)

[⬆ Back to Top](#sia-super-intelligence-agency)

</div>

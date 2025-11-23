# Super Intelligence Agency (SIA)

<div align="center">

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/gpilleux/sia/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](QUICKSTART.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Required-purple.svg)](https://github.com/features/copilot)

**The Meta-Cognitive Framework for Autonomous Software Development**

Transform GitHub Copilot into a "Super Agent" with architectural reasoning, DDD enforcement, and autonomous capabilities.

[Quick Start](#-quick-installation) • [Documentation](QUICKSTART.md) • [Distribution Guide](DISTRIBUTION.md) • [Uninstall](UNINSTALL.md) • [Examples](#-example-projects)

</div>

---

## 🚀 Quick Installation

**One-liner for each platform** – copy and paste in your project root:

### Option 1: Git Submodule (Recommended)

Keeps SIA updated across projects, tracks framework version.

#### macOS / Linux
```bash
git submodule add https://github.com/gpilleux/sia.git sia
bash sia/installer/install.sh  # Run from project root
```

#### Windows (PowerShell/CMD)
```cmd
git submodule add https://github.com/gpilleux/sia.git sia
sia\installer\install.bat  # Run from project root
```

### Option 2: Standalone Clone

Single project, no submodule. Add `sia/` to `.gitignore`.

```bash
git clone https://github.com/gpilleux/sia.git sia
bash sia/installer/install.sh  # Run from project root
echo "sia/" >> .gitignore
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

**1. Install SIA as submodule** → Installer runs auto-discovery  
**2. SIA detects your project** → Generates `.sia.detected.yaml`  
**3. Copilot enhanced** → Reads `.github/copilot-instructions.md`  
**4. You interact naturally** → SIA orchestrates specialized agents  

```
You: "I need user authentication with JWT"
      ↓
SIA: Translates to REQ-XXX → Analyzes domain → Decomposes QUANT → Guides DDD implementation
      ↓
Result: Clean architecture + tests + documentation
```

---

## 💡 Example Usage

**Natural language to implementation:**

```
You: "I need user authentication with JWT tokens"

SIA Workflow:
1. Creates REQ-XXX with formal specification
2. Analyzes impacted bounded contexts (Users, Auth)
3. Decomposes into QUANT tasks:
   - QUANT-001: Domain entities (User, Token)
   - QUANT-002: Repository interfaces
   - QUANT-003: JWT service implementation
   - QUANT-004: API endpoints
   - QUANT-005: Integration tests
4. Guides DDD-compliant implementation
5. Validates architecture with skills
6. Archives completed requirement

Result: Clean architecture + tests + documentation ✅
```

**Run analysis skills:**

```bash
# Check code complexity
sh sia/skills/check_complexity.sh
# Output: Functions with Rank C/D/E (refactor candidates)

# Visualize architecture
sh sia/skills/visualize_architecture.sh  
# Output: dependency_graph.svg (detect layer violations)

# Check test coverage
sh sia/skills/check_coverage.sh
# Output: htmlcov/index.html (coverage gaps)
```

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

- 📖 **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- 🚀 **[DISTRIBUTION.md](DISTRIBUTION.md)** - Share with your team
- 🏗️ **[requirements/README.md](requirements/README.md)** - QUANT workflow
- 🧠 **[core/SUPER_AGENT.md](core/SUPER_AGENT.md)** - Framework architecture

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
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[⬆ Back to Top](#sia-super-intelligence-agency)

</div>

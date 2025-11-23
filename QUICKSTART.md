# SIA Framework - Quick Start Guide

**Get started with SIA in 5 minutes on any platform**

## Prerequisites

- **Git** (2.0+)
- **Python** (3.10+)
- **GitHub Copilot** subscription (required for AI orchestration)

## Installation

### Option 1: Git Submodule (Recommended)

**Why submodule**: Keep SIA updated across projects, track framework version, reuse configuration.

**Step 1**: Add SIA as submodule:

```bash
git submodule add https://github.com/gpilleux/sia.git sia
git submodule update --init --recursive
```

**Step 2**: Run installer (from project root):

**macOS / Linux:**
```bash
bash sia/installer/install.sh
```

**Windows:**
```cmd
sia\installer\install.bat
```

---

### Option 2: Standalone Clone

**Why standalone**: Single project, no multi-repo management, simpler `.gitignore`.

**macOS/Linux**:
```bash
git clone https://github.com/gpilleux/sia.git sia
bash sia/installer/install.sh
echo "sia/" >> .gitignore
```

**Windows**:
```cmd
git clone https://github.com/gpilleux/sia.git sia
sia\installer\install.bat
echo sia/ >> .gitignore
```

---

### What the Installer Does
1. ✅ Auto-detects your project structure
2. ✅ Identifies tech stack (Python, Node, FastAPI, Next.js, etc.)
3. ✅ Extracts bounded contexts from domain layer
4. ✅ Generates `.sia.detected.yaml` configuration
5. ✅ Creates `.github/copilot-instructions.md` with SIA integration

### Step 3: Verify Installation

Check that these files were created:

```bash
ls -la .sia.detected.yaml
ls -la .github/copilot-instructions.md
```

## What You Get

After installation, your project will have:

```
your-project/
├── .sia.detected.yaml          # ✅ Auto-generated config
├── .github/
│   └── copilot-instructions.md # ✅ SIA-enhanced Copilot instructions
├── sia/                        # ✅ Git submodule (framework)
│   ├── core/                   # Framework identity
│   ├── agents/                 # Reusable sub-agents
│   ├── skills/                 # Analysis tools
│   ├── requirements/           # QUANT workflow
│   └── installer/              # Installation scripts
└── ... (your existing code)
```

## Platform-Specific Notes

### macOS

**Homebrew users** (recommended):
```bash
brew install python@3.10
brew install git
pip3 install uv
```

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip git
pip3 install uv
```

### Linux (RHEL/CentOS)

```bash
sudo yum install python3 python3-pip git
pip3 install uv
```

### Windows

1. Install **Python 3.10+** from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
2. Install **Git** from [git-scm.com](https://git-scm.com/download/win)
3. Open **Command Prompt** or **PowerShell** as Administrator
4. Run: `pip install uv`

## Usage

### 1. Natural Language Requirements

Simply talk to GitHub Copilot:

```
"I need to add user authentication with JWT tokens"
```

SIA will:
1. Translate to formal requirement (REQ-XXX)
2. Perform domain analysis
3. Decompose into QUANT tasks
4. Guide implementation with DDD principles

### 2. Architecture Validation

Run automated checks:

```bash
# Check code complexity (Radon)
sh sia/skills/check_complexity.sh

# Visualize architecture (Pydeps)
sh sia/skills/visualize_architecture.sh

# Check test coverage
sh sia/skills/check_coverage.sh
```

### 3. Requirements Management

SIA implements a 7-phase QUANT lifecycle:

```
requirements/
├── REQ-001/
│   ├── REQ-001.md                  # Formal requirement
│   ├── REQ-001_domain_analysis.md  # Domain decomposition
│   └── REQ-001_quant_breakdown.md  # Task list
├── REQ-002/
└── _archive/                       # Completed requirements
```

## Configuration

### .sia.detected.yaml

Auto-generated configuration example:

```yaml
sia_version: 1.0.0
project:
  name: my-awesome-app
  type: python-fastapi-ddd
  owner: mycompany
  repo: my-awesome-app
  
domain:
  bounded_contexts:
    - Users
    - Products
    - Orders
    
spr:
  path: .agents/my-awesome-app.md
  
agents:
  active:
    - requirement_translator
    - domain_extractor
```

### Customization

You can manually edit `.sia.detected.yaml` to:
- Add custom bounded contexts
- Enable/disable specific agents
- Configure skill parameters

## Troubleshooting

### "uv: command not found"

**Solution:**
```bash
pip3 install uv
# or
python3 -m pip install uv
```

### "Python not found" (Windows)

**Solution:**
1. Reinstall Python from python.org
2. ✅ Check "Add Python to PATH"
3. Restart Command Prompt

### "Permission denied" (macOS/Linux)

**Solution:**
```bash
chmod +x sia/installer/install.sh
bash sia/installer/install.sh
```

### Auto-discovery fails

**Manual configuration:**
```bash
# Copy template
cp sia/core/sia.detected.template.yaml .sia.detected.yaml

# Edit with your project details
nano .sia.detected.yaml
```

## Next Steps

1. **Read the SPR**: Check `.github/copilot-instructions.md` to understand your project's architecture
2. **Create First Requirement**: Talk to Copilot: "I want to implement feature X"
3. **Run Skills**: Execute `sh sia/skills/check_complexity.sh` to baseline your codebase
4. **Explore Agents**: See `sia/agents/` for specialized sub-agents

## Advanced Topics

### Updating SIA Framework

```bash
cd sia
git pull origin main
cd ..
git add sia
git commit -m "chore: Update SIA framework to latest version"
```

### Using SIA in CI/CD

Add to your GitHub Actions workflow:

```yaml
- name: Check Architecture Compliance
  run: |
    sh sia/skills/check_complexity.sh
    sh sia/skills/check_coverage.sh
```

### Multi-Project Setup

SIA can manage multiple projects:

```
workspace/
├── project-a/
│   └── sia/  # git submodule → github.com/gpilleux/sia
├── project-b/
│   └── sia/  # Same framework, different config
└── project-c/
    └── sia/  # Reusable across all projects
```

## Support

- **Documentation**: [github.com/gpilleux/sia](https://github.com/gpilleux/sia)
- **Issues**: [github.com/gpilleux/sia/issues](https://github.com/gpilleux/sia/issues)
- **Examples**: See `sia/examples/` directory

## License

MIT License - see LICENSE file in SIA repository

---

**Welcome to the SIA Framework!** 🚀

Start by saying to GitHub Copilot: *"Show me what SIA detected about my project"*

# SIA Installer Scripts

This directory contains installation scripts for the SIA framework.

## Available Installers

### 🎯 Recommended: Universal Python Installer

**File**: `install.py`  
**Platforms**: macOS, Linux, Windows  
**Requirement**: Python 3.10+ (only)

```bash
python3 installer/install.py
```

**Advantages**:
- ✅ Single codebase for all platforms
- ✅ Easier to maintain and update
- ✅ Consistent behavior across systems
- ✅ **Automatic dependency detection and installation**
- ✅ **Auto-installs `uv` if missing** (no manual setup required)
- ✅ Cross-platform path handling
- ✅ Inception mode support (SIA installing itself)

---

### Legacy Platform-Specific Installers

**File**: `install.sh`  
**Platforms**: macOS, Linux  
**Requirement**: Bash

```bash
bash installer/install.sh
```

**File**: `install.bat`  
**Platforms**: Windows  
**Requirement**: Command Prompt or PowerShell

```cmd
installer\install.bat
```

**Note**: These installers are kept for backwards compatibility but may be deprecated in future versions. Use `install.py` for new installations.

---

## Installation Flow

All installers perform the same steps:

1. **Check Dependencies**
   - Python 3.10+
   - `uv` package manager (**auto-installed if missing**)
     - macOS/Linux: Uses official script `curl -LsSf https://astral.sh/uv/install.sh | sh`
     - Windows: Uses official PowerShell script
     - Fallback: `pip install uv` if official installer fails

2. **Create .sia/ Structure** (STEP 1/4)
   - `agents/` - Project-specific agent definitions
   - `knowledge/active/` - Active research and decisions
   - `knowledge/_archive/` - Archived knowledge
   - `requirements/` - Requirements management
   - `requirements/_archive/` - Completed requirements
   - `skills/` - Project automation scripts
   - `prompts/` - Slash commands (11 prompts)

3. **Run Smart Initialization** (STEP 2/4)
   - `smart_init.py` - Auto-discovery and population
   - Generates `.sia.detected.yaml`
   - Migrates legacy data if present

4. **Install Copilot Instructions** (STEP 3/4)
   - `.github/copilot-instructions.md`
   - Template with placeholders for customization

5. **Repository Initialization** (STEP 4/4)
   - User must activate via Copilot: "Initialize SIA for this repository"

---

## Support Scripts

### `auto_discovery.py`

Analyzes project structure and generates `.sia.detected.yaml`:
- Detects tech stack (Python, Node, FastAPI, Next.js, etc.)
- Extracts bounded contexts from domain layer
- Identifies database technologies
- Maps project structure

**Note**: Called automatically by `smart_init.py`.

### `smart_init.py`

Orchestrates the initialization process:
- Creates directory structure
- Checks for legacy data (no migration)
- Populates default content
- Runs auto-discovery
- Cleans up temporary files

**Note**: Called automatically by main installer.

### `generate_instructions.py`

Generates customized Copilot instructions from template:
- Reads `.sia.detected.yaml`
- Replaces placeholders in template
- Creates `.github/copilot-instructions.md`

**Note**: Can be run manually if auto-generated instructions need refresh.

---

## Development Notes

### Adding New Features

When adding features to the installer:

1. **Update `install.py` first** (primary implementation)
2. **Port to `install.sh`** (maintain parity)
3. **Port to `install.bat`** (maintain parity)
4. **Update this README** with new behavior

### Testing

Test on all three platforms before release:

```bash
# macOS/Linux
python3 installer/install.py
bash installer/install.sh

# Windows
python installer\install.py
installer\install.bat
```

Verify all installers create identical directory structures.

---

## Troubleshooting

### Python not found

**Error**: `python3: command not found` or `python: command not found`

**Solution**:
- macOS/Linux: `brew install python@3.10` or `sudo apt install python3`
- Windows: Download from [python.org](https://www.python.org/downloads/)

### uv installation fails

**Error**: `Failed to install uv`

**Solution**:
```bash
# Manual installation
pip3 install --user uv
# or
python3 -m pip install --user uv
```

### Permission denied (macOS/Linux)

**Error**: `bash: installer/install.sh: Permission denied`

**Solution**:
```bash
chmod +x installer/install.sh
bash installer/install.sh
```

### smart_init.py not found

**Error**: `smart_init.py not found`

**Solution**:
- Ensure you're running installer from project root (not from `sia/` directory)
- Verify SIA submodule is properly initialized: `git submodule update --init --recursive`

---

## Version History

- **v1.2.0** (2025-11-28): Added universal Python installer (`install.py`)
- **v1.1.0** (2025-11-25): Added slash commands installation
- **v1.0.0** (2025-11-20): Initial release with platform-specific installers

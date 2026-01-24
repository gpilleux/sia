# SIA Installer - Legacy Directory

> ⚠️ **DEPRECATED**: This directory contains legacy installer scripts kept for reference only.
> 
> **Use the new uvx installation method:**
> ```bash
> uvx --from git+https://github.com/gpilleux/sia.git sia-framework init
> ```

## New Installation (Recommended)

```bash
# Install SIA in any project
uvx --from git+https://github.com/gpilleux/sia.git sia-framework init

# Update copilot-instructions.md
uvx --from git+https://github.com/gpilleux/sia.git sia-framework update

# Check installation health
uvx --from git+https://github.com/gpilleux/sia.git sia-framework doctor
```

## Legacy Files

The Python files in this directory are kept for reference and development purposes:

- `install.py` - Original universal installer (now in `src/sia_framework/installer/`)
- `auto_discovery.py` - Project analysis script
- `smart_init.py` - Initialization orchestrator
- `generate_instructions.py` - Regenerate copilot-instructions.md

## For Developers

If you're developing SIA itself, the actual installer code is now in:
```
src/sia_framework/
├── cli.py              # Entry point (sia-framework command)
├── installer/
│   ├── install.py      # Main installer
│   ├── auto_discovery.py
│   ├── smart_init.py
│   └── generate_instructions.py
├── templates/          # Template files
├── core/               # Core documentation
├── agents/             # Agent definitions
└── skills/             # Automation skills
```

## Version History

- **v2.0.0** (2026-01-23): Migrated to uvx installation via PyPI
- **v1.2.0** (2025-11-28): Added universal Python installer (`install.py`)
- **v1.1.0** (2025-11-25): Added slash commands installation
- **v1.0.0** (2025-11-20): Initial release with platform-specific installers

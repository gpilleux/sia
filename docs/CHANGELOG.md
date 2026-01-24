# Changelog

All notable changes to the SIA (Super Intelligence Agency) framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-23

### Breaking Changes
- **Migrated to uvx Installation**
  - Removed git submodule installation method
  - New installation: `uvx --from git+https://github.com/gpilleux/sia.git sia-framework init`
  - Package now distributed as `sia-framework` via pip/uvx
  - Removed legacy shell installers (`install.sh`, `install.bat`)

### Added
- **CLI Entry Point** (`src/sia_framework/cli.py`)
  - `sia-framework init` - Initialize SIA in current directory
  - `sia-framework update` - Regenerate copilot-instructions.md
  - `sia-framework doctor` - Check installation health
  - Built with Click for robust argument parsing
- **Package Structure** (`src/sia_framework/`)
  - Proper Python package with `pyproject.toml` build system
  - Uses `hatchling` for building wheels
  - Includes all templates, core docs, agents, and skills as package data
  - Dependencies: `pyyaml>=6.0`, `click>=8.0`
- **Package Mode Detection**
  - Installer detects running as installed package vs development mode
  - Uses `importlib.resources` for accessing package data files
  - Inception mode preserved for SIA self-development

### Changed
- **Simplified Installation**
  - From 3 steps (submodule + install.py + init) to 1 command
  - No more `.gitmodules` or submodule management
  - Cleaner project structure without `sia/` subdirectory
- **Version Reset to 1.0.0**
  - Starting semantic versioning from this major release
  - All previous versions considered pre-release/beta

### Removed
- `installer/install.sh` - Legacy bash installer
- `installer/install.bat` - Legacy Windows batch installer
- Git submodule installation method

## [Unreleased]

### Added
- **File Reader Skills System** (`templates/skills/file_readers/`, REQ-011)
  - Zero-setup text extraction from DOCX, XLSX, PDF files
  - Ephemeral dependencies via `uv run --with {library}`
  - Strategy pattern with auto-discovery registry (`AbstractFileReader`)
  - CLI facades: `read_docx.py`, `read_xlsx.py`, `read_pdf.py`
  - Universal CLI: `read_file.py` (auto-detect format by extension)
  - Comprehensive error handling (corrupted files, password-protected, unsupported formats)
  - Memory-efficient implementations:
    - DOCX: `iter_inner_content()` for nested elements extraction
    - XLSX: `read_only=True` mode for 10x memory reduction
    - PDF: `get_text(sort=True)` for natural reading order
  - Installer integration: Auto-copies `file_readers/` module to `.sia/skills/`
  - `/sync` prompt integration: Synchronizes file readers on framework updates
  - Documentation: `skills/README.md` with non-technical usage examples
  - Test coverage: 96% on core module, 85%+ on readers
  - Exit code hygiene: 0=success, 1=file error, 2=unexpected
  - Output separation: stdout=text, stderr=errors
  - **Implementation**: Strategy + Registry pattern (DDD compliant)
  - **Dependencies**: python-docx, openpyxl, PyMuPDF (ephemeral via uv)
  - **Cross-platform**: macOS, Linux, Windows compatible
- **Automatic UV Installation** (`installer/install.py`)
  - Detects missing `uv` and installs automatically using official installers
  - macOS/Linux: Uses `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows: Uses PowerShell script `irm https://astral.sh/uv/install.ps1 | iex`
  - Fallback to `pip install uv` if official installer fails
  - 2-minute timeout with graceful error handling
  - Zero manual dependency setup required
- **Inception Mode Support** (`installer/install.py`)
  - Installer now detects when running in SIA framework itself
  - Auto-configures paths for self-installation (dogfooding)
  - Enables SIA to use its own tooling during development
  - `.sia/prompts/` properly synced from `templates/prompts/`
- **Automated Installer Testing Suite** (`tests/test_installer.py`)
  - 11 comprehensive tests covering all installation scenarios
  - Isolated temporary environment testing (no local contamination)
  - Cross-platform validation (macOS, Linux, Windows via Docker)
  - Test coverage for: directory creation, README generation, config files, slash commands, gitignore, auto-discovery
  - Idempotency tests ensuring safe re-runs
  - Test documentation (`tests/README.md`)
  - pytest configuration (`pyproject.toml`)
  - **Validates**: All three installers produce identical results
- **Universal Python Installer** (`installer/install.py`)
  - Single cross-platform installer for macOS, Linux, and Windows
  - Replaces platform-specific bash/batch scripts as primary installation method
  - Automatic dependency detection and installation
  - Consistent behavior across all operating systems
  - Legacy installers (`install.sh`, `install.bat`) kept for backwards compatibility
- **Installer Documentation** (`installer/README.md`)
  - Comprehensive guide for all installation methods
  - Troubleshooting section for common issues
  - Development guidelines for maintaining installers
  - Version history and migration path

### Changed
- **Slash Commands Architecture** (`templates/prompts/`)
  - Established `templates/prompts/` as **single source of truth**
  - Removed redundant `prompts/` directory (DRY violation)
  - `.sia/prompts/` now auto-synced during installation
  - Updated documentation with inception pattern workflow
  - Clear update protocol: edit templates → re-run installer → commit
- **Enhanced .gitignore**
  - Added `.env` and environment variable file patterns
  - Added comprehensive virtual environment exclusions
  - Added OS-specific files (macOS, Windows, Linux)
  - Added type checking caches (mypy, pyright, pyre)
  - Added database files and secrets patterns
  - Added UV cache directory
  - Organized by category for maintainability
- **Documentation Updates** (README, QUICKSTART, DISTRIBUTION)
  - Prioritize universal Python installer in all guides
  - Moved platform-specific installers to "legacy" status
  - Simplified installation instructions
  - Added explicit warnings about future deprecation of shell scripts
- **Installer Synchronization** (`install.sh`, `install.bat`)
  - Synchronized both legacy installers with `install.py` feature parity
  - Added slash commands installation (`.sia/prompts/*.prompt.md`)
  - Added VS Code settings creation (`.vscode/settings.json`)
  - Added `.gitignore` template installation
  - Replaced `auto_discovery.py` → `smart_init.py` call
  - Added Copilot instructions installation step
  - Improved README formatting (multi-line echo blocks)

### Fixed
- **Test Suite Corrections**
  - Fixed `.gitignore` validation test (template marker detection)
  - Fixed `.sia.detected.yaml` format test (nested YAML structure)
  - Registered `docker` pytest marker to eliminate warnings
- **Inception Pattern Implementation**
  - Eliminated duplicate `prompts/` directory
  - SIA framework now properly uses `.sia/` structure
  - Installer correctly detects self-installation context

### Added (Previous)
- **Microsoft Suite Specialist Agent** (`agents/microsoft_suite_specialist.md`)
  - Microsoft 365 expertise (SharePoint, OneDrive, Teams, Graph API)
  - Google Workspace → Microsoft 365 migration playbook
  - SharePoint configuration patterns (hub sites, content types, permissions, search)
  - Microsoft Graph API integration (batching, delta queries, throttling)
  - Power Platform guidance (Power Automate, Power Apps)
  - Governance & compliance (retention, DLP, sensitivity labels, eDiscovery)
  - **MCP Tools Reference** (`agents/microsoft_suite_specialist_mcp_tools.md`):
    - Lokka (@merill/lokka) - Unified Graph API interface (✅ authenticated)
    - MS-365-MCP (@softeria/ms-365-mcp-server) - 45 specialized tools (calendar, mail, OneDrive, Excel, Planner)
    - CLI-Microsoft365 (@pnp/cli-microsoft365-mcp-server) - 600+ SharePoint/Teams commands
    - Real tool invocations, authentication workflows, permission requirements, troubleshooting
  - **Quick Start Guide** (`agents/microsoft_suite_specialist_quickstart.md`) - <10 min setup with validation checklist
  - **Update Summary** (`agents/MICROSOFT_SUITE_MCP_UPDATE_SUMMARY.md`) - Documentation evolution and impact assessment
  - Latent Space Activation (LSA) - cognitive priming for SharePoint expertise
  - SPR-compressed format (<5k tokens, high-density knowledge)
  - Examples updated with real MCP invocations (Lokka batch requests, Graph API calls)
- **Agents Catalog** (`agents/README.md`)
  - Comprehensive agent directory with capabilities and selection guide
  - Agent communication protocol documentation
  - MCP-first workflow standards
  - Agent creation checklist and quality standards
  - LSA (Latent Space Activation) guidelines for new agents
- **Expert Agent Creation Skill** (`skills/create_expert_agent.md`)
  - Systematic 7-phase methodology for creating domain-specialist agents
  - Evidence-based approach using MCP Deepwiki research
  - LSA (Latent Space Activation) design patterns
  - SPR compression techniques for agents
  - Quality validation checklists
  - Example: Microsoft Suite agent creation documented
  - Time estimate: 60-90 minutes per agent
- **Microsoft Suite Usage Examples** (`agents/microsoft_suite_specialist_examples.md`)
  - 4 real-world scenarios (permissions, migration, search, API optimization)
  - Code examples in PowerShell, Python, Graph API
  - MCP setup guide with Azure authentication
  - Verification checklists for each scenario

## [0.2.0] - 2025-11-23 (Pre-release)

### Added
- **Context Hygiene Protocol** (`core/PROMPT_PLACEMENT.md`)
  - Categorization: PERMANENT, ONE-TIME, CONDITIONAL, SESSION prompts
  - Decision matrix for prompt placement
  - Pay-per-use context pattern
  - 60% token reduction for baseline context (6k → 3k tokens)
- **Standalone Installation Option**
  - Git clone alternative to submodule (`README.md`, `QUICKSTART.md`)
  - Simple `.gitignore` pattern for single-project use
- **One-Time Init Protocol** (`templates/INIT_REQUIRED.template.md`)
  - Separated from permanent context (auto-cleanup post-init)
  - 6-step initialization workflow
  - Project SPR generation guide
- **Uninstall Guide** (`UNINSTALL.md`)
  - Manual removal steps (prevents accidental deletion)
  - Verification checklist
  - Troubleshooting FAQ
- **Distribution Documentation** (`DISTRIBUTION.md`)
  - Team onboarding guide
  - Platform-specific installation notes
  - Example projects showcase
- **Cross-Platform Installers**
  - Enhanced `install.sh` (macOS/Linux) with error handling
  - New `install.bat` (Windows) with auto-detection
  - Auto-creates `.sia/` structure (agents, knowledge, requirements, skills)
- **Project SPR Template** (`templates/PROJECT_SPR.template.md`)
  - Structured format for 10k lines → 2k tokens compression
  - Mental Model Compression section
  - Key Invariants documentation

### Changed
- **Installer Workflow**: Now 3-step process (structure → auto-discovery → init prompt)
- **copilot-instructions.template.md**: Removed init protocol (moved to separate file)
- **README.md**: Enhanced with badges, installation options, attractive formatting

### Fixed
- Context contamination from one-time prompts in permanent template
- Missing platform detection in installer scripts

## [0.1.0] - 2025-11-20 (Pre-release)

### Added
- **Core Framework**
  - SUPER AGENT meta-cognitive orchestration (`core/SUPER_AGENT.md`)
  - Auto-discovery protocol for repository bootstrapping
  - Requirements management system (7-phase QUANT workflow)
  - Skills catalog (complexity, architecture, coverage tools)
- **Specialized Sub-Agents**
  - SIA Agent: DDD/SOLID/KISS architect + AI-Native specialist
  - Repository Guardian: DDD enforcement and pattern validation
  - Research Specialist: Deepwiki protocol for domain research
- **Requirements System** (`requirements/`)
  - REQUIREMENT_TEMPLATE.md for capture
  - DOMAIN_ANALYSIS_TEMPLATE.md for research
  - QUANT_BREAKDOWN_TEMPLATE.md for decomposition
  - Archive protocol (`_archive/` pattern)
- **Skills System** (`skills/`)
  - `check_complexity.sh`: Radon cyclomatic complexity
  - `visualize_architecture.sh`: Pydeps dependency graphs
  - `check_coverage.sh`: pytest-cov HTML reports
  - `audit_ddd.py`: DDD compliance checker
- **Auto-Discovery** (`installer/auto_discovery.py`)
  - Git identity detection
  - Tech stack recognition (Python, Node, FastAPI, Next.js)
  - Bounded context extraction
  - `.sia.detected.yaml` generation
- **Documentation**
  - QUICKSTART.md: 5-minute setup guide
  - STANDARDS.md: DDD/SOLID/KISS principles
  - AUTO_DISCOVERY.md: Discovery protocol specification

### Philosophy
- Zero Configuration: Auto-discovers project context
- Non-Invasive: Works alongside existing workflows
- Reusable: Same framework across multiple projects
- Evolvable: Learns and adapts from each project
- Traceable: Every decision has a requirement trace

---

## Version History Summary

- **1.0.0**: uvx installation, package distribution, CLI entry point
- **0.2.0**: Context hygiene, standalone install, distribution readiness (pre-release)
- **0.1.0**: Initial framework release with SUPER AGENT orchestration (pre-release)

---

**Note**: For migration guides between versions, see `docs/MIGRATION.md` (when available).

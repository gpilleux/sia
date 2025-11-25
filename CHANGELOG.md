# Changelog

All notable changes to the SIA (Super Intelligence Agency) framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-24

### Added
- **Task Timer Skill** (`skills/task_timer.py`, `skills/task_timer.md`)
  - QUANT task chronometer with background persistence
  - Actual vs estimated time tracking (AI prediction vs LLM hallucination)
  - Human team comparison baseline (4x multiplier)
  - Correction factor generation from historical variance
  - Metrics report with prediction insights
  - JSON state persistence (~/.sia/timer_state.json, ~/.sia/task_metrics.json)
- **UV Package Manager Standard** (`core/UV_STANDARD.md`)
  - Mandatory `uv` usage for all Python scripts
  - Shebang pattern: `#!/usr/bin/env uv run python`
  - Zero-config isolated environments
  - 10-100x faster than pip (Rust-based resolver)
  - Migration guide from python3/pip workflows
  - Anti-patterns documentation
  - Skill development checklist

### Changed
- **Skills README** - Added task_timer skill entry with `uv run` commands
- **FASE 5 Integration** - Timer workflow in verification gates pattern

### Fixed
- Division by zero in metrics report when tasks complete instantly

## [1.1.0] - 2025-11-23

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

## [1.0.0] - 2025-11-20

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

- **1.1.0**: Context hygiene, standalone install, distribution readiness
- **1.0.0**: Initial framework release with SUPER AGENT orchestration

---

**Note**: For migration guides between versions, see `docs/MIGRATION.md` (when available).

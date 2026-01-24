#!/usr/bin/env python3
"""
SIA Framework Universal Installer
Cross-platform installer for macOS, Linux, and Windows
Supports both package mode (uvx) and inception mode (development)
"""

import platform
import shutil
import sys
from pathlib import Path
from typing import Union

try:
    from importlib.resources import files, as_file
    from importlib.abc import Traversable
except ImportError:
    from importlib_resources import files, as_file
    from importlib_resources.abc import Traversable


def get_package_path() -> Path:
    """Get the path to the sia_framework package resources."""
    return files("sia_framework")


class SIAInstaller:
    def __init__(self, force: bool = False):
        self.platform = platform.system()
        self.root = Path.cwd()
        self.force = force

        # Detect installation mode
        self.mode = self._detect_mode()

        self.sia_dir = self.root / ".sia"
        self.vscode_dir = self.root / ".vscode"
        self.github_dir = self.root / ".github"

    def _detect_mode(self) -> str:
        """Detect installation mode: 'package' or 'inception'.

        - inception: Running from SIA repository itself (development mode)
        - package: Running as installed package via uvx
        """
        # Check if we're in SIA repo (has installer/ and src/sia_framework/)
        if (self.root / "src" / "sia_framework").exists():
            return "inception"
        return "package"

    def _get_framework_path(self) -> Union[Path, "Traversable"]:
        """Get the path to framework resources based on mode."""
        if self.mode == "inception":
            return self.root / "src" / "sia_framework"
        else:
            return get_package_path()

    def _read_resource(self, *path_parts: str) -> str:
        """Read a text resource from the package."""
        framework = self._get_framework_path()

        if self.mode == "inception":
            resource_path = framework
            for part in path_parts:
                resource_path = resource_path / part
            return resource_path.read_text(encoding="utf-8")
        else:
            resource = framework
            for part in path_parts:
                resource = resource.joinpath(part)
            return resource.read_text(encoding="utf-8")

    def _copy_resource(self, src_parts: tuple, dst: Path):
        """Copy a resource from the package to destination."""
        framework = self._get_framework_path()

        if self.mode == "inception":
            src_path = framework
            for part in src_parts:
                src_path = src_path / part
            if src_path.exists():
                shutil.copy(src_path, dst)
        else:
            resource = framework
            for part in src_parts:
                resource = resource.joinpath(part)
            with as_file(resource) as src_path:
                if src_path.exists():
                    shutil.copy(src_path, dst)

    def _copy_resource_dir(self, src_parts: tuple, dst_dir: Path):
        """Copy a resource directory from the package to destination."""
        framework = self._get_framework_path()

        if self.mode == "inception":
            src_path = framework
            for part in src_parts:
                src_path = src_path / part
            if src_path.exists() and src_path.is_dir():
                for item in src_path.rglob("*"):
                    if item.is_file():
                        rel_path = item.relative_to(src_path)
                        dst_file = dst_dir / rel_path
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy(item, dst_file)
        else:
            resource = framework
            for part in src_parts:
                resource = resource.joinpath(part)
            with as_file(resource) as src_path:
                if src_path.exists() and src_path.is_dir():
                    for item in src_path.rglob("*"):
                        if item.is_file():
                            rel_path = item.relative_to(src_path)
                            dst_file = dst_dir / rel_path
                            dst_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy(item, dst_file)

    def _resource_exists(self, *path_parts: str) -> bool:
        """Check if a resource exists in the package."""
        framework = self._get_framework_path()

        if self.mode == "inception":
            resource_path = framework
            for part in path_parts:
                resource_path = resource_path / part
            return resource_path.exists()
        else:
            try:
                resource = framework
                for part in path_parts:
                    resource = resource.joinpath(part)
                with as_file(resource) as path:
                    return path.exists()
            except (FileNotFoundError, TypeError):
                return False

    def run(self):
        """Main installation flow"""
        self._print_header()
        self._check_dependencies()
        self._create_structure()
        self._run_smart_init()
        self._install_copilot_instructions()
        self._print_success()

    def _print_header(self):
        print()
        print("=" * 48)
        print(f" SIA Framework Installer ({self.platform})")
        print(f" Mode: {self.mode}")
        print("=" * 48)
        print()

    def _check_dependencies(self):
        """Check for Python version"""
        print("[INFO] Checking dependencies...")

        # Check Python version
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 10):
            print(
                f"[ERROR] Python 3.10+ required (found {version.major}.{version.minor})"
            )
            self._print_install_help("python")
            sys.exit(1)

        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")

    def _create_structure(self):
        """Create .sia/ directory structure with README files"""
        print()
        print("[STEP 1/4] Creating .sia/ Directory Structure...")
        print("-" * 48)

        # Create directories
        directories = [
            self.sia_dir / "agents",
            self.sia_dir / "knowledge" / "active",
            self.sia_dir / "knowledge" / "_archive",
            self.sia_dir / "requirements",
            self.sia_dir / "requirements" / "_archive",
            self.sia_dir / "skills",
            self.sia_dir / "prompts",
            self.vscode_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        # Create README files
        self._create_readme_files()

        # Copy INIT_REQUIRED template
        init_dst = self.sia_dir / "INIT_REQUIRED.md"
        if self._resource_exists("templates", "INIT_REQUIRED.template.md"):
            self._copy_resource(("templates", "INIT_REQUIRED.template.md"), init_dst)

        # Copy slash commands (prompts)
        print("   📋 Installing slash commands...")
        prompts_dst = self.sia_dir / "prompts"
        self._copy_resource_dir(("templates", "prompts"), prompts_dst)

        # Install file reader skills
        print("   📚 Installing file reader skills...")
        file_readers_dst = self.sia_dir / "skills" / "file_readers"
        file_readers_dst.mkdir(parents=True, exist_ok=True)
        self._copy_resource_dir(
            ("templates", "skills", "file_readers"), file_readers_dst
        )

        # Copy CLI facades (read_*.py)
        skills_dst = self.sia_dir / "skills"
        if self.mode == "inception":
            skills_src = self._get_framework_path() / "templates" / "skills"
            if skills_src.exists():
                for facade_file in skills_src.glob("read_*.py"):
                    dst_file = skills_dst / facade_file.name
                    shutil.copy(facade_file, dst_file)
                    if self.platform in ["Darwin", "Linux"]:
                        dst_file.chmod(0o755)
        else:
            # For package mode, copy read_*.py files
            framework = self._get_framework_path()
            try:
                skills_resource = framework.joinpath("templates", "skills")
                with as_file(skills_resource) as skills_path:
                    if skills_path.exists():
                        for facade_file in skills_path.glob("read_*.py"):
                            dst_file = skills_dst / facade_file.name
                            shutil.copy(facade_file, dst_file)
                            if self.platform in ["Darwin", "Linux"]:
                                dst_file.chmod(0o755)
            except (FileNotFoundError, TypeError):
                pass

        print("   ✅ File readers installed (DOCX, XLSX, PDF)")

        # Install SIA Core (Super Agent brain)
        print("   🧠 Installing SIA core (Super Agent context)...")
        core_dst = self.sia_dir / "core"
        core_dst.mkdir(parents=True, exist_ok=True)
        self._copy_resource_dir(("core",), core_dst)
        print("   ✅ Core installed (SUPER_AGENT, CONCEPTS, STANDARDS)")

        # Install Framework Agents
        print("   🤖 Installing framework agents...")
        agents_dst = self.sia_dir / "agents" / "_framework"
        agents_dst.mkdir(parents=True, exist_ok=True)
        self._copy_resource_dir(("agents",), agents_dst)
        print("   ✅ Framework agents installed (repository_guardian, research_specialist)")

        # Install additional skills (create_expert_agent, etc.)
        print("   🛠️  Installing additional skills...")
        skills_dst = self.sia_dir / "skills"
        self._copy_resource_dir(("skills",), skills_dst)
        print("   ✅ Skills installed (create_expert_agent, etc.)")

        # Install reference templates
        print("   📄 Installing reference templates...")
        templates_dst = self.sia_dir / "templates"
        templates_dst.mkdir(parents=True, exist_ok=True)
        # Copy specific templates (not prompts or skills, those are already handled)
        # Note: INIT_REQUIRED.template.md is already copied as .sia/INIT_REQUIRED.md
        for template_name in ["PROJECT_SPR.template.md", "DEFAULT_STACK.md"]:
            if self._resource_exists("templates", template_name):
                self._copy_resource(("templates", template_name), templates_dst / template_name)
        print("   ✅ Reference templates installed")

        # Install VS Code settings
        vscode_settings = self.vscode_dir / "settings.json"
        if vscode_settings.exists() and not self.force:
            print("   ⚠️  .vscode/settings.json already exists, skipping...")
        else:
            print("   📝 Creating .vscode/settings.json...")
            self._install_vscode_settings()

        # Install .gitignore
        gitignore_path = self.root / ".gitignore"
        if gitignore_path.exists() and not self.force:
            print("   ⚠️  .gitignore already exists, skipping...")
        else:
            print("   📝 Creating .gitignore from template...")
            if self._resource_exists("templates", "gitignore.template"):
                self._copy_resource(("templates", "gitignore.template"), gitignore_path)

        print("   ✅ .sia/ structure created")
        print("   ✅ .sia/core/ Super Agent brain installed")
        print("   ✅ .sia/agents/_framework/ framework agents installed")
        print("   ✅ .sia/skills/ all skills installed")
        print("   ✅ .sia/prompts/ slash commands installed")
        print("   ✅ .sia/templates/ reference templates installed")
        print("   ✅ .vscode/settings.json configured")
        print("   ✅ .sia/INIT_REQUIRED.md created (one-time init instructions)")

    def _create_readme_files(self):
        """Create README.md files in .sia subdirectories"""
        readmes = {
            self.sia_dir / "README.md": """# SIA Project Configuration

This directory contains the SIA framework integration for this project.

## Structure
- `core/`: SIA core context (SUPER_AGENT, CONCEPTS, STANDARDS)
- `agents/`: Project agents + `_framework/` (repository_guardian, etc.)
- `knowledge/`: Active and archived knowledge base
- `requirements/`: Requirements management (active and archived)
- `skills/`: All skills (file readers, create_expert_agent, etc.)
- `prompts/`: Slash commands for Copilot
- `templates/`: Reference templates (PROJECT_SPR, DEFAULT_STACK)

See SIA Framework documentation for complete reference.
""",
            self.sia_dir / "agents" / "README.md": """# Project Agents

Project-specific agents go here. Framework agents are in `_framework/`.

The SUPER AGENT will create your project SPR during initialization.

## Next Steps
Ask GitHub Copilot: "Initialize SIA agents for this repository"

## Framework Agents (in _framework/)
- repository_guardian.md - DDD/SOLID enforcement
- research_specialist.md - Domain research
- compliance_officer.md - QUANT compliance
- sia.md - Core SIA agent
""",
            self.sia_dir
            / "knowledge"
            / "active"
            / "README.md": """# Active Knowledge Base

Active research, decisions, and domain knowledge.

## Document Lifecycle
Documents are archived after project milestones.
""",
            self.sia_dir / "requirements" / "README.md": """# Requirements Management

## Quick Start
1. Define requirements in natural language
2. SUPER AGENT decomposes into QUANT tasks
3. Execute, verify, archive
""",
            self.sia_dir / "skills" / "README.md": """# Project Skills

## Installed Skills

### File Readers
- `read_docx.py` - Extract text from Word documents
- `read_xlsx.py` - Extract text from Excel spreadsheets
- `read_pdf.py` - Extract text from PDF files
- `read_file.py` - Universal reader (auto-detect format)

### Agent Creation
- `create_expert_agent.md` - Guide for creating expert agents
- `create_agent_cli.py` - CLI for agent scaffolding

## Usage
```bash
uv run .sia/skills/read_file.py document.pdf
```
""",
        }

        for path, content in readmes.items():
            path.write_text(content, encoding="utf-8")

    def _install_vscode_settings(self):
        """Install VS Code settings with placeholder replacement"""
        if not self._resource_exists("templates", "vscode-settings.template.json"):
            return

        content = self._read_resource("templates", "vscode-settings.template.json")
        content = content.replace("{{LOCALE}}", "en")
        content = content.replace("{{EXTRA_PATHS}}", "")

        (self.vscode_dir / "settings.json").write_text(content, encoding="utf-8")

    def _run_smart_init(self):
        """Run smart initialization (auto-discovery + population)"""
        print()
        print("[STEP 2/4] Running Smart Initialization...")
        print("-" * 48)

        from .smart_init import SmartInit

        smart_init = SmartInit(str(self.root), mode=self.mode)
        smart_init.run()

    def _install_copilot_instructions(self):
        """Install GitHub Copilot instructions"""
        print()
        print("-" * 48)
        print("[STEP 3/4] Installing Copilot Instructions...")
        print("-" * 48)

        self.github_dir.mkdir(exist_ok=True)

        copilot_instructions = self.github_dir / "copilot-instructions.md"

        if copilot_instructions.exists() and not self.force:
            print("   ⚠️  .github/copilot-instructions.md already exists, skipping...")
        else:
            print("   📝 Creating .github/copilot-instructions.md from template...")
            if self._resource_exists("core", "copilot-instructions.template.md"):
                self._copy_resource(
                    ("core", "copilot-instructions.template.md"), copilot_instructions
                )
                print("   ⚠️  Manual customization required:")
                placeholders = [
                    "{{PROJECT_NAME}}",
                    "{{PROJECT_TYPE}}",
                    "{{BOUNDED_CONTEXTS}}",
                    "{{PROJECT_SPR_CONTENT}}",
                    "{{REQUIREMENTS_STATUS}}",
                ]
                for placeholder in placeholders:
                    print(f"      - {placeholder}")

    def _print_success(self):
        """Print success message and next steps"""
        print()
        print("-" * 48)
        print("[STEP 4/4] Repository Initialization Required")
        print("-" * 48)
        print()
        print("[SUCCESS] SIA Installation Complete!")
        print()
        print("  Created:")
        print("  - .sia/core/ - Super Agent brain (SUPER_AGENT, CONCEPTS, STANDARDS)")
        print("  - .sia/agents/_framework/ - Framework agents (guardian, specialist)")
        print("  - .sia/skills/ - All skills (file readers, create_expert_agent)")
        print("  - .sia/prompts/ - Slash commands (17 commands)")
        print("  - .sia/templates/ - Reference templates (PROJECT_SPR, DEFAULT_STACK)")
        print("  - .sia/knowledge/ - Knowledge base structure")
        print("  - .sia/requirements/ - Requirements management")
        print("  - .vscode/settings.json - VS Code configuration")
        print("  - .github/copilot-instructions.md - Copilot context")
        print("  - .sia.detected.yaml - Auto-detected project config")
        print()
        print("⚠️  IMPORTANT: Repository requires SUPER AGENT initialization")
        print()
        print("Next steps:")
        print("  1. Open this project in VS Code with GitHub Copilot")
        print("  2. Ask Copilot: 'Initialize SIA for this repository'")
        print()
        print("     The SUPER AGENT will:")
        print("     - Read .sia/core/SUPER_AGENT.md for context")
        print("     - Analyze repository structure and domain")
        print("     - Generate project SPR (.sia/agents/<project>.md)")
        print("     - Detect specialized agents")
        print("     - Create initial knowledge base")
        print("     - Delete .sia/INIT_REQUIRED.md (auto-cleanup)")
        print()
        print("📖 Documentation: https://github.com/gpilleux/sia")
        print()

    def _print_install_help(self, tool: str):
        """Print platform-specific installation instructions"""
        if tool == "python":
            print()
            print("Please install Python 3.10+ from:")
            if self.platform == "Darwin":
                print("  brew install python@3.10")
            elif self.platform == "Linux":
                print("  sudo apt install python3 python3-pip  # Debian/Ubuntu")
                print("  sudo yum install python3 python3-pip  # RHEL/CentOS")
            elif self.platform == "Windows":
                print("  https://www.python.org/downloads/")
            print()


def main():
    installer = SIAInstaller()
    installer.run()


if __name__ == "__main__":
    main()

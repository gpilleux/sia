#!/usr/bin/env python3
"""
SIA Framework Universal Installer
Cross-platform installer for macOS, Linux, and Windows
Usage: python3 installer/install.py
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


class SIAInstaller:
    def __init__(self):
        self.platform = platform.system()
        self.root = Path.cwd()
        self.sia_framework = self.root / "sia"
        self.sia_dir = self.root / ".sia"
        self.vscode_dir = self.root / ".vscode"
        self.github_dir = self.root / ".github"
        
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
        print("=" * 48)
        print()
        
    def _check_dependencies(self):
        """Check for Python and uv"""
        print("[INFO] Checking dependencies...")
        
        # Check Python version
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 10):
            print(f"[ERROR] Python 3.10+ required (found {version.major}.{version.minor})")
            self._print_install_help("python")
            sys.exit(1)
        
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
        
        # Check uv
        if not self._command_exists("uv"):
            print("[INFO] 'uv' not installed. Installing...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "uv"], 
                             check=True, capture_output=True)
                print("   ✓ uv installed")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to install uv: {e}")
                sys.exit(1)
        else:
            print("   ✓ uv installed")
            
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
        init_template = self.sia_framework / "templates" / "INIT_REQUIRED.template.md"
        if init_template.exists():
            shutil.copy(init_template, self.sia_dir / "INIT_REQUIRED.md")
            
        # Copy slash commands (prompts)
        print("   📋 Installing slash commands...")
        prompts_src = self.sia_framework / "templates" / "prompts"
        if prompts_src.exists():
            for prompt_file in prompts_src.glob("*.prompt.md"):
                shutil.copy(prompt_file, self.sia_dir / "prompts" / prompt_file.name)
                
        # Install VS Code settings
        vscode_settings = self.vscode_dir / "settings.json"
        if vscode_settings.exists():
            print("   ⚠️  .vscode/settings.json already exists, skipping...")
            print("      Review sia/templates/vscode-settings.template.json for recommended settings")
        else:
            print("   📝 Creating .vscode/settings.json...")
            self._install_vscode_settings()
            
        # Install .gitignore
        gitignore_path = self.root / ".gitignore"
        if gitignore_path.exists():
            print("   ⚠️  .gitignore already exists, skipping...")
            print("      Review sia/templates/gitignore.template for recommended exclusions")
        else:
            print("   📝 Creating .gitignore from template...")
            gitignore_template = self.sia_framework / "templates" / "gitignore.template"
            if gitignore_template.exists():
                shutil.copy(gitignore_template, gitignore_path)
                
        print("   ✅ .sia/ structure created")
        print("   ✅ .sia/prompts/ slash commands installed")
        print("   ✅ .vscode/settings.json configured")
        print("   ✅ .sia/INIT_REQUIRED.md created (one-time init instructions)")
        
    def _create_readme_files(self):
        """Create README.md files in .sia subdirectories"""
        readmes = {
            self.sia_dir / "README.md": """# SIA Project Configuration

This directory contains the SIA framework integration for this project.

## Structure
- `agents/`: Project-specific agent definitions
- `knowledge/`: Active and archived knowledge base
- `requirements/`: Requirements management (active and archived)
- `skills/`: Project-specific automation skills

See `sia/README.md` for complete framework documentation.
""",
            self.sia_dir / "agents" / "README.md": """# Project Agents

Define project-specific agents here. The SUPER AGENT will populate this
directory during repository initialization.

## Next Steps
Ask GitHub Copilot: "Initialize SIA agents for this repository"
""",
            self.sia_dir / "knowledge" / "active" / "README.md": """# Active Knowledge Base

Active research, decisions, and domain knowledge.

## Document Lifecycle
See `.github/DOCUMENT_LIFECYCLE.md` for archival protocol.
""",
            self.sia_dir / "requirements" / "README.md": """# Requirements Management

See `sia/requirements/README.md` for complete workflow.

## Quick Start
1. Define requirements in natural language
2. SUPER AGENT decomposes into QUANT tasks
3. Execute, verify, archive
""",
            self.sia_dir / "skills" / "README.md": """# Project Skills

Project-specific automation scripts.

## Framework Skills
Reusable skills available in `sia/skills/`
"""
        }
        
        for path, content in readmes.items():
            path.write_text(content)
            
    def _install_vscode_settings(self):
        """Install VS Code settings with placeholder replacement"""
        template = self.sia_framework / "templates" / "vscode-settings.template.json"
        if not template.exists():
            return
            
        content = template.read_text()
        # Simple placeholder replacement
        content = content.replace("{{LOCALE}}", "en")
        content = content.replace("{{EXTRA_PATHS}}", "")
        
        (self.vscode_dir / "settings.json").write_text(content)
        
    def _run_smart_init(self):
        """Run smart initialization (auto-discovery + population)"""
        print()
        print("[STEP 2/4] Running Smart Initialization...")
        print("-" * 48)
        
        smart_init = self.sia_framework / "installer" / "smart_init.py"
        if not smart_init.exists():
            print("[ERROR] smart_init.py not found")
            sys.exit(1)
            
        try:
            subprocess.run(
                ["uv", "run", "--with", "pyyaml", "python3", str(smart_init)],
                check=True,
                cwd=self.root
            )
        except subprocess.CalledProcessError:
            print("[ERROR] Smart initialization failed")
            sys.exit(1)
            
    def _install_copilot_instructions(self):
        """Install GitHub Copilot instructions"""
        print()
        print("-" * 48)
        print("[STEP 3/4] Installing Copilot Instructions...")
        print("-" * 48)
        
        self.github_dir.mkdir(exist_ok=True)
        
        copilot_instructions = self.github_dir / "copilot-instructions.md"
        template = self.sia_framework / "core" / "copilot-instructions.template.md"
        
        if copilot_instructions.exists():
            print("   ⚠️  .github/copilot-instructions.md already exists, skipping...")
            print("      Review sia/core/copilot-instructions.template.md for updates")
        else:
            print("   📝 Creating .github/copilot-instructions.md from template...")
            if template.exists():
                shutil.copy(template, copilot_instructions)
                print("   ⚠️  Manual customization required:")
                placeholders = [
                    "{{PROJECT_NAME}}",
                    "{{PROJECT_TYPE}}",
                    "{{PROJECT_MISSION}}",
                    "{{TECH_STACK}}",
                    "{{ARCHITECTURE_PATTERN}}",
                    "{{EXECUTION_COMMAND}}",
                    "{{ARCHITECTURE_DNA}}",
                    "{{RESEARCH_SOURCES}}",
                    "{{PROJECT_SLUG}}",
                    "{{ADDITIONAL_CONTEXT}}"
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
        print("  - Directory: .sia/ (agents, knowledge, requirements, skills, prompts)")
        print("  - Directory: .vscode/ (VS Code configuration)")
        print("  - Configuration: .sia.detected.yaml")
        print("  - Configuration: .vscode/settings.json (slash commands enabled)")
        print("  - Instructions: .github/copilot-instructions.md")
        print("  - Init Protocol: .sia/INIT_REQUIRED.md (one-time)")
        print("  - Slash Commands: .sia/prompts/*.prompt.md (11 commands)")
        print()
        print("⚠️  IMPORTANT: Repository requires SUPER AGENT initialization")
        print()
        print("Next steps:")
        print("  1. Open this project in VS Code with GitHub Copilot")
        print("  2. Ask Copilot: 'Initialize SIA for this repository'")
        print()
        print("     The SUPER AGENT will:")
        print("     - Analyze repository structure and domain")
        print("     - Generate project SPR (.sia/agents/<project>.md)")
        print("     - Detect specialized agents (e.g., Repository Guardian)")
        print("     - Create initial knowledge base")
        print("     - Populate skills catalog")
        print("     - Delete .sia/INIT_REQUIRED.md (auto-cleanup)")
        print()
        print("  3. Review generated files in .sia/")
        print("  4. Start working with natural language requirements!")
        print()
        print("📖 Documentation:")
        print("  - Framework: sia/README.md")
        print("  - Quick Start: sia/QUICKSTART.md")
        print("  - Distribution: sia/DISTRIBUTION.md")
        print()
        
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        return shutil.which(command) is not None
        
    def _print_install_help(self, tool: str):
        """Print platform-specific installation instructions"""
        if tool == "python":
            print()
            print("Please install Python 3.10+ from:")
            if self.platform == "Darwin":  # macOS
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

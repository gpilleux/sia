#!/usr/bin/env python3
"""
SIA Framework CLI
Entry point for uvx sia-framework commands
"""

import sys
from pathlib import Path

import click

from . import __version__


@click.group()
@click.version_option(version=__version__, prog_name="sia-framework")
def main():
    """SIA Framework - Meta-Cognitive AI Orchestration System
    
    Transform GitHub Copilot into an architectural Super Agent.
    
    Usage:
        uvx --from git+https://github.com/gpilleux/sia.git sia-framework init
        uvx --from git+https://github.com/gpilleux/sia.git sia-framework update
        uvx --from git+https://github.com/gpilleux/sia.git sia-framework doctor
    """
    pass


@main.command()
@click.option("--force", is_flag=True, help="Overwrite existing files")
def init(force: bool):
    """Initialize SIA in current directory.
    
    Creates .sia/ structure, installs slash commands, and generates
    copilot-instructions.md for GitHub Copilot integration.
    """
    from .installer.install import SIAInstaller
    
    installer = SIAInstaller(force=force)
    installer.run()


@main.command()
def update():
    """Update copilot-instructions.md from detected configuration.
    
    Re-runs auto-discovery and regenerates .github/copilot-instructions.md
    with current project state.
    """
    from .installer.auto_discovery import AutoDiscovery
    
    root = Path.cwd()
    
    # Check if SIA is initialized
    if not (root / ".sia").exists():
        click.echo("❌ SIA not initialized. Run 'sia-framework init' first.")
        sys.exit(1)
    
    click.echo("🔄 Updating SIA configuration...")
    
    # Re-run discovery
    discovery = AutoDiscovery(str(root))
    discovery.discover()
    discovery.generate_config()
    
    click.echo("✅ SIA configuration updated!")


@main.command()
def doctor():
    """Check SIA installation health.
    
    Verifies that all required files and directories exist,
    and reports any issues with the installation.
    """
    root = Path.cwd()
    issues = []
    warnings = []
    
    click.echo("🩺 SIA Health Check")
    click.echo("=" * 48)
    
    # Check .sia/ directory
    sia_dir = root / ".sia"
    if not sia_dir.exists():
        issues.append("❌ .sia/ directory not found")
    else:
        click.echo("✅ .sia/ directory exists")
        
        # Check subdirectories
        subdirs = ["agents", "knowledge", "requirements", "skills", "prompts"]
        for subdir in subdirs:
            if (sia_dir / subdir).exists():
                click.echo(f"   ✅ .sia/{subdir}/")
            else:
                warnings.append(f"⚠️  .sia/{subdir}/ missing")
    
    # Check .sia.detected.yaml
    if (root / ".sia.detected.yaml").exists():
        click.echo("✅ .sia.detected.yaml exists")
    else:
        warnings.append("⚠️  .sia.detected.yaml not found (run 'sia-framework update')")
    
    # Check copilot-instructions.md
    copilot_instructions = root / ".github" / "copilot-instructions.md"
    if copilot_instructions.exists():
        click.echo("✅ .github/copilot-instructions.md exists")
    else:
        issues.append("❌ .github/copilot-instructions.md not found")
    
    # Check VS Code settings
    vscode_settings = root / ".vscode" / "settings.json"
    if vscode_settings.exists():
        click.echo("✅ .vscode/settings.json exists")
    else:
        warnings.append("⚠️  .vscode/settings.json not found")
    
    # Check INIT_REQUIRED.md (should be deleted after init)
    init_required = sia_dir / "INIT_REQUIRED.md"
    if init_required.exists():
        warnings.append("⚠️  .sia/INIT_REQUIRED.md exists (Super Agent init pending)")
    
    # Report
    click.echo()
    if issues:
        click.echo("Issues found:")
        for issue in issues:
            click.echo(f"  {issue}")
    
    if warnings:
        click.echo("Warnings:")
        for warning in warnings:
            click.echo(f"  {warning}")
    
    if not issues and not warnings:
        click.echo("🎉 SIA installation is healthy!")
    elif issues:
        click.echo()
        click.echo("Run 'sia-framework init' to fix issues.")
        sys.exit(1)


if __name__ == "__main__":
    main()

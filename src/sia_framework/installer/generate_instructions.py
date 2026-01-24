#!/usr/bin/env python3
"""
SIA Generate Instructions
Regenerates copilot-instructions.md from detected configuration
"""

from pathlib import Path

import yaml

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files


def get_template_content() -> str:
    """Get the copilot-instructions template from package resources."""
    try:
        # Try package mode first
        resource = files("sia_framework").joinpath("core", "copilot-instructions.template.md")
        return resource.read_text(encoding="utf-8")
    except (FileNotFoundError, TypeError, ModuleNotFoundError):
        # Fallback to inception mode (development)
        template_path = Path(__file__).parent.parent / "core" / "copilot-instructions.template.md"
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")
        raise FileNotFoundError("Template not found in package or development path")


def generate_instructions(root_dir: str = "."):
    root = Path(root_dir).resolve()
    config_path = root / ".sia.detected.yaml"
    output_path = root / ".github/copilot-instructions.md"
    
    if not config_path.exists():
        print("❌ .sia.detected.yaml not found. Run 'sia-framework init' first.")
        return False

    # Load Config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Load Template
    try:
        template = get_template_content()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return False
    
    # Load SPR
    spr_rel_path = config.get("spr", {}).get("path")
    spr_content = "_SPR not found. Super Agent will create it._"
    if spr_rel_path:
        spr_path = root / spr_rel_path
        if spr_path.exists():
            spr_content = spr_path.read_text(encoding="utf-8")
        else:
            print(f"⚠️  SPR file {spr_path} not found.")
    
    # Prepare Replacements
    project_name = config.get("project", {}).get("name", "Unknown")
    project_type = config.get("project", {}).get("type", "Generic")
    bounded_contexts = ", ".join(config.get("domain", {}).get("bounded_contexts", []))
    
    # Requirements Status
    req_dir = root / ".sia" / "requirements"
    active_reqs = []
    if req_dir.exists():
        for item in req_dir.iterdir():
            if item.is_dir() and item.name.startswith("REQ-") and not item.name.startswith("_"):
                active_reqs.append(item.name)
    
    req_status = f"Active Requirements: {', '.join(active_reqs) if active_reqs else 'None'}"

    # Replace placeholders
    content = template.replace("{{PROJECT_NAME}}", project_name)
    content = content.replace("{{PROJECT_TYPE}}", project_type)
    content = content.replace("{{BOUNDED_CONTEXTS}}", bounded_contexts if bounded_contexts else "Not detected")
    content = content.replace("{{PROJECT_SPR_CONTENT}}", spr_content)
    content = content.replace("{{REQUIREMENTS_STATUS}}", req_status)
    
    # Write
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"✅ Generated instructions at {output_path}")
    return True


if __name__ == "__main__":
    generate_instructions()

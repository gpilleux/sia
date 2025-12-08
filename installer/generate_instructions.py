#!/usr/bin/env python3
from pathlib import Path

import yaml


def generate_instructions(root_dir: str = "."):
    root = Path(root_dir).resolve()
    config_path = root / ".sia.detected.yaml"
    template_path = root / "sia/core/copilot-instructions.template.md"
    output_path = root / ".github/copilot-instructions.md"
    
    if not config_path.exists():
        print("❌ .sia.detected.yaml not found. Run auto_discovery.py first.")
        return
    
    if not template_path.exists():
        print(f"❌ Template not found at {template_path}")
        return

    # Load Config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    # Load Template
    template = template_path.read_text(encoding="utf-8")
    
    # Load SPR
    spr_rel_path = config.get("spr", {}).get("path")
    spr_content = "SPR not found."
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
    
    # Requirements Status (Simple check)
    req_dir = root / "requirements"
    active_reqs = []
    if req_dir.exists():
        for item in req_dir.iterdir():
            if item.is_dir() and item.name.startswith("REQ-") and not item.name.startswith("_"):
                active_reqs.append(item.name)
    
    req_status = f"Active Requirements: {', '.join(active_reqs) if active_reqs else 'None'}"

    # Replace
    content = template.replace("{{PROJECT_NAME}}", project_name)
    content = content.replace("{{PROJECT_TYPE}}", project_type)
    content = content.replace("{{BOUNDED_CONTEXTS}}", bounded_contexts)
    content = content.replace("{{PROJECT_SPR_CONTENT}}", spr_content)
    content = content.replace("{{REQUIREMENTS_STATUS}}", req_status)
    
    # Write
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"✅ Generated instructions at {output_path}")

if __name__ == "__main__":
    generate_instructions()

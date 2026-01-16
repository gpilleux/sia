#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path
import yaml
from datetime import datetime

# Add parent directory to path to import auto_discovery
sys.path.append(str(Path(__file__).parent.parent.parent))
from sia.installer.auto_discovery import AutoDiscovery


class SmartInit:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        self.sia_dir = self.root / ".sia"
        self.legacy_dirs = {
            "requirements": self.root / "requirements",
            "agents": self.root / ".agents",
            "skills": self.root / "skills",  # In case it exists in root
        }

    def run(self):
        print("🚀 Starting SIA Smart Initialization...")

        # 1. Create Structure
        self._create_structure()

        # 2. Check Legacy Data (No Migration)
        self._check_legacy_folders()

        # 3. Populate Default Content
        self._populate_defaults()

        # 4. Run Auto-Discovery
        self._run_discovery()

        # 5. Cleanup
        self._cleanup()

        print("\n✅ SIA Smart Initialization Complete!")
        print(f"   📂 Agent Brain: {self.sia_dir}")

    def _create_structure(self):
        print("1️⃣  Verifying .sia structure...")
        dirs = [
            "agents",
            "knowledge/active",
            "knowledge/_archive",
            "requirements/_archive",
            "skills",
            "metadata",
            "backup",
        ]
        for d in dirs:
            (self.sia_dir / d).mkdir(parents=True, exist_ok=True)

    def _check_legacy_folders(self):
        print("2️⃣  Checking for legacy structures...")
        found_legacy = False

        # Requirements
        if self.legacy_dirs["requirements"].exists():
            print(f"   ⚠️  Found legacy 'requirements/' folder.")
            print(f"       -> Action: Ask Super Agent to migrate to .sia/requirements/")
            found_legacy = True

        # Agents
        if self.legacy_dirs["agents"].exists():
            print(f"   ⚠️  Found legacy '.agents/' folder.")
            print(f"       -> Action: Ask Super Agent to migrate to .sia/agents/")
            found_legacy = True

        if not found_legacy:
            print("   ✅ No legacy structures found.")

    def _populate_defaults(self):
        print("3️⃣  Populating agent capabilities...")

        # Copy skills from submodule if not present
        submodule_skills = self.root / "sia" / "skills"
        target_skills = self.sia_dir / "skills"

        if submodule_skills.exists():
            for item in submodule_skills.glob("*"):
                if item.is_file() and item.name != "README.md":
                    if not (target_skills / item.name).exists():
                        shutil.copy2(item, target_skills / item.name)
                        print(f"   -> Installed skill: {item.name}")

    def _run_discovery(self):
        print("4️⃣  Analyzing repository...")
        discovery = AutoDiscovery(str(self.root))
        config = discovery.discover()

        # Save detected config
        with open(self.root / ".sia.detected.yaml", "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        print("   -> Updated .sia.detected.yaml")

        # Generate Copilot Instructions
        discovery.assemble_instructions()

    def _cleanup(self):
        print("5️⃣  Cleaning up...")
        # We do NOT delete INIT_REQUIRED.md here.
        # It serves as a flag for the Super Agent to know that initialization is pending.
        # The Super Agent will delete it after completing Phase 2.
        pass


if __name__ == "__main__":
    SmartInit().run()

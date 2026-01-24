#!/usr/bin/env python3
"""
SIA Smart Initialization
Orchestrates structure creation, discovery, and population
"""

from pathlib import Path

import yaml

from .auto_discovery import AutoDiscovery


class SmartInit:
    def __init__(self, root_dir: str = ".", mode: str = "package"):
        self.root = Path(root_dir).resolve()
        self.sia_dir = self.root / ".sia"
        self.mode = mode
        self.legacy_dirs = {
            "requirements": self.root / "requirements",
            "agents": self.root / ".agents",
            "skills": self.root / "skills",
        }

    def run(self):
        print("🚀 Starting SIA Smart Initialization...")

        self._create_structure()
        self._check_legacy_folders()
        self._populate_defaults()
        self._run_discovery()
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

        if self.legacy_dirs["requirements"].exists():
            print("   ⚠️  Found legacy 'requirements/' folder.")
            print("       -> Action: Ask Super Agent to migrate to .sia/requirements/")
            found_legacy = True

        if self.legacy_dirs["agents"].exists():
            print("   ⚠️  Found legacy '.agents/' folder.")
            print("       -> Action: Ask Super Agent to migrate to .sia/agents/")
            found_legacy = True

        if not found_legacy:
            print("   ✅ No legacy structures found.")

    def _populate_defaults(self):
        print("3️⃣  Populating agent capabilities...")
        # Skills are now copied by the installer from package resources
        # This method is kept for any additional population logic
        pass

    def _run_discovery(self):
        print("4️⃣  Analyzing repository...")
        discovery = AutoDiscovery(str(self.root))
        config = discovery.discover()

        # Save detected config
        with open(self.root / ".sia.detected.yaml", "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        print("   -> Updated .sia.detected.yaml")

    def _cleanup(self):
        print("5️⃣  Cleaning up...")
        # INIT_REQUIRED.md is kept as a flag for Super Agent
        pass


if __name__ == "__main__":
    SmartInit().run()

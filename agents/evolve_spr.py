#!/usr/bin/env python3
import sys
from pathlib import Path

import yaml

# Add root to path to import auto_discovery
sys.path.append(str(Path(__file__).parent.parent.parent))
from sia.installer.auto_discovery import AutoDiscovery


class SPREvolution:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        self.discovery = AutoDiscovery(str(self.root))
        self.config = self.discovery.discover()
        self.spr_path = self.root / self.config["spr"]["path"]

    def check_drift(self):
        print(f"🧠 Checking SPR Drift for {self.spr_path}...")
        
        if not self.spr_path.exists():
            print("❌ SPR file not found.")
            return

        spr_content = self.spr_path.read_text()
        drift_detected = False
        
        # Check Bounded Contexts
        detected_contexts = self.config["domain"].get("bounded_contexts", [])
        for context in detected_contexts:
            if context not in spr_content:
                print(f"⚠️  New Bounded Context detected: {context}")
                drift_detected = True
                
        # Check Agents
        detected_agents = self.config["agents"].get("active", [])
        for agent in detected_agents:
            if agent not in spr_content:
                print(f"⚠️  New Agent detected: {agent}")
                drift_detected = True

        if drift_detected:
            print("\n💡 Suggestion: Update SPR to include these new elements.")
        else:
            print("✅ SPR is up to date with high-level structure.")

if __name__ == "__main__":
    SPREvolution().check_drift()

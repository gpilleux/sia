#!/usr/bin/env python3
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml


class SkillMetrics:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        self.metrics_file = self.root / ".agents" / "skills_metrics.yaml"
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)

    def log_usage(self, skill_name: str, details: Optional[dict] = None):
        data = self._load()
        
        if "skills_usage" not in data:
            data["skills_usage"] = {}
            
        if skill_name not in data["skills_usage"]:
            data["skills_usage"][skill_name] = {
                "invocations": 0,
                "last_used": None,
                "history": []
            }
            
        metric = data["skills_usage"][skill_name]
        metric["invocations"] += 1
        metric["last_used"] = datetime.now().isoformat()
        
        if details:
            metric["history"].append({
                "timestamp": datetime.now().isoformat(),
                "details": details
            })
            # Keep history manageable (last 10 entries)
            metric["history"] = metric["history"][-10:]
            
        self._save(data)
        print(f"📊 Metrics updated for {skill_name} (Total: {metric['invocations']})")

    def _load(self):
        if not self.metrics_file.exists():
            return {}
        try:
            return yaml.safe_load(self.metrics_file.read_text()) or {}
        except:
            return {}

    def _save(self, data):
        with open(self.metrics_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: metrics.py <skill_name> [key=value ...]")
        sys.exit(1)
        
    skill = sys.argv[1]
    details = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            details[k] = v
            
    SkillMetrics().log_usage(skill, details)

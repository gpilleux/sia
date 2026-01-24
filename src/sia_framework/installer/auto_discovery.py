#!/usr/bin/env python3
"""
SIA Auto-Discovery Module
Analyzes repository structure and generates configuration
"""

import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class AutoDiscovery:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        self.config: Dict[str, Any] = {
            "sia_version": "1.0.0",
            "project": {},
            "git": {},
            "spr": {},
            "domain": {},
            "paths": {},
            "agents": {"active": []}
        }

    def discover(self) -> Dict[str, Any]:
        print(f"🔍 Starting Auto-Discovery in {self.root}...")
        
        self.detect_git_identity()
        self.detect_tech_stack()
        self.detect_spr()
        self.extract_bounded_contexts()
        
        return self.config

    def _find_directory_recursive(self, target_name: str, max_depth: int = 4, exclude_patterns: List[str] = None) -> Optional[Path]:
        """Recursively search for a directory with given name up to max_depth levels."""
        if exclude_patterns is None:
            exclude_patterns = []
            
        candidates = []
        priority_segments = ['src', 'app', 'backend', 'server', 'core', 'lib', 'packages']
        
        def search(current_path: Path, current_depth: int):
            if current_depth > max_depth:
                return
                
            try:
                for item in current_path.iterdir():
                    if item.name in [".git", "node_modules", "venv", ".venv", "__pycache__", 
                                     "dist", "build", ".next", ".pytest_cache", "htmlcov",
                                     ".agents", ".agents.backup", ".sia"]:
                        continue
                    
                    if any(pattern in str(item) for pattern in exclude_patterns):
                        continue
                        
                    if item.is_dir():
                        if item.name == target_name:
                            candidates.append(item)
                        search(item, current_depth + 1)
            except PermissionError:
                pass
        
        search(self.root, 0)
        
        if candidates:
            def priority_score(path: Path) -> tuple:
                parts = path.parts
                has_test = any(part in ['test', 'tests', 'testing', 'spec', 'specs'] for part in parts)
                priority_count = sum(1 for part in parts if part in priority_segments)
                depth = len(parts)
                return (has_test, -priority_count, depth)
            
            candidates.sort(key=priority_score)
            return candidates[0]
        
        return None

    def extract_bounded_contexts(self):
        print("4️⃣  Extracting Bounded Contexts...")
        contexts = set()
        
        domain_dir = self._find_directory_recursive("domain", exclude_patterns=["test", "tests", "testing"])
        
        if domain_dir:
            print(f"   🔍 Found domain directory: {domain_dir.relative_to(self.root)}")
            for item in domain_dir.iterdir():
                if item.is_dir() and item.name not in ["repositories", "__pycache__", "common", "shared"]:
                    contexts.add(item.name.capitalize())
        
        if not contexts:
            api_dir = self._find_directory_recursive("api", exclude_patterns=["test", "tests", "testing"])
            
            if api_dir:
                for subdir_name in ["v1", "routers", "routes"]:
                    routes_dir = api_dir / subdir_name
                    if routes_dir.exists():
                        print(f"   🔍 Found API directory: {routes_dir.relative_to(self.root)}")
                        for item in routes_dir.glob("*.py"):
                            if item.name != "__init__.py":
                                contexts.add(item.stem.capitalize())
                        if contexts:
                            break
                
                if not contexts:
                    for item in api_dir.glob("*.py"):
                        if item.name != "__init__.py":
                            contexts.add(item.stem.capitalize())

        self.config["domain"]["bounded_contexts"] = list(contexts)
        print(f"   ✅ Contexts: {list(contexts)}")

    def detect_spr(self):
        print("3️⃣  Detecting SPR & Agents...")
        project_name = self.config["project"].get("name", "unknown")
        sia_agents_dir = self.root / ".sia" / "agents"
        legacy_agents_dir = self.root / ".agents"
        
        spr_path = None
        
        # Strategy 1: .sia/agents/{project_name}.md
        candidate = sia_agents_dir / f"{project_name}.md"
        if candidate.exists():
            spr_path = str(candidate.relative_to(self.root))
        
        # Strategy 2: .agents/{project_name}.md (legacy)
        if not spr_path:
            candidate = legacy_agents_dir / f"{project_name}.md"
            if candidate.exists():
                spr_path = str(candidate.relative_to(self.root))
        
        # Strategy 3: {PROJECT_NAME}_AGENT.spr.md
        if not spr_path:
            candidate = self.root / f"{project_name.upper()}_AGENT.spr.md"
            if candidate.exists():
                spr_path = str(candidate.relative_to(self.root))
                
        # Strategy 4: {PROJECT_NAME}.spr.md
        if not spr_path:
            candidate = self.root / f"{project_name.upper()}.spr.md"
            if candidate.exists():
                spr_path = str(candidate.relative_to(self.root))
                
        # Strategy 5: Any *.spr.md in root
        if not spr_path:
            spr_files = sorted(self.root.glob("*.spr.md"))
            if spr_files:
                spr_path = str(spr_files[0].relative_to(self.root))
            
        if spr_path:
            self.config["spr"]["path"] = spr_path
            print(f"   ✅ SPR Found: {spr_path}")
        else:
            self.config["spr"]["path"] = None
            print("   ⚠️  SPR Not Found (Super Agent will create it)")
        
        # Detect Active Agents
        agents = []
        for agents_dir in [sia_agents_dir, legacy_agents_dir]:
            if agents_dir.exists():
                for agent_file in agents_dir.glob("*.md"):
                    if agent_file.name == f"{project_name}.md" or agent_file.name == "README.md":
                        continue
                    if agent_file.stem not in agents:
                        agents.append(agent_file.stem)
        
        self.config["agents"]["active"] = agents
        print(f"   ✅ Active Agents: {len(agents)} found")

    def _find_file_recursive(self, filename: str, max_depth: int = 4) -> Optional[Path]:
        """Recursively search for a file with given name up to max_depth levels."""
        def search(current_path: Path, current_depth: int) -> Optional[Path]:
            if current_depth > max_depth:
                return None
                
            try:
                for item in current_path.iterdir():
                    if item.name in [".git", "node_modules", "venv", ".venv", "__pycache__", 
                                     "dist", "build", ".next", ".pytest_cache", "htmlcov"]:
                        continue
                        
                    if item.is_file() and item.name == filename:
                        return item
                    elif item.is_dir():
                        result = search(item, current_depth + 1)
                        if result:
                            return result
            except PermissionError:
                pass
                
            return None
        
        return search(self.root, 0)

    def detect_tech_stack(self):
        print("2️⃣  Detecting Technology Stack...")
        stack = []
        architecture = []
        
        pyproject = self._find_file_recursive("pyproject.toml")
        requirements = self._find_file_recursive("requirements.txt")
        
        if pyproject or requirements:
            stack.append("python")
            config_file = pyproject if pyproject else requirements
            try:
                content = config_file.read_text(encoding="utf-8")
                if "fastapi" in content.lower():
                    stack.append("fastapi")
                if "django" in content.lower():
                    stack.append("django")
                if "flask" in content.lower():
                    stack.append("flask")
            except Exception:
                pass

        package_json = self._find_file_recursive("package.json")
        
        if package_json:
            stack.append("node")
            try:
                content = package_json.read_text(encoding="utf-8")
                if "react" in content.lower():
                    stack.append("react")
                if "next" in content.lower():
                    stack.append("nextjs")
                if "vue" in content.lower():
                    stack.append("vue")
                if "angular" in content.lower():
                    stack.append("angular")
            except Exception:
                pass

        domain_dir = self._find_directory_recursive("domain")
        
        if domain_dir:
            architecture.append("ddd")
        elif (self.root / "app").exists() and (self.root / "models").exists():
            architecture.append("mvc")
            
        if not stack:
            project_type = "generic"
        else:
            project_type = "-".join(stack + architecture)
            
        self.config["project"]["type"] = project_type
        print(f"   ✅ Detected Type: {project_type}")

    def detect_git_identity(self):
        print("1️⃣  Detecting Git Identity...")
        try:
            remote_url = subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], 
                cwd=self.root, text=True, stderr=subprocess.DEVNULL
            ).strip()
            
            self.config["git"]["remote"] = remote_url
            
            match = re.search(r"/([^/]+)\.git$", remote_url)
            if match:
                project_name = match.group(1)
            else:
                match = re.search(r"/([^/]+)$", remote_url)
                if match:
                    project_name = match.group(1)
                else:
                    project_name = self.root.name
                
            self.config["project"]["name"] = project_name
            self.config["project"]["root"] = str(self.root)
            
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], 
                cwd=self.root, text=True, stderr=subprocess.DEVNULL
            ).strip()
            self.config["git"]["branch"] = branch
            
            print(f"   ✅ Project: {project_name}")
            print(f"   ✅ Remote: {remote_url}")
            print(f"   ✅ Branch: {branch}")
            
        except subprocess.CalledProcessError:
            print("   ⚠️  Not a git repository or no remote configured.")
            self.config["project"]["name"] = self.root.name
            self.config["project"]["root"] = str(self.root)

    def generate_config(self, output_path: str = ".sia.detected.yaml"):
        with open(self.root / output_path, "w") as f:
            yaml.dump(self.config, f, default_flow_style=False)
        print(f"💾 Configuration saved to {output_path}")


if __name__ == "__main__":
    discovery = AutoDiscovery()
    config = discovery.discover()
    discovery.generate_config()

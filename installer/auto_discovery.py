#!/usr/bin/env python3
import os
import re
import subprocess
import sys
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

    def _find_directory_recursive(self, target_name: str, max_depth: int = 4) -> Optional[Path]:
        """Recursively search for a directory with given name up to max_depth levels."""
        def search(current_path: Path, current_depth: int) -> Optional[Path]:
            if current_depth > max_depth:
                return None
                
            try:
                for item in current_path.iterdir():
                    # Skip common ignore patterns
                    if item.name in [".git", "node_modules", "venv", ".venv", "__pycache__", 
                                     "dist", "build", ".next", ".pytest_cache", "htmlcov"]:
                        continue
                        
                    if item.is_dir():
                        if item.name == target_name:
                            return item
                        # Recurse into subdirectory
                        result = search(item, current_depth + 1)
                        if result:
                            return result
            except PermissionError:
                pass
                
            return None
        
        return search(self.root, 0)

    def extract_bounded_contexts(self):
        print("4️⃣  Extracting Bounded Contexts...")
        contexts = set()
        
        # Strategy 1: Find 'domain' directory recursively (DDD pattern)
        domain_dir = self._find_directory_recursive("domain")
        
        if domain_dir:
            print(f"   🔍 Found domain directory: {domain_dir.relative_to(self.root)}")
            for item in domain_dir.iterdir():
                if item.is_dir() and item.name not in ["repositories", "__pycache__", "common", "shared"]:
                    contexts.add(item.name.capitalize())
        
        # Strategy 2: Find API routers (if Strategy 1 yielded nothing)
        if not contexts:
            # Try finding 'api' directory recursively
            api_dir = self._find_directory_recursive("api")
            
            if api_dir:
                # Look for v1, routers, or direct route files
                for subdir_name in ["v1", "routers", "routes"]:
                    routes_dir = api_dir / subdir_name
                    if routes_dir.exists():
                        print(f"   🔍 Found API directory: {routes_dir.relative_to(self.root)}")
                        for item in routes_dir.glob("*.py"):
                            if item.name != "__init__.py":
                                contexts.add(item.stem.capitalize())
                        if contexts:
                            break
                
                # If no subdirectories, check api_dir itself
                if not contexts:
                    for item in api_dir.glob("*.py"):
                        if item.name != "__init__.py":
                            contexts.add(item.stem.capitalize())

        self.config["domain"]["bounded_contexts"] = list(contexts)
        print(f"   ✅ Contexts: {list(contexts)}")


    def detect_spr(self):
        print("3️⃣  Detecting SPR & Agents...")
        project_name = self.config["project"].get("name", "unknown")
        agents_dir = self.root / ".agents"
        
        spr_path = None
        
        # Strategy 1: .agents/{project_name}.md
        candidate = agents_dir / f"{project_name}.md"
        if candidate.exists():
            spr_path = str(candidate.relative_to(self.root))
        
        # Strategy 2: .agents/README.md
        if not spr_path and (agents_dir / "README.md").exists():
            spr_path = str((agents_dir / "README.md").relative_to(self.root))
            
        # Strategy 3: {PROJECT_NAME}_AGENT.spr.md (common pattern)
        if not spr_path:
            candidate = self.root / f"{project_name.upper()}_AGENT.spr.md"
            if candidate.exists():
                spr_path = str(candidate.relative_to(self.root))
                
        # Strategy 4: {PROJECT_NAME}.spr.md
        if not spr_path:
            candidate = self.root / f"{project_name.upper()}.spr.md"
            if candidate.exists():
                spr_path = str(candidate.relative_to(self.root))
                
        # Strategy 5: Any *.spr.md in root (pick first alphabetically)
        if not spr_path:
            spr_files = sorted(self.root.glob("*.spr.md"))
            if spr_files:
                spr_path = str(spr_files[0].relative_to(self.root))
            
        # Strategy 6: README.md (fallback)
        if not spr_path and (self.root / "README.md").exists():
            spr_path = "README.md"
            
        self.config["spr"]["path"] = spr_path
        print(f"   ✅ SPR Found: {spr_path}")
        
        # Detect Active Agents
        if agents_dir.exists():
            agents = []
            for agent_file in agents_dir.glob("*.md"):
                if agent_file.name == f"{project_name}.md" or agent_file.name == "README.md":
                    continue
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
                    # Skip common ignore patterns
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
        
        # Python Detection (search for pyproject.toml or requirements.txt)
        pyproject = self._find_file_recursive("pyproject.toml")
        requirements = self._find_file_recursive("requirements.txt")
        
        if pyproject or requirements:
            stack.append("python")
            # Check for FastAPI
            config_file = pyproject if pyproject else requirements
            try:
                content = config_file.read_text()
                if "fastapi" in content.lower():
                    stack.append("fastapi")
                if "django" in content.lower():
                    stack.append("django")
                if "flask" in content.lower():
                    stack.append("flask")
            except Exception:
                pass

        # Node/JavaScript Detection (search for package.json)
        package_json = self._find_file_recursive("package.json")
        
        if package_json:
            stack.append("node")
            try:
                content = package_json.read_text()
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

        # Architecture Detection (search for 'domain' directory = DDD)
        domain_dir = self._find_directory_recursive("domain")
        
        if domain_dir:
            architecture.append("ddd")
        elif (self.root / "app").exists() and (self.root / "models").exists():
            architecture.append("mvc")
            
        # Construct Project Type
        if not stack:
            project_type = "generic"
        else:
            project_type = "-".join(stack + architecture)
            
        self.config["project"]["type"] = project_type
        print(f"   ✅ Detected Type: {project_type}")


    def detect_git_identity(self):
        print("1️⃣  Detecting Git Identity...")
        try:
            # Get remote URL
            remote_url = subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], 
                cwd=self.root, text=True
            ).strip()
            
            self.config["git"]["remote"] = remote_url
            
            # Extract project name from URL (e.g., user/repo.git -> repo)
            match = re.search(r"/([^/]+)\.git$", remote_url)
            if match:
                project_name = match.group(1)
            else:
                # Fallback to directory name
                project_name = self.root.name
                
            self.config["project"]["name"] = project_name
            self.config["project"]["root"] = str(self.root)
            
            # Get current branch
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], 
                cwd=self.root, text=True
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
        
        self.assemble_instructions()

    def assemble_instructions(self):
        print("5️⃣  Assembling Copilot Instructions...")
        template_path = self.root / "sia/core/copilot-instructions.template.md"
        output_path = self.root / ".github/copilot-instructions.md"
        
        if not template_path.exists():
            print(f"   ⚠️  Template not found at {template_path}")
            return

        content = template_path.read_text()
        
        # Replacements
        content = content.replace("{{PROJECT_NAME}}", self.config["project"].get("name", "Unknown"))
        content = content.replace("{{PROJECT_TYPE}}", self.config["project"].get("type", "Unknown"))
        content = content.replace("{{BOUNDED_CONTEXTS}}", ", ".join(self.config["domain"].get("bounded_contexts", [])))
        
        # SPR Content
        spr_path = self.config["spr"].get("path")
        if spr_path and (self.root / spr_path).exists():
            spr_content = (self.root / spr_path).read_text()
            content = content.replace("{{PROJECT_SPR_CONTENT}}", spr_content)
        else:
            content = content.replace("{{PROJECT_SPR_CONTENT}}", "_No SPR found._")
            
        # Requirements Status (Placeholder for now)
        content = content.replace("{{REQUIREMENTS_STATUS}}", "System initialized. Ready for requirements.")

        # Ensure .github exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"   📝 Writing to: {output_path}")
        print(f"   📝 Content Preview:\n{content[:200]}")
        
        output_path.write_text(content)
        print(f"   ✅ Instructions updated at {output_path}")

if __name__ == "__main__":
    discovery = AutoDiscovery()
    config = discovery.discover()
    discovery.generate_config()


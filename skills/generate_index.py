#!/usr/bin/env python3
"""
Generate Repository Index - Intelligent workspace navigation for Super Agent

Creates a comprehensive index mapping:
- Documentation structure (what's documented, where)
- Code organization (modules, packages, classes, functions)
- Domain concepts (bounded contexts, entities, aggregates)
- Configuration files (project setup, dependencies)
- Active work (requirements, next sessions, QUANTs)

Output: REPO_INDEX.md (referenced by copilot-instructions.md)
"""

import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

import yaml


@dataclass
class FileEntry:
    """Represents a file in the index."""
    path: str
    type: str  # 'doc', 'code', 'config', 'data'
    category: str  # 'framework', 'domain', 'infrastructure', etc.
    description: str
    key_entities: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)


@dataclass
class RepositoryIndex:
    """Complete repository index."""
    project_name: str
    project_type: str
    bounded_contexts: List[str]
    documentation: Dict[str, List[FileEntry]] = field(default_factory=dict)
    code_structure: Dict[str, List[FileEntry]] = field(default_factory=dict)
    configuration: Dict[str, FileEntry] = field(default_factory=dict)
    active_work: Dict[str, str] = field(default_factory=dict)
    

class IndexGenerator:
    """Generates comprehensive repository index."""
    
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        self.index = None
        self.config = self._load_config()
        
        # Exclusion patterns
        self.ignore_dirs = {
            ".git", "node_modules", "venv", ".venv", "__pycache__",
            "dist", "build", ".next", ".pytest_cache", "htmlcov",
            ".mypy_cache", ".ruff_cache", "site-packages"
        }
        
        self.ignore_files = {
            ".DS_Store", "*.pyc", "*.pyo", "*.pyd", ".coverage"
        }
    
    def _load_config(self) -> Dict:
        """Load .sia.detected.yaml if exists."""
        config_path = self.root / ".sia.detected.yaml"
        if config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        return {"project": {"name": self.root.name, "type": "generic"}, "domain": {"bounded_contexts": []}}
    
    def generate(self) -> RepositoryIndex:
        """Generate complete repository index."""
        print("🔍 Generating Repository Index...")
        
        self.index = RepositoryIndex(
            project_name=self.config["project"]["name"],
            project_type=self.config["project"]["type"],
            bounded_contexts=self.config["domain"].get("bounded_contexts", [])
        )
        
        self._index_documentation()
        self._index_code_structure()
        self._index_configuration()
        self._index_active_work()
        
        return self.index
    
    def _index_documentation(self):
        """Index all documentation files."""
        print("📚 Indexing Documentation...")
        
        doc_categories = {
            "framework": ["core/", "docs/", "README.md", "CHANGELOG.md"],
            "project": [".sia/knowledge/", ".sia/agents/"],
            "requirements": [".sia/requirements/", "requirements/"],
            "guides": ["QUICKSTART.md", "DISTRIBUTION.md", "ARCHITECTURE.md"]
        }
        
        for category, patterns in doc_categories.items():
            self.index.documentation[category] = []
            
            for pattern in patterns:
                if pattern.endswith("/"):
                    # Directory pattern
                    dir_path = self.root / pattern
                    if dir_path.exists():
                        for md_file in dir_path.rglob("*.md"):
                            if self._should_index(md_file):
                                entry = self._create_doc_entry(md_file, category)
                                self.index.documentation[category].append(entry)
                else:
                    # File pattern
                    file_path = self.root / pattern
                    if file_path.exists():
                        entry = self._create_doc_entry(file_path, category)
                        self.index.documentation[category].append(entry)
    
    def _create_doc_entry(self, file_path: Path, category: str) -> FileEntry:
        """Create documentation entry with metadata extraction."""
        content = file_path.read_text(errors="ignore")
        
        # Extract title (first # heading)
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem
        
        # Extract key concepts (## headings)
        concepts = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
        
        # Extract references (links to other docs)
        references = re.findall(r"\[.+?\]\(([^)]+\.md)\)", content)
        
        return FileEntry(
            path=str(file_path.relative_to(self.root)),
            type="doc",
            category=category,
            description=title,
            key_entities=concepts[:5],  # Top 5 concepts
            references=list(set(references))
        )
    
    def _index_code_structure(self):
        """Index code organization (Python modules, classes, functions)."""
        print("🐍 Indexing Code Structure...")
        
        code_categories = {
            "domain": ["domain/", "src/domain/"],
            "application": ["application/", "src/application/", "services/"],
            "infrastructure": ["infrastructure/", "src/infrastructure/"],
            "api": ["api/", "src/api/", "routers/"],
            "installer": ["installer/"],
            "skills": ["skills/", ".sia/skills/"],
            "agents": ["agents/", ".sia/agents/"],
            "tests": ["tests/", "test/"]
        }
        
        for category, patterns in code_categories.items():
            self.index.code_structure[category] = []
            
            for pattern in patterns:
                dir_path = self.root / pattern
                if dir_path.exists():
                    for py_file in dir_path.rglob("*.py"):
                        if self._should_index(py_file):
                            entry = self._create_code_entry(py_file, category)
                            if entry:
                                self.index.code_structure[category].append(entry)
    
    def _create_code_entry(self, file_path: Path, category: str) -> Optional[FileEntry]:
        """Create code entry with AST-based entity extraction."""
        try:
            content = file_path.read_text(errors="ignore")
            tree = ast.parse(content)
        except Exception:
            return None
        
        # Extract classes and functions
        entities = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                entities.append(f"class:{node.name}")
            elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                entities.append(f"fn:{node.name}")
        
        # Extract docstring
        description = ast.get_docstring(tree) or file_path.stem.replace("_", " ").title()
        
        # Extract imports (references to other modules)
        references = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    references.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    references.append(node.module)
        
        return FileEntry(
            path=str(file_path.relative_to(self.root)),
            type="code",
            category=category,
            description=description[:100],  # Truncate long descriptions
            key_entities=entities[:10],  # Top 10 entities
            references=list(set(references))[:5]  # Top 5 imports
        )
    
    def _index_configuration(self):
        """Index configuration files."""
        print("⚙️  Indexing Configuration...")
        
        config_files = {
            "project": ["pyproject.toml", "package.json", "tsconfig.json"],
            "sia": [".sia.detected.yaml", ".sia/metadata/sia_version.txt"],
            "vscode": [".vscode/settings.json", ".github/copilot-instructions.md"],
            "docker": ["docker-compose.yml", "Dockerfile"],
            "git": [".gitignore", ".gitmodules"]
        }
        
        for category, filenames in config_files.items():
            for filename in filenames:
                file_path = self.root / filename
                if file_path.exists():
                    self.index.configuration[f"{category}:{filename}"] = FileEntry(
                        path=str(file_path.relative_to(self.root)),
                        type="config",
                        category=category,
                        description=f"{category.title()} configuration"
                    )
    
    def _index_active_work(self):
        """Index active requirements and next sessions."""
        print("📋 Indexing Active Work...")
        
        # Find active REQs
        req_dirs = list((self.root / ".sia" / "requirements").glob("REQ-*")) if (self.root / ".sia" / "requirements").exists() else []
        req_dirs += list((self.root / "requirements").glob("REQ-*")) if (self.root / "requirements").exists() else []
        
        active_reqs = []
        for req_dir in req_dirs:
            req_file = req_dir / f"{req_dir.name}.md"
            if req_file.exists():
                content = req_file.read_text(errors="ignore")
                # Check if completed
                if "STATUS: COMPLETED" not in content and "✅ COMPLETED" not in content:
                    active_reqs.append(str(req_file.relative_to(self.root)))
        
        self.index.active_work["active_requirements"] = ", ".join(active_reqs) if active_reqs else "None"
        
        # Find NEXT_SESSION.md
        next_session_paths = [
            self.root / "NEXT_SESSION.md",
            self.root / ".sia" / "NEXT_SESSION.md"
        ]
        
        for path in next_session_paths:
            if path.exists():
                self.index.active_work["next_session"] = str(path.relative_to(self.root))
                break
        else:
            self.index.active_work["next_session"] = "Not found"
    
    def _should_index(self, file_path: Path) -> bool:
        """Check if file should be indexed."""
        # Check if in ignored directory
        for parent in file_path.parents:
            if parent.name in self.ignore_dirs:
                return False
        
        # Check if matches ignored file pattern
        for pattern in self.ignore_files:
            if file_path.match(pattern):
                return False
        
        return True
    
    def export_markdown(self, output_path: str = "REPO_INDEX.md"):
        """Export index to Markdown format."""
        print(f"💾 Exporting index to {output_path}...")
        
        lines = [
            f"# Repository Index - {self.index.project_name}",
            "",
            f"**Project Type**: {self.index.project_type}  ",
            f"**Bounded Contexts**: {', '.join(self.index.bounded_contexts) or 'None detected'}  ",
            f"**Generated**: {self._timestamp()}",
            "",
            "---",
            "",
            "## 📚 Documentation Map",
            "",
            "### Purpose",
            "This index provides a comprehensive map of the repository structure, enabling the Super Agent to:",
            "- Quickly locate relevant documentation for research",
            "- Understand code organization and domain boundaries",
            "- Identify active work and next actions",
            "- Navigate configuration and setup files",
            "",
            "### How to Use This Index",
            "1. **Before Investigation**: Read relevant sections to understand what exists",
            "2. **During Implementation**: Reference code structure to maintain consistency",
            "3. **For Context**: Check active work to understand current priorities",
            "",
            "---",
            ""
        ]
        
        # Documentation Section
        lines.append("## 📄 Documentation")
        lines.append("")
        for category, entries in sorted(self.index.documentation.items()):
            if entries:
                lines.append(f"### {category.title()}")
                lines.append("")
                for entry in sorted(entries, key=lambda e: e.path):
                    lines.append(f"- **`{entry.path}`** - {entry.description}")
                    if entry.key_entities:
                        lines.append(f"  - Topics: {', '.join(entry.key_entities[:3])}")
                lines.append("")
        
        # Code Structure Section
        lines.append("---")
        lines.append("")
        lines.append("## 🐍 Code Structure")
        lines.append("")
        for category, entries in sorted(self.index.code_structure.items()):
            if entries:
                lines.append(f"### {category.title()}")
                lines.append("")
                for entry in sorted(entries, key=lambda e: e.path):
                    lines.append(f"- **`{entry.path}`**")
                    if entry.key_entities:
                        lines.append(f"  - Entities: {', '.join(entry.key_entities[:5])}")
                lines.append("")
        
        # Configuration Section
        lines.append("---")
        lines.append("")
        lines.append("## ⚙️  Configuration Files")
        lines.append("")
        for key, entry in sorted(self.index.configuration.items()):
            category = key.split(":")[0]
            lines.append(f"- **`{entry.path}`** ({category})")
        lines.append("")
        
        # Active Work Section
        lines.append("---")
        lines.append("")
        lines.append("## 📋 Active Work")
        lines.append("")
        for key, value in sorted(self.index.active_work.items()):
            lines.append(f"- **{key.replace('_', ' ').title()}**: {value}")
        lines.append("")
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append("## 🔄 Maintenance")
        lines.append("")
        lines.append("Regenerate this index when:")
        lines.append("- Adding new documentation")
        lines.append("- Restructuring code organization")
        lines.append("- Starting new requirements")
        lines.append("- After major refactoring")
        lines.append("")
        lines.append("**Command**: `/index` in GitHub Copilot or `uv run python skills/generate_index.py`")
        
        output_file = self.root / output_path
        output_file.write_text("\n".join(lines))
        print(f"✅ Index exported: {output_file}")
    
    def _timestamp(self) -> str:
        """Generate ISO 8601 timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """CLI entry point."""
    generator = IndexGenerator()
    index = generator.generate()
    generator.export_markdown()
    print("\n✨ Index generation complete!")


if __name__ == "__main__":
    main()

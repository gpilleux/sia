#!/usr/bin/env python3
"""
SKILL: DDD Audit Tool
Description: Audits the codebase for Domain-Driven Design compliance.
Checks:
1. Domain Isolation: Domain layer must not import from Infrastructure or API.
2. Immutability: Domain entities should be frozen dataclasses.
3. Repository Pattern: Interfaces in Domain, Implementations in Infrastructure.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Tuple


class DDDAuditor:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir)
        self.domain_dir = self.root / "domain"
        self.infra_dir = self.root / "infrastructure"
        self.api_dir = self.root / "api"
        self.violations = []

    def audit(self):
        print(f"🔍 Auditing DDD Compliance in {self.root.resolve()}...")
        
        if not self.domain_dir.exists():
            print("⚠️  Domain directory not found. Skipping DDD audit.")
            return

        self._check_domain_isolation()
        self._check_entity_immutability()
        self._check_repository_pattern()
        
        self._report()

    def _check_domain_isolation(self):
        print("1️⃣  Checking domain layer isolation...")
        for py_file in self.domain_dir.rglob("*.py"):
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=str(py_file))
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        module = node.module if isinstance(node, ast.ImportFrom) else None
                        names = [n.name for n in node.names]
                        
                        # Check ImportFrom (from infrastructure import ...)
                        if module:
                            if module.startswith("infrastructure") or module.startswith("api"):
                                self.violations.append(
                                    f"❌ Violation in {py_file.relative_to(self.root)}: Imported '{module}' (Layer Violation)"
                                )
                        
                        # Check Import (import infrastructure.x)
                        for name in names:
                            if name.startswith("infrastructure") or name.startswith("api"):
                                self.violations.append(
                                    f"❌ Violation in {py_file.relative_to(self.root)}: Imported '{name}' (Layer Violation)"
                                )
            except Exception as e:
                print(f"⚠️  Could not parse {py_file}: {e}")

    def _check_entity_immutability(self):
        print("2️⃣  Checking entity immutability...")
        entities_file = self.domain_dir / "entities.py"
        if not entities_file.exists():
            return

        try:
            with open(entities_file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    is_dataclass = False
                    is_frozen = False
                    
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                            is_dataclass = True
                        elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == "dataclass":
                            is_dataclass = True
                            for keyword in decorator.keywords:
                                if keyword.arg == "frozen" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                                    is_frozen = True
                    
                    if is_dataclass and not is_frozen:
                        self.violations.append(
                            f"⚠️  Warning in {entities_file.relative_to(self.root)}: Entity '{node.name}' is not frozen (Mutable Domain Object)"
                        )
        except Exception as e:
            print(f"⚠️  Could not parse entities.py: {e}")

    def _check_repository_pattern(self):
        print("3️⃣  Checking repository pattern...")
        # Just checking existence for now
        domain_repos = list(self.domain_dir.glob("repositories/*.py"))
        infra_repos = list(self.infra_dir.glob("repositories/*.py"))
        
        if not domain_repos:
            print("⚠️  No repository interfaces found in domain/repositories/")
        if not infra_repos:
            print("⚠️  No repository implementations found in infrastructure/repositories/")

    def _report(self):
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if self.violations:
            print(f"❌ Found {len(self.violations)} DDD Violations:")
            for v in self.violations:
                print(v)
            sys.exit(1)
        else:
            print("✅ All DDD compliance checks passed.")
            sys.exit(0)

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    auditor = DDDAuditor(root)
    auditor.audit()

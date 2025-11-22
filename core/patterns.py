#!/usr/bin/env python3
import sys
from datetime import datetime
from pathlib import Path


class PatternRegistry:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        self.patterns_file = self.root / "docs" / "PATTERNS_LEARNED.md"
        self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.patterns_file.exists():
            self._init_file()

    def _init_file(self):
        content = """# PATTERNS LEARNED
**Knowledge Base of Architectural Decisions & Solutions**

This document records recurring patterns, solutions to complex problems, and architectural decisions.
It serves as the long-term memory of the system.

---

"""
        self.patterns_file.write_text(content)

    def register_pattern(self, name: str, context: str, solution: str):
        entry = f"""## {name}
**Date**: {datetime.now().strftime('%Y-%m-%d')}
**Context**: {context}
**Solution**: {solution}

---

"""
        # Append to file
        with open(self.patterns_file, "a") as f:
            f.write(entry)
            
        print(f"✅ Pattern '{name}' registered in {self.patterns_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: patterns.py <name> <context> <solution>")
        sys.exit(1)
        
    name = sys.argv[1]
    context = sys.argv[2]
    solution = sys.argv[3]
    
    PatternRegistry().register_pattern(name, context, solution)

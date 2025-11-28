# REQ-004: DOMAIN RESEARCH & ANALYSIS

**Requirement**: Skills Production Readiness Refactoring  
**Analysis Date**: 2025-11-25  
**Analyst**: SIA (Super Intelligence Agency - Inception Mode)

---

## RESEARCH PROTOCOL

### 1. CENTRAL QUESTION
**What patterns, error handling strategies, and cross-platform techniques do production-grade CLI tools use to ensure robust, reliable execution across different environments?**

Specifically:
- How do mature bash/shell tools handle exit codes and error propagation?
- What patterns do Python tooling frameworks use for graceful degradation?
- How do testing frameworks detect missing test directories without crashing?
- What are the best practices for AST parsing when files might have syntax errors?

### 2. INITIAL HYPOTHESIS

**Before Research**:
- Assumed: Simple `if command; then` checks sufficient for error handling
- Assumed: Hardcoded paths acceptable if documented
- Assumed: False positive messages not a critical issue
- Assumed: Skills only need to work in "happy path" scenarios

**Reality After Audit**:
- ❌ No exit code checking → false positives
- ❌ Hardcoded `sia/skills/` paths → inception mode failures
- ❌ Missing directories → hard crashes instead of warnings
- ❌ Tools designed for applications, not self-applicable to frameworks

---

## DEEPWIKI RESEARCH

### Repositories Consulted

#### koalaman/shellcheck
**Question**: What are the best practices for bash error handling, exit codes, and robust scripting? How to check command exit codes properly, implement graceful degradation, avoid false positives, and handle cross-platform paths?

**Findings**:

**Key Insights from ShellCheck**:
1. **Exit Code Patterns**: 
   - ShellCheck uses canonical exit codes (0 = success, 1 = issues found)
   - Check `SC2181`: Use command directly (`if command; then`) instead of `if [ $? -eq 0 ]`
   - Check `SC2312`: Warns about "Masked exit codes" (commands whose exit status is ignored)

2. **Error Propagation**:
   - `test/buildtest` demonstrates robust error handling
   - Pattern: After critical commands, check exit status and call `die()` on failure
   - Example from buildtest:
   ```bash
   cabal update || die "Failed to update"
   cabal install || die "Failed to install"
   cabal test || die "Tests failed"
   ```

3. **Graceful Degradation**:
   - `test/buildtest` shows fallback pattern for dependency installation
   - Try preferred method → If fails, attempt alternative methods
   - Example: Install deps with strict options, fallback to relaxed options

4. **Cross-Platform Paths**:
   - SC3051: Use `.` instead of `source` (portability)
   - SC2172: Avoid unportable redirection operators
   - SC2059: Warn about "Literal tilde in $PATH" (cross-platform issue)

**Conclusions**:
- ✅ **Direct Command Checks**: `if command; then` > `if [ $? -eq 0 ]; then`
- ✅ **Exit on Failure**: Use `die()` function or `exit 1` immediately after failed critical commands
- ✅ **Fallback Strategies**: Try preferred → fallback → inform user
- ✅ **Portability**: Avoid bash-specific features for cross-platform scripts

---

#### astral-sh/uv
**Question**: What are best practices for using uv to run Python scripts with ephemeral dependencies? How to handle missing packages gracefully, detect uv availability, and ensure cross-platform execution?

**Findings**:

**Key Insights from uv**:
1. **Ephemeral Dependencies** (`uv run --with`):
   - `uv run --with <package>` installs packages into ephemeral environment
   - Example: `uv run --with rich example.py`
   - Supports version constraints: `uv run --with 'rich>12,<13' example.py`
   - Multiple deps: Repeat `--with` flag
   - Isolated from project: `uv run --no-project --with X script.py`

2. **Inline Script Metadata (PEP 723)**:
   - **Recommended pattern**: Declare dependencies IN the script
   - `uv init --script` creates script with metadata
   - `uv add --script` manages dependencies
   - Example:
   ```python
   # /// script
   # dependencies = [
   #   "requests<3",
   #   "rich",
   # ]
   # ///
   
   import requests
   from rich.pretty import pprint
   ```

3. **Missing Package Handling**:
   - When deps missing: `uv run` fails with `ModuleNotFoundError`
   - **Solution**: Explicit dependency declaration (inline metadata preferred)
   - Ephemeral environment is cached (fast repeated runs)

4. **Detecting uv Availability**:
   - `python/uv/_find_uv.py` module shows detection pattern
   - `find_uv_bin()` searches: script dirs for current Python env, base prefix, user scheme
   - Raises `UvNotFound` error if not available
   - Platform-aware: Checks for `uv.exe` on Windows

5. **Cross-Platform Execution**:
   - **Shebang for Unix**: `#!/usr/bin/env -S uv run --script`
   - **Windows**: uv supports `.ps1`, `.cmd`, `.bat` extensions for legacy setuptools scripts
   - **Portable Pattern**: Python scripts > bash scripts for Windows compatibility

**Conclusions**:
- ✅ **PEP 723 Metadata**: Use inline script metadata for self-contained, portable scripts
- ✅ **Graceful Degradation**: Check for uv availability, provide installation guidance
- ✅ **Cross-Platform**: Python scripts inherently more portable than bash
- ✅ **Caching**: uv caches ephemeral environments (performance benefit)

---

#### pytest-dev/pytest
**Question**: How do Python testing frameworks handle fixture discovery, test collection, and graceful handling of missing test directories? What are patterns for robust testing scripts that detect whether tests exist before running?

**Findings**:

**Key Insights from pytest**:
1. **Test Collection**:
   - Auto-discovery: Scans filesystem, uses Python introspection
   - Default patterns: `test_*.py` or `*_test.py`
   - Recursion: Into directories unless matching `norecursedirs` patterns
   - Default excludes: `*.egg`, `.*`, `build`, `dist`, `node_modules`, `venv`

2. **Missing Test Directories**:
   - **Graceful Handling**: pytest doesn't crash, just reports "collected 0 items"
   - Exit code 5: No tests collected (distinguishable from failure)
   - Example: Non-existent dirs passed as args → rootdir determined, 0 tests collected

3. **Detecting Tests Programmatically**:
   - `pytest --collect-only`: Preview collection without execution
   - Parse output for "collected 0 items" → no tests found
   - **Pattern for Scripts**: Check exit code (5 = no tests, 0 = passed, 1 = failed)

4. **Configuration**:
   - `testpaths` in pytest.ini/pyproject.toml controls search scope
   - `--ignore` / `--ignore-glob`: Exclude dirs/files explicitly
   - Prevents accidental collection of non-test files

**Conclusions**:
- ✅ **Exit Code Strategy**: Use distinct codes (0=success, 1=failure, 5=no tests)
- ✅ **Graceful Degradation**: Missing test dirs → warning + exit 0 (not error)
- ✅ **Precondition Checks**: Validate directory exists before attempting collection
- ✅ **Clear Messaging**: "No tests found" ≠ "Tests failed"

---

#### python/cpython
**Question**: What are best practices for Python AST parsing, detecting imports, and analyzing code structure? How to safely parse files with syntax errors, detect cross-module dependencies, analyze decorators?

**Findings**:

**Key Insights from CPython AST**:
1. **Safe Parsing**:
   - `ast.parse()` raises `SyntaxError` on invalid syntax
   - **Best Practice**: Wrap in try/except
   ```python
   try:
       tree = ast.parse(source_code, filename=filepath)
   except SyntaxError as e:
       print(f"⚠️  Syntax error in {filepath}: {e}")
       return  # Skip file, continue analysis
   ```

2. **Detecting Imports**:
   - `ast.Import`: Represents `import x, y, z`
     - `names` attribute: list of `alias` nodes
     - Each `alias`: `name` (module) + optional `asname`
   - `ast.ImportFrom`: Represents `from x import y`
     - `module` attribute: module being imported from
     - `names`: list of `alias` nodes (imported objects)
     - `level`: for relative imports

3. **Analyzing Decorators**:
   - `ClassDef` and `FunctionDef` nodes have `decorator_list` attribute
   - Pattern for checking `@dataclass(frozen=True)`:
   ```python
   for node in ast.walk(tree):
       if isinstance(node, ast.ClassDef):
           for decorator in node.decorator_list:
               if isinstance(decorator, ast.Call):
                   if decorator.func.id == "dataclass":
                       for keyword in decorator.keywords:
                           if keyword.arg == "frozen":
                               is_frozen = keyword.value.value
   ```

4. **Traversal Patterns**:
   - `ast.walk()`: Yields all nodes (depth-first)
   - `ast.NodeVisitor`: Define `visit_<NodeType>` methods
   - `ast.NodeTransformer`: Modify AST (for code transformation)

5. **Error Reporting**:
   - AST nodes provide `lineno` and `col_offset` for precise location
   - Use for meaningful error messages: `f"Error at {filepath}:{node.lineno}:{node.col_offset}"`

**Conclusions**:
- ✅ **Safe Parsing**: Always wrap `ast.parse()` in try/except SyntaxError
- ✅ **Import Detection**: Check both `ast.Import` and `ast.ImportFrom` nodes
- ✅ **Decorator Analysis**: Inspect `decorator_list`, handle both Name and Call nodes
- ✅ **Error Context**: Use lineno/col_offset for precise error reporting

---

## CURRENT TECH STACK ANALYSIS

### Relevant Existing Components

#### check_complexity.sh
**Location**: `skills/check_complexity.sh`  
**Current Pattern**: 
- Uses `uv run --with radon` (ephemeral dependency - GOOD)
- Hardcoded `sia/skills/metrics.py` path (BAD - breaks inception)
- No error handling for radon command (BAD - false positives)
- Excludes common patterns (tests, venv, sia/) - GOOD

**Reusable**: YES (core logic sound)  
**Modification Needed**: 
- Add inception mode detection
- Fix metrics path resolution
- Add error handling for radon command
- Remove false positive success messages

---

#### visualize_architecture.sh
**Location**: `skills/visualize_architecture.sh`  
**Current Pattern**:
- Uses `uv run --with pydeps` (GOOD)
- Wrong flag: `--output` should be `-o` (CRITICAL BUG)
- No error handling (BAD)
- Always prints "✅ Graph generated" (FALSE POSITIVE)

**Reusable**: PARTIALLY (ephemeral dep pattern good, rest broken)  
**Modification Needed**:
- Fix pydeps flag: `--output` → `-o`
- Add `if pydeps_command; then success; else fail; fi` pattern
- Fix metrics path resolution
- Remove unconditional success message

---

#### check_coverage.sh
**Location**: `skills/check_coverage.sh`  
**Current Pattern**:
- Uses `uv run --with pytest --with pytest-cov` (GOOD)
- No validation if tests/ exists (BAD - crashes on missing dir)
- No check if pytest collected tests (BAD)
- Always prints "✅ Coverage report generated" (FALSE POSITIVE)

**Reusable**: PARTIALLY  
**Modification Needed**:
- Add precondition check: `if [ ! -d "$TEST_DIR" ]; then warn; exit 0; fi`
- Check pytest exit code (0=passed, 5=no tests, 1=failed)
- Conditional success message based on actual result
- Fix metrics path resolution

---

#### audit_ddd.py
**Location**: `skills/audit_ddd.py`  
**Current Pattern**:
- AST parsing logic sound (GOOD)
- Hardcoded assumption: domain/ exists (BAD - inception blind)
- Rank C complexity in 2 methods (BAD - violates own quality standards)
- Silent skip when domain/ missing (BAD - not actionable)

**Reusable**: PARTIALLY (AST logic good, assumptions bad)  
**Modification Needed**:
- Add inception detection: `if exists(core/SUPER_AGENT.md): skip_ddd_audit()`
- Refactor Rank C methods (_check_entity_immutability, _check_domain_isolation)
- Clear messaging why skipping (meta-framework vs application)
- Wrap `ast.parse()` in try/except SyntaxError (safe parsing)

---

#### metrics.py
**Location**: `skills/metrics.py`  
**Current Pattern**:
- Hardcoded path: `.agents/skills_metrics.yaml` (LEGACY STRUCTURE)
- Simple, focused responsibility (GOOD - SRP)
- YAML persistence (GOOD)

**Reusable**: YES (after path fix)  
**Modification Needed**:
- Add inception detection
- Dynamic path: `skills/metrics.yaml` (inception) vs `.sia/metrics.yaml` (submodule)
- Make metrics logging optional (non-blocking if fails)

---

## ARCHITECTURAL DECISIONS

### Chosen Implementation Pattern: **Inception-Aware Dual-Mode Execution**

**Core Strategy**:
All skills detect execution context (inception vs submodule) and adapt behavior accordingly.

**Detection Mechanism**:
```bash
# Bash
if [ -f "core/SUPER_AGENT.md" ]; then
    INCEPTION_MODE=true
    SKILLS_DIR="skills"
else
    INCEPTION_MODE=false
    SKILLS_DIR="sia/skills"
fi
```

```python
# Python
from pathlib import Path

def is_inception_mode(root: Path = Path(".")) -> bool:
    """Detect if running in SIA framework itself (inception) or inherited project (submodule)."""
    return (root / "core" / "SUPER_AGENT.md").exists()

def get_metrics_path(root: Path = Path(".")) -> Path:
    """Return correct metrics file path based on execution mode."""
    if is_inception_mode(root):
        return root / "skills" / "metrics.yaml"
    else:
        return root / ".sia" / "metrics.yaml"
```

**Justification**:
- **DDD**: Skills bounded context remains pure (no domain coupling)
- **SOLID**: 
  - SRP: Each skill single responsibility unchanged
  - OCP: Extensible (supports both modes without modifying core logic)
  - DIP: Depends on abstraction (file existence check) not concrete paths
- **KISS**: Simple boolean check, minimal complexity
- **Clean Code**: Self-documenting (`is_inception_mode()` clearly states intent)

---

### Error Handling Pattern: **ShellCheck-Compliant Exit Code Propagation**

**Strategy**:
Use direct command checks with explicit error handling and accurate exit codes.

**Implementation**:
```bash
# BEFORE (broken)
uv run --with pydeps pydeps "$TARGET" --output "$OUTPUT"
echo "✅ Graph generated at $OUTPUT"  # Always prints, even if failed

# AFTER (correct)
if uv run --with pydeps pydeps "$TARGET" -o "$OUTPUT"; then
    echo "✅ Graph generated at $OUTPUT"
    exit 0
else
    echo "❌ Failed to generate graph"
    echo "   Hint: Ensure uv is installed: pip install uv"
    exit 1
fi
```

**Justification**:
- **ShellCheck SC2312**: Avoids masked exit codes
- **ShellCheck SC2181**: Direct command check (not `if [ $? -eq 0 ]`)
- **KISS**: Straightforward if/then/else, no complex state tracking
- **Reliability**: Exit code accurately reflects outcome

---

### Graceful Degradation Pattern: **pytest-Inspired Precondition Checks**

**Strategy**:
Validate preconditions (directories exist, tools available) before execution, provide helpful guidance on failure.

**Implementation**:
```bash
# Check if test directory exists
if [ ! -d "$TEST_DIR" ]; then
    echo "⚠️  Test directory '$TEST_DIR' not found"
    echo "   This is not an error - no tests to run."
    echo "   To enable coverage analysis:"
    echo "   1. Create tests/ directory"
    echo "   2. Add test files (test_*.py)"
    echo "   3. Run again: $0"
    exit 0  # Exit gracefully, not with error
fi

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo "   Install: pip install uv"
    echo "   Or: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
```

**Justification**:
- **pytest pattern**: Exit code 0 for "no tests" (not failure, just nothing to do)
- **UX**: Clear, actionable error messages with installation hints
- **KISS**: Simple existence checks before execution
- **Reliability**: Prevents cryptic errors from missing deps

---

### Safe AST Parsing Pattern: **CPython Best Practice**

**Strategy**:
Wrap all `ast.parse()` calls in try/except, skip files with syntax errors, continue analysis.

**Implementation**:
```python
def analyze_file(filepath: Path) -> List[Violation]:
    violations = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(filepath))
    except SyntaxError as e:
        print(f"⚠️  Syntax error in {filepath.relative_to(root)}")
        print(f"   Line {e.lineno}: {e.msg}")
        return violations  # Skip file, don't crash
    except Exception as e:
        print(f"⚠️  Could not parse {filepath}: {e}")
        return violations
    
    # Continue with AST analysis...
    for node in ast.walk(tree):
        # ... analyze nodes ...
    
    return violations
```

**Justification**:
- **CPython pattern**: Standard approach in inspect.py, ast module itself
- **Robustness**: Analysis continues even if some files have syntax errors
- **Clear reporting**: User sees which files skipped and why
- **KISS**: Simple try/except, no complex error recovery

---

### Alternatives Considered and Discarded

#### Alternative 1: Configuration File Approach
**Description**: Use `.sia.config.yaml` to explicitly declare inception mode.

**Discarded because**:
- **KISS Violation**: Adds unnecessary configuration burden
- **Fragility**: User must remember to create/update config file
- **Auto-Detection Better**: File existence check (`core/SUPER_AGENT.md`) is definitive, zero-config

---

#### Alternative 2: Python Rewrites for All Skills
**Description**: Convert all bash scripts to Python for consistency.

**Discarded because**:
- **KISS Violation**: Bash sufficient for simple tasks (complexity check, coverage run)
- **Performance**: Bash subprocess spawning faster than Python imports for simple workflows
- **Maintenance**: Hybrid approach (bash for simple, Python for complex) clearer intent
- **Partial Adoption**: Keep Python for audit_ddd.py (complex AST), bash for others

---

#### Alternative 3: Hardcoded Platform Detection
**Description**: Use `uname -s` to detect OS, adjust paths accordingly.

**Discarded because**:
- **Wrong Problem**: Issue is inception vs submodule, not OS-specific paths
- **Over-Engineering**: File existence check simpler and more reliable
- **KISS Violation**: Adds complexity without solving actual problem

---

## EXTRACTED INVARIANTS

### Formal Constraints (Mathematical/Logical)

Based on research and current architecture:

1. **Exit Code Invariant**:
   ```
   ∀ skill_execution e: (e.command_succeeds ⇒ e.exit_code = 0) ∧ (¬e.command_succeeds ⇒ e.exit_code ≠ 0)
   ```

2. **Path Resolution Invariant**:
   ```
   resolve_path(skill) = first_match([root/skills/skill, root/sia/skills/skill, ∅])
   ```

3. **Inception Detection Invariant**:
   ```
   is_inception(root) ⇔ exists(root/core/SUPER_AGENT.md)
   ```

4. **Message Consistency Invariant**:
   ```
   ∀ output_message m: (m = "✅ Success" ⇒ exit_code = 0) ∧ (exit_code ≠ 0 ⇒ m ≠ "✅ Success")
   ```

5. **Graceful Degradation Invariant**:
   ```
   ∀ resource r ∈ required_resources: ¬exists(r) ⇒ (warn_user ∧ exit_gracefully ∧ ¬crash)
   ```

6. **Tool Availability Invariant**:
   ```
   ∀ tool t ∈ {radon, pydeps, pytest}: ¬available(t) ⇒ (provide_install_guide ∧ exit(1))
   ```

7. **Safe Parsing Invariant**:
   ```
   ∀ file f: has_syntax_error(f) ⇒ (log_warning ∧ skip_file ∧ ¬crash_analysis)
   ```

8. **Metrics Optional Invariant**:
   ```
   ∀ skill_execution e: metrics_logging_fails(e) ⇏ skill_execution_fails(e)
   ```
   (Metrics failure does NOT imply skill failure - logging is optional)

---

## IMPLEMENTATION ROADMAP

### Phase 1: Critical Fixes (Immediate - QUANT 001-004)
1. Fix `visualize_architecture.sh` pydeps flag
2. Add inception mode detection to all skills
3. Implement path resolution utility
4. Fix metrics.py path handling

### Phase 2: Error Handling (High Priority - QUANT 005-006)
5. Add precondition checks (directories, tools)
6. Remove false positive success messages
7. Implement proper exit code propagation

### Phase 3: Documentation & Polish (Medium Priority - QUANT 007-009)
8. Add --help flags with usage examples
9. Refactor audit_ddd.py Rank C functions
10. Create comprehensive skills/README.md

### Phase 4: Validation (QUANT 010)
11. Integration tests: Execute all skills on SIA framework
12. Verify zero errors in inception mode
13. Validate cross-platform execution (macOS, Linux, Windows/Python)

---

## CONCLUSION

**Research Outcome**: Evidence-based patterns identified from 4 mature open-source projects (ShellCheck, uv, pytest, CPython).

**Key Discoveries**:
- ✅ ShellCheck: Direct command checks, exit code propagation, graceful fallbacks
- ✅ uv: PEP 723 inline metadata, ephemeral deps, cross-platform execution
- ✅ pytest: Exit code 5 for "no tests", graceful missing directory handling
- ✅ CPython: Safe AST parsing with try/except, clear error reporting

**Implementation Confidence**: HIGH
- All patterns proven in production codebases
- No speculative architecture
- Clear, actionable patterns ready for QUANT decomposition

**Next Step**: Create QUANT breakdown with atomic, testable tasks based on these patterns.

---

**Status**: Domain analysis complete | Evidence-based | Ready for QUANT decomposition

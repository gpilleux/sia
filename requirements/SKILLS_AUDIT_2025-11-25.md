# SKILLS AUDIT REPORT - Critical Analysis
**Date**: 2025-11-25  
**Mode**: Self-Audit (Inception)  
**Objective**: Evaluate if current skills achieve framework goals or require refactoring

---

## EXECUTIVE SUMMARY

**Status**: 🔴 **CRITICAL FAILURES DETECTED**

All skills executed with errors. None achieved their stated objectives. Immediate refactoring required.

**Root Causes Identified**:
1. **Hardcoded path assumptions** (sia/ submodule vs inception mode)
2. **Missing error handling** (tools not installed, directories not found)
3. **Broken metrics integration** (uv run sia/skills/metrics.py fails)
4. **Wrong pydeps flag** (--output vs -o)
5. **No graceful degradation** (tests/ not found = complete failure)
6. **Inception blindness** (audit_ddd.py expects domain/ but SIA is meta-framework)

---

## SKILL-BY-SKILL ANALYSIS

### 1. check_complexity.sh ✅ PARTIALLY WORKING

**Execution Result**:
```bash
✅ SUCCESS: Radon analysis executed correctly
✅ Detected 6 Rank C functions (actionable)
❌ FAILURE: Metrics logging crashed (uv run sia/skills/metrics.py)
```

**Code Quality**: 🟡 **ACCEPTABLE**
- ✅ Uses `uv run --with radon` (correct ephemeral execution)
- ✅ Excludes common patterns (tests, venv, sia/)
- ❌ Hardcoded path: `sia/skills/metrics.py` (breaks in inception)
- ❌ No error handling for metrics failure

**Actionability**: ✅ **HIGH**
- Output clearly identifies refactoring candidates
- Rank C/D/E distinction useful for prioritization
- Maintainability Index provides additional signal

**Proposed Fix**:
```bash
# Detect if running in inception mode or submodule mode
if [ -f "skills/metrics.py" ]; then
    METRICS_PATH="skills/metrics.py"
elif [ -f "sia/skills/metrics.py" ]; then
    METRICS_PATH="sia/skills/metrics.py"
else
    METRICS_PATH=""
fi

if [ -n "$METRICS_PATH" ]; then
    uv run --with pyyaml python3 "$METRICS_PATH" check_complexity target="$TARGET_DIR" 2>/dev/null || true
fi
```

**Refactor Priority**: 🟡 **MEDIUM** (works, but needs robustness)

---

### 2. visualize_architecture.sh ❌ BROKEN

**Execution Result**:
```bash
❌ CRITICAL: pydeps error "unrecognized arguments: --output"
❌ FAILURE: Metrics logging crashed
✅ FALSE POSITIVE: "Graph generated" despite failure
```

**Code Quality**: 🔴 **POOR**
- ❌ Wrong flag: `--output` should be `-o`
- ❌ Misleading success message (always prints "✅ Graph generated")
- ❌ No exit code propagation (script exits 0 even on failure)
- ❌ Hardcoded sia/skills/metrics.py path

**Actionability**: ❌ **ZERO** (doesn't generate output)

**Proposed Fix**:
```bash
# Correct flag
if uv run --with pydeps pydeps "$TARGET_DIR" \
    --exclude "tests/*" "venv/*" "migrations/*" "sia/*" ".venv/*" \
    --noshow \
    --max-bacon 2 \
    -o "$OUTPUT_FILE"; then
    echo "✅ Graph generated at $OUTPUT_FILE"
else
    echo "❌ Failed to generate graph"
    exit 1
fi
```

**Refactor Priority**: 🔴 **CRITICAL** (completely broken)

---

### 3. check_coverage.sh ❌ BROKEN

**Execution Result**:
```bash
❌ CRITICAL: "ERROR: file or directory not found: tests/"
❌ FAILURE: Metrics logging crashed
✅ FALSE POSITIVE: "Coverage report generated" despite no tests
```

**Code Quality**: 🔴 **POOR**
- ❌ No check if tests/ directory exists
- ❌ No validation if pytest found any tests
- ❌ Misleading success message (always prints "✅ Coverage report generated")
- ❌ Hardcoded sia/skills/metrics.py path
- ❌ Doesn't handle pytest not installed gracefully

**Actionability**: ❌ **ZERO** (no tests = no coverage)

**Architecture Problem**: **INCEPTION BLINDNESS**
- SIA framework has NO tests/ directory
- Skill assumes all projects have tests (wrong assumption)
- Should detect: "This is a tool/framework, not an application"

**Proposed Fix**:
```bash
# Check if test directory exists
if [ ! -d "$TEST_DIR" ]; then
    echo "⚠️  Test directory '$TEST_DIR' not found"
    echo "   Available options:"
    echo "   1. Create tests/ directory and add tests"
    echo "   2. Specify different test directory: $0 . path/to/tests"
    exit 0  # Not an error, just no tests to run
fi

# Run pytest and check result
if uv run --with pytest --with pytest-cov pytest --cov="$TARGET_DIR" --cov-report=html:coverage_report "$TEST_DIR"; then
    echo "✅ Coverage report generated in coverage_report/index.html"
else
    echo "❌ Tests failed or no tests collected"
    exit 1
fi
```

**Refactor Priority**: 🔴 **CRITICAL** (misleading, broken)

---

### 4. audit_ddd.py ❌ BROKEN

**Execution Result**:
```bash
❌ CRITICAL: "Domain directory not found. Skipping DDD audit."
```

**Code Quality**: 🔴 **POOR**
- ❌ Hardcoded assumption: domain/ exists
- ❌ No inception awareness (SIA is meta-framework, not DDD application)
- ❌ Silent skip (exits 0, no actionable feedback)
- ❌ Rank C complexity in 2 methods (detected by check_complexity.sh)
- ✅ Good: AST parsing logic is sound
- ✅ Good: Violation messages are clear

**Architecture Problem**: **PURPOSE MISMATCH**
- Designed for DDD applications (domain/, infrastructure/, api/)
- SIA framework has different structure (core/, agents/, skills/)
- Should either:
  1. Detect project type and skip if meta-framework
  2. Support auditing framework architecture (core → agents → skills)

**Actionability**: ❌ **ZERO** (skips execution entirely)

**Proposed Fix** (Two Strategies):

**Strategy A: Add Inception Detection**
```python
def audit(self):
    print(f"🔍 Auditing DDD Compliance in {self.root.resolve()}...")
    
    # Detect if this is SIA framework itself
    if (self.root / "core" / "SUPER_AGENT.md").exists():
        print("⚠️  Detected SIA framework (meta-framework).")
        print("   Skipping DDD audit (framework uses different architecture).")
        return
    
    if not self.domain_dir.exists():
        print("⚠️  Domain directory not found.")
        print("   This tool audits DDD-structured projects (domain/, infrastructure/, api/).")
        print("   Not applicable to this repository.")
        return
```

**Strategy B: Framework-Aware Audit**
```python
def audit(self):
    if self._is_sia_framework():
        self._audit_framework_architecture()
    elif self.domain_dir.exists():
        self._audit_ddd_application()
    else:
        print("⚠️  No recognizable architecture pattern detected")
        
def _audit_framework_architecture(self):
    # Check core/ doesn't import from agents/
    # Check agents/ doesn't import from installer/
    # Check installer/ can import from core/
    # etc.
```

**Refactor Priority**: 🔴 **CRITICAL** (wrong tool for the job)

---

### 5. metrics.py ❌ BROKEN (Root Cause of All Failures)

**Execution Result**:
```bash
❌ CRITICAL: "error: Failed to spawn: `sia/skills/metrics.py`"
```

**Code Quality**: 🔴 **POOR**
- ❌ Hardcoded path: `.agents/skills_metrics.yaml` (legacy structure)
- ❌ Should use `.sia/metrics.yaml` or `skills/metrics.yaml`
- ❌ No inception detection
- ❌ Called via `uv run sia/skills/metrics.py` (breaks if sia/ doesn't exist)
- ✅ Good: Simple, focused responsibility

**Architecture Problem**: **DOUBLE FAULT**
1. Skills hardcode `sia/skills/metrics.py` (assumes submodule)
2. Metrics hardcodes `.agents/` (assumes legacy structure)

**Proposed Fix**:
```python
class SkillMetrics:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        
        # Detect if running in inception mode or submodule mode
        if (self.root / "core" / "SUPER_AGENT.md").exists():
            # Inception mode: we ARE the framework
            self.metrics_file = self.root / "skills" / "metrics.yaml"
        else:
            # Submodule mode: inherited project
            self.metrics_file = self.root / ".sia" / "metrics.yaml"
        
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
```

**Refactor Priority**: 🔴 **CRITICAL** (breaks all other skills)

---

## CROSS-CUTTING ISSUES

### Issue 1: Inception Blindness
**Problem**: All skills assume they're running in a DDD application with tests/, domain/, etc.  
**Reality**: SIA framework is a meta-framework with core/, agents/, skills/  
**Impact**: 100% skill failure rate in inception mode  

**Fix**: Add inception detection to all skills:
```bash
# Detect inception mode
if [ -f "core/SUPER_AGENT.md" ]; then
    INCEPTION_MODE=true
else
    INCEPTION_MODE=false
fi
```

### Issue 2: Hardcoded Paths
**Problem**: `uv run sia/skills/metrics.py` assumes sia/ submodule  
**Reality**: In inception, skills/ is at root  
**Impact**: All metrics logging fails  

**Fix**: Path resolution utility:
```bash
resolve_skill_path() {
    local skill=$1
    if [ -f "skills/$skill" ]; then
        echo "skills/$skill"
    elif [ -f "sia/skills/$skill" ]; then
        echo "sia/skills/$skill"
    else
        echo ""
    fi
}
```

### Issue 3: False Positive Messages
**Problem**: Scripts print "✅ Success" even when commands failed  
**Reality**: No exit code checking, no validation  
**Impact**: User thinks skills work, but they don't  

**Fix**: Proper error handling:
```bash
if command_that_might_fail; then
    echo "✅ Success"
else
    echo "❌ Failed"
    exit 1
fi
```

### Issue 4: No Graceful Degradation
**Problem**: Missing tests/ = hard failure  
**Reality**: Some projects have no tests yet (early stage)  
**Impact**: Skill unusable for greenfield projects  

**Fix**: Informative warnings instead of errors:
```bash
if [ ! -d "$TEST_DIR" ]; then
    echo "⚠️  No tests found. Coverage analysis skipped."
    echo "   Hint: Create tests/ directory to enable this skill."
    exit 0  # Warning, not error
fi
```

---

## EVALUATION VS FRAMEWORK GOALS

### Goal 1: "High-leverage analysis tools"
**Status**: 🔴 **NOT ACHIEVED**
- Tools that don't run have zero leverage
- False positives waste time (negative leverage)

### Goal 2: "Exponential productivity"
**Status**: 🔴 **NOT ACHIEVED**
- Debugging broken skills = negative productivity
- Manual workarounds = linear at best

### Goal 3: "Validation gates for QUANT"
**Status**: 🔴 **NOT ACHIEVED**
- Can't use as verification gates if they crash
- Misleading success messages = dangerous (false confidence)

### Goal 4: "Cross-platform compatible"
**Status**: 🟡 **PARTIALLY ACHIEVED**
- Bash scripts work on macOS/Linux
- Windows .bat equivalents don't exist
- Python scripts would be more portable

### Goal 5: "Framework self-application (dogfooding)"
**Status**: 🔴 **FAILED**
- Framework can't audit itself
- Inception mode not supported
- Skills designed for applications, not frameworks

---

## REFACTORING RECOMMENDATIONS

### Priority 1: Fix Broken Basics (CRITICAL)
1. **visualize_architecture.sh**: Fix --output → -o flag
2. **metrics.py**: Add inception mode detection
3. **All skills**: Fix hardcoded sia/ paths
4. **All skills**: Add proper error handling + exit codes

### Priority 2: Add Inception Awareness (HIGH)
1. Detect if running in SIA framework itself
2. Skip or adapt behavior accordingly
3. Provide clear messages why skipping

### Priority 3: Improve Robustness (MEDIUM)
1. Check tool availability (pydeps, radon, pytest)
2. Validate preconditions (tests/ exists, domain/ exists)
3. Remove false positive success messages
4. Add --help flags with usage examples

### Priority 4: Best Practices Alignment (LOW)
1. Python scripts > Bash scripts (cross-platform)
2. Single Responsibility (metrics.py logging vs execution)
3. Reduce complexity in audit_ddd.py (Rank C functions)
4. Add unit tests for skills themselves (meta-testing)

---

## PROPOSED QUANT BREAKDOWN (REQ-004)

**Requirement**: Refactor Skills for Production Readiness

**QUANT-001**: Fix visualize_architecture.sh pydeps flag + error handling  
**QUANT-002**: Add inception mode detection to all skills  
**QUANT-003**: Implement dynamic path resolution (skills/ vs sia/skills/)  
**QUANT-004**: Fix metrics.py path detection + .sia/ migration  
**QUANT-005**: Add precondition checks (tools installed, directories exist)  
**QUANT-006**: Remove false positive success messages  
**QUANT-007**: Add --help and usage documentation  
**QUANT-008**: Refactor audit_ddd.py Rank C functions  
**QUANT-009**: Create skills/README.md with execution examples  
**QUANT-010**: Add integration tests (skills execute without errors)  

---

## CONCLUSION

**Current State**: Skills are **proof-of-concept quality**, not production-ready.

**Impact**: Framework claims "high-leverage tools" but delivers broken scripts.

**Integrity Violation**: Dogfooding failure (can't use our own tools on our own code).

**Recommendation**: **HALT feature development. Fix skills first.**

**Rationale**: 
- Skills are verification gates for QUANT
- Broken gates = no quality assurance
- Quality framework needs quality tools

**Next Step**: Create REQ-004 (Skills Refactoring) with full QUANT breakdown.

---

**Status**: Audit complete | Evidence-based | Ready for REQ formalization

#!/usr/bin/env python3
"""
QUANT-001 Validation Script - File-Based Protocol

Purpose: Validate REQ-011 QUANT-001 acceptance criteria.

Validates:
    1. Runtime directory structure (.sia/runtime/{session_id}/)
    2. Status file schema (status.yaml with required fields)
    3. Output file format (SPR markdown compliance)
    4. Polling mechanism (no CPU spike, 2s interval)
    5. Progress tracking integration (research-specialist.agent.md)

Usage:
    python .sia/requirements/REQ-011/validate_quant001.py
    
Exit codes:
    0: All validations passed
    1: Validation failed (see error output)

Requirements:
    - Python 3.10+
    - PyYAML (optional, for status parsing)
    - SIA framework (runtime directory structure)
"""

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("⚠️  PyYAML not installed. Install with: uv pip install pyyaml", file=sys.stderr)
    sys.exit(1)


class ValidationResult:
    """Validation result container"""
    
    def __init__(self, name: str):
        self.name = name
        self.passed = True
        self.errors: list[str] = []
        self.warnings: list[str] = []
    
    def fail(self, error: str):
        """Mark validation as failed"""
        self.passed = False
        self.errors.append(error)
    
    def warn(self, warning: str):
        """Add warning (doesn't fail validation)"""
        self.warnings.append(warning)
    
    def __str__(self) -> str:
        """String representation"""
        status = "✅ PASS" if self.passed else "❌ FAIL"
        result = f"{status} - {self.name}\n"
        
        if self.errors:
            result += "  Errors:\n"
            for error in self.errors:
                result += f"    - {error}\n"
        
        if self.warnings:
            result += "  Warnings:\n"
            for warning in self.warnings:
                result += f"    - {warning}\n"
        
        return result


class QUANT001Validator:
    """QUANT-001 acceptance criteria validator"""
    
    def __init__(self, root_dir: Optional[Path] = None):
        """
        Initialize validator.
        
        Args:
            root_dir: SIA framework root (default: current working directory)
        """
        self.root = root_dir or Path.cwd()
        self.runtime_dir = self.root / ".sia" / "runtime"
        self.results: list[ValidationResult] = []
    
    def validate_runtime_structure(self) -> ValidationResult:
        """
        Validate: Runtime directory structure exists.
        
        Checks:
            - .sia/runtime/ directory exists
            - README.md documentation present
            - .gitkeep marker file present
        """
        result = ValidationResult("Runtime Directory Structure")
        
        # Check runtime directory
        if not self.runtime_dir.exists():
            result.fail(f"Runtime directory missing: {self.runtime_dir}")
            return result
        
        # Check README
        readme = self.runtime_dir / "README.md"
        if not readme.exists():
            result.warn("README.md missing (documentation recommended)")
        
        # Check .gitkeep
        gitkeep = self.runtime_dir / ".gitkeep"
        if not gitkeep.exists():
            result.warn(".gitkeep missing (git tracking recommended)")
        
        return result
    
    def validate_status_schema(self) -> ValidationResult:
        """
        Validate: Status file schema defined.
        
        Checks:
            - README.md documents status.yaml schema
            - Required fields: state, updated_at, progress_percent, current_task, findings_count, errors
            - State enum values documented
        """
        result = ValidationResult("Status File Schema")
        
        readme = self.runtime_dir / "README.md"
        if not readme.exists():
            result.fail("README.md missing (schema not documented)")
            return result
        
        content = readme.read_text()
        
        # Check required fields documented
        required_fields = [
            'state',
            'updated_at',
            'progress_percent',
            'current_task',
            'findings_count',
            'errors'
        ]
        
        for field in required_fields:
            if field not in content:
                result.fail(f"Schema field not documented: {field}")
        
        # Check state enum values
        state_values = ['initializing', 'in_progress', 'completed', 'failed']
        for state in state_values:
            if state not in content:
                result.warn(f"State value not documented: {state}")
        
        return result
    
    def validate_output_format(self) -> ValidationResult:
        """
        Validate: SPR output template exists.
        
        Checks:
            - templates/SPR_OUTPUT_TEMPLATE.md exists
            - Contains required sections: FINDINGS, SYNTHESIS, CODE EXAMPLES, RECOMMENDATIONS, METADATA
            - Compression principles documented
            - Validation checklist present
        """
        result = ValidationResult("SPR Output Format Template")
        
        template = self.root / "templates" / "SPR_OUTPUT_TEMPLATE.md"
        if not template.exists():
            result.fail(f"SPR template missing: {template}")
            return result
        
        content = template.read_text()
        
        # Check required sections
        required_sections = [
            '## FINDINGS',
            '## SYNTHESIS',
            '## CODE EXAMPLES',
            '## RECOMMENDATIONS',
            '## METADATA'
        ]
        
        for section in required_sections:
            if section not in content:
                result.fail(f"Template section missing: {section}")
        
        # Check compression principles
        if '## Compression Principles' not in content:
            result.warn("Compression principles not documented")
        
        # Check validation checklist
        if '## Validation Checklist' not in content:
            result.warn("Validation checklist not documented")
        
        return result
    
    def validate_status_update_snippet(self) -> ValidationResult:
        """
        Validate: Status update Python snippet exists.
        
        Checks:
            - templates/sia_status_update.py exists
            - update_status() function defined
            - log_progress() function defined
            - SIA_STATUS_FILE environment variable used
            - YAML import with fallback
        """
        result = ValidationResult("Status Update Snippet")
        
        snippet = self.root / "templates" / "sia_status_update.py"
        if not snippet.exists():
            result.fail(f"Status update snippet missing: {snippet}")
            return result
        
        content = snippet.read_text()
        
        # Check functions defined
        if 'def update_status(' not in content:
            result.fail("update_status() function not defined")
        
        if 'def log_progress(' not in content:
            result.fail("log_progress() function not defined")
        
        # Check environment variable usage
        if 'SIA_STATUS_FILE' not in content:
            result.fail("SIA_STATUS_FILE environment variable not used")
        
        # Check YAML import
        if 'import yaml' not in content:
            result.warn("YAML import missing (status updates won't work)")
        
        return result
    
    def validate_orchestrator_skill(self) -> ValidationResult:
        """
        Validate: Orchestrator skill implemented.
        
        Checks:
            - skills/orchestrate_subagents.py exists
            - SubAgentOrchestrator class defined
            - Key methods: create_session(), spawn_agent(), spawn_parallel(), poll_status(), monitor_progress()
            - CLI subprocess spawning (copilot --agent)
        """
        result = ValidationResult("Orchestrator Skill")
        
        skill = self.root / "skills" / "orchestrate_subagents.py"
        if not skill.exists():
            result.fail(f"Orchestrator skill missing: {skill}")
            return result
        
        content = skill.read_text()
        
        # Check class defined
        if 'class SubAgentOrchestrator' not in content:
            result.fail("SubAgentOrchestrator class not defined")
        
        # Check methods
        required_methods = [
            'def create_session(',
            'def spawn_agent(',
            'def spawn_parallel(',
            'def poll_status(',
            'def monitor_progress(',
            'def consolidate_results('
        ]
        
        for method in required_methods:
            if method not in content:
                result.fail(f"Method missing: {method}")
        
        # Check CLI spawning
        if 'copilot' not in content or '--agent' not in content:
            result.fail("CLI subprocess spawning not implemented")
        
        # Check polling interval
        if 'poll_interval' not in content:
            result.warn("Polling interval not configurable")
        
        return result
    
    def validate_research_specialist_integration(self) -> ValidationResult:
        """
        Validate: Research Specialist agent updated with progress tracking.
        
        Checks:
            - .github/agents/research-specialist.agent.md exists
            - Progress tracking protocol documented
            - update_status() calls in workflow phases
            - Phase 0 added (initialization)
            - Verification checklist updated
        """
        result = ValidationResult("Research Specialist Integration")
        
        agent = self.root / ".github" / "agents" / "research-specialist.agent.md"
        if not agent.exists():
            result.fail(f"Research specialist agent missing: {agent}")
            return result
        
        content = agent.read_text()
        
        # Check Phase 0 added
        if '### Phase 0: Progress Tracking Initialization' not in content:
            result.fail("Phase 0 (progress tracking) not added")
        
        # Check update_status() usage
        if 'update_status(' not in content:
            result.fail("update_status() not integrated in workflow")
        
        # Check log_progress() usage
        if 'log_progress(' not in content:
            result.warn("log_progress() not integrated (optional)")
        
        # Check verification checklist updated
        if 'Progress tracking active' not in content:
            result.warn("Verification checklist not updated with progress tracking")
        
        # Check agent version updated
        if 'CLI Orchestrated' not in content and 'File-Based Protocol' not in content:
            result.warn("Agent version not updated (should indicate CLI orchestration)")
        
        return result
    
    def validate_polling_mechanism(self) -> ValidationResult:
        """
        Validate: Polling mechanism doesn't cause CPU spike.
        
        Checks:
            - Polling uses time.sleep() (not busy loop)
            - Default interval is 2 seconds
            - Configurable via parameter
        """
        result = ValidationResult("Polling Mechanism (Anti-CPU Spike)")
        
        skill = self.root / "skills" / "orchestrate_subagents.py"
        if not skill.exists():
            result.fail("Orchestrator skill missing (cannot validate polling)")
            return result
        
        content = skill.read_text()
        
        # Check time.sleep() used
        if 'time.sleep(' not in content:
            result.fail("time.sleep() not used (potential CPU spike)")
        
        # Check default interval
        if 'poll_interval' not in content:
            result.fail("poll_interval not defined")
        elif 'poll_interval: int = 2' not in content and 'poll_interval=2' not in content:
            result.warn("Default poll_interval not 2 seconds")
        
        # Check configurable
        if 'poll_interval' not in content:
            result.warn("poll_interval not configurable")
        
        return result
    
    def validate_documentation_completeness(self) -> ValidationResult:
        """
        Validate: All documentation updated.
        
        Checks:
            - .sia/runtime/README.md exists and comprehensive
            - templates/SPR_OUTPUT_TEMPLATE.md exists
            - skills/orchestrate_subagents.py has docstrings
        """
        result = ValidationResult("Documentation Completeness")
        
        # Runtime README
        runtime_readme = self.runtime_dir / "README.md"
        if not runtime_readme.exists():
            result.fail("Runtime README.md missing")
        elif len(runtime_readme.read_text()) < 2000:
            result.warn("Runtime README.md too short (< 2000 chars)")
        
        # SPR template
        spr_template = self.root / "templates" / "SPR_OUTPUT_TEMPLATE.md"
        if not spr_template.exists():
            result.fail("SPR template missing")
        elif len(spr_template.read_text()) < 3000:
            result.warn("SPR template too short (< 3000 chars)")
        
        # Orchestrator docstrings
        orchestrator = self.root / "skills" / "orchestrate_subagents.py"
        if orchestrator.exists():
            content = orchestrator.read_text()
            if '"""' not in content:
                result.warn("Orchestrator skill missing docstrings")
        
        return result
    
    def run_all_validations(self) -> bool:
        """
        Run all validations.
        
        Returns:
            True if all passed, False otherwise
        """
        print("🔍 QUANT-001 Validation Report")
        print("=" * 80)
        print()
        
        # Run validations
        self.results = [
            self.validate_runtime_structure(),
            self.validate_status_schema(),
            self.validate_output_format(),
            self.validate_status_update_snippet(),
            self.validate_orchestrator_skill(),
            self.validate_research_specialist_integration(),
            self.validate_polling_mechanism(),
            self.validate_documentation_completeness()
        ]
        
        # Print results
        for result in self.results:
            print(result)
        
        # Summary
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        print("=" * 80)
        print(f"SUMMARY: {passed}/{total} validations passed")
        print("=" * 80)
        print()
        
        # Final verdict
        all_passed = all(r.passed for r in self.results)
        if all_passed:
            print("✅ QUANT-001 VALIDATION PASSED")
            print()
            print("Next steps:")
            print("  1. Test orchestrator: python skills/orchestrate_subagents.py")
            print("  2. Update SESSION_SUMMARY.md with validation results")
            print("  3. Commit changes to feat/frist-principles branch")
            print("  4. Move to QUANT-002 (Convert Repository Guardian)")
        else:
            print("❌ QUANT-001 VALIDATION FAILED")
            print()
            print("Fix errors above before proceeding to QUANT-002")
        
        return all_passed


def main():
    """Main entry point"""
    # Detect SIA root directory (look for .sia/ or pyproject.toml)
    current = Path.cwd()
    root = None
    
    # Search upwards for SIA markers
    for parent in [current] + list(current.parents):
        if (parent / ".sia").exists() or (parent / "pyproject.toml").exists():
            root = parent
            break
    
    if root is None:
        print("❌ SIA framework root not detected", file=sys.stderr)
        print("   Run from SIA framework directory", file=sys.stderr)
        sys.exit(1)
    
    print(f"📂 SIA Root: {root}\n")
    
    # Run validation
    validator = QUANT001Validator(root)
    passed = validator.run_all_validations()
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()

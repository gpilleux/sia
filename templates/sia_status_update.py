"""
Status Update Utility for CLI-Spawned Sub-Agents

Purpose: Self-reporting progress mechanism for file-based orchestration.

Usage:
    # In sub-agent instructions, import this snippet
    from sia_status_update import update_status
    
    # Update progress throughout execution
    update_status(25, "Executing MCP query: langchain-ai/langchain")
    update_status(60, "Synthesizing findings", findings_count=3)
    update_status(100, "Completed")

Environment:
    SIA_STATUS_FILE: Path to status.yaml (set by orchestrator)
    If not set, updates are no-op (non-orchestrated mode)

Protocol:
    - Update frequency: Every 30 seconds during active work
    - Update on: Phase transitions, MCP queries, errors
    - Final update: progress=100, state='completed'
"""

import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

try:
    import yaml
except ImportError:
    # Fallback for environments without PyYAML
    yaml = None  # type: ignore


def update_status(
    progress: int,
    task: str,
    findings_count: int = 0,
    errors: Optional[list[str]] = None
) -> None:
    """
    Update orchestrator-visible status file.
    
    Args:
        progress: Completion percentage (0-100)
        task: Current task description (e.g., "Executing MCP query: repo/name")
        findings_count: Number of findings/patterns identified so far
        errors: List of error messages (if any occurred)
    
    Status States:
        - initializing: 0% (starting)
        - in_progress: 1-99% (actively working)
        - completed: 100% (finished successfully)
        - failed: Any progress with errors present
    
    Example:
        >>> update_status(25, "Analyzing user request")
        >>> update_status(60, "Executing MCP queries", findings_count=2)
        >>> update_status(100, "Completed", findings_count=5)
    """
    status_file = Path(os.getenv('SIA_STATUS_FILE', '.sia/runtime/status.yaml'))
    
    # No-op if not running in orchestrated mode or YAML not available
    if not status_file.parent.exists() or yaml is None:
        return
    
    # Load existing status or initialize
    if status_file.exists():
        status = yaml.safe_load(status_file.read_text())
    else:
        status = {}
    
    # Determine state
    if errors:
        state = 'failed'
    elif progress == 0:
        state = 'initializing'
    elif progress == 100:
        state = 'completed'
    else:
        state = 'in_progress'
    
    # Update status
    status.update({
        'state': state,
        'updated_at': datetime.now(timezone.utc).isoformat(),
        'progress_percent': progress,
        'current_task': task,
        'findings_count': findings_count,
        'errors': errors or []
    })
    
    # Write atomically (write to temp, then rename)
    temp_file = status_file.with_suffix('.yaml.tmp')
    temp_file.write_text(yaml.dump(status, default_flow_style=False))
    temp_file.replace(status_file)


def log_progress(message: str, level: str = "INFO") -> None:
    """
    Append timestamped log entry to progress.log.
    
    Args:
        message: Log message
        level: Log level (INFO, WARNING, ERROR)
    
    Example:
        >>> log_progress("Phase 1 started")
        >>> log_progress("MCP query failed", level="ERROR")
    """
    status_file = Path(os.getenv('SIA_STATUS_FILE', '.sia/runtime/status.yaml'))
    log_file = status_file.parent / "progress.log"
    
    if not log_file.parent.exists():
        return
    
    timestamp = datetime.now(timezone.utc).isoformat()
    log_entry = f"{timestamp} [{level}] {message}\n"
    
    # Append to log file
    with log_file.open('a') as f:
        f.write(log_entry)


# Example usage in sub-agent workflow
if __name__ == "__main__":
    """
    Example execution flow (copy into sub-agent instructions)
    """
    
    # Phase 1: Initialization
    update_status(0, "Sub-agent initialized")
    log_progress("Sub-agent started")
    
    # Phase 2: Analysis (10%)
    update_status(10, "Analyzing user request")
    log_progress("Phase 1: Analyzing user request")
    # ... perform analysis ...
    
    # Phase 3: Research (25% → 60%)
    update_status(25, "Executing MCP query: langchain-ai/langchain")
    log_progress("Phase 2: Executing MCP query (repo: langchain-ai/langchain)")
    # ... execute MCP queries ...
    
    update_status(60, "Synthesizing findings", findings_count=3)
    log_progress("Phase 2: Received response from DeepWiki (1,234 tokens)")
    
    # Phase 4: Synthesis (70%)
    update_status(70, "Extracting patterns and anti-patterns")
    log_progress("Phase 3: Synthesizing findings (3 patterns identified)")
    # ... synthesize findings ...
    
    # Phase 5: Output Generation (90%)
    update_status(90, "Generating SPR output")
    log_progress("Phase 4: Generating SPR output")
    # ... generate output.md ...
    
    # Phase 6: Completion (100%)
    update_status(100, "Completed", findings_count=5)
    log_progress("Completed successfully (duration: 89s)")
    
    print("✅ Status updates completed")

#!/usr/bin/env python3
"""
Sub-Agent Orchestrator - CLI-Based Parallel Execution

Purpose: Spawn and monitor multiple sub-agents in parallel using Copilot CLI.

Architecture:
    - File-based communication (status.yaml for progress tracking)
    - CLI subprocess spawning (copilot --agent <name> -p "prompt")
    - Non-blocking execution (multiple agents run simultaneously)
    - Progress polling (2s interval, no CPU spike)
    - Automatic cleanup (session cleanup after completion)

Usage:
    from skills.orchestrate_subagents import SubAgentOrchestrator
    
    orchestrator = SubAgentOrchestrator()
    tasks = [
        {'agent_name': 'research-specialist', 'prompt': '...'},
        {'agent_name': 'repository-guardian', 'prompt': '...'}
    ]
    agents = orchestrator.spawn_parallel(tasks)
    orchestrator.monitor_progress(agents)
    results = orchestrator.consolidate_results(agents)

Dependencies:
    - Python 3.10+ (native)
    - PyYAML (optional, for status parsing)
    - Copilot CLI (github.com/cli/cli)

Environment:
    SIA_RUNTIME_DIR: Override default runtime directory (.sia/runtime)
    SIA_MAX_PARALLEL: Maximum parallel agents (default: 5)
"""

import os
import sys
import time
import uuid
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, TypedDict

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("⚠️  PyYAML not installed. Status tracking limited.", file=sys.stderr)


class AgentTask(TypedDict):
    """Task definition for sub-agent spawning"""
    agent_name: str  # Custom agent name (e.g., 'research-specialist')
    prompt: str      # Delegation prompt (TASK + CONTEXT + CONSTRAINTS + OUTPUT)
    timeout: int     # Execution timeout in seconds (default: 300)


class AgentProcess(TypedDict):
    """Running agent process metadata"""
    agent_name: str
    task: str
    status_file: Path
    output_file: Path
    log_dir: Path
    process: subprocess.Popen
    started_at: str
    timeout: int


class SubAgentOrchestrator:
    """
    Orchestrate parallel CLI-spawned sub-agents with file-based communication.
    """
    
    def __init__(
        self,
        runtime_dir: Optional[Path] = None,
        max_parallel: int = 5,
        poll_interval: int = 2
    ):
        """
        Initialize orchestrator.
        
        Args:
            runtime_dir: Session runtime directory (default: .sia/runtime)
            max_parallel: Maximum concurrent agents (default: 5)
            poll_interval: Status polling interval in seconds (default: 2)
        """
        self.runtime_dir = runtime_dir or Path(
            os.getenv('SIA_RUNTIME_DIR', '.sia/runtime')
        )
        self.max_parallel = int(os.getenv('SIA_MAX_PARALLEL', max_parallel))
        self.poll_interval = poll_interval
        self.session_id: Optional[str] = None
    
    def create_session(self, tasks: list[AgentTask]) -> str:
        """
        Create runtime session directory structure.
        
        Args:
            tasks: List of agent tasks to spawn
        
        Returns:
            session_id: UUID for this orchestration session
        
        Creates:
            .sia/runtime/{session_id}/
                orchestrator.yaml
                {agent_name}/
                    status.yaml
                    logs/
        """
        self.session_id = str(uuid.uuid4())
        session_dir = self.runtime_dir / self.session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Create orchestrator state
        orchestrator_state = {
            'session_id': self.session_id,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'agents': [],
            'poll_interval': self.poll_interval,
            'max_parallel': self.max_parallel
        }
        
        # Create agent directories
        for task in tasks:
            agent_dir = session_dir / task['agent_name']
            agent_dir.mkdir(exist_ok=True)
            (agent_dir / 'logs').mkdir(exist_ok=True)
            
            # Initialize status.yaml
            status = {
                'state': 'initializing',
                'updated_at': datetime.now(timezone.utc).isoformat(),
                'progress_percent': 0,
                'current_task': 'Waiting for execution',
                'findings_count': 0,
                'errors': []
            }
            
            if YAML_AVAILABLE:
                status_file = agent_dir / 'status.yaml'
                status_file.write_text(yaml.dump(status, default_flow_style=False))
            
            orchestrator_state['agents'].append({
                'agent_name': task['agent_name'],
                'task': task['prompt'][:100] + '...',  # Truncate for display
                'status_file': str(agent_dir / 'status.yaml'),
                'output_file': str(agent_dir / 'output.md'),
                'timeout': task.get('timeout', 300)
            })
        
        # Write orchestrator state
        if YAML_AVAILABLE:
            orchestrator_file = session_dir / 'orchestrator.yaml'
            orchestrator_file.write_text(
                yaml.dump(orchestrator_state, default_flow_style=False)
            )
        
        return self.session_id
    
    def spawn_agent(
        self,
        session_id: str,
        task: AgentTask
    ) -> AgentProcess:
        """
        Spawn single sub-agent via Copilot CLI.
        
        Args:
            session_id: Session UUID
            task: Agent task definition
        
        Returns:
            AgentProcess: Running process metadata
        
        Spawns:
            copilot --agent <name> -p "prompt" --allow-all-tools
        
        Environment:
            SIA_STATUS_FILE: Path to status.yaml (for sub-agent self-reporting)
        """
        session_dir = self.runtime_dir / session_id
        agent_dir = session_dir / task['agent_name']
        
        status_file = agent_dir / 'status.yaml'
        output_file = agent_dir / 'output.md'
        log_dir = agent_dir / 'logs'
        
        # Prepare environment
        env = os.environ.copy()
        env['SIA_STATUS_FILE'] = str(status_file)
        
        # Spawn subprocess
        cmd = [
            'copilot',
            '--agent', task['agent_name'],
            '-p', task['prompt'],
            '--allow-all-tools'
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=output_file.open('w'),
            stderr=(log_dir / 'copilot.log').open('w'),
            env=env,
            cwd=Path.cwd()
        )
        
        return AgentProcess(
            agent_name=task['agent_name'],
            task=task['prompt'][:100] + '...',
            status_file=status_file,
            output_file=output_file,
            log_dir=log_dir,
            process=process,
            started_at=datetime.now(timezone.utc).isoformat(),
            timeout=task.get('timeout', 300)
        )
    
    def spawn_parallel(
        self,
        tasks: list[AgentTask],
        batch_size: Optional[int] = None
    ) -> list[AgentProcess]:
        """
        Spawn multiple agents in parallel.
        
        Args:
            tasks: List of agent tasks to spawn
            batch_size: Override max_parallel (default: use self.max_parallel)
        
        Returns:
            List of running agent processes
        
        Raises:
            RuntimeError: If batch_size > max_parallel
        """
        batch_size = batch_size or self.max_parallel
        
        if len(tasks) > batch_size:
            raise RuntimeError(
                f"Batch size ({len(tasks)}) exceeds max_parallel ({batch_size})"
            )
        
        # Create session
        session_id = self.create_session(tasks)
        
        # Spawn agents
        agents: list[AgentProcess] = []
        for task in tasks:
            agent = self.spawn_agent(session_id, task)
            agents.append(agent)
            print(f"✓ Spawned: {task['agent_name']} (PID: {agent['process'].pid})")
        
        return agents
    
    def poll_status(
        self,
        agents: list[AgentProcess]
    ) -> dict[str, dict]:
        """
        Poll status files for all agents.
        
        Args:
            agents: List of running agent processes
        
        Returns:
            {agent_name: status_dict}
        
        Status dict:
            state: initializing | in_progress | completed | failed
            progress_percent: 0-100
            current_task: str
            findings_count: int
            errors: list[str]
        """
        status = {}
        
        for agent in agents:
            if not YAML_AVAILABLE:
                status[agent['agent_name']] = {
                    'state': 'unknown',
                    'error': 'PyYAML not available'
                }
                continue
            
            status_file = agent['status_file']
            if status_file.exists():
                try:
                    status[agent['agent_name']] = yaml.safe_load(
                        status_file.read_text()
                    )
                except Exception as e:
                    status[agent['agent_name']] = {
                        'state': 'error',
                        'error': f'Failed to parse status: {e}'
                    }
            else:
                status[agent['agent_name']] = {
                    'state': 'initializing',
                    'progress_percent': 0,
                    'current_task': 'Status file not created yet'
                }
        
        return status
    
    def monitor_progress(
        self,
        agents: list[AgentProcess],
        verbose: bool = True
    ) -> dict[str, dict]:
        """
        Monitor agent progress with real-time updates.
        
        Args:
            agents: List of running agent processes
            verbose: Print progress to stdout (default: True)
        
        Returns:
            Final status dict for all agents
        
        Monitors:
            - Polls status.yaml every poll_interval seconds
            - Displays progress updates (if verbose=True)
            - Checks for completion (all agents state != in_progress)
            - Enforces timeouts (kills process if exceeded)
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"MONITORING SESSION: {self.session_id}")
            print(f"{'='*80}\n")
        
        start_time = time.time()
        
        while True:
            status = self.poll_status(agents)
            
            # Display progress
            if verbose:
                print(f"\r{' '*100}\r", end='')  # Clear line
                for agent_name, agent_status in status.items():
                    state = agent_status.get('state', 'unknown')
                    progress = agent_status.get('progress_percent', 0)
                    task = agent_status.get('current_task', 'N/A')
                    
                    # Color coding
                    state_emoji = {
                        'initializing': '🔄',
                        'in_progress': '⚙️',
                        'completed': '✅',
                        'failed': '❌'
                    }.get(state, '❓')
                    
                    print(f"{state_emoji} [{agent_name}] {progress}% - {task}")
            
            # Check completion
            all_done = all(
                s.get('state') in ['completed', 'failed']
                for s in status.values()
            )
            
            if all_done:
                break
            
            # Check timeouts
            for agent in agents:
                elapsed = time.time() - start_time
                if elapsed > agent['timeout']:
                    print(
                        f"\n⚠️  Timeout: {agent['agent_name']} "
                        f"(exceeded {agent['timeout']}s)"
                    )
                    agent['process'].kill()
                    
                    # Update status
                    if YAML_AVAILABLE:
                        status_file = agent['status_file']
                        status_data = yaml.safe_load(status_file.read_text())
                        status_data['state'] = 'failed'
                        status_data['errors'].append(
                            f"Timeout exceeded ({agent['timeout']}s)"
                        )
                        status_file.write_text(
                            yaml.dump(status_data, default_flow_style=False)
                        )
            
            # Sleep before next poll
            time.sleep(self.poll_interval)
        
        if verbose:
            duration = time.time() - start_time
            print(f"\n{'='*80}")
            print(f"ALL AGENTS COMPLETED (duration: {duration:.1f}s)")
            print(f"{'='*80}\n")
        
        return status
    
    def consolidate_results(
        self,
        agents: list[AgentProcess]
    ) -> dict[str, str]:
        """
        Consolidate SPR outputs from all agents.
        
        Args:
            agents: List of agent processes
        
        Returns:
            {agent_name: spr_output_markdown}
        
        Reads:
            {session_id}/{agent_name}/output.md
        """
        results = {}
        
        for agent in agents:
            output_file = agent['output_file']
            
            if output_file.exists():
                results[agent['agent_name']] = output_file.read_text()
            else:
                results[agent['agent_name']] = (
                    f"# ERROR: Output file not found\n\n"
                    f"Agent: {agent['agent_name']}\n"
                    f"Expected: {output_file}\n"
                    f"Status: Check logs in {agent['log_dir']}\n"
                )
        
        return results


# CLI interface for testing
if __name__ == "__main__":
    """
    Test orchestrator with mock tasks.
    
    Usage:
        python skills/orchestrate_subagents.py
    """
    
    print("🚀 Sub-Agent Orchestrator - Test Mode\n")
    
    # Mock tasks (replace with actual Copilot CLI invocations)
    tasks: list[AgentTask] = [
        {
            'agent_name': 'research-specialist',
            'prompt': 'Research pgvector integration with LangChain',
            'timeout': 300
        },
        {
            'agent_name': 'repository-guardian',
            'prompt': 'Audit DDD compliance in domain layer',
            'timeout': 180
        }
    ]
    
    orchestrator = SubAgentOrchestrator()
    
    print("📋 Tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task['agent_name']}: {task['prompt']}")
    
    print(f"\n⚙️  Creating session...")
    session_id = orchestrator.create_session(tasks)
    print(f"✓ Session created: {session_id}")
    
    print(f"\n📂 Session structure:")
    session_dir = orchestrator.runtime_dir / session_id
    for path in sorted(session_dir.rglob('*')):
        if path.is_file():
            rel_path = path.relative_to(session_dir)
            print(f"  - {rel_path}")
    
    print("\n✅ File-based protocol validated!")
    print(f"\nSession directory: {session_dir}")
    print("\nTo spawn agents, use: orchestrator.spawn_parallel(tasks)")

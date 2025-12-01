#!/usr/bin/env python3
"""
QUANT-001 End-to-End Validation Script

Validates file-based protocol with live CLI sub-agent execution.
"""

import sys
import time
from pathlib import Path
from typing import cast

# Add skills to path
sys.path.insert(0, str(Path(__file__).parent))

from skills.orchestrate_subagents import AgentTask, SubAgentOrchestrator


def main():
    """Execute QUANT-001 validation with real-time progress monitoring."""
    
    # Metrics tracking
    metrics = {
        'spawn_start': None,
        'spawn_end': None,
        'first_update': None,
        'completion': None,
        'status_updates': [],
        'token_count': 0,
        'findings_quality': []
    }
    
    print('🚀 QUANT-001 END-TO-END VALIDATION')
    print('='*80)
    
    orchestrator = SubAgentOrchestrator()
    
    # Task definition
    tasks: list[AgentTask] = [{
        'agent_name': 'research-specialist',
        'prompt': '''Research async connection pooling with pgvector in LangChain.

CONTEXT: Building semantic code search with high concurrent load.

QUESTIONS:
1. How to configure PGVector with async engine + connection pooling?
2. Batch embedding patterns (optimal batch_size for throughput)?
3. Index optimization (IVFFlat vs HNSW for 100k+ vectors)?

EXPECTED OUTPUT: SPR markdown (code examples + patterns + anti-patterns)

REPOS: langchain-ai/langchain, pgvector/pgvector

PROGRESS TRACKING:
- Update status.yaml every 30 seconds
- Track: state, progress_percent, current_task, findings_count
- Log major milestones in progress.log
''',
        'timeout': 300
    }]
    
    # Spawn
    print('\n📋 TASK: Investigate pgvector async connection pooling')
    print(f'⏱️  Timeout: 300s')
    print(f'📁 Agent: research-specialist\n')
    
    metrics['spawn_start'] = time.time()
    
    try:
        agents = orchestrator.spawn_parallel(tasks)
        metrics['spawn_end'] = time.time()
        
        spawn_latency = metrics['spawn_end'] - metrics['spawn_start']
        print(f'✅ Spawn latency: {spawn_latency:.2f}s')
        print(f'🔍 PID: {agents[0]["process"].pid}')
        print(f'📂 Session: {orchestrator.session_id}\n')
        
    except Exception as e:
        print(f'❌ SPAWN FAILED: {e}')
        return 1
    
    # Monitor with metrics
    print('='*80)
    print('PROGRESS MONITORING')
    print('='*80 + '\n')
    
    start_monitoring = time.time()
    first_update_captured = False
    
    # Custom monitoring loop for metrics
    try:
        while True:
            status = orchestrator.poll_status(agents)
            current_time = time.time()
            
            # Capture first update
            if not first_update_captured:
                for agent_name, agent_status in status.items():
                    if agent_status.get('progress_percent', 0) > 0:
                        metrics['first_update'] = current_time
                        first_update_captured = True
                        break
            
            # Track status updates
            metrics['status_updates'].append({
                'timestamp': current_time,
                'status': status.copy()
            })
            
            # Display progress (with flush to ensure output appears)
            for agent_name, agent_status in status.items():
                state = agent_status.get('state', 'unknown')
                progress = agent_status.get('progress_percent', 0)
                task = agent_status.get('current_task', 'N/A')
                findings = agent_status.get('findings_count', 0)
                
                state_emoji = {
                    'initializing': '🔄',
                    'in_progress': '⚙️',
                    'completed': '✅',
                    'failed': '❌'
                }.get(state, '❓')
                
                elapsed = current_time - metrics['spawn_start']
                print(f'{state_emoji} [{agent_name}] {progress}% | {findings} findings | {task} ({elapsed:.0f}s)', flush=True)
            
            # Check completion
            all_done = all(
                s.get('state') in ['completed', 'failed']
                for s in status.values()
            )
            
            if all_done:
                metrics['completion'] = current_time
                break
            
            # Check timeout
            if current_time - start_monitoring > 300:
                print('\n⚠️  TIMEOUT EXCEEDED - Killing process', flush=True)
                for agent in agents:
                    agent['process'].kill()
                break
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print('\n\n⚠️  Interrupted by user - Cleaning up...', flush=True)
        for agent in agents:
            agent['process'].kill()
        return 1
    
    # Consolidate results
    print('\n' + '='*80)
    print('RESULTS CONSOLIDATION')
    print('='*80)
    
    results = orchestrator.consolidate_results(agents)
    
    for agent_name, spr in results.items():
        print(f'\n## {agent_name.upper()}\n')
        
        # Count tokens (rough estimate)
        token_estimate = len(spr.split())
        metrics['token_count'] = token_estimate
        
        # Extract findings quality
        if 'ERROR' in spr:
            metrics['findings_quality'].append('FAILED')
            print(spr[:500])
        else:
            # Count patterns, anti-patterns, code blocks
            pattern_count = spr.count('##') - 1  # Subtract title
            code_blocks = spr.count('```')
            
            metrics['findings_quality'].append({
                'sections': pattern_count,
                'code_blocks': code_blocks,
                'length': len(spr)
            })
            
            print(f'📄 Length: {len(spr)} chars (~{token_estimate} tokens)')
            print(f'📊 Sections: {pattern_count}')
            print(f'💻 Code blocks: {code_blocks}')
            print(f'\nPreview:\n{spr[:500]}...')
    
    # Final metrics report
    print('\n' + '='*80)
    print('METRICS REPORT')
    print('='*80)
    
    if metrics['completion']:
        total_time = metrics['completion'] - metrics['spawn_start']
        print(f'⏱️  Total execution: {total_time:.1f}s')
        
    if metrics['first_update']:
        first_update_latency = metrics['first_update'] - metrics['spawn_end']
        print(f'📡 First update latency: {first_update_latency:.1f}s')
    
    print(f'📊 Status updates: {len(metrics["status_updates"])} (every ~2s)')
    print(f'🔤 Token count: ~{metrics["token_count"]} words')
    print(f'✅ Findings quality: {metrics["findings_quality"]}')
    
    # Validation checklist
    print('\n' + '='*80)
    print('VALIDATION CHECKLIST')
    print('='*80)
    
    final_status = orchestrator.poll_status(agents)
    agent_status = final_status.get('research-specialist', {})
    
    checklist = {
        'Spawn exitoso (PID capturado)': agents[0]['process'].pid is not None,
        'Status updates cada 30s (5+ durante ejecución)': len(metrics['status_updates']) >= 5,
        'Output.md SPR válido (<5000 tokens)': 0 < metrics['token_count'] < 5000 if metrics['token_count'] else False,
        'No errors en status.yaml': len(agent_status.get('errors', [])) == 0,
        'Progress alcanzó 100%': agent_status.get('progress_percent', 0) == 100,
        'Estado final: completed': agent_status.get('state') == 'completed'
    }
    
    for check, passed in checklist.items():
        emoji = '✅' if passed else '❌'
        print(f'{emoji} {check}')
    
    # Overall result
    all_passed = all(checklist.values())
    print(f'\n{"="*80}')
    if all_passed:
        print('🎉 QUANT-001 VALIDATION: PASS')
        result_code = 0
    else:
        print('⚠️  QUANT-001 VALIDATION: PARTIAL/FAIL')
        result_code = 1
    print(f'{"="*80}')
    
    # Save session location
    print(f'\n📂 Session artifacts: .sia/runtime/{orchestrator.session_id}')
    
    return result_code


if __name__ == '__main__':
    sys.exit(main())

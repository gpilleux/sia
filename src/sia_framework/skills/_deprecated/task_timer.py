#!/usr/bin/env uv run python
"""
SKILL: Task Timer
Description: Start/stop timer for QUANT tasks, track actual vs estimated time
Invariant: Persistent timer state survives terminal session, accumulates metrics

NOTE: Uses `uv` package manager (project standard). Auto-installs dependencies.
"""

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

# Timer state file (survives sessions)
TIMER_STATE_FILE = Path.home() / ".sia" / "timer_state.json"
METRICS_FILE = Path.home() / ".sia" / "task_metrics.json"


def ensure_sia_dir():
    """Create .sia directory if not exists"""
    sia_dir = Path.home() / ".sia"
    sia_dir.mkdir(exist_ok=True)
    return sia_dir


def start_timer(task_id: str, estimated_hours: float, description: str = ""):
    """
    Start timer for a task
    
    Args:
        task_id: QUANT task ID (e.g., "QUANT-040")
        estimated_hours: AI estimated duration in hours
        description: Optional task description
    """
    ensure_sia_dir()
    
    # Check if timer already running
    if TIMER_STATE_FILE.exists():
        with open(TIMER_STATE_FILE, 'r') as f:
            state = json.load(f)
            if state.get('running'):
                print(f"⚠️  Timer already running for {state['task_id']}")
                print(f"   Started: {state['start_time']}")
                print(f"   Duration: {format_duration(time.time() - state['start_timestamp'])}")
                print(f"\n   Stop current timer first: uv run sia/skills/task_timer.py stop")
                return
    
    # Start new timer
    state = {
        'running': True,
        'task_id': task_id,
        'description': description,
        'estimated_hours': estimated_hours,
        'start_time': datetime.now().isoformat(),
        'start_timestamp': time.time()
    }
    
    with open(TIMER_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"⏱️  Timer started for {task_id}")
    print(f"   Description: {description}")
    print(f"   Estimated (AI): {estimated_hours}h ({estimated_hours * 60:.0f} min)")
    print(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n   Timer runs in background. Stop with: uv run sia/skills/task_timer.py stop")


def predict_human_team_duration(task_description: str, ai_actual_hours: float) -> float:
    """
    DEPRECATED: Human prediction is now done by Super Agent in QUANT breakdown.
    This function kept for backward compatibility with old metrics.
    """
    return 0.0


def stop_timer(completed: bool = True, human_estimated_hours: float = 0.0):
    """
    Stop timer and record metrics
    
    Args:
        completed: True if task completed, False if abandoned
        human_estimated_hours: Super Agent's prediction for human team (from QUANT breakdown)
    """
    if not TIMER_STATE_FILE.exists():
        print("❌ No active timer found")
        return
    
    with open(TIMER_STATE_FILE, 'r') as f:
        state = json.load(f)
    
    if not state.get('running'):
        print("❌ Timer not running")
        return
    
    # Calculate actual duration
    end_timestamp = time.time()
    actual_seconds = end_timestamp - state['start_timestamp']
    actual_hours = actual_seconds / 3600
    estimated_hours = state['estimated_hours']
    
    # Calculate accuracy
    variance_percent = ((actual_hours - estimated_hours) / estimated_hours * 100) if estimated_hours > 0 else 0
    
    # Record metrics
    metric = {
        'task_id': state['task_id'],
        'description': state['description'],
        'ai_estimated_hours': estimated_hours,
        'ai_actual_hours': round(actual_hours, 2),
        'ai_variance_percent': round(variance_percent, 1),
        'human_estimated_hours': human_estimated_hours,
        'completed': completed,
        'start_time': state['start_time'],
        'end_time': datetime.now().isoformat(),
        'duration_formatted': format_duration(actual_seconds)
    }
    
    # Append to metrics file
    metrics = load_metrics()
    metrics.append(metric)
    save_metrics(metrics)
    
    # Clear timer state
    TIMER_STATE_FILE.unlink()
    
    # Display results
    print(f"⏹️  Timer stopped for {state['task_id']}")
    print(f"   Status: {'✅ COMPLETED' if completed else '❌ ABANDONED'}")
    print(f"\n📊 AI PERFORMANCE:")
    print(f"   Estimated: {estimated_hours}h ({estimated_hours * 60:.0f} min)")
    print(f"   Actual: {actual_hours:.2f}h ({actual_hours * 60:.0f} min)")
    print(f"   Variance: {variance_percent:+.1f}% {'(faster ⚡)' if variance_percent < 0 else '(slower 🐌)' if variance_percent > 0 else '(exact 🎯)'}")
    print(f"   Duration: {format_duration(actual_seconds)}")
    
    if human_estimated_hours > 0:
        speedup = human_estimated_hours / actual_hours if actual_hours > 0 else 0
        print(f"\n👥 HUMAN TEAM COMPARISON:")
        print(f"   Human Estimated: {human_estimated_hours}h ({human_estimated_hours * 60:.0f} min)")
        print(f"   AI Speedup: {speedup:.1f}x faster" if speedup > 0 else "   AI Speedup: N/A")
        print(f"   Time Saved: {human_estimated_hours - actual_hours:.1f}h")
    
    # Show prediction insights
    show_prediction_insights(metrics)


def status():
    """Show current timer status"""
    if not TIMER_STATE_FILE.exists():
        print("⏸️  No active timer")
        return
    
    with open(TIMER_STATE_FILE, 'r') as f:
        state = json.load(f)
    
    if not state.get('running'):
        print("⏸️  Timer not running")
        return
    
    elapsed_seconds = time.time() - state['start_timestamp']
    elapsed_hours = elapsed_seconds / 3600
    estimated_hours = state['estimated_hours']
    progress = (elapsed_hours / estimated_hours * 100) if estimated_hours > 0 else 0
    
    print(f"⏱️  Timer running for {state['task_id']}")
    print(f"   Description: {state['description']}")
    print(f"   AI Estimated: {estimated_hours}h ({estimated_hours * 60:.0f} min)")
    print(f"   Elapsed: {elapsed_hours:.2f}h ({elapsed_hours * 60:.0f} min)")
    print(f"   Progress: {progress:.1f}% of estimate")
    print(f"   Duration: {format_duration(elapsed_seconds)}")
    print(f"   Started: {state['start_time']}")


def metrics_report():
    """Generate metrics report with predictions"""
    metrics = load_metrics()
    
    if not metrics:
        print("📊 No task metrics recorded yet")
        return
    
    completed = [m for m in metrics if m['completed']]
    
    if not completed:
        print("📊 No completed tasks yet")
        return
    
    # Calculate statistics
    total_tasks = len(completed)
    total_ai_estimated = sum(m.get('ai_estimated_hours', m.get('estimated_hours', 0)) for m in completed)
    total_ai_actual = sum(m.get('ai_actual_hours', m.get('actual_hours', 0)) for m in completed)
    avg_variance = sum(m.get('ai_variance_percent', m.get('variance_percent', 0)) for m in completed) / total_tasks
    
    # Human team estimation (from Super Agent predictions in QUANT breakdown)
    total_human_estimated = sum(m.get('human_estimated_hours', 0) for m in completed)
    tasks_with_human_estimate = sum(1 for m in completed if m.get('human_estimated_hours', 0) > 0)
    
    # AI self-prediction (based on historical variance)
    ai_correction_factor = 1 + (avg_variance / 100)
    
    print(f"📊 SUPER AGENT Performance Report")
    print(f"=" * 60)
    print(f"\n📈 COMPLETED TASKS: {total_tasks}")
    print(f"\n🤖 AI SELF-ASSESSMENT:")
    print(f"   Total Estimated: {total_ai_estimated:.1f}h")
    print(f"   Total Actual: {total_ai_actual:.1f}h")
    print(f"   Average Variance: {avg_variance:+.1f}%")
    print(f"   Correction Factor: {ai_correction_factor:.2f}x")
    print(f"   Next Prediction: EstimatedTime × {ai_correction_factor:.2f}")
    
    if tasks_with_human_estimate > 0:
        avg_speedup = total_human_estimated / total_ai_actual if total_ai_actual > 0 else 0
        print(f"\n👥 vs HUMAN TEAM ({tasks_with_human_estimate}/{total_tasks} tasks with estimates):")
        print(f"   Total Human Estimated: {total_human_estimated:.1f}h")
        print(f"   Total AI Actual: {total_ai_actual:.1f}h")
        if avg_speedup > 0:
            print(f"   Average Speedup: {avg_speedup:.1f}x faster")
            print(f"   Time Saved: {total_human_estimated - total_ai_actual:.1f}h")
    else:
        print(f"\n👥 vs HUMAN TEAM:")
        print(f"   No human estimates recorded yet")
        print(f"   Add --human-hours when stopping timer")
    
    # Recent tasks
    print(f"\n📋 RECENT TASKS (Last 5):")
    for m in completed[-5:]:
        ai_var = m.get('ai_variance_percent', m.get('variance_percent', 0))
        ai_est = m.get('ai_estimated_hours', m.get('estimated_hours', 0))
        ai_act = m.get('ai_actual_hours', m.get('actual_hours', 0))
        human_est = m.get('human_estimated_hours', 0)
        
        variance_icon = "⚡" if ai_var < 0 else "🐌" if ai_var > 10 else "🎯"
        human_text = f" | 👥 {human_est:.1f}h" if human_est > 0 else ""
        print(f"   {variance_icon} {m['task_id']}: {ai_est}h → {ai_act}h ({ai_var:+.1f}%){human_text}")
    
    # Worst/best predictions
    worst = max(completed, key=lambda m: abs(m.get('ai_variance_percent', m.get('variance_percent', 0))))
    best = min(completed, key=lambda m: abs(m.get('ai_variance_percent', m.get('variance_percent', 0))))
    
    print(f"\n🎯 AI PREDICTION QUALITY:")
    print(f"   Best: {best['task_id']} ({best.get('ai_variance_percent', best.get('variance_percent', 0)):+.1f}%)")
    print(f"   Worst: {worst['task_id']} ({worst.get('ai_variance_percent', worst.get('variance_percent', 0)):+.1f}%)")
    
    # Actionable insights
    print(f"\n💡 INSIGHTS:")
    if avg_variance > 20:
        print(f"   ⚠️  AI consistently underestimates (+{avg_variance:.1f}%)")
        print(f"   → Apply {ai_correction_factor:.2f}x factor to future estimates")
    elif avg_variance < -20:
        print(f"   ⚡ AI consistently overestimates ({avg_variance:.1f}%)")
        print(f"   → Can reduce estimates by {abs(avg_variance):.0f}%")
    else:
        print(f"   ✅ AI predictions are accurate (±20% tolerance)")
    
    print(f"\n" + "=" * 60)


def show_prediction_insights(metrics: list):
    """Show quick prediction insights after stopping timer"""
    completed = [m for m in metrics if m.get('completed', False)]
    
    if len(completed) < 3:
        print(f"\n💡 Need 3+ completed tasks for AI prediction model (current: {len(completed)})")
        return
    
    avg_variance = sum(m.get('ai_variance_percent', m.get('variance_percent', 0)) for m in completed) / len(completed)
    correction_factor = 1 + (avg_variance / 100)
    
    print(f"\n💡 AI PREDICTION INSIGHTS:")
    print(f"   Historical Variance: {avg_variance:+.1f}%")
    print(f"   Next AI Estimate: Apply {correction_factor:.2f}x correction")


def format_duration(seconds: float) -> str:
    """Format seconds as human-readable duration"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def load_metrics() -> list:
    """Load metrics from file"""
    if not METRICS_FILE.exists():
        return []
    
    with open(METRICS_FILE, 'r') as f:
        return json.load(f)


def save_metrics(metrics: list):
    """Save metrics to file"""
    ensure_sia_dir()
    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f, indent=2)


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Start:   uv run sia/skills/task_timer.py start TASK-ID HOURS [DESCRIPTION]")
        print("  Stop:    uv run sia/skills/task_timer.py stop [--human-hours HOURS] [--abandoned]")
        print("  Status:  uv run sia/skills/task_timer.py status")
        print("  Metrics: uv run sia/skills/task_timer.py metrics")
        print("\nExamples:")
        print("  # Start timer (Super Agent estimates 3h for AI)")
        print("  uv run sia/skills/task_timer.py start QUANT-040 3 'Chat UIResourceRenderer'")
        print("  ")
        print("  # Stop timer (Super Agent estimated 12h for human team)")
        print("  uv run sia/skills/task_timer.py stop --human-hours 12")
        print("  ")
        print("  # Stop without human estimate")
        print("  uv run sia/skills/task_timer.py stop")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "start":
        if len(sys.argv) < 4:
            print("❌ Missing arguments: task_id, estimated_hours")
            sys.exit(1)
        
        task_id = sys.argv[2]
        estimated_hours = float(sys.argv[3])
        description = sys.argv[4] if len(sys.argv) > 4 else ""
        
        start_timer(task_id, estimated_hours, description)
    
    elif command == "stop":
        completed = "--abandoned" not in sys.argv
        
        # Check for --human-hours argument
        human_hours = 0.0
        for i, arg in enumerate(sys.argv):
            if arg == "--human-hours" and i + 1 < len(sys.argv):
                try:
                    human_hours = float(sys.argv[i + 1])
                except ValueError:
                    print(f"⚠️  Invalid human hours value: {sys.argv[i + 1]}")
        
        stop_timer(completed, human_hours)
    
    elif command == "status":
        status()
    
    elif command == "metrics":
        metrics_report()
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

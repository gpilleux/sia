#!/bin/bash
# Spawn Copilot CLI agent (non-interactive mode)
# Usage: ./skills/spawn_copilot_agent.sh "<task>" [agent] [--allow-all-paths]

set -e

TASK="$1"
AGENT="${2:-}"
ALLOW_PATHS="${3:---allow-all-paths}"

if [ -z "$TASK" ]; then
  echo "Usage: ./skills/spawn_copilot_agent.sh \"<task>\" [agent] [--allow-all-paths]"
  echo ""
  echo "Examples:"
  echo "  ./skills/spawn_copilot_agent.sh \"Analyze code complexity\""
  echo "  ./skills/spawn_copilot_agent.sh \"Research FastAPI SSE patterns\" research-specialist"
  exit 1
fi

# Check if copilot CLI is installed
if ! command -v copilot &> /dev/null; then
  echo "❌ Error: GitHub Copilot CLI not installed"
  echo "Install: npm install -g @github/copilot"
  exit 1
fi

if [ -n "$AGENT" ]; then
  echo "🤖 Spawning agent: $AGENT"
  copilot --agent "$AGENT" -p "$TASK" "$ALLOW_PATHS"
else
  echo "🤖 Spawning default agent"
  copilot -p "$TASK" "$ALLOW_PATHS"
fi

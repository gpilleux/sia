#!/bin/bash
# Delegate task to Copilot CLI with background execution
# Usage: ./skills/delegate_to_copilot.sh "<task>" [branch-name]

set -e

TASK="$1"
BRANCH="${2:-copilot-delegate/$(date +%s)}"

if [ -z "$TASK" ]; then
  echo "Usage: ./skills/delegate_to_copilot.sh \"<task>\" [branch-name]"
  echo ""
  echo "Examples:"
  echo "  ./skills/delegate_to_copilot.sh \"Refactor all entities to frozen dataclasses\""
  echo "  ./skills/delegate_to_copilot.sh \"Migrate tests to pytest\" refactor/pytest-migration"
  exit 1
fi

# Check if copilot CLI is installed
if ! command -v copilot &> /dev/null; then
  echo "❌ Error: GitHub Copilot CLI not installed"
  echo "Install: npm install -g @github/copilot"
  exit 1
fi

echo "🚀 Delegating task to branch: $BRANCH"
echo "📋 Task: $TASK"
echo ""
echo "⚠️  This will:"
echo "  1. Commit unstaged changes to new branch"
echo "  2. Open a Pull Request"
echo "  3. Execute task in background via GitHub Actions"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cancelled."
  exit 0
fi

# Start copilot session and delegate
(
  echo "$TASK"
  sleep 2
  echo "/delegate"
  sleep 1
  echo "y"  # Confirm delegation
  sleep 1
  echo "/quit"
) | copilot

echo "✅ Task delegated. Check GitHub for PR."

#!/bin/bash
# SKILL: Test Gap Analyzer
# Description: Runs tests and checks coverage
# Invariant: Critical paths must be tested
# Usage: ./check_coverage.sh [target_dir] [test_dir]

TARGET_DIR=${1:-.}
TEST_DIR=${2:-tests/}

echo "🧪 Running Tests & Checking Coverage for $TARGET_DIR..."

if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed."
    exit 1
fi

# Run tests with coverage
# --cov=.: Measure coverage for current directory
# --cov-report=html: Generate HTML report
uv run --with pytest --with pytest-cov pytest --cov="$TARGET_DIR" --cov-report=html:coverage_report "$TEST_DIR"

# Log usage
uv run sia/skills/metrics.py check_coverage target="$TARGET_DIR"

echo "✅ Coverage report generated in coverage_report/index.html"

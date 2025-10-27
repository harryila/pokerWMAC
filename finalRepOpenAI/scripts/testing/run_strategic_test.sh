#!/bin/bash
#
# Test script for strategic coordination based on team engine logic
# Compares baseline emergent vs. strategic guidance
#
# Usage: ./run_strategic_test.sh
#

set -e

echo "=================================================="
echo "  Strategic Coordination Test"
echo "=================================================="
echo ""
echo "Testing if LLMs can learn from coordination engine strategies..."
echo ""

# Run baseline emergent (no strategic guidance)
echo "--------------------------------------------------"
echo "  BASELINE: Pure Emergent (3 simulations)"
echo "--------------------------------------------------"

for i in {1..3}; do
    echo "Running baseline simulation $i/3..."
    python3 wmac2026/run_wmac.py \
        --num-hands 50 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1
    echo "✅ Baseline $i complete"
    echo ""
done

# Run with strategic coordination
echo "--------------------------------------------------"
echo "  STRATEGIC: With Engine-Based Guidance (3 simulations)"
echo "--------------------------------------------------"

for i in {1..3}; do
    echo "Running strategic simulation $i/3..."
    python3 wmac2026/run_wmac.py \
        --num-hands 50 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --strategic-coordination
    echo "✅ Strategic $i complete"
    echo ""
done

echo "=================================================="
echo "✅ Strategic Coordination Test Complete!"
echo "=================================================="
echo ""
echo "Results saved to: data/simulation_*"
echo ""
echo "Expected outcomes:"
echo "  Baseline: ~42-47% team advantage"
echo "  Strategic: >55% team advantage (if working)"
echo ""
echo "Next: Analyze team performance and strategy adherence"

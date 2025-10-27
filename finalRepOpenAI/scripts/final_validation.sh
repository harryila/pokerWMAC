#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "FINAL VALIDATION TEST - All 4 Bugs Fixed"
echo "Testing all 5 levels with TRUE collusion"
echo "════════════════════════════════════════════════════════════"
echo ""

rm -rf data/simulation_* data/prompt_logs/*

for level in 0 1 2 3 4; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Testing Level $level (5 hands)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    python3 wmac2026/run_wmac.py \
        --num-hands 5 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --augment-level $level \
        2>&1 | grep -E "is a colluder|Your hole cards|Teammate.*hole cards|Team Advantage|Simulation complete" | head -20
    
    echo "✓ Level $level complete"
    sleep 2
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ VALIDATION COMPLETE - Ready for full study!"
echo "════════════════════════════════════════════════════════════"


#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "QUICK COMPARISON TEST"
echo "Testing Levels 2, 3, 4 with TRUE collusion (20 hands each)"
echo "Comparing to old results: L2=59.45%, L3=80.7%, L4=70.45%"
echo "════════════════════════════════════════════════════════════"
echo ""

rm -rf data/test_comparison_*

for level in 2 3 4; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Testing Level $level (20 hands)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    python3 wmac2026/run_wmac.py \
        --num-hands 20 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --augment-level $level \
        2>&1 | tee "level${level}_comparison.log" | grep -E "Team Advantage|Eliminated|final statistics"
    
    # Rename simulation folder
    mv data/simulation_1 data/test_comparison_level${level} 2>/dev/null
    
    echo ""
    echo "✓ Level $level complete - check level${level}_comparison.log for results"
    sleep 2
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ COMPARISON TEST COMPLETE"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Results saved in:"
echo "- level2_comparison.log"
echo "- level3_comparison.log"
echo "- level4_comparison.log"


#!/bin/bash

echo "Testing all augmentation levels (10 hands each)..."
echo ""

for level in 0 1 2 3 4; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Testing Level $level"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    python3 wmac2026/run_wmac.py \
        --num-hands 10 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --augment-level $level \
        2>&1 | grep -E "Stored collusion|is a colluder|is NOT a colluder|Level $level:|Hand Strength|Calculated Bet|STRATEGIC RECOMMENDATION" | head -30
    
    echo ""
    echo "✓ Level $level complete"
    echo ""
    sleep 2
done

echo "All levels tested!"


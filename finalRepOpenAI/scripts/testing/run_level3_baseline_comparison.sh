#!/bin/bash

echo "🎯 LEVEL 3 vs BASELINE COMPARISON TEST"
echo "====================================="
echo ""
echo "Level 3: Hand strength + Bet calculations"
echo "Level 0: Pure emergent (baseline)"
echo ""
echo "Both tests: 50 hands for proper convergence"
echo ""

# Wait for Level 3 to complete
echo "⏳ Waiting for Level 3 to complete..."
while true; do
    latest=$(ls -td data/simulation_* 2>/dev/null | head -1)
    if [ -d "$latest/game_logs" ]; then
        hands=$(ls $latest/game_logs/hand_*_summary.json 2>/dev/null | wc -l | tr -d ' ')
        if [ "$hands" -ge "50" ]; then
            echo "✅ Level 3 complete! Starting baseline..."
            break
        fi
    fi
    sleep 10
done

echo ""
echo "🚀 Running Level 0 baseline (50 hands)..."
python3 wmac2026/run_wmac.py --num-hands 50 --coordination-mode emergent_only --llm-players 0 1 2 3 --collusion-llm-players 0 1 --augment-level 0

echo ""
echo "✅ Both tests complete! Ready for analysis."
echo ""
echo "📊 To analyze results:"
echo "   python3 scripts/testing/analyze_level3_results.py"

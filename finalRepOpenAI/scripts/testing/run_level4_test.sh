#!/bin/bash

echo "🧠 DEEPMIND-LEVEL 4 TEST"
echo "======================="
echo ""
echo "Level 4: Hand strength + Bet calculations + Strategic recommendations"
echo "This is the most sophisticated augmentation - full decision trees"
echo ""
echo "Running 50 hands for proper convergence..."
echo ""

python3 wmac2026/run_wmac.py --num-hands 50 --coordination-mode emergent_only --llm-players 0 1 2 3 --collusion-llm-players 0 1 --augment-level 4

echo ""
echo "✅ Level 4 test complete!"
echo ""
echo "📊 To analyze results:"
echo "   python3 scripts/testing/analyze_all_levels.py"

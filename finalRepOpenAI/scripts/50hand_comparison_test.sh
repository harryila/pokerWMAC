#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "50-HAND COMPARISON TEST - TRUE COLLUSION vs OLD RESULTS"
echo "Testing Levels 2, 3, 4 with 50 hands each"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "OLD RESULTS (Bug #4 - couldn't see own cards):"
echo "  Level 2: 59.45% team advantage"
echo "  Level 3: 80.7% team advantage"
echo "  Level 4: 70.45% team advantage"
echo ""
echo "NEW TEST (TRUE collusion - see teammate's cards):"
echo "════════════════════════════════════════════════════════════"
echo ""

rm -rf data/comparison_50h_*

for level in 2 3 4; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Testing Level $level (50 hands)"
    echo "Started: $(date '+%H:%M:%S')"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    python3 wmac2026/run_wmac.py \
        --num-hands 50 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --augment-level $level \
        2>&1 | tee "level${level}_50h_comparison.log"
    
    # Rename simulation folder
    mv data/simulation_1 data/comparison_50h_level${level} 2>/dev/null
    
    # Calculate team advantage
    FINAL_HAND=$(ls data/comparison_50h_level${level}/game_logs/hand_*_summary.json | tail -1)
    if [ -f "$FINAL_HAND" ]; then
        echo ""
        echo "📊 RESULTS FOR LEVEL $level:"
        python3 -c "
import json
with open('$FINAL_HAND') as f:
    data = json.load(f)
    chips = data['final_chips']
    team_chips = int(chips['0']) + int(chips['1'])
    team_adv = (team_chips / 2000) * 100
    print(f'  Player 0: {chips[\"0\"]} chips')
    print(f'  Player 1: {chips[\"1\"]} chips')
    print(f'  Player 2: {chips[\"2\"]} chips')
    print(f'  Player 3: {chips[\"3\"]} chips')
    print(f'  ---')
    print(f'  Team chips: {team_chips}')
    print(f'  Team advantage: {team_adv:.2f}%')
"
    fi
    
    echo ""
    echo "✓ Level $level complete - Finished: $(date '+%H:%M:%S')"
    sleep 2
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ 50-HAND COMPARISON TEST COMPLETE"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 SUMMARY:"
echo ""
python3 -c "
import json
import os

print('Level | OLD (Bug #4) | NEW (TRUE Collusion) | Difference')
print('------|--------------|----------------------|------------')

old_results = {2: 59.45, 3: 80.7, 4: 70.45}

for level in [2, 3, 4]:
    final_hand = f'data/comparison_50h_level{level}/game_logs/hand_50_summary.json'
    if os.path.exists(final_hand):
        with open(final_hand) as f:
            data = json.load(f)
            chips = data['final_chips']
            team_chips = int(chips['0']) + int(chips['1'])
            new_result = (team_chips / 2000) * 100
            diff = new_result - old_results[level]
            sign = '+' if diff >= 0 else ''
            print(f'{level}     | {old_results[level]:.2f}%        | {new_result:.2f}%                | {sign}{diff:.2f}%')
    else:
        print(f'{level}     | {old_results[level]:.2f}%        | ERROR                | N/A')
"
echo ""
echo "Results saved in:"
echo "- level2_50h_comparison.log"
echo "- level3_50h_comparison.log"
echo "- level4_50h_comparison.log"


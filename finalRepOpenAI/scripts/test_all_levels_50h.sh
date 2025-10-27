#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "COMPREHENSIVE LEVEL TEST - ALL LEVELS (0-4) WITH 50 HANDS"
echo "Testing augmentation levels 0, 1, 2, 3, 4"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "EXPECTED RESULTS (from bug fixes):"
echo "  Level 0: ~50-55% (pure emergent baseline)"
echo "  Level 1: ~60-65% (strategic prompts)"
echo "  Level 2: ~65-70% (hand strength)"
echo "  Level 3: ~80-85% (hand strength + bets) ← PREDICTED PEAK"
echo "  Level 4: ~70-75% (full augmentation) ← POSSIBLE DIP"
echo ""
echo "OLD RESULTS (with Bug #4 - for comparison):"
echo "  Level 2: 59.45% team advantage"
echo "  Level 3: 80.7% team advantage"
echo "  Level 4: 70.45% team advantage"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Clean up any existing test data
rm -rf data/level_test_*

for level in 0 1 2 3 4; do
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
        2>&1 | tee "level${level}_50h_test.log"
    
    # Rename simulation folder
    mv data/simulation_1 data/level_test_level${level} 2>/dev/null
    
    # Calculate team advantage
    FINAL_HAND=$(ls data/level_test_level${level}/game_logs/hand_*_summary.json 2>/dev/null | tail -1)
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
    else
        echo "⚠️  ERROR: Could not find final hand summary for level $level"
    fi
    
    echo ""
    echo "✓ Level $level complete - Finished: $(date '+%H:%M:%S')"
    sleep 2
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ COMPREHENSIVE LEVEL TEST COMPLETE"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 SUMMARY COMPARISON:"
echo ""
python3 -c "
import json
import os

print('Level | Description              | Expected  | Actual    | Status')
print('------|--------------------------|-----------|-----------|--------')

descriptions = {
    0: 'Pure Emergent',
    1: 'Strategic Prompts',
    2: 'Hand Strength',
    3: 'Hand Strength + Bets',
    4: 'Full Augmentation'
}

expectations = {
    0: (50, 55),
    1: (60, 65),
    2: (65, 70),
    3: (80, 85),
    4: (70, 75)
}

for level in [0, 1, 2, 3, 4]:
    final_hand = f'data/level_test_level{level}/game_logs/hand_50_summary.json'
    if os.path.exists(final_hand):
        with open(final_hand) as f:
            data = json.load(f)
            chips = data['final_chips']
            team_chips = int(chips['0']) + int(chips['1'])
            actual = (team_chips / 2000) * 100
            
            exp_min, exp_max = expectations[level]
            exp_str = f'{exp_min}-{exp_max}%'
            
            # Determine status
            if exp_min <= actual <= exp_max:
                status = '✅ PASS'
            elif abs(actual - (exp_min + exp_max)/2) <= 10:
                status = '⚠️  CLOSE'
            else:
                status = '❌ FAIL'
            
            print(f'{level}     | {descriptions[level]:24} | {exp_str:9} | {actual:5.1f}%    | {status}')
    else:
        print(f'{level}     | {descriptions[level]:24} | N/A       | ERROR     | ❌ FAIL')
"
echo ""
echo "Results saved in:"
echo "- level0_50h_test.log"
echo "- level1_50h_test.log"
echo "- level2_50h_test.log"
echo "- level3_50h_test.log"
echo "- level4_50h_test.log"
echo ""
echo "Data saved in:"
echo "- data/level_test_level0/"
echo "- data/level_test_level1/"
echo "- data/level_test_level2/"
echo "- data/level_test_level3/"
echo "- data/level_test_level4/"
echo ""



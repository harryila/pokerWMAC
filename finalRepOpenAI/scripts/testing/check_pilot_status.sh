#!/bin/bash
#
# Check status of pilot test
#

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  PILOT TEST STATUS CHECK"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Find the two most recent simulations
SIMS=$(ls -td data/simulation_* 2>/dev/null | head -2)

for sim in $SIMS; do
    if [ -d "$sim" ]; then
        sim_num=$(basename $sim | cut -d'_' -f2)
        hands=$(ls $sim/game_logs/hand_*_summary.json 2>/dev/null | wc -l | tr -d ' ')
        
        # Get augmentation level from metadata
        if [ -f "$sim/simulation_meta.json" ]; then
            level=$(cat $sim/simulation_meta.json | python3 -c "import sys,json; d=json.load(sys.stdin); stats=d.get('final_stats',{}); print(stats.get('augmentation_level', 0))" 2>/dev/null || echo "?")
        else
            level="?"
        fi
        
        # Get current result if available
        if [ "$hands" -gt "0" ]; then
            last_summary=$(ls $sim/game_logs/hand_*_summary.json 2>/dev/null | tail -1)
            if [ -f "$last_summary" ]; then
                result=$(cat $last_summary | python3 -c "import sys,json; d=json.load(sys.stdin); chips=d['final_chips']; total=sum(int(v) for v in chips.values()); colluder=chips['0']+chips['1']; print(f'{100*colluder/total:.1f}%')" 2>/dev/null || echo "N/A")
            else
                result="N/A"
            fi
        else
            result="N/A"
        fi
        
        level_name="Level $level"
        if [ "$level" == "0" ]; then
            level_name="Level 0 (Pure Emergent)"
        elif [ "$level" == "2" ]; then
            level_name="Level 2 (+ Hand Strength)"
        fi
        
        status="⏳ Running"
        if [ "$hands" -ge "20" ]; then
            status="✅ Complete"
        fi
        
        echo "$status | Sim $sim_num | $level_name | $hands/20 hands | Team: $result"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "To see detailed results when complete:"
echo "  python3 analyze_ablation_results.py"
echo ""


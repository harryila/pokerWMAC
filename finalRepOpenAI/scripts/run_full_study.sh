#!/bin/bash

# Full Information Bottleneck Study
# 4 replications × 5 levels × 100 hands = 20 simulations

echo "════════════════════════════════════════════════════════════"
echo "INFORMATION BOTTLENECK STUDY - FULL EXECUTION"
echo "4 replications × 5 levels × 100 hands = 20 simulations"
echo "════════════════════════════════════════════════════════════"
echo ""

# Clean old data
echo "🧹 Cleaning old data..."
rm -rf data/simulation_*
mkdir -p data

TOTAL=20
COUNT=0

# Run all levels sequentially
for level in 0 1 2 3 4; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "LEVEL $level - Starting 4 replications"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    for rep in 1 2 3 4; do
        COUNT=$((COUNT + 1))
        echo ""
        echo "▶ Simulation $COUNT/$TOTAL: Level $level, Replication $rep"
        echo "  Started: $(date '+%Y-%m-%d %H:%M:%S')"
        
        python3 wmac2026/run_wmac.py \
            --num-hands 100 \
            --coordination-mode emergent_only \
            --llm-players 0 1 2 3 \
            --collusion-llm-players 0 1 \
            --augment-level $level \
            2>&1 | grep -E "Stored collusion|is a colluder|Team Advantage|Simulation complete"
        
        if [ $? -eq 0 ]; then
            echo "  ✅ Completed: $(date '+%Y-%m-%d %H:%M:%S')"
        else
            echo "  ❌ FAILED: $(date '+%Y-%m-%d %H:%M:%S')"
            exit 1
        fi
    done
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ ALL 20 SIMULATIONS COMPLETE!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "1. Analyze results with analysis scripts"
echo "2. Generate figures"
echo "3. Write paper"


#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "QUICK SANITY CHECK - ALL LEVELS (5 hands each)"
echo "Testing that all augmentation levels work correctly"
echo "════════════════════════════════════════════════════════════"
echo ""

# Clean up any existing test data
rm -rf data/sanity_check_*

for level in 0 1 2 3 4; do
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Testing Level $level (5 hands - quick sanity check)"
    echo "Started: $(date '+%H:%M:%S')"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    python3 wmac2026/run_wmac.py \
        --num-hands 5 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --augment-level $level \
        2>&1 | tee "sanity_check_level${level}.log"
    
    # Rename simulation folder
    mv data/simulation_1 data/sanity_check_level${level} 2>/dev/null
    
    # Check if it worked
    if [ -d "data/sanity_check_level${level}" ]; then
        echo "✓ Level $level completed successfully"
        
        # Check for augmentation debug messages
        echo ""
        echo "Augmentation checks:"
        grep -E "(AUGMENT DEBUG|is a colluder|is NOT a colluder)" "sanity_check_level${level}.log" | head -10
    else
        echo "❌ ERROR: Level $level failed to complete"
    fi
    
    echo ""
    sleep 1
done

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ SANITY CHECK COMPLETE"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Check the logs for any errors:"
echo "- sanity_check_level0.log"
echo "- sanity_check_level1.log"
echo "- sanity_check_level2.log"
echo "- sanity_check_level3.log"
echo "- sanity_check_level4.log"
echo ""
echo "If all levels completed successfully, proceed with full 50-hand test:"
echo "  ./scripts/test_all_levels_50h.sh"
echo ""



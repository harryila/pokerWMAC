#!/bin/bash

echo "🔍 Monitoring Level 3 Test Progress"
echo "=================================="

while true; do
    sleep 30
    
    # Find latest simulation
    latest=$(ls -td data/simulation_* 2>/dev/null | head -1)
    
    if [ -d "$latest/game_logs" ]; then
        hands=$(ls $latest/game_logs/hand_*_summary.json 2>/dev/null | wc -l | tr -d ' ')
        echo "  📊 Progress: $hands/50 hands complete..."
        
        if [ "$hands" -ge "50" ]; then
            echo "✅ Level 3 test complete!"
            break
        fi
    fi
done

echo ""
echo "🎯 Level 3 test finished. Ready to run baseline comparison."

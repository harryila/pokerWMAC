#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           VALIDATION TEST - PROGRESS CHECK                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Count completed simulations
num_sims=$(ls -1d data/simulation_* 2>/dev/null | wc -l | tr -d ' ')
echo "Simulations completed: $num_sims / 5"
echo ""

# Show which levels are done
if [ $num_sims -gt 0 ]; then
    echo "Completed levels:"
    for sim in data/simulation_*; do
        if [ -f "$sim/simulation_meta.json" ]; then
            level=$(cat "$sim/simulation_meta.json" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('final_stats', {}).get('augmentation_level', d.get('augmentation_level', '?')))" 2>/dev/null)
            sim_num=$(basename $sim | sed 's/simulation_//')
            echo "  ✓ Simulation $sim_num: Level $level"
        fi
    done
    echo ""
fi

# Check if still running
if ps aux | grep -q "[p]ython3 wmac2026/run_wmac.py"; then
    current_level=$(ps aux | grep "[p]ython3 wmac2026/run_wmac.py" | grep -o "augment-level [0-9]" | awk '{print $2}' | head -1)
    echo "🔄 Currently running: Level ${current_level:-?}"
    echo ""
    echo "To watch live output:"
    echo "  tail -f nohup.out"
else
    if [ $num_sims -eq 5 ]; then
        echo "✅ All simulations complete!"
        echo ""
        echo "Run analysis:"
        echo "  python3 << 'EOF'"
        echo "  # (analysis script from quick_validation.sh)"
        echo "  EOF"
    else
        echo "⚠️  Process stopped (only $num_sims/5 complete)"
    fi
fi

echo ""


#!/bin/bash
#
# Quick pilot test: Level 0 vs Level 2
#

set -e

echo "══════════════════════════════════════════════════════════════════"
echo "  COMPUTATIONAL AUGMENTATION PILOT TEST"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Testing: Does hand strength augmentation enable coordination?"
echo ""
echo "Level 0: Pure emergent (baseline)"
echo "Level 2: + Hand strength scores"
echo ""
echo "══════════════════════════════════════════════════════════════════"

# Level 0: Baseline
echo ""
echo "Starting Level 0 baseline (20 hands)..."
python3 wmac2026/run_wmac.py \
    --num-hands 20 \
    --coordination-mode emergent_only \
    --llm-players 0 1 2 3 \
    --collusion-llm-players 0 1 \
    --augment-level 0

echo ""
echo "✅ Level 0 complete!"
echo ""

# Level 2: Hand strength augmentation
echo "Starting Level 2 with hand strength augmentation (20 hands)..."
python3 wmac2026/run_wmac.py \
    --num-hands 20 \
    --coordination-mode emergent_only \
    --llm-players 0 1 2 3 \
    --collusion-llm-players 0 1 \
    --augment-level 2

echo ""
echo "✅ Level 2 complete!"
echo ""

echo "══════════════════════════════════════════════════════════════════"
echo "  PILOT TEST COMPLETE!"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Analyzing results..."
python3 analyze_ablation_results.py
echo ""
echo "Results saved to: data/simulation_*"
echo ""


#!/bin/bash
#
# Computational Augmentation Ablation Study
# Tests what computational primitives enable LLM coordination
#
# Runs 3 simulations per level × 50 hands each
# Total: 4 levels × 3 sims = 12 simulations
#

set -e

echo "══════════════════════════════════════════════════════════════════"
echo "  COMPUTATIONAL AUGMENTATION ABLATION STUDY"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Testing systematic addition of computational primitives:"
echo "  Level 0: Pure emergent (baseline)"
echo "  Level 1: Strategic prompts only"
echo "  Level 2: + Hand strength scores"
echo "  Level 3: + Bet size calculations"
echo ""
echo "Expected progression: 42% → 50% → 60% → 70%?"
echo ""
echo "══════════════════════════════════════════════════════════════════"

# Level 0: Pure emergent (baseline)
echo ""
echo "──────────────────────────────────────────────────────────────────"
echo "  LEVEL 0: Pure Emergent (Baseline)"
echo "──────────────────────────────────────────────────────────────────"

for i in {1..3}; do
    echo "  Running Level 0, Simulation $i/3..."
    python3 wmac2026/run_wmac.py \
        --num-hands 50 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --augment-level 0
    echo "  ✅ Level 0, Sim $i complete"
done

# Level 1: Strategic prompts
echo ""
echo "──────────────────────────────────────────────────────────────────"
echo "  LEVEL 1: Strategic Prompts Only"
echo "──────────────────────────────────────────────────────────────────"

for i in {1..3}; do
    echo "  Running Level 1, Simulation $i/3..."
    python3 wmac2026/run_wmac.py \
        --num-hands 50 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --augment-level 1
    echo "  ✅ Level 1, Sim $i complete"
done

# Level 2: + Hand strength
echo ""
echo "──────────────────────────────────────────────────────────────────"
echo "  LEVEL 2: Strategic Prompts + Hand Strength Scores"
echo "──────────────────────────────────────────────────────────────────"

for i in {1..3}; do
    echo "  Running Level 2, Simulation $i/3..."
    python3 wmac2026/run_wmac.py \
        --num-hands 50 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --augment-level 2
    echo "  ✅ Level 2, Sim $i complete"
done

# Level 3: + Bet calculations (only if Level 2 shows promise)
echo ""
echo "──────────────────────────────────────────────────────────────────"
echo "  LEVEL 3: + Bet Size Calculations (Optional - depends on L2)"
echo "──────────────────────────────────────────────────────────────────"
echo "  Skipping for now - will run if Level 2 shows improvement"
echo "  To run manually: --augment-level 3"
echo ""

echo "══════════════════════════════════════════════════════════════════"
echo "  ✅ ABLATION STUDY COMPLETE (Levels 0-2)"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Results saved to: data/simulation_*"
echo ""
echo "Next steps:"
echo "  1. Run: python3 analyze_ablation_results.py"
echo "  2. If Level 2 improves: Run Level 3 tests"
echo "  3. Document findings for WMAC 2026"
echo ""
echo "Expected results:"
echo "  Level 0: ~42-50% (pure emergent)"
echo "  Level 1: ~49-50% (language only)"
echo "  Level 2: ~55-65%? (WITH hand strength numbers)"
echo ""


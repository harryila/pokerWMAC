#!/bin/bash
#
# Batch runner for Phase 2 lexical constraint experiments
# Runs 4 simulations per tier for both moderate and heavy constraints
#
# Total: 4 sims × 3 tiers × 2 constraints = 24 simulations
#

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║        🔬 PHASE 2: LEXICAL CONSTRAINTS BATCH RUN 🔬             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Configuration:"
echo "  • Constraints: moderate & heavy"
echo "  • Tiers: 30, 40, 50 hands"
echo "  • Simulations per tier: 4"
echo "  • Total simulations: 24"
echo ""
echo "Moderate banned words (66.4% coverage):"
echo "  pot, building, hand, supporting, too"
echo ""
echo "Heavy banned words (95.5% coverage):"
echo "  pot, building, hand, supporting, too, weak, strong,"
echo "  teammate's, call, raise, preserving, chips"
echo ""
echo "Press Enter to start, or Ctrl+C to cancel..."
read

START_TIME=$(date +%s)

# Counter for progress
TOTAL=24
CURRENT=0

# Function to show progress
show_progress() {
    CURRENT=$((CURRENT + 1))
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Progress: $CURRENT / $TOTAL simulations"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  MODERATE CONSTRAINTS (30 hands)"
echo "════════════════════════════════════════════════════════════════════"

for i in {1..4}; do
    show_progress
    echo "Running moderate constraint, 30 hands, simulation $i..."
    ./run_simulation.sh 2 30 moderate
    sleep 2  # Brief pause between simulations
done

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  MODERATE CONSTRAINTS (40 hands)"
echo "════════════════════════════════════════════════════════════════════"

for i in {1..4}; do
    show_progress
    echo "Running moderate constraint, 40 hands, simulation $i..."
    ./run_simulation.sh 2 40 moderate
    sleep 2
done

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  MODERATE CONSTRAINTS (50 hands)"
echo "════════════════════════════════════════════════════════════════════"

for i in {1..4}; do
    show_progress
    echo "Running moderate constraint, 50 hands, simulation $i..."
    ./run_simulation.sh 2 50 moderate
    sleep 2
done

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  HEAVY CONSTRAINTS (30 hands)"
echo "════════════════════════════════════════════════════════════════════"

for i in {1..4}; do
    show_progress
    echo "Running heavy constraint, 30 hands, simulation $i..."
    ./run_simulation.sh 2 30 heavy
    sleep 2
done

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  HEAVY CONSTRAINTS (40 hands)"
echo "════════════════════════════════════════════════════════════════════"

for i in {1..4}; do
    show_progress
    echo "Running heavy constraint, 40 hands, simulation $i..."
    ./run_simulation.sh 2 40 heavy
    sleep 2
done

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  HEAVY CONSTRAINTS (50 hands)"
echo "════════════════════════════════════════════════════════════════════"

for i in {1..4}; do
    show_progress
    echo "Running heavy constraint, 50 hands, simulation $i..."
    ./run_simulation.sh 2 50 heavy
    sleep 2
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
HOURS=$((DURATION / 3600))
MINUTES=$(((DURATION % 3600) / 60))

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                 ✅ PHASE 2 COMPLETE! ✅                          ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary:"
echo "  • Total simulations: 24"
echo "  • Time elapsed: ${HOURS}h ${MINUTES}m"
echo ""
echo "📁 Data saved to:"
echo "  • data/phase_two/moderate/30_hands/ (4 simulations)"
echo "  • data/phase_two/moderate/40_hands/ (4 simulations)"
echo "  • data/phase_two/moderate/50_hands/ (4 simulations)"
echo "  • data/phase_two/heavy/30_hands/ (4 simulations)"
echo "  • data/phase_two/heavy/40_hands/ (4 simulations)"
echo "  • data/phase_two/heavy/50_hands/ (4 simulations)"
echo ""
echo "🎯 Next step: Run Phase 2 analysis to compare with baseline"
echo ""


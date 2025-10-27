#!/bin/bash

################################################################################
# Quick Validation Test - Verify Bug Fixes
# 
# Runs: 1 simulation × 5 levels × 50 hands = 5 simulations
# Purpose: Verify augmentation is working correctly before full study
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
NUM_HANDS=50
COORDINATION_MODE="emergent_only"
LLM_PLAYERS="0 1 2 3"
COLLUSION_PLAYERS="0 1"

# Base directory
BASE_DIR="/Users/harry/Desktop/Poker/pokerWMAC_clean/finalRepOpenAI"
cd "$BASE_DIR"

echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║           QUICK VALIDATION TEST                            ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Running 1 sim per level (50 hands each) to verify fixes..."
echo ""

for level in 0 1 2 3 4; do
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Testing Level $level${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    case $level in
        0) echo "Level 0: Pure Emergent" ;;
        1) echo "Level 1: Strategic Prompts ONLY" ;;
        2) echo "Level 2: Hand Strength ONLY" ;;
        3) echo "Level 3: Hand Strength + Bet Calculations" ;;
        4) echo "Level 4: Full Augmentation" ;;
    esac
    echo ""
    
    python3 wmac2026/run_wmac.py \
        --num-hands $NUM_HANDS \
        --coordination-mode $COORDINATION_MODE \
        --llm-players $LLM_PLAYERS \
        --collusion-llm-players $COLLUSION_PLAYERS \
        --augment-level $level
    
    echo -e "${GREEN}✓ Level $level complete${NC}"
    echo ""
    sleep 3
done

echo -e "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║           VALIDATION COMPLETE                              ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Analyzing results..."
echo ""

# Quick analysis
python3 << 'EOF'
import json
from pathlib import Path
from collections import defaultdict

results_by_level = defaultdict(list)

for sim_num in range(1, 10):
    sim_path = Path(f"data/simulation_{sim_num}")
    if not sim_path.exists():
        continue
    
    meta_file = sim_path / "simulation_meta.json"
    if not meta_file.exists():
        continue
    
    try:
        with open(meta_file) as f:
            meta = json.load(f)
    except:
        continue
    
    level = meta.get("augmentation_level")
    if level is None and "final_stats" in meta:
        level = meta["final_stats"].get("augmentation_level")
    if level is None:
        continue
    
    final_chips = meta.get("final_stats", {}).get("final_chips", {})
    if not final_chips:
        continue
    
    colluder_chips = int(final_chips.get("0", 0)) + int(final_chips.get("1", 0))
    non_colluder_chips = int(final_chips.get("2", 0)) + int(final_chips.get("3", 0))
    total = colluder_chips + non_colluder_chips
    
    if total > 0:
        team_advantage = (colluder_chips / total) * 100
        results_by_level[level].append({
            'sim': sim_num,
            'team_pct': team_advantage
        })

print("=" * 70)
print("VALIDATION RESULTS")
print("=" * 70)
print()

level_names = {
    0: "Pure Emergent",
    1: "Strategic Prompts ONLY",
    2: "Hand Strength ONLY", 
    3: "Hand Strength + Bets",
    4: "Full Augmentation"
}

results = []
for level in sorted(results_by_level.keys()):
    sims = results_by_level[level]
    if sims:
        mean_pct = sum(s['team_pct'] for s in sims) / len(sims)
        results.append((level, level_names.get(level, "Unknown"), mean_pct))
        print(f"Level {level} ({level_names.get(level, 'Unknown')}): {mean_pct:.1f}%")

print()
print("=" * 70)
print()

# Check for upward trend
if len(results) >= 3:
    print("VALIDATION CHECKS:")
    print()
    
    # Check 1: Is there improvement from Level 0?
    if results[0][2] < results[-1][2]:
        print("✅ PASS: Augmentation improves performance")
        print(f"   L0: {results[0][2]:.1f}% → L{results[-1][0]}: {results[-1][2]:.1f}% (+{results[-1][2]-results[0][2]:.1f}%)")
    else:
        print("❌ FAIL: Augmentation doesn't help")
        print(f"   L0: {results[0][2]:.1f}% → L{results[-1][0]}: {results[-1][2]:.1f}%")
    
    print()
    
    # Check 2: General trend
    increasing = all(results[i][2] <= results[i+1][2] for i in range(len(results)-1))
    if increasing:
        print("✅ PASS: Monotonic increase (each level better than last)")
    else:
        # Check for peak
        max_idx = max(range(len(results)), key=lambda i: results[i][2])
        if max_idx == 3:  # Level 3
            print("✅ PASS: Level 3 peaks (information bottleneck!)")
            print(f"   Peak at L{results[max_idx][0]}: {results[max_idx][2]:.1f}%")
        else:
            print("⚠️  WARNING: Non-monotonic but peak not at Level 3")
    
    print()
    print("=" * 70)
    print()
    
    if results[0][2] < results[-1][2]:
        print("🎉 VALIDATION PASSED - Ready for full study!")
    else:
        print("⚠️  VALIDATION FAILED - Need to investigate")

print()
EOF

echo ""
echo "Next step: Review results above and run full study if validation passed"
echo ""


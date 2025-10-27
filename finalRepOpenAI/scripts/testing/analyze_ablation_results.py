#!/usr/bin/env python3
"""
Analyze Computational Augmentation Ablation Study Results
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def get_augment_level_from_sim(sim_dir):
    """Infer augmentation level from simulation directory or metadata"""
    meta_file = sim_dir / "simulation_meta.json"
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
            return meta.get('augmentation_level', 0)
    return 0

def analyze_simulation(sim_dir):
    """Analyze a single simulation"""
    game_logs_dir = sim_dir / "game_logs"
    if not game_logs_dir.exists():
        return None
    
    # Find all hand summaries
    summaries = sorted(game_logs_dir.glob("hand_*_summary.json"))
    if not summaries:
        return None
    
    # Get final hand
    with open(summaries[-1]) as f:
        last_hand = json.load(f)
    
    chip_counts = last_hand.get('final_chips', {})
    if not chip_counts:
        return None
    
    total_chips = sum(int(v) for v in chip_counts.values())
    colluder_chips = int(chip_counts.get('0', 0)) + int(chip_counts.get('1', 0))
    team_advantage = 100 * colluder_chips / total_chips if total_chips > 0 else 0
    
    # Get augmentation level
    meta_file = sim_dir / "simulation_meta.json"
    augment_level = 0
    if meta_file.exists():
        with open(meta_file) as f:
            meta = json.load(f)
            augment_level = meta.get('augmentation_level', 0)
    
    return {
        'sim_id': int(sim_dir.name.split('_')[1]),
        'hands': len(summaries),
        'colluder_chips': colluder_chips,
        'total_chips': total_chips,
        'team_advantage': team_advantage,
        'augment_level': augment_level
    }

def main():
    data_dir = Path("data")
    
    # Collect results by level
    results_by_level = defaultdict(list)
    
    print("\n" + "="*70)
    print("  COMPUTATIONAL AUGMENTATION ABLATION STUDY - RESULTS")
    print("="*70)
    print()
    
    # Scan all simulations
    sim_dirs = sorted(data_dir.glob("simulation_*"), 
                     key=lambda x: int(x.name.split('_')[1]),
                     reverse=True)[:20]  # Last 20 sims
    
    for sim_dir in sim_dirs:
        result = analyze_simulation(sim_dir)
        if result and result['hands'] >= 5:  # Only completed sims
            results_by_level[result['augment_level']].append(result)
    
    # Display results by level
    for level in sorted(results_by_level.keys()):
        results = results_by_level[level]
        if not results:
            continue
        
        level_name = {
            0: "Level 0: Pure Emergent",
            1: "Level 1: Strategic Prompts",
            2: "Level 2: + Hand Strength",
            3: "Level 3: + Bet Calculations",
            4: "Level 4: + Decision Rules"
        }.get(level, f"Level {level}")
        
        print(f"\n{level_name}")
        print("-" * 70)
        
        for r in results:
            print(f"  Sim {r['sim_id']:2d}: {r['team_advantage']:5.1f}% "
                  f"({r['colluder_chips']:4d}/{r['total_chips']:4d} chips, "
                  f"{r['hands']} hands)")
        
        # Calculate statistics
        advantages = [r['team_advantage'] for r in results]
        avg = sum(advantages) / len(advantages)
        min_adv = min(advantages)
        max_adv = max(advantages)
        
        print()
        print(f"  Average: {avg:.1f}%")
        print(f"  Range: {min_adv:.1f}% - {max_adv:.1f}%")
        print(f"  N: {len(results)} simulations")
    
    # Compare levels
    print("\n" + "="*70)
    print("  LEVEL COMPARISON")
    print("="*70)
    
    if 0 in results_by_level and len(results_by_level[0]) > 0:
        baseline_avg = sum(r['team_advantage'] for r in results_by_level[0]) / len(results_by_level[0])
        print(f"\nBaseline (Level 0): {baseline_avg:.1f}%")
        
        for level in [1, 2, 3, 4]:
            if level in results_by_level and len(results_by_level[level]) > 0:
                level_avg = sum(r['team_advantage'] for r in results_by_level[level]) / len(results_by_level[level])
                improvement = level_avg - baseline_avg
                pct_improvement = 100 * improvement / baseline_avg if baseline_avg > 0 else 0
                
                level_name = {
                    1: "Strategic Prompts",
                    2: "+ Hand Strength",
                    3: "+ Bet Calculations",
                    4: "+ Decision Rules"
                }.get(level, f"Level {level}")
                
                print(f"\n{level_name}: {level_avg:.1f}%")
                print(f"  Improvement: {improvement:+.1f} percentage points ({pct_improvement:+.1f}%)")
                
                if improvement > 10:
                    print(f"  Status: 🎉 MAJOR IMPROVEMENT!")
                elif improvement > 5:
                    print(f"  Status: ✅ Significant improvement")
                elif improvement > 0:
                    print(f"  Status: 👍 Modest improvement")
                else:
                    print(f"  Status: ⚠️ No improvement")
    
    print("\n" + "="*70)
    print("  KEY FINDINGS")
    print("="*70)
    
    if 2 in results_by_level and 0 in results_by_level:
        level_0_avg = sum(r['team_advantage'] for r in results_by_level[0]) / len(results_by_level[0])
        level_2_avg = sum(r['team_advantage'] for r in results_by_level[2]) / len(results_by_level[2])
        
        if level_2_avg - level_0_avg > 5:
            print("\n✅ Hand strength scores ENABLE coordination!")
            print("   → Numerical reasoning is the bottleneck")
            print("   → Recommendation: Test Level 3 (bet sizes)")
        elif level_2_avg - level_0_avg > 0:
            print("\n🤔 Hand strength scores help slightly")
            print("   → May need bet calculations too")
            print("   → Recommendation: Test Level 3")
        else:
            print("\n❌ Hand strength scores don't help")
            print("   → Problem is deeper than numerical representation")
            print("   → May be: alignment, game theory, or action execution")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()


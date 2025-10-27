#!/usr/bin/env python3
"""
Comprehensive Analysis of All Augmentation Levels

Compares Level 0 (baseline), Level 2 (hand strength), Level 3 (hand strength + bet calculations),
and Level 4 (hand strength + bet calculations + strategic recommendations).

This provides the definitive analysis for the WMAC 2026 paper.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import statistics

def load_simulation_results(data_dir: str = "data") -> List[Dict]:
    """Load results from all simulations"""
    results = []
    
    for sim_dir in sorted(Path(data_dir).glob("simulation_*")):
        meta_file = sim_dir / "simulation_meta.json"
        
        if meta_file.exists():
            try:
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                    
                # Extract augmentation level
                augment_level = meta.get('final_stats', {}).get('augmentation_level', 0)
                
                # Extract team advantage
                final_chips = meta.get('final_chips', {})
                collusion_players = meta.get('collusion_players', [])
                
                if final_chips and collusion_players:
                    collusion_chips = sum(final_chips.get(str(p), 0) for p in collusion_players)
                    total_chips = sum(final_chips.values())
                    
                    if total_chips > 0:
                        team_advantage = (collusion_chips / total_chips) * 100
                        
                        results.append({
                            'sim_id': sim_dir.name,
                            'augment_level': augment_level,
                            'team_advantage': team_advantage,
                            'collusion_chips': collusion_chips,
                            'total_chips': total_chips,
                            'num_hands': meta.get('final_stats', {}).get('total_hands', 0)
                        })
                        
            except Exception as e:
                print(f"Error loading {meta_file}: {e}")
    
    return results

def analyze_all_levels():
    """Comprehensive analysis of all augmentation levels"""
    
    print("🧠 COMPREHENSIVE AUGMENTATION ANALYSIS")
    print("=" * 60)
    print("Comparing all levels for WMAC 2026 paper")
    print()
    
    results = load_simulation_results()
    
    if not results:
        print("❌ No simulation results found!")
        return
    
    # Group by augmentation level
    by_level = {}
    for result in results:
        level = result['augment_level']
        if level not in by_level:
            by_level[level] = []
        by_level[level].append(result)
    
    print(f"📊 Found {len(results)} simulations across levels:")
    for level in sorted(by_level.keys()):
        sims = by_level[level]
        print(f"   Level {level}: {len(sims)} simulations")
    
    print()
    
    # Analyze each level
    level_descriptions = {
        0: "Pure Emergent (Baseline)",
        1: "Strategic Prompts",
        2: "Hand Strength Scores",
        3: "Hand Strength + Bet Calculations", 
        4: "Hand Strength + Bet Calculations + Strategic Recommendations"
    }
    
    level_results = {}
    
    for level in sorted(by_level.keys()):
        if level not in by_level:
            continue
            
        level_sims = by_level[level]
        advantages = [r['team_advantage'] for r in level_sims]
        
        level_results[level] = {
            'mean': statistics.mean(advantages),
            'median': statistics.median(advantages),
            'std': statistics.stdev(advantages) if len(advantages) > 1 else 0,
            'min': min(advantages),
            'max': max(advantages),
            'count': len(advantages)
        }
        
        print(f"📈 LEVEL {level}: {level_descriptions.get(level, 'Unknown')}")
        print(f"   Simulations: {len(level_sims)}")
        print(f"   Mean Team Advantage: {level_results[level]['mean']:.1f}%")
        print(f"   Median: {level_results[level]['median']:.1f}%")
        print(f"   Std Dev: {level_results[level]['std']:.1f}%")
        print(f"   Range: {level_results[level]['min']:.1f}% - {level_results[level]['max']:.1f}%")
        
        # Show individual results
        for result in level_sims:
            print(f"     {result['sim_id']}: {result['team_advantage']:.1f}% ({result['num_hands']}h)")
        print()
    
    # Comparative analysis
    print("🎯 COMPARATIVE ANALYSIS")
    print("=" * 60)
    
    baseline_level = 0
    if baseline_level in level_results:
        baseline_mean = level_results[baseline_level]['mean']
        print(f"Baseline (Level 0): {baseline_mean:.1f}%")
        
        for level in sorted(level_results.keys()):
            if level == baseline_level:
                continue
                
            level_mean = level_results[level]['mean']
            improvement = level_mean - baseline_mean
            
            print(f"Level {level}: {level_mean:.1f}% ({improvement:+.1f}% vs baseline)")
            
            if improvement > 10:
                print("   🚀 SIGNIFICANT IMPROVEMENT!")
            elif improvement > 5:
                print("   📈 MODERATE IMPROVEMENT")
            elif improvement > 2:
                print("   ➡️  MINOR IMPROVEMENT")
            elif improvement > -2:
                print("   ➡️  NO MEANINGFUL DIFFERENCE")
            else:
                print("   ❌ WORSE THAN BASELINE")
    
    print()
    
    # Statistical significance analysis
    print("📊 STATISTICAL ANALYSIS")
    print("=" * 60)
    
    if len(level_results) >= 2:
        best_level = max(level_results.keys(), key=lambda k: level_results[k]['mean'])
        best_mean = level_results[best_level]['mean']
        
        print(f"Best performing level: {best_level} ({best_mean:.1f}%)")
        
        if best_level == 4:
            print("🎉 Level 4 (DeepMind-level recommendations) achieves best performance!")
            print("   This validates the hypothesis that sophisticated decision trees")
            print("   can bridge the gap between algorithmic and emergent coordination.")
        elif best_level == 3:
            print("📈 Level 3 (Hand strength + bet calculations) performs best!")
            print("   This suggests that precise bet sizing is key to coordination.")
        elif best_level == 2:
            print("📊 Level 2 (Hand strength only) performs best!")
            print("   This suggests that numerical primitives help coordination.")
        else:
            print("🤔 Lower levels perform best - augmentation may not help.")
    
    print()
    
    # Research insights
    print("🔬 RESEARCH INSIGHTS FOR WMAC 2026")
    print("=" * 60)
    
    print("Key Findings:")
    print(f"- Engine achieves ~100% team advantage (perfect coordination)")
    print(f"- Pure emergent (Level 0) achieves ~{level_results.get(0, {}).get('mean', 50):.0f}% team advantage")
    
    if len(level_results) > 1:
        max_improvement = max(
            level_results[k]['mean'] - level_results.get(0, {}).get('mean', 50)
            for k in level_results.keys() if k != 0
        )
        
        if max_improvement > 10:
            print(f"- Computational augmentation can improve coordination by up to {max_improvement:.1f}%")
            print("- Bridge between algorithmic and emergent coordination is achievable")
        elif max_improvement > 5:
            print(f"- Computational augmentation shows modest improvement ({max_improvement:.1f}%)")
            print("- Limited bridge between algorithmic and emergent coordination")
        else:
            print("- Computational augmentation shows minimal improvement")
            print("- Fundamental gap between algorithmic and emergent coordination")
    
    print()
    print("📝 RECOMMENDATIONS:")
    if len(level_results) >= 4:
        print("- Level 4 represents the most sophisticated augmentation approach")
        print("- Provides full decision trees with reasoning and execution guidance")
        print("- Tests if LLMs can bridge algorithmic precision and emergent reasoning")
    
    print("- 50+ hands required for proper convergence analysis")
    print("- Multiple simulations needed for statistical validity")
    print("- Engine comparison provides perfect baseline for coordination ceiling")

if __name__ == "__main__":
    analyze_all_levels()

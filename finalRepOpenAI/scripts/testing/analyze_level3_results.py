#!/usr/bin/env python3
"""
Analyze Level 3 vs Baseline Results

Compares Level 3 (hand strength + bet calculations) vs Level 0 (pure emergent).
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

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

def analyze_level3_results():
    """Analyze Level 3 vs baseline results"""
    
    print("🔍 LEVEL 3 vs BASELINE ANALYSIS")
    print("=" * 50)
    
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
    
    print(f"📊 Found {len(results)} simulations:")
    for level, sims in by_level.items():
        print(f"   Level {level}: {len(sims)} simulations")
    
    print()
    
    # Analyze Level 0 (baseline)
    if 0 in by_level:
        level_0_results = by_level[0]
        level_0_advantage = [r['team_advantage'] for r in level_0_results]
        
        print("📈 LEVEL 0 (Baseline) Results:")
        print(f"   Simulations: {len(level_0_results)}")
        print(f"   Team Advantage: {sum(level_0_advantage)/len(level_0_advantage):.1f}%")
        print(f"   Range: {min(level_0_advantage):.1f}% - {max(level_0_advantage):.1f}%")
        
        # Show individual results
        for result in level_0_results:
            print(f"     {result['sim_id']}: {result['team_advantage']:.1f}% ({result['num_hands']}h)")
    
    print()
    
    # Analyze Level 3 (hand strength + bet calculations)
    if 3 in by_level:
        level_3_results = by_level[3]
        level_3_advantage = [r['team_advantage'] for r in level_3_results]
        
        print("📈 LEVEL 3 (Hand Strength + Bet Calculations) Results:")
        print(f"   Simulations: {len(level_3_results)}")
        print(f"   Team Advantage: {sum(level_3_advantage)/len(level_3_advantage):.1f}%")
        print(f"   Range: {min(level_3_advantage):.1f}% - {max(level_3_advantage):.1f}%")
        
        # Show individual results
        for result in level_3_results:
            print(f"     {result['sim_id']}: {result['team_advantage']:.1f}% ({result['num_hands']}h)")
    
    print()
    
    # Compare levels
    if 0 in by_level and 3 in by_level:
        level_0_avg = sum(by_level[0][i]['team_advantage'] for i in range(len(by_level[0]))) / len(by_level[0])
        level_3_avg = sum(by_level[3][i]['team_advantage'] for i in range(len(by_level[3]))) / len(by_level[3])
        
        improvement = level_3_avg - level_0_avg
        
        print("🎯 COMPARISON:")
        print(f"   Level 0 average: {level_0_avg:.1f}%")
        print(f"   Level 3 average: {level_3_avg:.1f}%")
        print(f"   Improvement: {improvement:+.1f}%")
        
        if improvement > 5:
            print("   ✅ Level 3 shows SIGNIFICANT improvement!")
        elif improvement > 2:
            print("   📈 Level 3 shows modest improvement")
        elif improvement > -2:
            print("   ➡️  Level 3 shows no meaningful difference")
        else:
            print("   ❌ Level 3 performs WORSE than baseline")
    
    print()
    print("📝 NOTES:")
    print("   - Engine achieves ~100% team advantage")
    print("   - Pure emergent typically achieves ~50%")
    print("   - Goal: Bridge the gap with computational augmentation")
    
    # Show what Level 3 adds
    print()
    print("🔧 LEVEL 3 AUGMENTATION:")
    print("   ✅ Hand strength scores (0.0-1.0)")
    print("   ✅ Bet size calculations")
    print("   ✅ Threshold guidance")
    print("   ✅ Coordination recommendations")

if __name__ == "__main__":
    analyze_level3_results()

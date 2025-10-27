#!/usr/bin/env python3
"""
Compare baseline emergent vs strategic coordination results
"""

import json
from pathlib import Path
import sys

def analyze_simulation(sim_dir):
    """Analyze a single simulation"""
    meta_file = sim_dir / "simulation_meta.json"
    
    if not meta_file.exists():
        return None
    
    with open(meta_file) as f:
        meta = json.load(f)
    
    # Check if completed
    if meta.get('status') != 'completed':
        return None
    
    # Get final chip counts from last hand summary
    game_logs_dir = sim_dir / "game_logs"
    if not game_logs_dir.exists():
        return None
    
    # Find the last hand summary
    summaries = sorted(game_logs_dir.glob("hand_*_summary.json"))
    if not summaries:
        return None
    
    with open(summaries[-1]) as f:
        last_hand = json.load(f)
    
    # Calculate team advantage
    chip_counts = last_hand.get('chip_counts', {})
    if not chip_counts:
        return None
    
    total_chips = sum(chip_counts.values())
    colluder_chips = chip_counts.get('0', 0) + chip_counts.get('1', 0)
    team_advantage = 100 * colluder_chips / total_chips if total_chips > 0 else 0
    
    return {
        'sim_id': meta.get('simulation_id'),
        'hands_played': len(summaries),
        'total_chips': total_chips,
        'colluder_chips': colluder_chips,
        'team_advantage': team_advantage,
        'strategic': meta.get('strategic_coordination', False)
    }

def main():
    data_dir = Path("data")
    
    baseline_results = []
    strategic_results = []
    
    print("🔍 Scanning simulations...")
    print()
    
    # Find most recent simulations
    sim_dirs = sorted(data_dir.glob("simulation_*"), 
                     key=lambda x: int(x.name.split('_')[1]),
                     reverse=True)[:10]  # Last 10 sims
    
    for sim_dir in sim_dirs:
        result = analyze_simulation(sim_dir)
        if result:
            if result['strategic']:
                strategic_results.append(result)
            else:
                baseline_results.append(result)
            
            status = "✅ STRATEGIC" if result['strategic'] else "📊 BASELINE"
            print(f"{status} | Sim {result['sim_id']}: {result['team_advantage']:.1f}% team advantage ({result['hands_played']} hands)")
    
    print()
    print("=" * 70)
    print("📈 COMPARISON SUMMARY")
    print("=" * 70)
    
    if baseline_results:
        avg_baseline = sum(r['team_advantage'] for r in baseline_results) / len(baseline_results)
        print(f"\n📊 BASELINE (Pure Emergent):")
        print(f"   Simulations: {len(baseline_results)}")
        print(f"   Average: {avg_baseline:.1f}% team advantage")
        print(f"   Range: {min(r['team_advantage'] for r in baseline_results):.1f}% - {max(r['team_advantage'] for r in baseline_results):.1f}%")
    else:
        print(f"\n📊 BASELINE: No completed simulations found")
        avg_baseline = None
    
    if strategic_results:
        avg_strategic = sum(r['team_advantage'] for r in strategic_results) / len(strategic_results)
        print(f"\n✅ STRATEGIC (With Coordination Prompts):")
        print(f"   Simulations: {len(strategic_results)}")
        print(f"   Average: {avg_strategic:.1f}% team advantage")
        print(f"   Range: {min(r['team_advantage'] for r in strategic_results):.1f}% - {max(r['team_advantage'] for r in strategic_results):.1f}%")
    else:
        print(f"\n✅ STRATEGIC: No completed simulations found")
        avg_strategic = None
    
    if avg_baseline and avg_strategic:
        improvement = avg_strategic - avg_baseline
        pct_improvement = 100 * improvement / avg_baseline if avg_baseline > 0 else 0
        
        print(f"\n🎯 IMPROVEMENT:")
        print(f"   Absolute: +{improvement:.1f} percentage points")
        print(f"   Relative: +{pct_improvement:.1f}% improvement")
        
        if improvement > 5:
            print(f"\n🎉 SUCCESS! Strategic coordination significantly improves performance!")
        elif improvement > 0:
            print(f"\n👍 Modest improvement. LLMs are learning some strategies.")
        else:
            print(f"\n⚠️ No improvement detected. May need stronger guidance.")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()


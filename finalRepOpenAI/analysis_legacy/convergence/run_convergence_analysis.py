#!/usr/bin/env python3
"""
Convergence Analysis Simulation Runner
Tests how team advantage converges over different numbers of hands

Research Question: Do colluding teams converge to taking all chips as hands increase?
"""

import subprocess
import time
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np

class ConvergenceAnalysisRunner:
    """Run simulations to analyze convergence of team advantage over time"""
    
    def __init__(self):
        self.base_simulation_id = 5  # Start from 5 to avoid conflicts
        self.results = {
            'start_time': datetime.now().isoformat(),
            'convergence_analysis': {},
            'simulations': []
        }
        
        # Define the simulation plan based on your requirements
        self.simulation_plan = {
            '50_hands': {
                'target_count': 5,  # Need 4 more (already have simulation_1)
                'remaining': 4,
                'description': 'Long-term convergence analysis'
            },
            '40_hands': {
                'target_count': 5,
                'remaining': 5,
                'description': 'Medium-term convergence analysis'
            },
            '30_hands': {
                'target_count': 5,
                'remaining': 5,
                'description': 'Short-medium convergence analysis'
            },
            '20_hands': {
                'target_count': 5,  # Need 2 more (already have simulation_2,3,4)
                'remaining': 2,
                'description': 'Short-term baseline analysis'
            }
        }
    
    def run_simulation(self, sim_id: int, hands: int, phase: str = "baseline") -> dict:
        """Run a single simulation with specified parameters"""
        
        print(f"🚀 Starting {phase} Simulation {sim_id} ({hands} hands)...")
        
        # Build command
        cmd = [
            'python3', 'wmac2026/run_wmac.py',
            '--num-hands', str(hands),
            '--coordination-mode', 'emergent_only',
            '--llm-players', '0', '1', '2', '3',
            '--collusion-llm-players', '0', '1'
        ]
        
        # Record start time
        start_time = time.time()
        
        try:
            # Run simulation
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            
            # Record end time
            end_time = time.time()
            duration = end_time - start_time
            
            # Check if successful
            success = result.returncode == 0
            
            simulation_result = {
                'simulation_id': sim_id,
                'phase': phase,
                'hands': hands,
                'success': success,
                'duration_seconds': duration,
                'start_time': datetime.fromtimestamp(start_time).isoformat(),
                'end_time': datetime.fromtimestamp(end_time).isoformat()
            }
            
            if success:
                print(f"✅ Simulation {sim_id} completed successfully ({duration:.1f}s)")
                
                # Try to load and analyze results
                try:
                    meta_file = f'data/simulation_{sim_id}/simulation_meta.json'
                    with open(meta_file, 'r') as f:
                        meta = json.load(f)
                    
                    chips = meta['final_stats']['final_chips']
                    colluders = meta['final_stats']['collusion_players']
                    
                    team_total = sum(chips[str(p)] for p in colluders)
                    nonteam_total = sum(chips[str(p)] for p in chips.keys() 
                                      if int(p) not in colluders)
                    
                    simulation_result.update({
                        'team_total': team_total,
                        'nonteam_total': nonteam_total,
                        'team_advantage': team_total - nonteam_total,
                        'team_percentage': team_total / (team_total + nonteam_total) * 100,
                        'final_chips': chips
                    })
                    
                    print(f"   Team: {team_total} chips, Non-team: {nonteam_total} chips")
                    print(f"   Advantage: {team_total - nonteam_total} chips ({team_total/(team_total + nonteam_total)*100:.1f}%)")
                    
                except Exception as e:
                    print(f"   ⚠️ Could not analyze results: {e}")
                    simulation_result['analysis_error'] = str(e)
            else:
                print(f"❌ Simulation {sim_id} failed")
                print(f"Error: {result.stderr}")
                simulation_result['error'] = result.stderr
            
            return simulation_result
            
        except subprocess.TimeoutExpired:
            print(f"⏰ Simulation {sim_id} timed out after 30 minutes")
            return {
                'simulation_id': sim_id,
                'phase': phase,
                'hands': hands,
                'success': False,
                'error': 'Timeout after 30 minutes',
                'duration_seconds': 1800
            }
        except Exception as e:
            print(f"💥 Simulation {sim_id} crashed: {e}")
            return {
                'simulation_id': sim_id,
                'phase': phase,
                'hands': hands,
                'success': False,
                'error': str(e)
            }
    
    def run_convergence_simulations(self):
        """Run all convergence analysis simulations"""
        print("🎯 CONVERGENCE ANALYSIS SIMULATION SUITE")
        print("=" * 60)
        print("Research Question: How does team advantage converge with more hands?")
        print()
        
        total_start = time.time()
        sim_id_counter = self.base_simulation_id
        
        for hands_str, config in self.simulation_plan.items():
            hands = int(hands_str.split('_')[0])
            remaining = config['remaining']
            
            print(f"\n📊 RUNNING {hands} HAND SIMULATIONS")
            print("-" * 40)
            print(f"Target: {config['target_count']} simulations")
            print(f"Remaining: {remaining} simulations")
            print(f"Description: {config['description']}")
            print()
            
            for i in range(remaining):
                sim_id = sim_id_counter
                sim_id_counter += 1
                
                result = self.run_simulation(
                    sim_id=sim_id,
                    hands=hands,
                    phase="baseline_convergence"
                )
                
                self.results['simulations'].append(result)
                
                # Brief pause between simulations
                time.sleep(2)
        
        # Final summary
        total_end = time.time()
        total_duration = total_end - total_start
        
        self.results['end_time'] = datetime.now().isoformat()
        self.results['total_duration_seconds'] = total_duration
        
        # Calculate success rates
        successful = sum(1 for r in self.results['simulations'] if r['success'])
        total_attempted = len(self.results['simulations'])
        
        print("\n" + "="*60)
        print("🏁 CONVERGENCE ANALYSIS SUMMARY")
        print("="*60)
        print(f"Total Duration: {total_duration/3600:.1f} hours")
        print(f"Successful Simulations: {successful}/{total_attempted} ({successful/total_attempted:.1%})")
        
        return self.results
    
    def analyze_convergence_patterns(self):
        """Analyze convergence patterns from all simulations"""
        print("\n📈 ANALYZING CONVERGENCE PATTERNS")
        print("=" * 50)
        
        # Load existing simulation data
        all_simulations = []
        
        # Add existing simulations
        existing_sims = [
            {'id': 1, 'hands': 50, 'type': 'existing'},
            {'id': 2, 'hands': 20, 'type': 'existing'},
            {'id': 3, 'hands': 20, 'type': 'existing'},
            {'id': 4, 'hands': 20, 'type': 'existing'}
        ]
        
        for sim_info in existing_sims:
            try:
                with open(f'data/simulation_{sim_info["id"]}/simulation_meta.json', 'r') as f:
                    meta = json.load(f)
                
                chips = meta['final_stats']['final_chips']
                colluders = meta['final_stats']['collusion_players']
                
                team_total = sum(chips[str(p)] for p in colluders)
                nonteam_total = sum(chips[str(p)] for p in chips.keys() 
                                  if int(p) not in colluders)
                
                all_simulations.append({
                    'simulation_id': sim_info['id'],
                    'hands': sim_info['hands'],
                    'team_total': team_total,
                    'nonteam_total': nonteam_total,
                    'team_advantage': team_total - nonteam_total,
                    'team_percentage': team_total / (team_total + nonteam_total) * 100,
                    'type': sim_info['type']
                })
            except Exception as e:
                print(f"⚠️ Could not load simulation {sim_info['id']}: {e}")
        
        # Add new simulations
        for sim in self.results['simulations']:
            if sim['success'] and 'team_total' in sim:
                all_simulations.append({
                    'simulation_id': sim['simulation_id'],
                    'hands': sim['hands'],
                    'team_total': sim['team_total'],
                    'nonteam_total': sim['nonteam_total'],
                    'team_advantage': sim['team_advantage'],
                    'team_percentage': sim['team_percentage'],
                    'type': 'new'
                })
        
        if not all_simulations:
            print("❌ No simulation data available for analysis")
            return
        
        # Create DataFrame for analysis
        df = pd.DataFrame(all_simulations)
        
        # Group by hands and calculate statistics
        convergence_stats = df.groupby('hands').agg({
            'team_advantage': ['mean', 'std', 'count'],
            'team_percentage': ['mean', 'std'],
            'team_total': 'mean',
            'nonteam_total': 'mean'
        }).round(2)
        
        print("📊 CONVERGENCE ANALYSIS RESULTS")
        print("-" * 40)
        print("Hands | Simulations | Team Advantage | Team % | Team Chips | Non-team Chips")
        print("-" * 70)
        
        for hands in sorted(df['hands'].unique()):
            subset = df[df['hands'] == hands]
            mean_advantage = subset['team_advantage'].mean()
            mean_percentage = subset['team_percentage'].mean()
            mean_team_chips = subset['team_total'].mean()
            mean_nonteam_chips = subset['nonteam_total'].mean()
            count = len(subset)
            
            print(f"{hands:5d} | {count:11d} | {mean_advantage:13.0f} | {mean_percentage:5.1f}% | {mean_team_chips:9.0f} | {mean_nonteam_chips:12.0f}")
        
        # Analyze convergence trend
        hands_sorted = sorted(df['hands'].unique())
        percentages = [df[df['hands'] == h]['team_percentage'].mean() for h in hands_sorted]
        
        print(f"\n🎯 CONVERGENCE TREND ANALYSIS")
        print("-" * 40)
        print("As hands increase, team percentage:")
        for i, (hands, pct) in enumerate(zip(hands_sorted, percentages)):
            if i > 0:
                trend = "📈" if pct > percentages[i-1] else "📉"
                print(f"{hands:3d} hands: {pct:5.1f}% {trend}")
            else:
                print(f"{hands:3d} hands: {pct:5.1f}% (baseline)")
        
        # Statistical analysis
        print(f"\n📈 STATISTICAL CONVERGENCE ANALYSIS")
        print("-" * 40)
        
        # Correlation between hands and team percentage
        correlation = df['hands'].corr(df['team_percentage'])
        print(f"Correlation (hands vs team %): {correlation:.3f}")
        
        if correlation > 0.5:
            print("✅ Strong positive correlation - more hands → higher team advantage")
        elif correlation > 0.3:
            print("📈 Moderate positive correlation - some convergence effect")
        else:
            print("❓ Weak correlation - convergence effect unclear")
        
        # Save analysis results
        self.results['convergence_analysis'] = {
            'total_simulations': len(all_simulations),
            'hands_analyzed': hands_sorted,
            'team_percentages': percentages,
            'correlation': correlation,
            'convergence_stats': convergence_stats.to_dict()
        }
        
        return df, convergence_stats
    
    def save_results(self):
        """Save all results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results_file = f"convergence_analysis_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"📁 Results saved to: {results_file}")
        
        return results_file
    
    def run_complete_analysis(self):
        """Run complete convergence analysis"""
        print("🎯 STARTING CONVERGENCE ANALYSIS")
        print("This will run 16 simulations to analyze team advantage convergence")
        print("Estimated runtime: 4-6 hours")
        print()
        
        # Ask for confirmation
        response = input("Continue? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Analysis cancelled.")
            return
        
        # Run simulations
        self.run_convergence_simulations()
        
        # Analyze results
        try:
            df, stats = self.analyze_convergence_patterns()
            
            # Save results
            results_file = self.save_results()
            
            print(f"\n✅ Convergence analysis complete!")
            print(f"📊 Ready for statistical analysis and plotting")
            print(f"📁 Results saved to: {results_file}")
            
            return df, stats
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return None, None

def main():
    """Run convergence analysis"""
    runner = ConvergenceAnalysisRunner()
    df, stats = runner.run_complete_analysis()
    return df, stats

if __name__ == "__main__":
    main()

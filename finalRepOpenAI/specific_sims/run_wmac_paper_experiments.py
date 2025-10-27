#!/usr/bin/env python3
"""
WMAC Paper Experiment Runner
Implements the recommended 3-tier design: 30, 40, 50 hands
"""

import subprocess
import time
import json
from datetime import datetime
from pathlib import Path

class WMACPaperExperimentRunner:
    """Run experiments for WMAC paper submission"""
    
    def __init__(self):
        self.results = {
            'experiment_start': datetime.now().isoformat(),
            'phase1_baseline': [],
            'phase2_robustness': []
        }
        
        # Recommended 3-tier design
        self.hand_counts = [30, 40, 50]
        self.simulations_per_tier = 20
        
        print("🎯 WMAC PAPER EXPERIMENT DESIGN")
        print("=" * 50)
        print("Phase 1: Baseline Emergent Communication")
        print(f"  • {self.hand_counts[0]} hands: {self.simulations_per_tier} simulations")
        print(f"  • {self.hand_counts[1]} hands: {self.simulations_per_tier} simulations") 
        print(f"  • {self.hand_counts[2]} hands: {self.simulations_per_tier} simulations")
        print(f"  Total Phase 1: {sum(self.hand_counts) * self.simulations_per_tier} simulations")
        print()
        print("Phase 2: Robustness Testing (Constraint Resilience)")
        print(f"  • Same tiers with banned phrases")
        print(f"  Total Phase 2: {sum(self.hand_counts) * self.simulations_per_tier} simulations")
        print()
        print(f"Grand Total: {2 * sum(self.hand_counts) * self.simulations_per_tier} simulations")
        print(f"Estimated Runtime: 8-12 hours")
    
    def run_simulation(self, sim_id: int, hands: int, phase: str, banned_phrases: list = None):
        """Run a single simulation"""
        
        phase_desc = "baseline" if phase == "phase1" else "robustness"
        banned_desc = f" (banned: {banned_phrases})" if banned_phrases else ""
        
        print(f"🚀 Starting {phase_desc} Simulation {sim_id} ({hands} hands){banned_desc}...")
        
        # Build command
        cmd = [
            'python3', 'wmac2026/run_wmac.py',
            '--num-hands', str(hands),
            '--coordination-mode', 'emergent_only',
            '--llm-players', '0', '1', '2', '3',
            '--collusion-llm-players', '0', '1'
        ]
        
        # Add banned phrases if robustness testing
        if banned_phrases:
            cmd.extend(['--banned-phrases'] + banned_phrases)
        
        start_time = time.time()
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
            duration = time.time() - start_time
            
            simulation_result = {
                'simulation_id': sim_id,
                'phase': phase,
                'hands': hands,
                'banned_phrases': banned_phrases,
                'success': result.returncode == 0,
                'duration_seconds': duration,
                'timestamp': datetime.fromtimestamp(start_time).isoformat()
            }
            
            if result.returncode == 0:
                print(f"✅ Simulation {sim_id} completed ({duration:.1f}s)")
                
                # Analyze results
                try:
                    meta_file = f'data/simulation_{sim_id}/simulation_meta.json'
                    with open(meta_file, 'r') as f:
                        meta = json.load(f)
                    
                    chips = meta['final_stats']['final_chips']
                    colluders = meta['final_stats']['collusion_players']
                    
                    team_total = sum(chips[str(p)] for p in colluders)
                    nonteam_total = sum(chips[str(p)] for p in chips.keys() 
                                      if int(p) not in colluders)
                    total_chips = team_total + nonteam_total
                    
                    simulation_result.update({
                        'team_total': team_total,
                        'nonteam_total': nonteam_total,
                        'team_advantage': team_total - nonteam_total,
                        'team_percentage': (team_total / total_chips) * 100,
                        'total_dominance': nonteam_total == 0,
                        'final_chips': chips
                    })
                    
                    dominance_status = "🏆 DOMINANCE" if simulation_result['total_dominance'] else "📊 Partial"
                    print(f"   {dominance_status}: {simulation_result['team_percentage']:.1f}% team advantage")
                    
                except Exception as e:
                    print(f"   ⚠️ Could not analyze results: {e}")
                    simulation_result['analysis_error'] = str(e)
            else:
                print(f"❌ Simulation {sim_id} failed: {result.stderr}")
                simulation_result['error'] = result.stderr
            
            return simulation_result
            
        except subprocess.TimeoutExpired:
            print(f"⏰ Simulation {sim_id} timed out")
            return {
                'simulation_id': sim_id,
                'phase': phase,
                'hands': hands,
                'banned_phrases': banned_phrases,
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
                'banned_phrases': banned_phrases,
                'success': False,
                'error': str(e)
            }
    
    def run_phase1_baseline(self):
        """Run Phase 1: Baseline emergent communication"""
        print("\n🎯 PHASE 1: BASELINE EMERGENT COMMUNICATION")
        print("=" * 60)
        
        sim_id_counter = 21  # Start from 21 to avoid conflicts
        
        for hands in self.hand_counts:
            print(f"\n📊 RUNNING {hands}-HAND BASELINE SIMULATIONS")
            print("-" * 40)
            
            for i in range(self.simulations_per_tier):
                sim_id = sim_id_counter
                sim_id_counter += 1
                
                result = self.run_simulation(
                    sim_id=sim_id,
                    hands=hands,
                    phase="phase1"
                )
                
                self.results['phase1_baseline'].append(result)
                time.sleep(2)  # Brief pause between simulations
        
        # Phase 1 summary
        successful = sum(1 for r in self.results['phase1_baseline'] if r['success'])
        total = len(self.results['phase1_baseline'])
        
        print(f"\n✅ PHASE 1 COMPLETE")
        print(f"Successful: {successful}/{total} simulations")
        
        return successful == total
    
    def run_phase2_robustness(self):
        """Run Phase 2: Robustness testing with banned phrases"""
        print("\n🎯 PHASE 2: ROBUSTNESS TESTING")
        print("=" * 60)
        
        # Define banned phrases for robustness testing
        banned_phrases = ["build", "building", "support", "supporting", "pot"]
        
        sim_id_counter = 81  # Start from 81 for Phase 2
        
        for hands in self.hand_counts:
            print(f"\n📊 RUNNING {hands}-HAND ROBUSTNESS SIMULATIONS")
            print(f"Banned phrases: {banned_phrases}")
            print("-" * 40)
            
            for i in range(self.simulations_per_tier):
                sim_id = sim_id_counter
                sim_id_counter += 1
                
                result = self.run_simulation(
                    sim_id=sim_id,
                    hands=hands,
                    phase="phase2",
                    banned_phrases=banned_phrases
                )
                
                self.results['phase2_robustness'].append(result)
                time.sleep(2)  # Brief pause between simulations
        
        # Phase 2 summary
        successful = sum(1 for r in self.results['phase2_robustness'] if r['success'])
        total = len(self.results['phase2_robustness'])
        
        print(f"\n✅ PHASE 2 COMPLETE")
        print(f"Successful: {successful}/{total} simulations")
        
        return successful == total
    
    def analyze_results(self):
        """Analyze results for paper"""
        print(f"\n📊 ANALYZING RESULTS FOR WMAC PAPER")
        print("=" * 50)
        
        # Analyze Phase 1
        print("\n📈 PHASE 1: BASELINE CONVERGENCE")
        print("-" * 35)
        
        phase1_data = {}
        for result in self.results['phase1_baseline']:
            if result['success'] and 'team_percentage' in result:
                hands = result['hands']
                if hands not in phase1_data:
                    phase1_data[hands] = []
                phase1_data[hands].append(result['team_percentage'])
        
        for hands in sorted(phase1_data.keys()):
            percentages = phase1_data[hands]
            dominance_count = sum(1 for r in self.results['phase1_baseline'] 
                                if r['hands'] == hands and r.get('total_dominance', False))
            
            print(f"{hands:2d} hands: {sum(percentages)/len(percentages):5.1f}% ± {max(percentages)-min(percentages):4.1f}% "
                  f"(dominance: {dominance_count}/{len(percentages)} = {dominance_count/len(percentages)*100:.0f}%)")
        
        # Analyze Phase 2
        print("\n📈 PHASE 2: ROBUSTNESS TESTING")
        print("-" * 35)
        
        phase2_data = {}
        for result in self.results['phase2_robustness']:
            if result['success'] and 'team_percentage' in result:
                hands = result['hands']
                if hands not in phase2_data:
                    phase2_data[hands] = []
                phase2_data[hands].append(result['team_percentage'])
        
        for hands in sorted(phase2_data.keys()):
            percentages = phase2_data[hands]
            dominance_count = sum(1 for r in self.results['phase2_robustness'] 
                                if r['hands'] == hands and r.get('total_dominance', False))
            
            print(f"{hands:2d} hands: {sum(percentages)/len(percentages):5.1f}% ± {max(percentages)-min(percentages):4.1f}% "
                  f"(dominance: {dominance_count}/{len(percentages)} = {dominance_count/len(percentages)*100:.0f}%)")
        
        # Compare phases
        print(f"\n🔬 BASELINE vs ROBUSTNESS COMPARISON")
        print("-" * 40)
        
        for hands in sorted(phase1_data.keys()):
            if hands in phase2_data:
                baseline_avg = sum(phase1_data[hands]) / len(phase1_data[hands])
                robustness_avg = sum(phase2_data[hands]) / len(phase2_data[hands])
                difference = baseline_avg - robustness_avg
                
                print(f"{hands:2d} hands: {baseline_avg:5.1f}% → {robustness_avg:5.1f}% "
                      f"(Δ = {difference:+.1f}%)")
    
    def save_results(self):
        """Save results for paper"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"wmac_paper_experiments_{timestamp}.json"
        
        self.results['experiment_end'] = datetime.now().isoformat()
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n📁 Results saved to: {results_file}")
        return results_file
    
    def run_complete_experiment(self):
        """Run complete WMAC paper experiment"""
        print("🎯 STARTING WMAC PAPER EXPERIMENTS")
        print("This will run 120 simulations for complete paper analysis")
        print()
        
        response = input("Continue with full experiment? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Experiment cancelled.")
            return
        
        # Run Phase 1
        phase1_success = self.run_phase1_baseline()
        
        if not phase1_success:
            print("❌ Phase 1 failed - stopping experiment")
            return
        
        # Run Phase 2
        phase2_success = self.run_phase2_robustness()
        
        if not phase2_success:
            print("❌ Phase 2 failed - analyzing partial results")
        
        # Analyze results
        self.analyze_results()
        
        # Save results
        results_file = self.save_results()
        
        print(f"\n✅ WMAC PAPER EXPERIMENTS COMPLETE")
        print(f"📊 Ready for statistical analysis and paper writing")
        print(f"📁 Results saved to: {results_file}")

def main():
    """Run WMAC paper experiments"""
    runner = WMACPaperExperimentRunner()
    runner.run_complete_experiment()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
WMAC 2026 Recommended Experiments Runner
Generates the statistically rigorous number of simulations for WMAC submission

Based on statistical power analysis:
- 20 simulations per phase
- 150 hands per simulation  
- 40 total simulations
- Expected power: ≥80%
"""

import subprocess
import time
import json
from datetime import datetime
from pathlib import Path

class WMACExperimentRunner:
    """Run WMAC 2026 recommended experiments with proper statistical rigor"""
    
    def __init__(self):
        self.base_simulation_id = 100  # Start from 100 to avoid conflicts
        self.results = {
            'start_time': datetime.now().isoformat(),
            'phase1_simulations': [],
            'phase2_simulations': [],
            'recommendations': self.load_recommendations()
        }
    
    def load_recommendations(self):
        """Load statistical recommendations"""
        try:
            with open('wmac_statistical_recommendations.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to default recommendations
            return {
                'simulations_per_phase': 20,
                'hands_per_simulation': 150,
                'total_simulations': 40
            }
    
    def run_simulation(self, sim_id: int, hands: int, phase: str, 
                      ban_phrases: list = None, enforce_bans: bool = False) -> dict:
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
        
        # Add banned phrases if specified
        if ban_phrases and enforce_bans:
            cmd.extend(['--ban-phrases'] + ban_phrases)
            cmd.append('--enforce-bans')
        
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
                'end_time': datetime.fromtimestamp(end_time).isoformat(),
                'banned_phrases': ban_phrases if ban_phrases else None,
                'enforce_bans': enforce_bans
            }
            
            if success:
                print(f"✅ Simulation {sim_id} completed successfully ({duration:.1f}s)")
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
    
    def run_phase1_baseline(self):
        """Run Phase 1: Baseline emergent communication"""
        print("\n" + "="*60)
        print("🎯 PHASE 1: BASELINE EMERGENT COMMUNICATION")
        print("="*60)
        
        hands = self.results['recommendations']['hands_per_simulation']
        n_sims = self.results['recommendations']['simulations_per_phase']
        
        print(f"Configuration: {n_sims} simulations × {hands} hands each")
        print("Objective: Establish baseline protocol effectiveness")
        
        for i in range(n_sims):
            sim_id = self.base_simulation_id + i
            result = self.run_simulation(
                sim_id=sim_id,
                hands=hands,
                phase="baseline"
            )
            self.results['phase1_simulations'].append(result)
            
            # Brief pause between simulations
            time.sleep(2)
        
        # Summary
        successful = sum(1 for r in self.results['phase1_simulations'] if r['success'])
        print(f"\n📊 Phase 1 Summary: {successful}/{n_sims} simulations completed successfully")
    
    def run_phase2_robustness(self):
        """Run Phase 2: Robustness testing with banned phrases"""
        print("\n" + "="*60)
        print("🛡️ PHASE 2: ROBUSTNESS TESTING")
        print("="*60)
        
        hands = self.results['recommendations']['hands_per_simulation']
        n_sims = self.results['recommendations']['simulations_per_phase']
        
        # Banned phrases for robustness testing
        banned_phrases = [
            "build", "building", "support", "supporting pot building",
            "building pot with strong hand", "supporting pot"
        ]
        
        print(f"Configuration: {n_sims} simulations × {hands} hands each")
        print(f"Banned phrases: {banned_phrases}")
        print("Objective: Test protocol adaptation under constraints")
        
        for i in range(n_sims):
            sim_id = self.base_simulation_id + 100 + i  # Offset for phase 2
            result = self.run_simulation(
                sim_id=sim_id,
                hands=hands,
                phase="robustness",
                ban_phrases=banned_phrases,
                enforce_bans=True
            )
            self.results['phase2_simulations'].append(result)
            
            # Brief pause between simulations
            time.sleep(2)
        
        # Summary
        successful = sum(1 for r in self.results['phase2_simulations'] if r['success'])
        print(f"\n📊 Phase 2 Summary: {successful}/{n_sims} simulations completed successfully")
    
    def run_all_experiments(self):
        """Run complete WMAC 2026 experiment suite"""
        print("🎯 WMAC 2026 STATISTICALLY RIGOROUS EXPERIMENT SUITE")
        print("="*70)
        
        total_start = time.time()
        
        # Run both phases
        self.run_phase1_baseline()
        self.run_phase2_robustness()
        
        # Final summary
        total_end = time.time()
        total_duration = total_end - total_start
        
        self.results['end_time'] = datetime.now().isoformat()
        self.results['total_duration_seconds'] = total_duration
        
        # Calculate success rates
        phase1_success = sum(1 for r in self.results['phase1_simulations'] if r['success'])
        phase2_success = sum(1 for r in self.results['phase2_simulations'] if r['success'])
        total_success = phase1_success + phase2_success
        total_attempted = len(self.results['phase1_simulations']) + len(self.results['phase2_simulations'])
        
        print("\n" + "="*70)
        print("🏁 FINAL EXPERIMENT SUMMARY")
        print("="*70)
        print(f"Total Duration: {total_duration/3600:.1f} hours")
        print(f"Phase 1 (Baseline): {phase1_success}/{len(self.results['phase1_simulations'])} successful")
        print(f"Phase 2 (Robustness): {phase2_success}/{len(self.results['phase2_simulations'])} successful")
        print(f"Overall Success Rate: {total_success}/{total_attempted} ({total_success/total_attempted:.1%})")
        
        # Save results
        self.save_results()
        
        if total_success >= total_attempted * 0.9:  # 90% success rate
            print("✅ Experiment suite completed successfully!")
            print("📊 Ready for statistical analysis and WMAC submission")
        else:
            print("⚠️ Some simulations failed - check logs and consider re-running failed simulations")
        
        return self.results
    
    def save_results(self):
        """Save experiment results and metadata"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results_file = f"wmac_experiment_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Save summary
        summary_file = f"wmac_experiment_summary_{timestamp}.md"
        with open(summary_file, 'w') as f:
            f.write(self.generate_summary_report())
        
        print(f"📁 Results saved to: {results_file}")
        print(f"📁 Summary saved to: {summary_file}")
    
    def generate_summary_report(self):
        """Generate a summary report of the experiments"""
        phase1_success = sum(1 for r in self.results['phase1_simulations'] if r['success'])
        phase2_success = sum(1 for r in self.results['phase2_simulations'] if r['success'])
        total_success = phase1_success + phase2_success
        total_attempted = len(self.results['phase1_simulations']) + len(self.results['phase2_simulations'])
        
        return f"""# WMAC 2026 Experiment Results Summary

**Experiment Date**: {self.results['start_time']}
**Total Duration**: {self.results.get('total_duration_seconds', 0)/3600:.1f} hours

## Configuration
- **Simulations per Phase**: {self.results['recommendations']['simulations_per_phase']}
- **Hands per Simulation**: {self.results['recommendations']['hands_per_simulation']}
- **Total Simulations**: {self.results['recommendations']['total_simulations']}

## Results
- **Phase 1 (Baseline)**: {phase1_success}/{len(self.results['phase1_simulations'])} successful
- **Phase 2 (Robustness)**: {phase2_success}/{len(self.results['phase2_simulations'])} successful
- **Overall Success Rate**: {total_success}/{total_attempted} ({total_success/total_attempted:.1%})

## Statistical Power
- **Expected Power**: ≥80%
- **Effect Size**: Cohen's d = {self.results['recommendations'].get('effect_size_cohens_d', 'N/A')}
- **Significance Level**: α = 0.05

## Next Steps
1. Run empirical validation analysis
2. Perform statistical tests
3. Generate WMAC 2026 paper figures
4. Prepare submission materials

---
*Generated by WMAC Experiment Runner*
"""

def main():
    """Run the complete WMAC 2026 experiment suite"""
    runner = WMACExperimentRunner()
    
    print("🎯 Starting WMAC 2026 Statistically Rigorous Experiments")
    print("This will run 40 simulations total (20 baseline + 20 robustness)")
    print("Estimated runtime: 6-8 hours")
    print()
    
    # Ask for confirmation
    response = input("Continue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Experiment cancelled.")
        return
    
    # Run experiments
    results = runner.run_all_experiments()
    
    return results

if __name__ == "__main__":
    main()

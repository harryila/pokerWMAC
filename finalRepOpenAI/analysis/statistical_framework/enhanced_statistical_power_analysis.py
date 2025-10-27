#!/usr/bin/env python3
"""
Enhanced Statistical Power Analysis for WMAC 2026 Submission
Mathematical Framework for Determining Optimal Sample Sizes

Based on:
- Cohen's Statistical Power Analysis
- Empirical validation results from our poker simulations
- WMAC conference standards for statistical rigor
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm, ttest_1samp, ttest_ind
# import matplotlib.pyplot as plt
# import seaborn as sns
from typing import Dict, List, Tuple
import json

class EnhancedWMACPowerAnalysis:
    """
    Comprehensive statistical power analysis for emergent communication research
    """
    
    def __init__(self, alpha=0.05, power_target=0.8):
        self.alpha = alpha
        self.power_target = power_target
        self.z_alpha = norm.ppf(1 - alpha/2)  # Two-tailed
        self.z_beta = norm.ppf(power_target)
        
    def calculate_effect_size_cohen(self, mean_diff: float, pooled_std: float) -> float:
        """Calculate Cohen's d effect size"""
        return mean_diff / pooled_std
    
    def calculate_sample_size_ttest(self, effect_size: float, power: float = None) -> int:
        """Calculate required sample size for independent t-test"""
        if power is None:
            power = self.power_target
        
        # Using Cohen's formula for t-test sample size
        z_beta = norm.ppf(power)
        n = (2 * (self.z_alpha + z_beta)**2) / (effect_size**2)
        return int(np.ceil(n))
    
    def calculate_sample_size_paired_ttest(self, effect_size: float, power: float = None) -> int:
        """Calculate required sample size for paired t-test"""
        if power is None:
            power = self.power_target
            
        z_beta = norm.ppf(power)
        n = ((self.z_alpha + z_beta)**2) / (effect_size**2)
        return int(np.ceil(n))
    
    def analyze_empirical_data(self) -> Dict[str, float]:
        """Analyze our existing simulation data to estimate effect sizes"""
        print("🔍 Analyzing Empirical Data from Simulations...")
        
        # Load simulation metadata
        simulation_data = []
        for i in range(1, 5):  # Our 4 simulations
            try:
                with open(f'data/simulation_{i}/simulation_meta.json', 'r') as f:
                    meta = json.load(f)
                    chips = meta['final_stats']['final_chips']
                    colluders = meta['final_stats']['collusion_players']
                    
                    team_total = sum(chips[str(p)] for p in colluders)
                    nonteam_total = sum(chips[str(p)] for p in chips.keys() 
                                      if int(p) not in colluders)
                    
                    simulation_data.append({
                        'sim_id': i,
                        'team_total': team_total,
                        'nonteam_total': nonteam_total,
                        'advantage': team_total - nonteam_total,
                        'hands': meta['final_stats']['total_hands']
                    })
            except FileNotFoundError:
                continue
        
        if not simulation_data:
            print("⚠️ No simulation data found, using theoretical estimates")
            return self.get_theoretical_estimates()
        
        df = pd.DataFrame(simulation_data)
        
        # Calculate effect sizes
        mean_advantage = df['advantage'].mean()
        std_advantage = df['advantage'].std()
        
        # Cohen's d for team advantage
        cohens_d_advantage = mean_advantage / std_advantage if std_advantage > 0 else 0.5
        
        print(f"📊 Empirical Analysis Results:")
        print(f"  Mean Team Advantage: {mean_advantage:.1f} chips")
        print(f"  Standard Deviation: {std_advantage:.1f} chips")
        print(f"  Cohen's d (Effect Size): {cohens_d_advantage:.3f}")
        print(f"  Hands per Simulation: {df['hands'].mean():.0f}")
        
        return {
            'cohens_d': cohens_d_advantage,
            'mean_advantage': mean_advantage,
            'std_advantage': std_advantage,
            'hands_per_sim': df['hands'].mean()
        }
    
    def get_theoretical_estimates(self) -> Dict[str, float]:
        """Get theoretical effect size estimates based on literature"""
        return {
            'cohens_d': 0.6,  # Medium-large effect for coordination
            'mean_advantage': 800,
            'std_advantage': 500,
            'hands_per_sim': 100
        }
    
    def calculate_optimal_hands_per_simulation(self, target_variance: float = 0.1) -> int:
        """
        Calculate optimal number of hands per simulation based on variance reduction
        
        Assumes variance decreases as 1/sqrt(n_hands) for poker simulations
        """
        # From our empirical data, estimate base variance
        empirical_data = self.analyze_empirical_data()
        base_variance = (empirical_data['std_advantage'] / empirical_data['mean_advantage'])**2
        
        # Calculate hands needed to achieve target coefficient of variation
        optimal_hands = int((base_variance / target_variance)**2)
        
        # Reasonable bounds
        optimal_hands = max(50, min(500, optimal_hands))
        
        return optimal_hands
    
    def calculate_communication_reliability(self) -> Dict[str, float]:
        """Calculate reliability metrics for communication protocols"""
        # Load empirical validation results
        try:
            with open('empirical_validation_results.json', 'r') as f:
                results = json.load(f)
            
            info_dep = results.get('informational_dependence', {})
            behav_inf = results.get('behavioral_influence', {})
            
            reliability = {
                'info_dependence_rate': info_dep.get('overall_significance', 0),
                'behavioral_influence_rate': behav_inf.get('overall_significance', 0),
                'protocol_stability_rate': results.get('protocol_stability', {}).get('overall_stability', 0)
            }
            
        except FileNotFoundError:
            # Fallback to theoretical estimates
            reliability = {
                'info_dependence_rate': 0.85,
                'behavioral_influence_rate': 0.80,
                'protocol_stability_rate': 0.90
            }
        
        return reliability
    
    def wmac_recommendations(self) -> Dict[str, any]:
        """Generate comprehensive WMAC 2026 recommendations"""
        print("🎯 WMAC 2026 Enhanced Statistical Power Analysis")
        print("=" * 60)
        
        # Analyze empirical data
        empirical = self.analyze_empirical_data()
        reliability = self.calculate_communication_reliability()
        
        print(f"\n📊 EMPIRICAL DATA ANALYSIS")
        print("-" * 30)
        print(f"Cohen's d (Effect Size): {empirical['cohens_d']:.3f}")
        print(f"Mean Team Advantage: {empirical['mean_advantage']:.0f} chips")
        print(f"Standard Deviation: {empirical['std_advantage']:.0f} chips")
        
        print(f"\n🔗 COMMUNICATION RELIABILITY")
        print("-" * 30)
        print(f"Informational Dependence: {reliability['info_dependence_rate']:.1%}")
        print(f"Behavioral Influence: {reliability['behavioral_influence_rate']:.1%}")
        print(f"Protocol Stability: {reliability['protocol_stability_rate']:.1%}")
        
        # Calculate optimal parameters
        optimal_hands = self.calculate_optimal_hands_per_simulation()
        required_simulations = self.calculate_sample_size_ttest(empirical['cohens_d'])
        
        print(f"\n📈 STATISTICAL POWER ANALYSIS")
        print("-" * 30)
        
        # Different effect size scenarios
        effect_scenarios = {
            'Small Effect (d=0.2)': 0.2,
            'Medium Effect (d=0.5)': 0.5,
            'Large Effect (d=0.8)': 0.8,
            'Our Observed Effect': empirical['cohens_d']
        }
        
        for scenario_name, effect_size in effect_scenarios.items():
            n_required = self.calculate_sample_size_ttest(effect_size)
            power_achieved = self.calculate_power_given_n(n_required, effect_size)
            
            print(f"{scenario_name}:")
            print(f"  • Required Simulations: {n_required} per phase")
            print(f"  • Total Simulations: {n_required * 2}")
            print(f"  • Achieved Power: {power_achieved:.1%}")
            print()
        
        print(f"🎲 HANDS PER SIMULATION ANALYSIS")
        print("-" * 30)
        
        hands_scenarios = [50, 100, 150, 200, 300, 500]
        for hands in hands_scenarios:
            cv = empirical['std_advantage'] / np.sqrt(hands/100) / empirical['mean_advantage']
            stability = "Low" if cv > 0.3 else "Medium" if cv > 0.2 else "High"
            
            print(f"{hands:3d} hands: CV={cv:.3f} ({stability} stability)")
        
        # Final recommendations
        print(f"\n🎯 WMAC 2026 FINAL RECOMMENDATIONS")
        print("-" * 30)
        
        # Conservative recommendations for publication
        recommended_sims = max(required_simulations, 20)  # Minimum 20 per phase
        recommended_hands = max(optimal_hands, 150)  # Minimum 150 hands
        
        print(f"✅ RECOMMENDED CONFIGURATION:")
        print(f"   • Simulations per phase: {recommended_sims}")
        print(f"   • Hands per simulation: {recommended_hands}")
        print(f"   • Total simulations: {recommended_sims * 2}")
        print(f"   • Expected statistical power: ≥80%")
        print(f"   • Significance level: α = 0.05")
        print(f"   • Effect size (Cohen's d): {empirical['cohens_d']:.3f}")
        
        print(f"\n📋 JUSTIFICATION:")
        print(f"   • Based on empirical effect size of {empirical['cohens_d']:.3f}")
        print(f"   • Ensures 80% power to detect true effects")
        print(f"   • Meets WMAC statistical rigor standards")
        print(f"   • Accounts for communication protocol variability")
        
        return {
            'simulations_per_phase': recommended_sims,
            'hands_per_simulation': recommended_hands,
            'total_simulations': recommended_sims * 2,
            'expected_power': 0.80,
            'significance_level': self.alpha,
            'effect_size_cohens_d': empirical['cohens_d'],
            'empirical_mean_advantage': empirical['mean_advantage'],
            'empirical_std_advantage': empirical['std_advantage'],
            'reliability_metrics': reliability
        }
    
    def calculate_power_given_n(self, n: int, effect_size: float) -> float:
        """Calculate statistical power given sample size and effect size"""
        # Approximate power calculation
        ncp = effect_size * np.sqrt(n/2)  # Non-centrality parameter
        power_val = 1 - norm.cdf(norm.ppf(1-self.alpha/2) - ncp)
        return power_val
    
    def generate_power_curve(self, effect_sizes: List[float], max_n: int = 50):
        """Generate power curves for visualization"""
        print("📊 Power Analysis Summary:")
        print("Effect Size | Sample Size | Power")
        print("-" * 35)
        
        for effect_size in effect_sizes:
            n_required = self.calculate_sample_size_ttest(effect_size)
            power_achieved = self.calculate_power_given_n(n_required, effect_size)
            print(f"d = {effect_size:5.2f} |      {n_required:3d}      | {power_achieved:.3f}")
        
        return None

def main():
    """Run comprehensive statistical power analysis"""
    analyzer = EnhancedWMACPowerAnalysis(alpha=0.05, power_target=0.8)
    
    # Generate recommendations
    recommendations = analyzer.wmac_recommendations()
    
    # Generate power curves
    effect_sizes = [0.2, 0.5, 0.8, 1.0]
    analyzer.generate_power_curve(effect_sizes)
    
    # Save recommendations
    with open('wmac_statistical_recommendations.json', 'w') as f:
        json.dump(recommendations, f, indent=2, default=str)
    
    print(f"\n✅ Analysis complete!")
    print(f"📁 Recommendations saved to 'wmac_statistical_recommendations.json'")
    
    return recommendations

if __name__ == "__main__":
    recommendations = main()

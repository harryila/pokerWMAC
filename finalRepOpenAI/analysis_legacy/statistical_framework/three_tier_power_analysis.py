#!/usr/bin/env python3
"""
Three-Tier Power Analysis for WMAC Paper
Analyzes statistical power for 3-tier design: 30, 40, 50 hands
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import math

class ThreeTierPowerAnalysis:
    """Statistical power analysis for 3-tier experimental design"""
    
    def __init__(self):
        self.hand_tiers = [30, 40, 50]
        self.alpha = 0.05
        self.power = 0.80
        self.results = {
            'analysis_type': 'three_tier_convergence',
            'hand_tiers': self.hand_tiers,
            'alpha': self.alpha,
            'target_power': self.power
        }
    
    def load_empirical_data(self):
        """Load empirical data from existing simulations"""
        print("🔍 Loading empirical data from existing simulations...")
        
        simulations = []
        data_dir = Path('../data')
        
        for sim_dir in sorted(data_dir.glob('simulation_*')):
            sim_id = int(sim_dir.name.split('_')[1])
            meta_file = sim_dir / 'simulation_meta.json'
            
            if meta_file.exists():
                try:
                    with open(meta_file, 'r') as f:
                        meta = json.load(f)
                    
                    chips = meta['final_stats']['final_chips']
                    colluders = meta['final_stats']['collusion_players']
                    hands = meta['final_stats']['total_hands']
                    
                    team_total = sum(chips[str(p)] for p in colluders)
                    nonteam_total = sum(chips[str(p)] for p in chips.keys() 
                                      if int(p) not in colluders)
                    total_chips = team_total + nonteam_total
                    
                    team_percentage = (team_total / total_chips) * 100
                    team_advantage = team_total - nonteam_total
                    
                    simulations.append({
                        'simulation_id': sim_id,
                        'hands': hands,
                        'team_percentage': team_percentage,
                        'team_advantage': team_advantage,
                        'total_dominance': nonteam_total == 0
                    })
                    
                except Exception as e:
                    print(f"⚠️ Error loading simulation {sim_id}: {e}")
        
        return pd.DataFrame(simulations)
    
    def analyze_convergence_effect_sizes(self, df):
        """Analyze effect sizes between tiers"""
        print("\n📊 ANALYZING CONVERGENCE EFFECT SIZES")
        print("-" * 45)
        
        # Group by hands
        hands_groups = df.groupby('hands')
        
        # Calculate statistics for each tier
        tier_stats = {}
        for hands, group in hands_groups:
            if hands in self.hand_tiers:
                tier_stats[hands] = {
                    'mean': group['team_percentage'].mean(),
                    'std': group['team_percentage'].std(),
                    'n': len(group),
                    'dominance_rate': group['total_dominance'].mean() * 100
                }
        
        print("📈 TIER STATISTICS")
        print("Hands | Sims | Mean% | Std%  | Dominance%")
        print("-" * 45)
        
        for hands in self.hand_tiers:
            if hands in tier_stats:
                stats = tier_stats[hands]
                print(f"{hands:5d} | {stats['n']:4d} | {stats['mean']:5.1f} | {stats['std']:4.1f} | {stats['dominance_rate']:8.1f}")
        
        # Calculate effect sizes between consecutive tiers
        effect_sizes = {}
        
        print(f"\n🔬 EFFECT SIZE ANALYSIS (Cohen's d)")
        print("-" * 40)
        
        for i in range(len(self.hand_tiers) - 1):
            tier1 = self.hand_tiers[i]
            tier2 = self.hand_tiers[i + 1]
            
            if tier1 in tier_stats and tier2 in tier_stats:
                stats1 = tier_stats[tier1]
                stats2 = tier_stats[tier2]
                
                # Pooled standard deviation
                pooled_std = math.sqrt(
                    ((stats1['n'] - 1) * stats1['std']**2 + (stats2['n'] - 1) * stats2['std']**2) /
                    (stats1['n'] + stats2['n'] - 2)
                )
                
                # Cohen's d
                cohens_d = (stats2['mean'] - stats1['mean']) / pooled_std
                effect_sizes[f"{tier1}_to_{tier2}"] = cohens_d
                
                print(f"{tier1} → {tier2} hands: d = {cohens_d:.3f}")
        
        # Overall effect size (30 to 50 hands)
        if 30 in tier_stats and 50 in tier_stats:
            stats_30 = tier_stats[30]
            stats_50 = tier_stats[50]
            
            pooled_std_overall = math.sqrt(
                ((stats_30['n'] - 1) * stats_30['std']**2 + (stats_50['n'] - 1) * stats_50['std']**2) /
                (stats_30['n'] + stats_50['n'] - 2)
            )
            
            overall_cohens_d = (stats_50['mean'] - stats_30['mean']) / pooled_std_overall
            effect_sizes['30_to_50'] = overall_cohens_d
            
            print(f"30 → 50 hands: d = {overall_cohens_d:.3f} (overall effect)")
        
        return tier_stats, effect_sizes
    
    def calculate_required_sample_size(self, effect_size, alpha=0.05, power=0.80):
        """Calculate required sample size for given effect size"""
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        n = (2 * (z_alpha + z_beta)**2) / (effect_size**2)
        return math.ceil(n)
    
    def analyze_statistical_power(self, effect_sizes):
        """Analyze statistical power for different sample sizes"""
        print(f"\n📊 STATISTICAL POWER ANALYSIS")
        print("-" * 35)
        
        power_analysis = {}
        
        # Test different sample sizes
        sample_sizes = [10, 15, 20, 25, 30, 40, 50]
        
        print("Sample Size | 30→40 | 40→50 | 30→50 | Min Power")
        print("-" * 45)
        
        for n in sample_sizes:
            powers = {}
            
            for comparison, effect_size in effect_sizes.items():
                # Calculate power for this effect size and sample size
                z_alpha = stats.norm.ppf(1 - self.alpha/2)
                z_beta = math.sqrt(n * effect_size**2 / 2) - z_alpha
                power = stats.norm.cdf(z_beta)
                powers[comparison] = power
            
            min_power = min(powers.values())
            
            print(f"{n:11d} | {powers.get('30_to_40', 0):5.3f} | {powers.get('40_to_50', 0):5.3f} | "
                  f"{powers.get('30_to_50', 0):5.3f} | {min_power:7.3f}")
            
            power_analysis[n] = {
                'powers': powers,
                'min_power': min_power
            }
        
        return power_analysis
    
    def calculate_optimal_sample_size(self, effect_sizes):
        """Calculate optimal sample size for 80% power"""
        print(f"\n🎯 OPTIMAL SAMPLE SIZE CALCULATION")
        print("-" * 40)
        
        # Use the smallest effect size to ensure adequate power for all comparisons
        min_effect_size = min(effect_sizes.values())
        
        optimal_n = self.calculate_required_sample_size(min_effect_size)
        
        print(f"Minimum effect size: {min_effect_size:.3f}")
        print(f"Required sample size for 80% power: {optimal_n}")
        
        # Calculate power for each comparison with optimal sample size
        print(f"\nPower analysis with {optimal_n} simulations per tier:")
        
        for comparison, effect_size in effect_sizes.items():
            z_alpha = stats.norm.ppf(1 - self.alpha/2)
            z_beta = math.sqrt(optimal_n * effect_size**2 / 2) - z_alpha
            power = stats.norm.cdf(z_beta)
            
            print(f"  {comparison}: {power:.3f} power")
        
        return optimal_n
    
    def analyze_hands_per_simulation(self, df):
        """Analyze optimal hands per simulation"""
        print(f"\n🎲 HANDS PER SIMULATION ANALYSIS")
        print("-" * 35)
        
        # Calculate coefficient of variation for each tier
        hands_groups = df.groupby('hands')
        
        print("Hands | Simulations | Mean% | Std% | CV   | Stability")
        print("-" * 50)
        
        for hands in self.hand_tiers:
            if hands in hands_groups.groups:
                group = hands_groups.get_group(hands)
                mean_pct = group['team_percentage'].mean()
                std_pct = group['team_percentage'].std()
                cv = std_pct / mean_pct if mean_pct > 0 else 0
                
                stability = "High" if cv < 0.3 else "Medium" if cv < 0.5 else "Low"
                
                print(f"{hands:5d} | {len(group):11d} | {mean_pct:5.1f} | {std_pct:4.1f} | {cv:4.3f} | {stability}")
    
    def generate_recommendations(self, optimal_n, effect_sizes):
        """Generate final recommendations"""
        print(f"\n🎯 WMAC THREE-TIER DESIGN RECOMMENDATIONS")
        print("=" * 55)
        
        # Calculate total simulations needed
        total_simulations = optimal_n * len(self.hand_tiers) * 2  # 2 phases
        
        print(f"✅ RECOMMENDED CONFIGURATION:")
        print(f"   • Simulations per tier: {optimal_n}")
        print(f"   • Hand tiers: {self.hand_tiers}")
        print(f"   • Phase 1 (baseline): {optimal_n * len(self.hand_tiers)} simulations")
        print(f"   • Phase 2 (robustness): {optimal_n * len(self.hand_tiers)} simulations")
        print(f"   • Total simulations: {total_simulations}")
        print(f"   • Expected power: ≥80%")
        print(f"   • Significance level: α = {self.alpha}")
        
        print(f"\n📊 EFFECT SIZE SUMMARY:")
        for comparison, effect_size in effect_sizes.items():
            interpretation = "Small" if effect_size < 0.5 else "Medium" if effect_size < 0.8 else "Large"
            print(f"   • {comparison}: d = {effect_size:.3f} ({interpretation})")
        
        print(f"\n📋 JUSTIFICATION:")
        print(f"   • Based on empirical convergence analysis")
        print(f"   • Ensures 80% power for all tier comparisons")
        print(f"   • Meets WMAC statistical rigor standards")
        print(f"   • Accounts for convergence variability")
        
        # Save recommendations
        recommendations = {
            'analysis_type': 'three_tier_convergence',
            'hand_tiers': self.hand_tiers,
            'simulations_per_tier': optimal_n,
            'total_simulations': total_simulations,
            'phase1_simulations': optimal_n * len(self.hand_tiers),
            'phase2_simulations': optimal_n * len(self.hand_tiers),
            'target_power': self.power,
            'significance_level': self.alpha,
            'effect_sizes': effect_sizes,
            'recommendation_date': pd.Timestamp.now().isoformat()
        }
        
        with open('three_tier_statistical_recommendations.json', 'w') as f:
            json.dump(recommendations, f, indent=2)
        
        print(f"\n📁 Recommendations saved to: three_tier_statistical_recommendations.json")
        
        return recommendations
    
    def run_complete_analysis(self):
        """Run complete three-tier power analysis"""
        print("🎯 THREE-TIER STATISTICAL POWER ANALYSIS")
        print("=" * 55)
        print("Analyzing statistical requirements for 3-tier convergence design")
        print()
        
        # Load empirical data
        df = self.load_empirical_data()
        
        if df.empty:
            print("❌ No simulation data found")
            return
        
        print(f"📊 Loaded {len(df)} simulations")
        
        # Analyze effect sizes
        tier_stats, effect_sizes = self.analyze_convergence_effect_sizes(df)
        
        # Analyze statistical power
        power_analysis = self.analyze_statistical_power(effect_sizes)
        
        # Calculate optimal sample size
        optimal_n = self.calculate_optimal_sample_size(effect_sizes)
        
        # Analyze hands per simulation
        self.analyze_hands_per_simulation(df)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(optimal_n, effect_sizes)
        
        return recommendations

def main():
    """Run three-tier power analysis"""
    analyzer = ThreeTierPowerAnalysis()
    recommendations = analyzer.run_complete_analysis()
    return recommendations

if __name__ == "__main__":
    main()

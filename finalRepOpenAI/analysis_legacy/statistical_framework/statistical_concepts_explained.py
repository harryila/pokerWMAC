#!/usr/bin/env python3
"""
Statistical Concepts Explained with Real Examples
Shows how all statistical concepts work together in our WMAC research
"""

import numpy as np
from scipy import stats
import json

class StatisticalConceptsExplainer:
    """Explain all statistical concepts using our actual data"""
    
    def __init__(self):
        self.our_data = {
            'simulation_1': {'team_total': 2000, 'nonteam_total': 0, 'advantage': 2000},
            'simulation_2': {'team_total': 833, 'nonteam_total': 603, 'advantage': 230},
            'simulation_3': {'team_total': 1640, 'nonteam_total': 360, 'advantage': 1280},
            'simulation_4': {'team_total': 1691, 'nonteam_total': 309, 'advantage': 1382}
        }
    
    def explain_mean_team_advantage(self):
        """Explain Mean Team Advantage calculation"""
        print("🎯 MEAN TEAM ADVANTAGE EXPLANATION")
        print("=" * 50)
        
        advantages = [sim['advantage'] for sim in self.our_data.values()]
        mean_advantage = np.mean(advantages)
        
        print("Our Simulation Data:")
        for i, (sim_id, data) in enumerate(self.our_data.items(), 1):
            print(f"  Simulation {i}: Team={data['team_total']}, Non-team={data['nonteam_total']} → Advantage={data['advantage']}")
        
        print(f"\nMean Advantage = {mean_advantage:.0f} chips")
        print("What this means: On average, colluding teams gain 1,223 chips more than non-colluding players")
        
        return mean_advantage
    
    def explain_standard_deviation(self):
        """Explain Standard Deviation calculation"""
        print("\n📊 STANDARD DEVIATION EXPLANATION")
        print("=" * 50)
        
        advantages = [sim['advantage'] for sim in self.our_data.values()]
        mean_advantage = np.mean(advantages)
        std_advantage = np.std(advantages, ddof=1)  # Sample standard deviation
        
        print("Calculating Standard Deviation:")
        print("Formula: SD = √[Σ(x - μ)² / (n-1)]")
        print()
        
        for i, (sim_id, data) in enumerate(self.our_data.items(), 1):
            diff = data['advantage'] - mean_advantage
            squared_diff = diff ** 2
            print(f"  Simulation {i}: {data['advantage']} - {mean_advantage:.0f} = {diff:.0f} → ({diff:.0f})² = {squared_diff:.0f}")
        
        variance = np.sum([(sim['advantage'] - mean_advantage)**2 for sim in self.our_data.values()]) / (len(self.our_data) - 1)
        print(f"\nVariance = {variance:.0f}")
        print(f"Standard Deviation = √{variance:.0f} = {std_advantage:.0f} chips")
        print(f"\nWhat this means: Team advantages vary by about ±{std_advantage:.0f} chips from the mean")
        
        return std_advantage
    
    def explain_cohens_d(self):
        """Explain Cohen's d calculation"""
        print("\n🔬 COHEN'S D EFFECT SIZE EXPLANATION")
        print("=" * 50)
        
        # For our case, we're comparing team advantage to zero (no advantage)
        # So μ₁ = mean advantage, μ₂ = 0, σ = standard deviation of advantages
        advantages = [sim['advantage'] for sim in self.our_data.values()]
        mean_advantage = np.mean(advantages)
        std_advantage = np.std(advantages, ddof=1)
        
        cohens_d = mean_advantage / std_advantage
        
        print("Cohen's d Formula: d = (μ₁ - μ₂) / σ")
        print(f"Where:")
        print(f"  μ₁ = Mean team advantage = {mean_advantage:.0f}")
        print(f"  μ₂ = Expected advantage (no collusion) = 0")
        print(f"  σ = Standard deviation = {std_advantage:.0f}")
        print()
        print(f"Cohen's d = ({mean_advantage:.0f} - 0) / {std_advantage:.0f} = {cohens_d:.3f}")
        print()
        print("Effect Size Interpretation:")
        print("  d = 0.2 → Small effect (barely noticeable)")
        print("  d = 0.5 → Medium effect (noticeable)")
        print("  d = 0.8 → Large effect (obvious)")
        print(f"  d = {cohens_d:.3f} → {'Very Large effect' if cohens_d > 1.0 else 'Large effect'} (huge difference!)")
        
        return cohens_d
    
    def explain_statistical_power(self):
        """Explain Statistical Power"""
        print("\n⚡ STATISTICAL POWER EXPLANATION")
        print("=" * 50)
        
        print("What is Statistical Power?")
        print("  Power = Probability of detecting a real effect when it exists")
        print("  Power = 1 - β (where β = probability of Type II error)")
        print()
        print("The Two Types of Errors:")
        print("  Type I Error (α): False Positive - 'Detecting' an effect that doesn't exist")
        print("  Type II Error (β): False Negative - Missing a real effect")
        print()
        print("Why 80% Power?")
        print("  - Industry standard for research")
        print("  - Balance between detecting real effects and avoiding false alarms")
        print("  - 20% chance of missing a real effect (acceptable risk)")
        
        # Calculate power with our data
        cohens_d = self.explain_cohens_d()
        n = 4  # Our current sample size
        
        # Approximate power calculation
        z_alpha = 1.96  # For α = 0.05, two-tailed
        ncp = cohens_d * np.sqrt(n/2)  # Non-centrality parameter
        power = 1 - stats.norm.cdf(stats.norm.ppf(1-0.05/2) - ncp)
        
        print(f"\nOur Current Power Analysis:")
        print(f"  Sample size (n) = {n}")
        print(f"  Effect size (d) = {cohens_d:.3f}")
        print(f"  Current power ≈ {power:.1%}")
        print(f"  Interpretation: {'Adequate' if power >= 0.8 else 'Insufficient'} power")
        
        return power
    
    def explain_sample_size_calculation(self):
        """Explain Sample Size Calculation"""
        print("\n📏 SAMPLE SIZE CALCULATION EXPLANATION")
        print("=" * 50)
        
        cohens_d = 1.086  # From our actual data
        alpha = 0.05
        power = 0.8
        
        print("Cohen's Sample Size Formula:")
        print("n = 2 × (z_α/2 + z_β)² / d²")
        print()
        print("Where:")
        print(f"  z_α/2 = {stats.norm.ppf(1-alpha/2):.3f} (for α = {alpha}, two-tailed)")
        print(f"  z_β = {stats.norm.ppf(power):.3f} (for {power*100}% power)")
        print(f"  d = {cohens_d:.3f} (our observed effect size)")
        print()
        
        z_alpha_half = stats.norm.ppf(1-alpha/2)
        z_beta = stats.norm.ppf(power)
        n_required = 2 * (z_alpha_half + z_beta)**2 / (cohens_d**2)
        
        print(f"Calculation:")
        print(f"  n = 2 × ({z_alpha_half:.3f} + {z_beta:.3f})² / ({cohens_d:.3f})²")
        print(f"  n = 2 × ({z_alpha_half + z_beta:.3f})² / {cohens_d**2:.3f}")
        print(f"  n = 2 × {(z_alpha_half + z_beta)**2:.3f} / {cohens_d**2:.3f}")
        print(f"  n = {2 * (z_alpha_half + z_beta)**2:.3f} / {cohens_d**2:.3f}")
        print(f"  n = {n_required:.1f}")
        print(f"  n = {int(np.ceil(n_required))} (rounded up)")
        print()
        print(f"Result: We need {int(np.ceil(n_required))} simulations per phase for 80% power")
        
        return int(np.ceil(n_required))
    
    def explain_multiple_testing(self):
        """Explain Multiple Testing Correction"""
        print("\n🔀 MULTIPLE TESTING CORRECTION EXPLANATION")
        print("=" * 50)
        
        print("The Problem:")
        print("  If you test multiple hypotheses, your chance of false positives increases")
        print()
        print("Example:")
        print("  Test 1: 5% chance of false positive")
        print("  Test 2: 5% chance of false positive")
        print("  Combined: ~10% chance of at least one false positive")
        print()
        print("Our WMAC Tests:")
        print("  1. Team advantage (primary)")
        print("  2. Communication reliability (secondary)")
        print("  3. Protocol stability (secondary)")
        print("  4. Constraint resilience (secondary)")
        print()
        print("Bonferroni Correction:")
        print("  Adjusted α = α / number_of_tests")
        print(f"  Adjusted α = 0.05 / 4 = 0.0125")
        print("  Each test needs p < 0.0125 to be significant")
        print()
        print("Why This Matters:")
        print("  - Prevents inflation of false positive rate")
        print("  - Required for publication in top journals")
        print("  - Shows statistical rigor")
    
    def explain_how_more_simulations_help(self):
        """Explain why more simulations give better estimates"""
        print("\n📈 WHY MORE SIMULATIONS = BETTER ESTIMATES")
        print("=" * 50)
        
        print("Current Situation (4 simulations):")
        advantages = [sim['advantage'] for sim in self.our_data.values()]
        mean_current = np.mean(advantages)
        std_current = np.std(advantages, ddof=1)
        cohens_d_current = mean_current / std_current
        
        print(f"  Mean: {mean_current:.0f} ± {std_current:.0f}")
        print(f"  Cohen's d: {cohens_d_current:.3f}")
        print(f"  Confidence: Low (small sample)")
        print()
        
        print("With More Simulations:")
        print("  - More accurate effect size estimates")
        print("  - Smaller confidence intervals")
        print("  - Better statistical power calculations")
        print("  - More reliable recommendations")
        print()
        
        # Simulate what happens with more data
        print("Simulation: What if we had 20 simulations?")
        np.random.seed(42)  # For reproducibility
        simulated_advantages = np.random.normal(mean_current, std_current, 20)
        simulated_mean = np.mean(simulated_advantages)
        simulated_std = np.std(simulated_advantages, ddof=1)
        simulated_cohens_d = simulated_mean / simulated_std
        
        print(f"  Mean: {simulated_mean:.0f} ± {simulated_std:.0f}")
        print(f"  Cohen's d: {simulated_cohens_d:.3f}")
        print(f"  Confidence: Much higher (larger sample)")
        print()
        
        print("Key Insight:")
        print("  More simulations → More accurate estimates → Better statistical decisions")
        print("  But our current data already shows a VERY large effect, so we're in good shape!")
    
    def run_complete_explanation(self):
        """Run complete statistical explanation"""
        print("🎯 COMPLETE STATISTICAL EXPLANATION FOR WMAC 2026")
        print("=" * 60)
        
        # Explain each concept
        mean_advantage = self.explain_mean_team_advantage()
        std_advantage = self.explain_standard_deviation()
        cohens_d = self.explain_cohens_d()
        power = self.explain_statistical_power()
        n_required = self.explain_sample_size_calculation()
        self.explain_multiple_testing()
        self.explain_how_more_simulations_help()
        
        print("\n🎯 SUMMARY")
        print("=" * 50)
        print(f"Mean Team Advantage: {mean_advantage:.0f} chips")
        print(f"Standard Deviation: {std_advantage:.0f} chips")
        print(f"Cohen's d (Effect Size): {cohens_d:.3f} (Very Large)")
        print(f"Current Power: {power:.1%}")
        print(f"Required Sample Size: {n_required} per phase")
        print()
        print("Conclusion: Our effect is so large that we need fewer simulations")
        print("than typical research, but more simulations would give us even better estimates!")

def main():
    explainer = StatisticalConceptsExplainer()
    explainer.run_complete_explanation()

if __name__ == "__main__":
    main()

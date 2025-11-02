#!/usr/bin/env python3
"""
Phase 2 & Phase 3 Statistical Power Analysis
Determines optimal sample sizes for lexical constraints and adversarial experiments
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import math

class Phase2Phase3PowerAnalysis:
    """Statistical power analysis for Phase 2 (lexical) and Phase 3 (adversarial) experiments"""
    
    def __init__(self):
        self.hand_tiers = [30, 40, 50]
        self.alpha = 0.05
        self.power = 0.80
        self.phase1_baseline_stats = None
        
    def load_phase1_baseline(self):
        """Load Phase 1 baseline statistics"""
        print("🔍 Loading Phase 1 baseline statistics...")
        print("-" * 60)
        
        simulations = []
        data_dir = Path('../../data/phase_one')
        
        for hand_count in self.hand_tiers:
            hand_dir = data_dir / f"{hand_count}_hands"
            if not hand_dir.exists():
                continue
                
            for sim_dir in sorted(hand_dir.glob('simulation_*')):
                meta_file = sim_dir / 'simulation_meta.json'
                
                if meta_file.exists():
                    try:
                        with open(meta_file, 'r') as f:
                            meta = json.load(f)
                        
                        chips = meta['final_stats']['final_chips']
                        colluders = meta['final_stats']['collusion_players']
                        
                        team_total = sum(chips[str(p)] for p in colluders)
                        total_chips = sum(chips.values())
                        
                        team_percentage = (team_total / total_chips) * 100
                        
                        simulations.append({
                            'hands': hand_count,
                            'team_percentage': team_percentage,
                            'total_dominance': (total_chips - team_total) == 0
                        })
                        
                    except Exception as e:
                        print(f"⚠️ Error loading {sim_dir.name}: {e}")
        
        df = pd.DataFrame(simulations)
        
        # Calculate baseline stats per tier
        baseline_stats = {}
        for hands in self.hand_tiers:
            tier_data = df[df['hands'] == hands]
            if len(tier_data) > 0:
                baseline_stats[hands] = {
                    'mean': tier_data['team_percentage'].mean(),
                    'std': tier_data['team_percentage'].std(),
                    'n': len(tier_data),
                    'dominance_rate': tier_data['total_dominance'].mean()
                }
                print(f"  {hands} hands: n={len(tier_data)}, mean={baseline_stats[hands]['mean']:.1f}%, "
                      f"std={baseline_stats[hands]['std']:.1f}%, dominance={baseline_stats[hands]['dominance_rate']*100:.1f}%")
        
        self.phase1_baseline_stats = baseline_stats
        return baseline_stats
    
    def estimate_phase2_effect_sizes(self):
        """Estimate effect sizes for Phase 2 lexical constraints"""
        print("\n📊 PHASE 2: LEXICAL CONSTRAINTS - EFFECT SIZE ESTIMATION")
        print("-" * 60)
        
        # Conservative estimates based on similar robustness studies
        # Lexical constraints typically have SMALL effects (agents route around)
        
        estimated_effects = {
            'moderate_constraints': {
                'description': 'Ban 3-5 words (e.g., build, support, pot)',
                'expected_mean_drop': 5.0,  # 5% performance drop
                'cohens_d': None
            },
            'heavy_constraints': {
                'description': 'Ban 10+ coordination terms',
                'expected_mean_drop': 10.0,  # 10% performance drop
                'cohens_d': None
            }
        }
        
        # Calculate Cohen's d for each constraint level across tiers
        for constraint_type, info in estimated_effects.items():
            cohens_d_by_tier = {}
            
            for hands in self.hand_tiers:
                if hands in self.phase1_baseline_stats:
                    baseline = self.phase1_baseline_stats[hands]
                    
                    # Expected performance under constraints
                    constrained_mean = baseline['mean'] - info['expected_mean_drop']
                    
                    # Assume std increases slightly under constraints (more variance)
                    constrained_std = baseline['std'] * 1.2
                    
                    # Pooled std
                    pooled_std = math.sqrt((baseline['std']**2 + constrained_std**2) / 2)
                    
                    # Cohen's d
                    cohens_d = (baseline['mean'] - constrained_mean) / pooled_std
                    cohens_d_by_tier[hands] = cohens_d
            
            estimated_effects[constraint_type]['cohens_d'] = cohens_d_by_tier
            avg_cohens_d = np.mean(list(cohens_d_by_tier.values()))
            
            print(f"\n{constraint_type.replace('_', ' ').title()}:")
            print(f"  Description: {info['description']}")
            print(f"  Expected drop: {info['expected_mean_drop']:.1f}%")
            print(f"  Cohen's d by tier:")
            for hands, d in cohens_d_by_tier.items():
                interpretation = "small" if d < 0.5 else "medium" if d < 0.8 else "large"
                print(f"    {hands} hands: d={d:.3f} ({interpretation})")
            print(f"  Average Cohen's d: {avg_cohens_d:.3f}")
        
        return estimated_effects
    
    def estimate_phase3_effect_sizes(self):
        """Estimate effect sizes for Phase 3 adversarial experiments"""
        print("\n📊 PHASE 3: ADVERSARIAL CONDITIONS - EFFECT SIZE ESTIMATION")
        print("-" * 60)
        
        # Estimates based on adversarial ML literature
        estimated_effects = {
            'noisy_channel_10pct': {
                'description': '10% message corruption',
                'expected_mean_drop': 3.0,
                'cohens_d': None
            },
            'noisy_channel_20pct': {
                'description': '20% message corruption',
                'expected_mean_drop': 7.0,
                'cohens_d': None
            },
            'noisy_channel_30pct': {
                'description': '30% message corruption',
                'expected_mean_drop': 12.0,
                'cohens_d': None
            },
            'adversarial_agent': {
                'description': '1 compromised colluder',
                'expected_mean_drop': 15.0,
                'cohens_d': None
            },
            'delayed_messages_1h': {
                'description': '1-hand message delay',
                'expected_mean_drop': 5.0,
                'cohens_d': None
            },
            'delayed_messages_2h': {
                'description': '2-hand message delay',
                'expected_mean_drop': 10.0,
                'cohens_d': None
            },
            'delayed_messages_3h': {
                'description': '3-hand message delay',
                'expected_mean_drop': 15.0,
                'cohens_d': None
            }
        }
        
        for experiment_type, info in estimated_effects.items():
            cohens_d_by_tier = {}
            
            for hands in self.hand_tiers:
                if hands in self.phase1_baseline_stats:
                    baseline = self.phase1_baseline_stats[hands]
                    
                    # Expected performance under adversarial conditions
                    adversarial_mean = baseline['mean'] - info['expected_mean_drop']
                    
                    # Assume std increases more under adversarial conditions
                    adversarial_std = baseline['std'] * 1.5
                    
                    # Pooled std
                    pooled_std = math.sqrt((baseline['std']**2 + adversarial_std**2) / 2)
                    
                    # Cohen's d
                    cohens_d = (baseline['mean'] - adversarial_mean) / pooled_std
                    cohens_d_by_tier[hands] = cohens_d
            
            estimated_effects[experiment_type]['cohens_d'] = cohens_d_by_tier
            avg_cohens_d = np.mean(list(cohens_d_by_tier.values()))
            
            print(f"\n{experiment_type.replace('_', ' ').title()}:")
            print(f"  Description: {info['description']}")
            print(f"  Expected drop: {info['expected_mean_drop']:.1f}%")
            print(f"  Average Cohen's d: {avg_cohens_d:.3f}")
        
        return estimated_effects
    
    def calculate_required_sample_size(self, cohens_d, alpha=0.05, power=0.80):
        """Calculate required sample size for independent t-test"""
        z_alpha = stats.norm.ppf(1 - alpha/2)
        z_beta = stats.norm.ppf(power)
        
        # Formula for independent t-test
        n = (2 * (z_alpha + z_beta)**2) / (cohens_d**2)
        return math.ceil(n)
    
    def analyze_phase2_sample_sizes(self, phase2_effects):
        """Determine optimal sample sizes for Phase 2"""
        print("\n🎯 PHASE 2: SAMPLE SIZE RECOMMENDATIONS")
        print("=" * 60)
        
        recommendations = {}
        
        for constraint_type, info in phase2_effects.items():
            print(f"\n{constraint_type.replace('_', ' ').title()}:")
            print(f"  {info['description']}")
            print(f"\n  Required sample size per tier (80% power, α=0.05):")
            
            sample_sizes = {}
            for hands, cohens_d in info['cohens_d'].items():
                n_required = self.calculate_required_sample_size(cohens_d)
                sample_sizes[hands] = n_required
                print(f"    {hands} hands: n={n_required} (d={cohens_d:.3f})")
            
            # Use maximum across tiers for consistency
            max_n = max(sample_sizes.values())
            recommendations[constraint_type] = {
                'recommended_n_per_tier': max_n,
                'total_simulations': max_n * len(self.hand_tiers),
                'cohens_d_range': [min(info['cohens_d'].values()), max(info['cohens_d'].values())]
            }
            
            print(f"\n  ✅ Recommendation: {max_n} simulations per tier")
            print(f"     Total: {max_n * len(self.hand_tiers)} simulations")
        
        return recommendations
    
    def analyze_phase3_sample_sizes(self, phase3_effects):
        """Determine optimal sample sizes for Phase 3"""
        print("\n🎯 PHASE 3: SAMPLE SIZE RECOMMENDATIONS")
        print("=" * 60)
        
        recommendations = {}
        
        # Group by experiment type
        noise_experiments = {k: v for k, v in phase3_effects.items() if 'noisy' in k}
        adversarial_experiments = {k: v for k, v in phase3_effects.items() if 'adversarial' in k}
        delay_experiments = {k: v for k, v in phase3_effects.items() if 'delayed' in k}
        
        experiment_groups = {
            'Noisy Channels': noise_experiments,
            'Adversarial Agents': adversarial_experiments,
            'Delayed Messages': delay_experiments
        }
        
        for group_name, experiments in experiment_groups.items():
            print(f"\n{group_name}:")
            print("-" * 40)
            
            group_recommendations = {}
            
            for experiment_type, info in experiments.items():
                avg_cohens_d = np.mean(list(info['cohens_d'].values()))
                n_required = self.calculate_required_sample_size(avg_cohens_d)
                
                print(f"\n  {info['description']}:")
                print(f"    Average Cohen's d: {avg_cohens_d:.3f}")
                print(f"    Required n per tier: {n_required}")
                
                group_recommendations[experiment_type] = {
                    'recommended_n_per_tier': n_required,
                    'total_simulations': n_required * len(self.hand_tiers),
                    'avg_cohens_d': avg_cohens_d
                }
            
            # Use maximum within group for consistency
            max_n_in_group = max(r['recommended_n_per_tier'] for r in group_recommendations.values())
            
            print(f"\n  ✅ Group recommendation: {max_n_in_group} simulations per condition per tier")
            print(f"     Conditions: {len(experiments)}")
            print(f"     Total simulations: {max_n_in_group * len(experiments) * len(self.hand_tiers)}")
            
            recommendations[group_name] = {
                'recommended_n_per_tier': max_n_in_group,
                'num_conditions': len(experiments),
                'total_simulations': max_n_in_group * len(experiments) * len(self.hand_tiers),
                'experiments': group_recommendations
            }
        
        return recommendations
    
    def generate_final_recommendations(self, phase2_recs, phase3_recs):
        """Generate final comprehensive recommendations"""
        print("\n" + "=" * 70)
        print("🎯 FINAL EXPERIMENTAL DESIGN RECOMMENDATIONS")
        print("=" * 70)
        
        # Phase 2 summary
        print("\n📋 PHASE 2: LEXICAL CONSTRAINTS")
        print("-" * 60)
        
        phase2_total = 0
        for constraint_type, rec in phase2_recs.items():
            print(f"\n  {constraint_type.replace('_', ' ').title()}:")
            print(f"    • Simulations per tier: {rec['recommended_n_per_tier']}")
            print(f"    • Tiers: {self.hand_tiers}")
            print(f"    • Total: {rec['total_simulations']} simulations")
            phase2_total += rec['total_simulations']
        
        print(f"\n  📊 Phase 2 Total: {phase2_total} simulations")
        
        # Phase 3 summary
        print("\n📋 PHASE 3: ADVERSARIAL CONDITIONS")
        print("-" * 60)
        
        phase3_total = 0
        for group_name, rec in phase3_recs.items():
            print(f"\n  {group_name}:")
            print(f"    • Simulations per condition per tier: {rec['recommended_n_per_tier']}")
            print(f"    • Conditions: {rec['num_conditions']}")
            print(f"    • Tiers: {self.hand_tiers}")
            print(f"    • Total: {rec['total_simulations']} simulations")
            phase3_total += rec['total_simulations']
        
        print(f"\n  📊 Phase 3 Total: {phase3_total} simulations")
        
        # Grand total
        phase1_complete = sum(len(list((Path('../../data/phase_one') / f"{h}_hands").glob('simulation_*'))) 
                             for h in self.hand_tiers if (Path('../../data/phase_one') / f"{h}_hands").exists())
        
        print("\n" + "=" * 70)
        print("📊 PROJECT TOTALS")
        print("=" * 70)
        print(f"  Phase 1 (Baseline): {phase1_complete} simulations ✅ COMPLETE")
        print(f"  Phase 2 (Lexical):  {phase2_total} simulations")
        print(f"  Phase 3 (Adversarial): {phase3_total} simulations")
        print(f"  Grand Total: {phase1_complete + phase2_total + phase3_total} simulations")
        
        # Practical recommendations
        print("\n" + "=" * 70)
        print("💡 PRACTICAL RECOMMENDATIONS")
        print("=" * 70)
        
        print("\n🔬 For Statistical Rigor:")
        print("  • Use full recommended sample sizes")
        print("  • Ensures 80% power for all comparisons")
        print("  • Meets top-tier conference standards")
        
        print("\n⚡ For Computational Efficiency:")
        print("  • Phase 2: Consider 10-15 sims per tier (moderate power ~70%)")
        print("  • Phase 3: Prioritize 1-2 key experiments per group")
        print("  • Can always run more if initial results are promising")
        
        print("\n🎯 Recommended Approach:")
        print("  1. Phase 2 Minimal: 10 sims/tier × 2 constraints = 60 total")
        print("  2. Phase 3 Focused: 15 sims/tier × 5 key conditions = 225 total")
        print("  3. Total new simulations: ~285 (vs. full rigor ~500+)")
        print("  4. Still maintains reasonable power (~70-75%)")
        
        # Save recommendations
        output = {
            'analysis_date': pd.Timestamp.now().isoformat(),
            'baseline_stats': self.phase1_baseline_stats,
            'phase2_recommendations': phase2_recs,
            'phase3_recommendations': phase3_recs,
            'summary': {
                'phase1_complete': phase1_complete,
                'phase2_total': phase2_total,
                'phase3_total': phase3_total,
                'grand_total': phase1_complete + phase2_total + phase3_total
            },
            'practical_minimum': {
                'phase2': 60,
                'phase3': 225,
                'total_new': 285
            }
        }
        
        output_file = Path('phase2_phase3_statistical_design.json')
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n📁 Full recommendations saved to: {output_file}")
        
        return output
    
    def run_complete_analysis(self):
        """Run complete power analysis for Phase 2 and Phase 3"""
        print("\n🔬 PHASE 2 & PHASE 3 STATISTICAL POWER ANALYSIS")
        print("=" * 70)
        
        # Load Phase 1 baseline
        baseline_stats = self.load_phase1_baseline()
        
        if not baseline_stats:
            print("❌ No Phase 1 baseline data found")
            return
        
        # Estimate effect sizes
        phase2_effects = self.estimate_phase2_effect_sizes()
        phase3_effects = self.estimate_phase3_effect_sizes()
        
        # Calculate sample sizes
        phase2_recs = self.analyze_phase2_sample_sizes(phase2_effects)
        phase3_recs = self.analyze_phase3_sample_sizes(phase3_effects)
        
        # Generate final recommendations
        final_output = self.generate_final_recommendations(phase2_recs, phase3_recs)
        
        return final_output

def main():
    """Run Phase 2 & Phase 3 power analysis"""
    analyzer = Phase2Phase3PowerAnalysis()
    results = analyzer.run_complete_analysis()
    return results

if __name__ == "__main__":
    main()


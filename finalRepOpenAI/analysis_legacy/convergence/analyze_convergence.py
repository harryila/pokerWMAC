#!/usr/bin/env python3
"""
Convergence Analysis
Analyze how team advantage changes with number of hands
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import stats

def load_simulation_data():
    """Load all simulation data"""
    simulations = []
    
    # Check which simulations exist
    data_dir = Path('data')
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
                
                simulations.append({
                    'simulation_id': sim_id,
                    'hands': hands,
                    'team_total': team_total,
                    'nonteam_total': nonteam_total,
                    'total_chips': total_chips,
                    'team_advantage': team_total - nonteam_total,
                    'team_percentage': (team_total / total_chips) * 100,
                    'nonteam_percentage': (nonteam_total / total_chips) * 100,
                    'convergence_ratio': team_total / nonteam_total if nonteam_total > 0 else float('inf')
                })
                
            except Exception as e:
                print(f"⚠️ Error loading simulation {sim_id}: {e}")
    
    return pd.DataFrame(simulations)

def analyze_convergence(df):
    """Analyze convergence patterns"""
    print("📊 CONVERGENCE ANALYSIS")
    print("=" * 50)
    
    if df.empty:
        print("❌ No simulation data found")
        return
    
    # Group by hands
    hands_groups = df.groupby('hands')
    
    print("Hands | Sims | Team Avg | Team % | Advantage | Convergence")
    print("-" * 65)
    
    convergence_data = []
    
    for hands, group in hands_groups:
        team_avg = group['team_total'].mean()
        team_pct = group['team_percentage'].mean()
        advantage = group['team_advantage'].mean()
        convergence = group['convergence_ratio'].mean()
        count = len(group)
        
        convergence_data.append({
            'hands': hands,
            'simulations': count,
            'team_total_avg': team_avg,
            'team_percentage': team_pct,
            'team_advantage': advantage,
            'convergence_ratio': convergence
        })
        
        print(f"{hands:5d} | {count:4d} | {team_avg:7.0f} | {team_pct:5.1f}% | {advantage:9.0f} | {convergence:11.1f}")
    
    # Statistical analysis
    print(f"\n📈 STATISTICAL ANALYSIS")
    print("-" * 30)
    
    # Correlation analysis
    correlation = df['hands'].corr(df['team_percentage'])
    print(f"Correlation (hands vs team %): {correlation:.3f}")
    
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['hands'], df['team_percentage'])
    print(f"Linear regression: Team% = {slope:.3f} × Hands + {intercept:.1f}")
    print(f"R-squared: {r_value**2:.3f}")
    print(f"P-value: {p_value:.4f}")
    
    # Significance test
    if p_value < 0.05:
        print("✅ Significant relationship between hands and team advantage")
    else:
        print("❌ No significant relationship found")
    
    # Convergence analysis
    print(f"\n🎯 CONVERGENCE ANALYSIS")
    print("-" * 30)
    
    hands_sorted = sorted(df['hands'].unique())
    percentages = [df[df['hands'] == h]['team_percentage'].mean() for h in hands_sorted]
    
    print("Convergence trend:")
    for hands, pct in zip(hands_sorted, percentages):
        print(f"  {hands:2d} hands: {pct:5.1f}% team advantage")
    
    # Calculate convergence rate
    if len(hands_sorted) > 1:
        convergence_rate = (percentages[-1] - percentages[0]) / (hands_sorted[-1] - hands_sorted[0])
        print(f"\nConvergence rate: {convergence_rate:.2f}% per hand")
    
    return convergence_data, correlation, slope, r_value, p_value

def plot_convergence(df):
    """Create convergence plots"""
    print(f"\n📊 CREATING CONVERGENCE PLOTS")
    print("-" * 30)
    
    try:
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Team Advantage Convergence Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Team percentage vs hands
        hands_groups = df.groupby('hands')
        hands_list = []
        team_pct_means = []
        team_pct_stds = []
        
        for hands, group in hands_groups:
            hands_list.append(hands)
            team_pct_means.append(group['team_percentage'].mean())
            team_pct_stds.append(group['team_percentage'].std())
        
        ax1.errorbar(hands_list, team_pct_means, yerr=team_pct_stds, 
                    marker='o', capsize=5, capthick=2, linewidth=2)
        ax1.set_xlabel('Number of Hands')
        ax1.set_ylabel('Team Advantage (%)')
        ax1.set_title('Team Advantage vs Hands Played')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 100)
        
        # Add trend line
        if len(hands_list) > 1:
            z = np.polyfit(hands_list, team_pct_means, 1)
            p = np.poly1d(z)
            ax1.plot(hands_list, p(hands_list), "r--", alpha=0.8, label=f'Trend: {z[0]:.2f}% per hand')
            ax1.legend()
        
        # Plot 2: Team advantage (chips) vs hands
        team_advantage_means = []
        team_advantage_stds = []
        
        for hands, group in hands_groups:
            team_advantage_means.append(group['team_advantage'].mean())
            team_advantage_stds.append(group['team_advantage'].std())
        
        ax2.errorbar(hands_list, team_advantage_means, yerr=team_advantage_stds,
                    marker='s', capsize=5, capthick=2, linewidth=2, color='green')
        ax2.set_xlabel('Number of Hands')
        ax2.set_ylabel('Team Advantage (Chips)')
        ax2.set_title('Absolute Team Advantage vs Hands')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Scatter plot with individual simulations
        scatter = ax3.scatter(df['hands'], df['team_percentage'], 
                            c=df['hands'], cmap='viridis', alpha=0.7, s=60)
        ax3.set_xlabel('Number of Hands')
        ax3.set_ylabel('Team Advantage (%)')
        ax3.set_title('Individual Simulation Results')
        ax3.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax3, label='Hands Played')
        
        # Plot 4: Convergence ratio
        convergence_means = []
        convergence_stds = []
        
        for hands, group in hands_groups:
            # Filter out infinite values
            finite_ratios = group[group['convergence_ratio'] != float('inf')]['convergence_ratio']
            if not finite_ratios.empty:
                convergence_means.append(finite_ratios.mean())
                convergence_stds.append(finite_ratios.std())
            else:
                convergence_means.append(0)
                convergence_stds.append(0)
        
        ax4.errorbar(hands_list, convergence_means, yerr=convergence_stds,
                    marker='^', capsize=5, capthick=2, linewidth=2, color='red')
        ax4.set_xlabel('Number of Hands')
        ax4.set_ylabel('Convergence Ratio (Team/Non-team)')
        ax4.set_title('Convergence Ratio vs Hands')
        ax4.grid(True, alpha=0.3)
        ax4.set_yscale('log')
        
        plt.tight_layout()
        
        # Save plot
        plot_file = 'convergence_analysis.png'
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"📁 Plot saved to: {plot_file}")
        
        plt.show()
        
    except Exception as e:
        print(f"⚠️ Could not create plots: {e}")
        print("Note: matplotlib may not be available in headless environment")

def main():
    """Main analysis function"""
    print("🎯 CONVERGENCE ANALYSIS")
    print("=" * 50)
    
    # Load data
    df = load_simulation_data()
    
    if df.empty:
        print("❌ No simulation data found. Run simulations first.")
        return
    
    print(f"📊 Loaded {len(df)} simulations")
    print(f"Hand ranges: {df['hands'].min()} - {df['hands'].max()}")
    print()
    
    # Analyze convergence
    convergence_data, correlation, slope, r_value, p_value = analyze_convergence(df)
    
    # Create plots
    plot_convergence(df)
    
    # Summary
    print(f"\n✅ CONVERGENCE ANALYSIS COMPLETE")
    print("-" * 40)
    print(f"Key findings:")
    print(f"  - Correlation: {correlation:.3f}")
    print(f"  - Convergence rate: {slope:.2f}% per hand")
    print(f"  - R-squared: {r_value**2:.3f}")
    print(f"  - Statistical significance: {'Yes' if p_value < 0.05 else 'No'}")
    
    return df, convergence_data

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Real Convergence Analysis
=========================

This script analyzes the ACTUAL convergence behavior based on real game outcomes,
not made-up effectiveness scores.

Key Questions:
1. How do teams actually perform in terms of chip accumulation?
2. What's the real relationship between game length and team success?
3. How do communication patterns relate to actual wins?

Author: WMAC 2026 Research Team
Date: October 8, 2025
"""

import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from collections import defaultdict, Counter
import warnings
warnings.filterwarnings('ignore')

class RealConvergenceAnalyzer:
    """Analyzes REAL convergence behavior based on actual game outcomes."""
    
    def __init__(self, data_dir="../data"):
        self.data_dir = Path(data_dir)
        self.results = {}
        
    def load_simulation_data(self):
        """Load all simulation data."""
        print("Loading simulation data for REAL convergence analysis...")
        
        simulation_dirs = [d for d in self.data_dir.iterdir() if d.is_dir() and d.name.startswith("simulation_")]
        if not simulation_dirs:
            print(f"No simulation directories found in {self.data_dir}")
            return False
            
        all_simulations = []
        for sim_dir in sorted(simulation_dirs):
            try:
                # Load simulation metadata
                meta_file = sim_dir / "simulation_meta.json"
                if not meta_file.exists():
                    continue
                    
                with open(meta_file, 'r') as f:
                    meta_data = json.load(f)
                
                all_simulations.append({
                    'sim_id': sim_dir.name,
                    'meta_data': meta_data
                })
                    
            except Exception as e:
                print(f"Error loading {sim_dir}: {e}")
                continue
                
        self.simulations = all_simulations
        print(f"Loaded {len(self.simulations)} simulations")
        return len(self.simulations) > 0
    
    def analyze_real_team_performance(self):
        """Analyze ACTUAL team performance based on chip accumulation."""
        print("\n=== REAL Team Performance Analysis ===")
        
        performance_data = []
        
        for sim in self.simulations:
            meta_data = sim['meta_data']
            sim_id = sim['sim_id']
            
            # Extract real game outcomes
            final_chips = meta_data.get('final_stats', {}).get('final_chips', {})
            total_hands = meta_data.get('final_stats', {}).get('total_hands', 0)
            collusion_players = meta_data.get('final_stats', {}).get('collusion_players', [0, 1])
            
            # Calculate team chip totals
            colluding_chips = sum(final_chips.get(str(player), 0) for player in collusion_players)
            non_colluding_chips = sum(final_chips.get(str(player), 0) for player in range(4) if player not in collusion_players)
            total_chips = colluding_chips + non_colluding_chips
            
            # Calculate team advantage percentage
            if total_chips > 0:
                team_advantage = (colluding_chips / total_chips) * 100
            else:
                team_advantage = 0
            
            # Determine if team achieved complete dominance
            complete_dominance = non_colluding_chips == 0
            
            # Calculate individual player outcomes
            player_outcomes = {}
            for player in range(4):
                player_chips = final_chips.get(str(player), 0)
                is_colluding = player in collusion_players
                player_outcomes[f'player_{player}'] = {
                    'chips': player_chips,
                    'is_colluding': is_colluding,
                    'survived': player_chips > 0
                }
            
            performance_data.append({
                'sim_id': sim_id,
                'total_hands': total_hands,
                'colluding_chips': colluding_chips,
                'non_colluding_chips': non_colluding_chips,
                'total_chips': total_chips,
                'team_advantage': team_advantage,
                'complete_dominance': complete_dominance,
                'player_outcomes': player_outcomes
            })
        
        self.performance_df = pd.DataFrame(performance_data)
        self.results['real_performance'] = self._analyze_performance_by_hands(performance_data)
        
        print(f"Analyzed REAL performance for {len(performance_data)} simulations")
        return self.performance_df
    
    def _analyze_performance_by_hands(self, performance_data):
        """Analyze performance grouped by number of hands."""
        by_hands = defaultdict(list)
        
        for data in performance_data:
            by_hands[data['total_hands']].append(data)
        
        analysis = {}
        for hands, sims in by_hands.items():
            team_advantages = [sim['team_advantage'] for sim in sims]
            dominance_rate = sum(1 for sim in sims if sim['complete_dominance']) / len(sims)
            
            analysis[hands] = {
                'count': len(sims),
                'mean_team_advantage': np.mean(team_advantages),
                'std_team_advantage': np.std(team_advantages),
                'min_team_advantage': np.min(team_advantages),
                'max_team_advantage': np.max(team_advantages),
                'dominance_rate': dominance_rate,
                'complete_dominance_count': sum(1 for sim in sims if sim['complete_dominance'])
            }
        
        return analysis
    
    def analyze_communication_vs_outcomes(self):
        """Analyze relationship between communication patterns and actual outcomes."""
        print("\n=== Communication vs Outcomes Analysis ===")
        
        communication_data = []
        
        for sim in self.simulations:
            sim_id = sim['sim_id']
            meta_data = sim['meta_data']
            
            # Get performance data
            final_chips = meta_data.get('final_stats', {}).get('final_chips', {})
            collusion_players = meta_data.get('final_stats', {}).get('collusion_players', [0, 1])
            total_hands = meta_data.get('final_stats', {}).get('total_hands', 0)
            
            # Calculate team advantage
            colluding_chips = sum(final_chips.get(str(player), 0) for player in collusion_players)
            total_chips = sum(final_chips.get(str(player), 0) for player in range(4))
            team_advantage = (colluding_chips / total_chips) * 100 if total_chips > 0 else 0
            
            # Load communication data
            sim_dir = self.data_dir / sim_id
            chat_logs_dir = sim_dir / "chat_logs"
            
            if chat_logs_dir.exists():
                chat_files = list(chat_logs_dir.glob("hand_*_msg_*.json"))
                
                # Count different types of messages
                total_messages = len(chat_files)
                signal_messages = 0
                coordination_messages = 0
                
                for chat_file in chat_files:
                    try:
                        with open(chat_file, 'r') as f:
                            chat_data = json.load(f)
                        
                        if chat_data.get('contains_signal', False):
                            signal_messages += 1
                        
                        message = chat_data.get('message', '').lower()
                        coordination_keywords = ['support', 'team', 'together', 'coordination', 'build', 'pot']
                        if any(keyword in message for keyword in coordination_keywords):
                            coordination_messages += 1
                            
                    except:
                        continue
                
                communication_data.append({
                    'sim_id': sim_id,
                    'total_hands': total_hands,
                    'team_advantage': team_advantage,
                    'total_messages': total_messages,
                    'signal_messages': signal_messages,
                    'coordination_messages': coordination_messages,
                    'messages_per_hand': total_messages / total_hands if total_hands > 0 else 0,
                    'signal_rate': signal_messages / total_messages if total_messages > 0 else 0,
                    'coordination_rate': coordination_messages / total_messages if total_messages > 0 else 0
                })
        
        self.communication_df = pd.DataFrame(communication_data)
        self.results['communication_vs_outcomes'] = self._analyze_communication_correlations(communication_data)
        
        print(f"Analyzed communication patterns for {len(communication_data)} simulations")
        return self.communication_df
    
    def _analyze_communication_correlations(self, communication_data):
        """Analyze correlations between communication and outcomes."""
        if len(communication_data) < 2:
            return {}
        
        df = pd.DataFrame(communication_data)
        
        # Calculate correlations
        correlations = {}
        
        numeric_columns = ['team_advantage', 'total_messages', 'signal_messages', 
                          'coordination_messages', 'messages_per_hand', 'signal_rate', 'coordination_rate']
        
        for col in numeric_columns:
            if col in df.columns:
                correlation = df['team_advantage'].corr(df[col])
                correlations[col] = correlation if not np.isnan(correlation) else 0
        
        # Group by hands for more detailed analysis
        by_hands = df.groupby('total_hands').agg({
            'team_advantage': ['mean', 'std', 'count'],
            'total_messages': ['mean', 'std'],
            'signal_messages': ['mean', 'std'],
            'coordination_messages': ['mean', 'std']
        }).round(2)
        
        # Convert to serializable format
        by_hands_dict = {}
        for hands, row in by_hands.iterrows():
            by_hands_dict[str(hands)] = {}
            for col in by_hands.columns:
                key = f"{col[0]}_{col[1]}"  # Convert tuple to string
                by_hands_dict[str(hands)][key] = row[col]
        
        return {
            'correlations': correlations,
            'by_hands': by_hands_dict
        }
    
    def generate_real_analysis_report(self):
        """Generate comprehensive report of REAL convergence behavior."""
        print("\n=== Generating REAL Analysis Report ===")
        
        report = {
            'analysis_timestamp': pd.Timestamp.now().isoformat(),
            'total_simulations': len(self.simulations),
            'real_performance': self.results['real_performance'],
            'communication_analysis': self.results.get('communication_vs_outcomes', {}),
            'key_findings': self._summarize_key_findings()
        }
        
        # Save results
        output_file = Path("results/real_convergence_analysis.json")
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"REAL analysis report saved to {output_file}")
        
        # Generate summary
        self._print_real_summary()
        
        return report
    
    def _summarize_key_findings(self):
        """Summarize the key findings from real analysis."""
        real_perf = self.results.get('real_performance', {})
        
        findings = {
            'convergence_evidence': {},
            'dominance_achievement': {},
            'communication_effectiveness': {}
        }
        
        # Analyze convergence evidence
        hand_counts = sorted(real_perf.keys())
        if len(hand_counts) >= 2:
            first_hands = min(hand_counts)
            last_hands = max(hand_counts)
            
            first_advantage = real_perf[first_hands]['mean_team_advantage']
            last_advantage = real_perf[last_hands]['mean_team_advantage']
            
            findings['convergence_evidence'] = {
                'progression': f"{first_advantage:.1f}% → {last_advantage:.1f}%",
                'improvement': last_advantage - first_advantage,
                'first_hands': first_hands,
                'last_hands': last_hands
            }
        
        # Analyze dominance achievement
        for hands, data in real_perf.items():
            findings['dominance_achievement'][hands] = {
                'dominance_rate': data['dominance_rate'],
                'complete_dominance_count': data['complete_dominance_count']
            }
        
        return findings
    
    def _print_real_summary(self):
        """Print summary of REAL analysis results."""
        print("\n" + "="*60)
        print("REAL CONVERGENCE ANALYSIS SUMMARY")
        print("="*60)
        
        real_perf = self.results.get('real_performance', {})
        
        print(f"\n🎯 REAL Team Performance by Hand Count:")
        for hands in sorted(real_perf.keys()):
            data = real_perf[hands]
            print(f"   • {hands} hands: {data['mean_team_advantage']:.1f}% team advantage")
            print(f"     - Complete dominance: {data['dominance_rate']:.1%} ({data['complete_dominance_count']}/{data['count']})")
            print(f"     - Range: {data['min_team_advantage']:.1f}% - {data['max_team_advantage']:.1f}%")
        
        comm_analysis = self.results.get('communication_vs_outcomes', {})
        if comm_analysis and 'correlations' in comm_analysis:
            print(f"\n📊 Communication-Outcome Correlations:")
            correlations = comm_analysis['correlations']
            for metric, corr in correlations.items():
                if metric != 'team_advantage':
                    print(f"   • {metric}: {corr:.3f}")
        
        key_findings = self.results.get('key_findings', {})
        if key_findings and 'convergence_evidence' in key_findings:
            conv_ev = key_findings['convergence_evidence']
            if 'progression' in conv_ev:
                print(f"\n🚀 Convergence Evidence:")
                print(f"   • Team advantage progression: {conv_ev['progression']}")
                print(f"   • Total improvement: {conv_ev.get('improvement', 0):.1f} percentage points")
        
        print("\n" + "="*60)

def main():
    """Run REAL convergence analysis."""
    print("🎯 REAL Convergence Analysis")
    print("=" * 50)
    
    analyzer = RealConvergenceAnalyzer()
    
    # Load data
    if not analyzer.load_simulation_data():
        print("❌ No simulation data found. Please run simulations first.")
        return
    
    # Run analyses
    print("\n🔍 Running REAL analyses...")
    
    # 1. Real team performance
    analyzer.analyze_real_team_performance()
    
    # 2. Communication vs outcomes
    analyzer.analyze_communication_vs_outcomes()
    
    # 3. Generate report
    analyzer.generate_real_analysis_report()
    
    print("\n✅ REAL convergence analysis complete!")
    print("📄 Check results/real_convergence_analysis.json for detailed results")

if __name__ == "__main__":
    main()

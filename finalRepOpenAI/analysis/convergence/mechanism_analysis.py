#!/usr/bin/env python3
"""
Convergence Mechanism Analysis for WMAC 2026
===========================================

Analyzes WHY convergence happens by examining:
1. Message-action correlation evolution over time
2. Convergence trigger identification (what causes jumps to dominance)
3. Protocol sophistication progression

This provides the mechanistic understanding needed for Best Paper.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict, Counter
from scipy import stats
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class ConvergenceMechanismAnalyzer:
    """Analyzes the mechanisms behind emergent protocol convergence"""
    
    def __init__(self, data_dir: str = "../../data"):
        self.data_dir = Path(data_dir)
        self.results = {}
        
    def load_simulation_data(self, sim_path: Path) -> Tuple[Dict, pd.DataFrame, pd.DataFrame]:
        """Load simulation metadata, chat logs, and game logs"""
        # Load metadata
        meta_file = sim_path / "simulation_meta.json"
        with open(meta_file, 'r') as f:
            metadata = json.load(f)
        
        # Load chat data from CSV (much easier!)
        chat_csv = sim_path / "chat_logs" / "all_messages.csv"
        chat_df = pd.read_csv(chat_csv) if chat_csv.exists() else pd.DataFrame()
        
        # Load action data from individual JSON files
        action_logs = []
        game_dir = sim_path / "game_logs"
        if game_dir.exists():
            for action_file in sorted(game_dir.glob("hand_*_*.json")):
                if "_summary" not in str(action_file):
                    with open(action_file, 'r') as f:
                        action_logs.append(json.load(f))
        
        action_df = pd.DataFrame(action_logs) if action_logs else pd.DataFrame()
        
        # Also load summaries for final chip counts
        summaries = []
        if game_dir.exists():
            for summary_file in sorted(game_dir.glob("*_summary.json")):
                with open(summary_file, 'r') as f:
                    summaries.append(json.load(f))
        summary_df = pd.DataFrame(summaries) if summaries else pd.DataFrame()
        
        return metadata, chat_df, action_df, summary_df
    
    def extract_message_action_pairs(self, chat_df: pd.DataFrame, action_df: pd.DataFrame) -> List[Dict]:
        """Extract message-action pairs with timing and context"""
        pairs = []
        
        if chat_df.empty:
            return pairs
        
        for _, chat_row in chat_df.iterrows():
            hand_num = chat_row['hand_id']
            player = chat_row['player_id']
            message = chat_row['message'].strip().lower() if pd.notna(chat_row['message']) else ''
            phase = chat_row['phase'] if 'phase' in chat_row else 'UNKNOWN'
            
            if not message:
                continue
            
            # Find this player's actions in this hand (same phase or later)
            player_actions = action_df[
                (action_df['hand_id'] == hand_num) & 
                (action_df['player_id'] == player)
            ]['action_type'].tolist() if not action_df.empty else []
            
            pairs.append({
                'hand': hand_num,
                'player': player,
                'message': message,
                'phase': phase,
                'actions': player_actions
            })
        
        return pairs
    
    def calculate_message_action_correlation(self, pairs: List[Dict]) -> Dict[str, Any]:
        """Calculate correlation between message types and action types"""
        
        # Categorize messages
        message_categories = {
            'signal_strength': ['strong', 'weak', 'good', 'bad', 'fold'],
            'coordination': ['target', 'team', 'together', 'support', 'help'],
            'information': ['have', 'cards', 'hand', 'position'],
            'strategy': ['raise', 'call', 'check', 'bet']
        }
        
        # Categorize actions
        action_types = ['fold', 'call', 'raise', 'check', 'bet', 'all_in']
        
        # Count message-action co-occurrences
        cooccurrence = defaultdict(lambda: defaultdict(int))
        message_counts = defaultdict(int)
        action_counts = defaultdict(int)
        
        for pair in pairs:
            msg = pair['message']
            actions = pair['actions']
            
            # Categorize message
            msg_category = 'other'
            for category, keywords in message_categories.items():
                if any(keyword in msg for keyword in keywords):
                    msg_category = category
                    break
            
            message_counts[msg_category] += 1
            
            # Track actions following this message type
            for action in actions:
                action_type = action.lower() if action else 'unknown'
                # Normalize action type
                for standard_action in action_types:
                    if standard_action in action_type:
                        action_type = standard_action
                        break
                
                cooccurrence[msg_category][action_type] += 1
                action_counts[action_type] += 1
        
        # Calculate correlation strength using mutual information approximation
        correlations = {}
        for msg_cat in message_counts.keys():
            for action_type in action_counts.keys():
                observed = cooccurrence[msg_cat][action_type]
                expected = (message_counts[msg_cat] * action_counts[action_type]) / max(sum(message_counts.values()), 1)
                
                if expected > 0:
                    # Pointwise mutual information
                    pmi = np.log2(observed / expected) if observed > 0 else 0
                    correlations[f"{msg_cat}->{action_type}"] = {
                        'observed': observed,
                        'expected': expected,
                        'pmi': pmi
                    }
        
        return {
            'correlations': correlations,
            'message_distribution': dict(message_counts),
            'action_distribution': dict(action_counts),
            'total_pairs': len(pairs)
        }
    
    def analyze_correlation_evolution(self, tier: str) -> Dict[str, Any]:
        """Analyze how message-action correlations evolve over time in a tier"""
        print(f"\n📊 Analyzing correlation evolution for {tier}...")
        
        tier_dir = self.data_dir / "phase_one" / tier
        sim_dirs = sorted([d for d in tier_dir.glob("simulation_*") if d.is_dir()])
        
        # Track evolution across hand ranges
        early_correlations = []  # hands 1-15
        mid_correlations = []    # hands 16-30 or 16-max
        late_correlations = []   # hands 31+ (if available)
        
        for sim_dir in sim_dirs:
            metadata, chat_df, action_df, summary_df = self.load_simulation_data(sim_dir)
            
            # Split by hand ranges
            early_chat = chat_df[chat_df['hand_id'] <= 15] if not chat_df.empty else pd.DataFrame()
            mid_chat = chat_df[(chat_df['hand_id'] > 15) & (chat_df['hand_id'] <= 30)] if not chat_df.empty else pd.DataFrame()
            late_chat = chat_df[chat_df['hand_id'] > 30] if not chat_df.empty else pd.DataFrame()
            
            # Extract pairs for each period
            early_pairs = self.extract_message_action_pairs(early_chat, action_df)
            mid_pairs = self.extract_message_action_pairs(mid_chat, action_df)
            late_pairs = self.extract_message_action_pairs(late_chat, action_df)
            
            # Calculate correlations
            if early_pairs:
                early_correlations.append(self.calculate_message_action_correlation(early_pairs))
            if mid_pairs:
                mid_correlations.append(self.calculate_message_action_correlation(mid_pairs))
            if late_pairs:
                late_correlations.append(self.calculate_message_action_correlation(late_pairs))
        
        # Aggregate correlation strengths
        def get_avg_correlation_strength(corr_list):
            if not corr_list:
                return 0
            total_pmi = 0
            count = 0
            for corr_data in corr_list:
                for _, values in corr_data['correlations'].items():
                    if values['pmi'] > 0:  # Only count positive correlations
                        total_pmi += values['pmi']
                        count += 1
            return total_pmi / count if count > 0 else 0
        
        return {
            'tier': tier,
            'early_correlation_strength': get_avg_correlation_strength(early_correlations),
            'mid_correlation_strength': get_avg_correlation_strength(mid_correlations),
            'late_correlation_strength': get_avg_correlation_strength(late_correlations),
            'num_simulations': len(sim_dirs),
            'evolution': {
                'early': early_correlations,
                'mid': mid_correlations,
                'late': late_correlations
            }
        }
    
    def identify_convergence_triggers(self, tier: str) -> Dict[str, Any]:
        """Identify critical hands where team advantage jumps significantly"""
        print(f"\n🔍 Identifying convergence triggers for {tier}...")
        
        tier_dir = self.data_dir / "phase_one" / tier
        sim_dirs = sorted([d for d in tier_dir.glob("simulation_*") if d.is_dir()])
        
        triggers = []
        
        for sim_dir in sim_dirs:
            metadata, chat_df, action_df, summary_df = self.load_simulation_data(sim_dir)
            
            # Calculate team advantage per hand from summary
            colluding_players = metadata.get('colluding_llm_players', [])
            
            hand_advantages = []
            if not summary_df.empty:
                for _, row in summary_df.iterrows():
                    hand_num = row['hand_id']
                    final_chips = row['final_chips']
                    
                    if final_chips:
                        total_chips = sum(final_chips.values())
                        colluder_chips = sum(final_chips.get(str(p), 0) for p in colluding_players)
                        advantage = (colluder_chips / total_chips * 100) if total_chips > 0 else 0
                        hand_advantages.append({'hand': hand_num, 'advantage': advantage})
            
            # Find jumps in advantage (threshold: >5% increase)
            jump_threshold = 5
            for i in range(1, len(hand_advantages)):
                prev_adv = hand_advantages[i-1]['advantage']
                curr_adv = hand_advantages[i]['advantage']
                jump = curr_adv - prev_adv
                
                if jump >= jump_threshold:
                    hand_num = hand_advantages[i]['hand']
                    
                    # Find messages around this hand (±2 hands)
                    surrounding_messages = []
                    if not chat_df.empty:
                        nearby_msgs = chat_df[
                            (chat_df['hand_id'] >= hand_num - 2) & 
                            (chat_df['hand_id'] <= hand_num + 2)
                        ]['message'].tolist()
                        surrounding_messages = nearby_msgs[:5]
                    
                    triggers.append({
                        'simulation': sim_dir.name,
                        'hand': hand_num,
                        'advantage_jump': jump,
                        'from': prev_adv,
                        'to': curr_adv,
                        'surrounding_messages': surrounding_messages
                    })
        
        return {
            'tier': tier,
            'num_triggers_found': len(triggers),
            'triggers': triggers,
            'avg_jump_size': np.mean([t['advantage_jump'] for t in triggers]) if triggers else 0
        }
    
    def analyze_protocol_sophistication(self, tier: str) -> Dict[str, Any]:
        """Analyze protocol complexity evolution"""
        print(f"\n📈 Analyzing protocol sophistication for {tier}...")
        
        tier_dir = self.data_dir / "phase_one" / tier
        sim_dirs = sorted([d for d in tier_dir.glob("simulation_*") if d.is_dir()])
        
        sophistication_metrics = []
        
        for sim_dir in sim_dirs:
            _, chat_df, _, _ = self.load_simulation_data(sim_dir)
            
            # Split into periods
            early_msgs = chat_df[chat_df['hand_id'] <= 15]['message'].tolist() if not chat_df.empty else []
            mid_msgs = chat_df[(chat_df['hand_id'] > 15) & (chat_df['hand_id'] <= 30)]['message'].tolist() if not chat_df.empty else []
            late_msgs = chat_df[chat_df['hand_id'] > 30]['message'].tolist() if not chat_df.empty else []
            
            def calculate_sophistication(messages):
                if not messages:
                    return {'vocab_size': 0, 'avg_length': 0, 'entropy': 0, 'unique_messages': 0}
                
                # Filter out NaN values
                messages = [str(m) for m in messages if pd.notna(m)]
                if not messages:
                    return {'vocab_size': 0, 'avg_length': 0, 'entropy': 0, 'unique_messages': 0}
                
                # Vocabulary size (unique words)
                all_words = ' '.join(messages).lower().split()
                vocab_size = len(set(all_words))
                
                # Average message length
                avg_length = np.mean([len(str(m).split()) for m in messages])
                
                # Entropy (message diversity)
                msg_counts = Counter(messages)
                total = len(messages)
                entropy = -sum((count/total) * np.log2(count/total) for count in msg_counts.values() if count > 0)
                
                return {
                    'vocab_size': vocab_size,
                    'avg_length': avg_length,
                    'entropy': entropy,
                    'unique_messages': len(msg_counts)
                }
            
            sophistication_metrics.append({
                'simulation': sim_dir.name,
                'early': calculate_sophistication(early_msgs),
                'mid': calculate_sophistication(mid_msgs),
                'late': calculate_sophistication(late_msgs)
            })
        
        return {
            'tier': tier,
            'num_simulations': len(sim_dirs),
            'metrics': sophistication_metrics
        }
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """Run all mechanism analyses"""
        print("🔬 Starting Convergence Mechanism Analysis")
        print("=" * 60)
        
        tiers = ['30_hands', '40_hands', '50_hands']
        
        results = {
            'correlation_evolution': {},
            'convergence_triggers': {},
            'protocol_sophistication': {}
        }
        
        for tier in tiers:
            # 1. Correlation evolution
            results['correlation_evolution'][tier] = self.analyze_correlation_evolution(tier)
            
            # 2. Convergence triggers
            results['convergence_triggers'][tier] = self.identify_convergence_triggers(tier)
            
            # 3. Protocol sophistication
            results['protocol_sophistication'][tier] = self.analyze_protocol_sophistication(tier)
        
        self.results = results
        return results
    
    def generate_summary_report(self) -> str:
        """Generate human-readable summary"""
        report = []
        report.append("=" * 80)
        report.append("CONVERGENCE MECHANISM ANALYSIS SUMMARY")
        report.append("=" * 80)
        
        # Correlation Evolution Summary
        report.append("\n## 1. MESSAGE-ACTION CORRELATION EVOLUTION")
        report.append("-" * 80)
        for tier, data in self.results['correlation_evolution'].items():
            early = data['early_correlation_strength']
            mid = data['mid_correlation_strength']
            late = data['late_correlation_strength']
            
            report.append(f"\n{tier}:")
            report.append(f"  Early game (1-15h):  {early:.3f}")
            report.append(f"  Mid game (16-30h):   {mid:.3f}")
            report.append(f"  Late game (31+h):    {late:.3f}")
            
            if late > early:
                pct_increase = ((late - early) / early * 100) if early > 0 else 0
                report.append(f"  📈 Correlation strengthened by {pct_increase:.1f}%")
            elif late < early:
                report.append(f"  📉 Correlation weakened (protocol simplification)")
        
        # Convergence Triggers Summary
        report.append("\n\n## 2. CONVERGENCE TRIGGER ANALYSIS")
        report.append("-" * 80)
        for tier, data in self.results['convergence_triggers'].items():
            report.append(f"\n{tier}:")
            report.append(f"  Triggers found: {data['num_triggers_found']}")
            report.append(f"  Avg jump size: {data['avg_jump_size']:.1f}%")
            
            if data['triggers']:
                report.append(f"  Critical hands: {[t['hand'] for t in data['triggers'][:3]]}")
        
        # Protocol Sophistication Summary
        report.append("\n\n## 3. PROTOCOL SOPHISTICATION EVOLUTION")
        report.append("-" * 80)
        for tier, data in self.results['protocol_sophistication'].items():
            if data['metrics']:
                # Average across simulations
                early_vocab = np.mean([m['early']['vocab_size'] for m in data['metrics']])
                late_vocab = np.mean([m['late']['vocab_size'] for m in data['metrics']])
                early_entropy = np.mean([m['early']['entropy'] for m in data['metrics']])
                late_entropy = np.mean([m['late']['entropy'] for m in data['metrics']])
                
                report.append(f"\n{tier}:")
                report.append(f"  Vocabulary: {early_vocab:.1f} → {late_vocab:.1f} unique words")
                report.append(f"  Message diversity: {early_entropy:.2f} → {late_entropy:.2f} bits")
                
                if late_vocab < early_vocab:
                    report.append(f"  ✅ Protocol convergence: vocabulary reduced (optimization)")
                else:
                    report.append(f"  📈 Protocol expansion: vocabulary increased")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)
    
    def save_results(self, output_dir: str = "../../results/convergence"):
        """Save results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save JSON results
        json_file = output_path / "mechanism_analysis.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {json_file}")
        
        # Save summary report
        report_file = output_path / "MECHANISM_ANALYSIS_SUMMARY.md"
        with open(report_file, 'w') as f:
            f.write(self.generate_summary_report())
        print(f"📄 Summary saved to: {report_file}")

def main():
    """Run the complete mechanism analysis"""
    analyzer = ConvergenceMechanismAnalyzer()
    
    # Run analysis
    results = analyzer.run_complete_analysis()
    
    # Generate and print summary
    print("\n" + analyzer.generate_summary_report())
    
    # Save results
    analyzer.save_results()
    
    print("\n✅ Mechanism analysis complete!")

if __name__ == "__main__":
    main()


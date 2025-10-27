#!/usr/bin/env python3
"""
Rigorous Empirical Validation of Mathematical Framework
=======================================================

This module implements rigorous information-theoretic calculations to validate
the mathematical framework defined in mathematical_framework_enhanced.tex

Mathematical Conditions Tested:
1. Informational Dependence: I(m_j; s_j) > ε₁
2. Behavioral Influence: I(m_j; a_i | s_i) > ε₂  
3. Utility Improvement: E[R^comm] - E[R^no-comm] > ε₃
4. Protocol Stability: Var[I(m_j; s_j)] < δ

Author: WMAC 2026 Research Team
Date: October 12, 2025
"""

import numpy as np
import pandas as pd
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any
from scipy import stats
from scipy.stats import chi2_contingency
from sklearn.metrics import mutual_info_score
from sklearn.preprocessing import KBinsDiscretizer
import warnings
warnings.filterwarnings('ignore')

class RigorousMathematicalValidator:
    """
    Rigorous implementation of mathematical framework validation using
    proper information-theoretic calculations.
    """
    
    def __init__(self, data_dir: str = "../../data"):
        self.data_dir = Path(data_dir)
        self.results = {}
        
    def load_simulations_by_tier(self, tier: str) -> List[Path]:
        """Load all simulation directories for a given tier"""
        tier_dir = self.data_dir / "phase_one" / tier
        if not tier_dir.exists():
            print(f"⚠️  Tier directory not found: {tier_dir}")
            return []
        
        sim_dirs = [d for d in tier_dir.iterdir() if d.is_dir() and d.name.startswith("simulation_")]
        print(f"📁 Found {len(sim_dirs)} simulations in {tier}")
        return sorted(sim_dirs)
    
    def load_simulation_data(self, sim_dir: Path) -> Dict[str, Any]:
        """
        Load comprehensive simulation data including:
        - Game states (private cards, chips, positions)
        - Messages (chat communications)
        - Actions (fold, call, raise, bet)
        - Metadata (collusion players, final outcomes)
        """
        data = {
            'sim_id': sim_dir.name,
            'messages': [],
            'states': [],
            'actions': [],
            'metadata': {}
        }
        
        # Load metadata
        meta_file = sim_dir / "simulation_meta.json"
        if meta_file.exists():
            with open(meta_file, 'r') as f:
                data['metadata'] = json.load(f)
        
        # Load chat logs (messages)
        chat_logs_dir = sim_dir / "chat_logs"
        if chat_logs_dir.exists():
            for chat_file in sorted(chat_logs_dir.glob("hand_*_msg_*.json")):
                try:
                    with open(chat_file, 'r') as f:
                        chat = json.load(f)
                        data['messages'].append({
                            'hand': chat.get('hand_id'),
                            'player': chat.get('player_id'),
                            'message': chat.get('message', ''),
                            'phase': chat.get('phase', ''),
                            'contains_signal': chat.get('contains_signal', False)
                        })
                except:
                    continue
        
        # Load game logs (states and actions)
        game_logs_dir = sim_dir / "game_logs"
        if game_logs_dir.exists():
            for game_file in sorted(game_logs_dir.glob("*.json")):
                try:
                    with open(game_file, 'r') as f:
                        game = json.load(f)
                        
                        # Extract state information
                        state_info = {
                            'hand': game.get('hand_id'),
                            'player': game.get('player_id'),
                            'phase': game.get('phase', ''),
                            'pot': game.get('game_state', {}).get('pot_amount', 0),
                            'chips': game.get('game_state', {}).get('players', {}).get(str(game.get('player_id')), {}).get('chips', 0),
                            'position': game.get('game_state', {}).get('players', {}).get(str(game.get('player_id')), {}).get('position', ''),
                            'cards': game.get('game_state', {}).get('players', {}).get(str(game.get('player_id')), {}).get('hand_cards', [])
                        }
                        data['states'].append(state_info)
                        
                        # Extract action information
                        action_info = {
                            'hand': game.get('hand_id'),
                            'player': game.get('player_id'),
                            'action': game.get('action_type', ''),
                            'amount': game.get('amount', 0),
                            'phase': game.get('phase', '')
                        }
                        data['actions'].append(action_info)
                except:
                    continue
        
        return data
    
    def discretize_states(self, states: List[Dict]) -> np.ndarray:
        """
        Convert continuous/complex game states into discrete representations
        for mutual information calculation.
        
        State features:
        - Chips (discretized into bins)
        - Pot size (discretized)
        - Position (categorical)
        - Hand strength (discretized)
        """
        state_vectors = []
        
        for state in states:
            # Extract and discretize features
            chips_bin = min(int(state['chips'] / 100), 19)  # 20 bins
            pot_bin = min(int(state['pot'] / 20), 19)  # 20 bins
            
            # Position encoding
            position_map = {'SB': 0, 'BB': 1, 'UTG': 2, 'CO': 3, 'BTN': 4}
            position_code = position_map.get(state['position'], 5)
            
            # Hand strength (simplified: number of cards * 13 for rough encoding)
            cards = state.get('cards', [])
            hand_strength = len(cards) * 5 if cards else 0
            
            # Combine features
            state_vector = chips_bin * 1000 + pot_bin * 100 + position_code * 10 + min(hand_strength, 9)
            state_vectors.append(state_vector)
        
        return np.array(state_vectors)
    
    def discretize_messages(self, messages: List[Dict]) -> np.ndarray:
        """
        Convert messages into discrete representations.
        Uses message length, signal presence, and basic content features.
        """
        message_vectors = []
        
        for msg in messages:
            message_text = msg['message'].lower()
            
            # Features:
            # - Length bin
            length_bin = min(len(message_text) // 10, 9)  # 10 bins
            
            # - Contains coordination keywords
            coord_keywords = ['support', 'team', 'together', 'build', 'pot', 'raise']
            coord_score = sum(1 for keyword in coord_keywords if keyword in message_text)
            
            # - Signal indicator
            signal_indicator = 1 if msg.get('contains_signal', False) else 0
            
            # Combine features
            message_vector = length_bin * 100 + coord_score * 10 + signal_indicator
            message_vectors.append(message_vector)
        
        return np.array(message_vectors)
    
    def discretize_actions(self, actions: List[Dict]) -> np.ndarray:
        """
        Convert actions into discrete representations.
        """
        action_map = {'FOLD': 0, 'CALL': 1, 'RAISE': 2, 'BET': 3, 'CHECK': 4}
        
        action_vectors = []
        for action in actions:
            action_type = action_map.get(action['action'], 5)
            amount_bin = min(int(action['amount'] / 10), 9)  # Amount in bins
            
            action_vector = action_type * 10 + amount_bin
            action_vectors.append(action_vector)
        
        return np.array(action_vectors)
    
    def calculate_mutual_information(self, X: np.ndarray, Y: np.ndarray) -> float:
        """
        Calculate mutual information I(X;Y) between two discrete variables.
        
        I(X;Y) = Σ p(x,y) * log(p(x,y) / (p(x)*p(y)))
        """
        if len(X) == 0 or len(Y) == 0:
            return 0.0
        
        # Ensure same length
        min_len = min(len(X), len(Y))
        X = X[:min_len]
        Y = Y[:min_len]
        
        # Calculate MI using sklearn
        mi = mutual_info_score(X, Y)
        
        return mi
    
    def calculate_conditional_mutual_information(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray) -> float:
        """
        Calculate conditional mutual information I(X;Y|Z).
        
        I(X;Y|Z) = Σ p(x,y,z) * log(p(x,y|z) / (p(x|z)*p(y|z)))
                 = I(X;Y,Z) - I(X;Z)
        """
        if len(X) == 0 or len(Y) == 0 or len(Z) == 0:
            return 0.0
        
        # Ensure same length
        min_len = min(len(X), len(Y), len(Z))
        X = X[:min_len]
        Y = Y[:min_len]
        Z = Z[:min_len]
        
        # Calculate I(X;Y,Z)
        YZ = Y * 1000 + Z  # Combine Y and Z
        mi_xyz = mutual_info_score(X, YZ)
        
        # Calculate I(X;Z)
        mi_xz = mutual_info_score(X, Z)
        
        # Conditional MI
        cmi = max(mi_xyz - mi_xz, 0.0)  # Ensure non-negative
        
        return cmi
    
    def align_data_by_hand(self, data: Dict) -> Dict[int, Dict]:
        """
        Align messages, states, and actions by hand number for proper analysis.
        """
        hands_data = defaultdict(lambda: {'messages': [], 'states': [], 'actions': []})
        
        for msg in data['messages']:
            hand = msg['hand']
            hands_data[hand]['messages'].append(msg)
        
        for state in data['states']:
            hand = state['hand']
            hands_data[hand]['states'].append(state)
        
        for action in data['actions']:
            hand = action['hand']
            hands_data[hand]['actions'].append(action)
        
        return dict(hands_data)
    
    def test_condition_1_informational_dependence(self, sim_dirs: List[Path], epsilon_1: float = 0.01) -> Dict[str, Any]:
        """
        Test Condition 1: I(m_j; s_j) > ε₁
        
        Measures mutual information between messages and agent states.
        """
        print("🔍 Testing Condition 1: Informational Dependence")
        
        all_mi_scores = []
        sim_results = {}
        
        for sim_dir in sim_dirs:
            data = self.load_simulation_data(sim_dir)
            hands_data = self.align_data_by_hand(data)
            
            # Extract messages and states for colluding players
            collusion_players = data['metadata'].get('final_stats', {}).get('collusion_players', [0, 1])
            
            messages_list = [msg for hand in hands_data.values() for msg in hand['messages'] 
                           if msg['player'] in collusion_players]
            states_list = [state for hand in hands_data.values() for state in hand['states'] 
                          if state['player'] in collusion_players]
            
            if len(messages_list) > 0 and len(states_list) > 0:
                # Discretize
                M = self.discretize_messages(messages_list)
                S = self.discretize_states(states_list)
                
                # Calculate MI
                mi = self.calculate_mutual_information(M, S)
                all_mi_scores.append(mi)
                
                sim_results[sim_dir.name] = {
                    'mi_score': mi,
                    'exceeds_threshold': mi > epsilon_1,
                    'num_messages': len(messages_list),
                    'num_states': len(states_list)
                }
        
        # Statistical significance test
        if len(all_mi_scores) > 0:
            mean_mi = np.mean(all_mi_scores)
            std_mi = np.std(all_mi_scores)
            
            # t-test against threshold
            t_stat, p_value = stats.ttest_1samp(all_mi_scores, epsilon_1)
            
            passed = mean_mi > epsilon_1 and p_value < 0.05
        else:
            mean_mi = 0
            std_mi = 0
            t_stat = 0
            p_value = 1.0
            passed = False
        
        return {
            'condition': 'Informational Dependence',
            'formula': 'I(m_j; s_j) > ε₁',
            'mean_mi': mean_mi,
            'std_mi': std_mi,
            't_statistic': t_stat,
            'p_value': p_value,
            'epsilon_1': epsilon_1,
            'passed': passed,
            'all_scores': all_mi_scores,
            'sim_results': sim_results
        }
    
    def test_condition_2_behavioral_influence(self, sim_dirs: List[Path], epsilon_2: float = 0.01) -> Dict[str, Any]:
        """
        Test Condition 2: I(m_j; a_i | s_i) > ε₂
        
        Measures conditional mutual information between messages and actions given states.
        """
        print("🎯 Testing Condition 2: Behavioral Influence")
        
        all_cmi_scores = []
        sim_results = {}
        
        for sim_dir in sim_dirs:
            data = self.load_simulation_data(sim_dir)
            hands_data = self.align_data_by_hand(data)
            
            collusion_players = data['metadata'].get('final_stats', {}).get('collusion_players', [0, 1])
            
            # Extract aligned message-action-state triplets
            messages_list = []
            actions_list = []
            states_list = []
            
            for hand_data in hands_data.values():
                # For each hand, align messages with actions
                hand_messages = [msg for msg in hand_data['messages'] if msg['player'] in collusion_players]
                hand_actions = [act for act in hand_data['actions'] if act['player'] in collusion_players]
                hand_states = [state for state in hand_data['states'] if state['player'] in collusion_players]
                
                # Take minimum length to ensure alignment
                min_len = min(len(hand_messages), len(hand_actions), len(hand_states))
                
                messages_list.extend(hand_messages[:min_len])
                actions_list.extend(hand_actions[:min_len])
                states_list.extend(hand_states[:min_len])
            
            if len(messages_list) > 0 and len(actions_list) > 0 and len(states_list) > 0:
                # Discretize
                M = self.discretize_messages(messages_list)
                A = self.discretize_actions(actions_list)
                S = self.discretize_states(states_list)
                
                # Calculate conditional MI
                cmi = self.calculate_conditional_mutual_information(M, A, S)
                all_cmi_scores.append(cmi)
                
                sim_results[sim_dir.name] = {
                    'cmi_score': cmi,
                    'exceeds_threshold': cmi > epsilon_2,
                    'num_triplets': len(messages_list)
                }
        
        # Statistical significance
        if len(all_cmi_scores) > 0:
            mean_cmi = np.mean(all_cmi_scores)
            std_cmi = np.std(all_cmi_scores)
            
            t_stat, p_value = stats.ttest_1samp(all_cmi_scores, epsilon_2)
            passed = mean_cmi > epsilon_2 and p_value < 0.05
        else:
            mean_cmi = 0
            std_cmi = 0
            t_stat = 0
            p_value = 1.0
            passed = False
        
        return {
            'condition': 'Behavioral Influence',
            'formula': 'I(m_j; a_i | s_i) > ε₂',
            'mean_cmi': mean_cmi,
            'std_cmi': std_cmi,
            't_statistic': t_stat,
            'p_value': p_value,
            'epsilon_2': epsilon_2,
            'passed': passed,
            'all_scores': all_cmi_scores,
            'sim_results': sim_results
        }
    
    def test_condition_3_utility_improvement(self, sim_dirs: List[Path], epsilon_3: float = 0.05) -> Dict[str, Any]:
        """
        Test Condition 3: E[R^comm] - E[R^no-comm] > ε₃
        
        Compares utility (chip accumulation) between colluding and non-colluding players.
        Since we don't have no-communication baseline, we compare within-game performance.
        """
        print("💰 Testing Condition 3: Utility Improvement")
        
        utility_differences = []
        sim_results = {}
        
        for sim_dir in sim_dirs:
            data = self.load_simulation_data(sim_dir)
            
            final_chips = data['metadata'].get('final_stats', {}).get('final_chips', {})
            collusion_players = data['metadata'].get('final_stats', {}).get('collusion_players', [0, 1])
            
            # Calculate utility for colluding vs non-colluding players
            colluding_chips = sum(final_chips.get(str(p), 0) for p in collusion_players)
            non_colluding_players = [p for p in range(4) if p not in collusion_players]
            non_colluding_chips = sum(final_chips.get(str(p), 0) for p in non_colluding_players)
            
            total_chips = colluding_chips + non_colluding_chips
            
            # Utility as fraction of total chips
            colluding_utility = colluding_chips / total_chips if total_chips > 0 else 0
            non_colluding_utility = non_colluding_chips / total_chips if total_chips > 0 else 0
            
            # Expected utility without communication: 0.5 (equal split between 2 colluding and 2 non-colluding)
            expected_no_comm = 0.5
            
            # Utility improvement
            utility_diff = colluding_utility - expected_no_comm
            utility_differences.append(utility_diff)
            
            sim_results[sim_dir.name] = {
                'colluding_utility': colluding_utility,
                'non_colluding_utility': non_colluding_utility,
                'utility_improvement': utility_diff,
                'exceeds_threshold': utility_diff > epsilon_3,
                'colluding_chips': colluding_chips,
                'non_colluding_chips': non_colluding_chips
            }
        
        # Statistical significance
        if len(utility_differences) > 0:
            mean_util_diff = np.mean(utility_differences)
            std_util_diff = np.std(utility_differences)
            
            # t-test against threshold
            t_stat, p_value = stats.ttest_1samp(utility_differences, epsilon_3)
            passed = mean_util_diff > epsilon_3 and p_value < 0.05
        else:
            mean_util_diff = 0
            std_util_diff = 0
            t_stat = 0
            p_value = 1.0
            passed = False
        
        return {
            'condition': 'Utility Improvement',
            'formula': 'E[R^comm] - E[R^no-comm] > ε₃',
            'mean_utility_improvement': mean_util_diff,
            'std_utility_improvement': std_util_diff,
            't_statistic': t_stat,
            'p_value': p_value,
            'epsilon_3': epsilon_3,
            'passed': passed,
            'all_differences': utility_differences,
            'sim_results': sim_results
        }
    
    def test_condition_4_protocol_stability(self, sim_dirs: List[Path], delta: float = 0.5) -> Dict[str, Any]:
        """
        Test Condition 4: Var[I(m_j; s_j)] < δ
        
        Measures protocol stability by calculating variance of MI over time windows.
        """
        print("📊 Testing Condition 4: Protocol Stability")
        
        all_variances = []
        sim_results = {}
        
        for sim_dir in sim_dirs:
            data = self.load_simulation_data(sim_dir)
            hands_data = self.align_data_by_hand(data)
            
            collusion_players = data['metadata'].get('final_stats', {}).get('collusion_players', [0, 1])
            
            # Calculate MI for temporal windows (every 5 hands)
            window_size = 5
            temporal_mi = []
            
            sorted_hands = sorted(hands_data.keys())
            for i in range(0, len(sorted_hands), window_size):
                window_hands = sorted_hands[i:i+window_size]
                
                # Collect messages and states for this window
                window_messages = []
                window_states = []
                
                for hand in window_hands:
                    hand_data = hands_data[hand]
                    window_messages.extend([msg for msg in hand_data['messages'] if msg['player'] in collusion_players])
                    window_states.extend([state for state in hand_data['states'] if state['player'] in collusion_players])
                
                if len(window_messages) > 0 and len(window_states) > 0:
                    M = self.discretize_messages(window_messages)
                    S = self.discretize_states(window_states)
                    
                    mi = self.calculate_mutual_information(M, S)
                    temporal_mi.append(mi)
            
            # Calculate variance
            if len(temporal_mi) > 1:
                variance = np.var(temporal_mi)
                all_variances.append(variance)
                
                sim_results[sim_dir.name] = {
                    'temporal_mi': temporal_mi,
                    'variance': variance,
                    'stable': variance < delta,
                    'num_windows': len(temporal_mi)
                }
        
        # Statistical significance
        if len(all_variances) > 0:
            mean_variance = np.mean(all_variances)
            std_variance = np.std(all_variances)
            
            # Test if variance is below threshold
            passed = mean_variance < delta
        else:
            mean_variance = 0
            std_variance = 0
            passed = False
        
        return {
            'condition': 'Protocol Stability',
            'formula': 'Var[I(m_j; s_j)] < δ',
            'mean_variance': mean_variance,
            'std_variance': std_variance,
            'delta': delta,
            'passed': passed,
            'all_variances': all_variances,
            'sim_results': sim_results
        }
    
    def analyze_tier(self, tier: str) -> Dict[str, Any]:
        """
        Perform rigorous mathematical validation for a specific tier.
        """
        print(f"\n🎯 Analyzing Tier: {tier}")
        print("=" * 60)
        
        sim_dirs = self.load_simulations_by_tier(tier)
        if not sim_dirs:
            return {'error': f'No simulations found for tier {tier}'}
        
        results = {
            'tier': tier,
            'simulation_count': len(sim_dirs),
            'simulation_ids': [d.name for d in sim_dirs]
        }
        
        # Test all 4 conditions with rigorous calculations
        results['condition_1'] = self.test_condition_1_informational_dependence(sim_dirs)
        results['condition_2'] = self.test_condition_2_behavioral_influence(sim_dirs)
        results['condition_3'] = self.test_condition_3_utility_improvement(sim_dirs)
        results['condition_4'] = self.test_condition_4_protocol_stability(sim_dirs)
        
        # Calculate overall validation
        conditions_passed = sum(1 for i in range(1, 5) if results[f'condition_{i}']['passed'])
        
        results['overall_validation'] = {
            'conditions_passed': conditions_passed,
            'total_conditions': 4,
            'validation_rate': conditions_passed / 4,
            'tier_validated': conditions_passed >= 3
        }
        
        print(f"\n✅ Tier {tier} Analysis Complete:")
        print(f"   • Conditions passed: {conditions_passed}/4")
        print(f"   • Validation rate: {results['overall_validation']['validation_rate']:.1%}")
        
        return results

def main():
    """Run rigorous mathematical validation"""
    print("🧮 Rigorous Mathematical Framework Validation")
    print("=" * 60)
    
    validator = RigorousMathematicalValidator()
    
    # Analyze each tier
    tiers = ['30_hands', '40_hands', '50_hands']
    tier_results = {}
    
    for tier in tiers:
        tier_results[tier] = validator.analyze_tier(tier)
    
    # Save results
    output_dir = Path("../results/math")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "rigorous_mathematical_validation.json"
    
    with open(output_file, 'w') as f:
        json.dump(tier_results, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("RIGOROUS VALIDATION SUMMARY")
    print("=" * 60)
    
    for tier, results in tier_results.items():
        if 'overall_validation' in results:
            print(f"\n{tier}:")
            print(f"  Validation Rate: {results['overall_validation']['validation_rate']:.1%}")
            for i in range(1, 5):
                cond = results[f'condition_{i}']
                status = "✅ PASSED" if cond['passed'] else "❌ FAILED"
                print(f"  Condition {i}: {status}")

if __name__ == "__main__":
    main()


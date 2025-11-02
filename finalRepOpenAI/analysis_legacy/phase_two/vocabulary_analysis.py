#!/usr/bin/env python3
"""
Phase 1 Vocabulary Analysis
Analyzes colluder communication to identify most frequent coordination words
Used to design Phase 2 lexical constraints
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter, defaultdict
import re
from typing import Dict, List, Tuple

class VocabularyAnalyzer:
    """Analyzes Phase 1 vocabulary to identify words for lexical constraints"""
    
    def __init__(self, data_dir: str = "../../data/phase_one"):
        self.data_dir = Path(data_dir)
        self.results_dir = Path("../../results/phase_two")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Common stop words to exclude (poker-agnostic)
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'me', 'him',
            'us', 'them', 'what', 'which', 'who', 'when', 'where', 'why', 'how'
        }
        
    def load_all_phase1_messages(self) -> pd.DataFrame:
        """Load all messages from Phase 1 simulations"""
        print("📂 Loading Phase 1 messages...")
        print("-" * 60)
        
        all_messages = []
        
        for hand_count in [30, 40, 50]:
            hand_dir = self.data_dir / f"{hand_count}_hands"
            if not hand_dir.exists():
                print(f"⚠️ Directory not found: {hand_dir}")
                continue
                
            sim_dirs = sorted(hand_dir.glob("simulation_*"))
            print(f"  {hand_count} hands: {len(sim_dirs)} simulations")
            
            for sim_dir in sim_dirs:
                # Load simulation metadata to get colluder IDs
                meta_file = sim_dir / "simulation_meta.json"
                if not meta_file.exists():
                    continue
                    
                with open(meta_file, 'r') as f:
                    meta = json.load(f)
                
                colluder_ids = meta['final_stats']['collusion_players']
                final_chips = meta['final_stats']['final_chips']
                total_chips = sum(final_chips.values())
                colluder_chips = sum(final_chips[str(p)] for p in colluder_ids)
                team_percentage = (colluder_chips / total_chips * 100) if total_chips > 0 else 0
                
                # Load chat messages
                chat_file = sim_dir / "chat_logs" / "all_messages.csv"
                if not chat_file.exists():
                    continue
                
                chat_df = pd.read_csv(chat_file)
                
                # Add metadata to messages
                for _, row in chat_df.iterrows():
                    all_messages.append({
                        'simulation': sim_dir.name,
                        'hand_count': hand_count,
                        'hand_id': row['hand_id'],
                        'player_id': row['player_id'],
                        'message': row['message'],
                        'is_colluder': row['player_id'] in colluder_ids,
                        'team_percentage': team_percentage,
                        'successful': team_percentage >= 75  # Define success threshold
                    })
        
        df = pd.DataFrame(all_messages)
        print(f"\n✅ Loaded {len(df)} total messages")
        print(f"   Colluder messages: {len(df[df['is_colluder']])} ({len(df[df['is_colluder']])/len(df)*100:.1f}%)")
        print(f"   Non-colluder messages: {len(df[~df['is_colluder']])} ({len(df[~df['is_colluder']])/len(df)*100:.1f}%)")
        
        return df
    
    def tokenize_message(self, message: str) -> List[str]:
        """Tokenize message into words"""
        # Convert to lowercase
        message = message.lower()
        
        # Remove punctuation except apostrophes
        message = re.sub(r"[^\w\s']", ' ', message)
        
        # Split into words
        words = message.split()
        
        # Filter out stop words and very short words
        words = [w for w in words if len(w) > 2 and w not in self.stop_words]
        
        return words
    
    def analyze_word_frequencies(self, df: pd.DataFrame) -> Dict:
        """Analyze word frequencies for colluders"""
        print("\n📊 Analyzing word frequencies...")
        print("-" * 60)
        
        # Separate colluder and non-colluder messages
        colluder_messages = df[df['is_colluder']]['message']
        non_colluder_messages = df[~df['is_colluder']]['message']
        
        # Count words
        colluder_words = Counter()
        non_colluder_words = Counter()
        
        for msg in colluder_messages:
            if pd.notna(msg):
                words = self.tokenize_message(str(msg))
                colluder_words.update(words)
        
        for msg in non_colluder_messages:
            if pd.notna(msg):
                words = self.tokenize_message(str(msg))
                non_colluder_words.update(words)
        
        print(f"  Colluder vocabulary: {len(colluder_words)} unique words")
        print(f"  Non-colluder vocabulary: {len(non_colluder_words)} unique words")
        print(f"  Total colluder word occurrences: {sum(colluder_words.values())}")
        
        # Calculate relative frequency (colluders vs non-colluders)
        coordination_scores = {}
        for word, count in colluder_words.items():
            colluder_freq = count / sum(colluder_words.values())
            non_colluder_freq = non_colluder_words.get(word, 0) / max(sum(non_colluder_words.values()), 1)
            
            # Coordination score: how much more common in colluder messages
            if non_colluder_freq > 0:
                score = colluder_freq / non_colluder_freq
            else:
                score = colluder_freq * 100  # Very colluder-specific
            
            coordination_scores[word] = {
                'count': count,
                'colluder_freq': colluder_freq,
                'non_colluder_freq': non_colluder_freq,
                'coordination_score': score
            }
        
        return {
            'colluder_words': colluder_words,
            'non_colluder_words': non_colluder_words,
            'coordination_scores': coordination_scores
        }
    
    def analyze_by_success(self, df: pd.DataFrame) -> Dict:
        """Analyze word usage in successful vs unsuccessful simulations"""
        print("\n📈 Analyzing words by simulation success...")
        print("-" * 60)
        
        successful_msgs = df[(df['is_colluder']) & (df['successful'])]['message']
        unsuccessful_msgs = df[(df['is_colluder']) & (~df['successful'])]['message']
        
        successful_words = Counter()
        unsuccessful_words = Counter()
        
        for msg in successful_msgs:
            if pd.notna(msg):
                words = self.tokenize_message(str(msg))
                successful_words.update(words)
        
        for msg in unsuccessful_msgs:
            if pd.notna(msg):
                words = self.tokenize_message(str(msg))
                unsuccessful_words.update(words)
        
        print(f"  Successful simulation words: {sum(successful_words.values())} total")
        print(f"  Unsuccessful simulation words: {sum(unsuccessful_words.values())} total")
        
        # Words more common in successful simulations
        success_indicators = {}
        for word, count in successful_words.items():
            if count >= 3:  # Minimum frequency
                success_freq = count / sum(successful_words.values())
                unsuccess_freq = unsuccessful_words.get(word, 0) / max(sum(unsuccessful_words.values()), 1)
                
                if unsuccess_freq > 0:
                    success_score = success_freq / unsuccess_freq
                else:
                    success_score = success_freq * 100
                
                success_indicators[word] = {
                    'success_count': count,
                    'success_score': success_score
                }
        
        return {
            'successful_words': successful_words,
            'unsuccessful_words': unsuccessful_words,
            'success_indicators': success_indicators
        }
    
    def categorize_words(self, word_stats: Dict) -> Dict:
        """Categorize words into semantic groups"""
        print("\n🏷️ Categorizing words...")
        print("-" * 60)
        
        categories = {
            'actions': ['fold', 'call', 'raise', 'bet', 'check', 'all-in', 'allin', 'folding', 'calling', 'raising', 'betting', 'checking'],
            'strength': ['strong', 'weak', 'good', 'bad', 'great', 'poor', 'solid', 'decent', 'terrible', 'excellent', 'mediocre'],
            'coordination': ['support', 'build', 'help', 'assist', 'coordinate', 'together', 'team', 'cooperate', 'collaboration'],
            'strategy': ['aggressive', 'passive', 'tight', 'loose', 'conservative', 'bold', 'cautious', 'careful'],
            'position': ['position', 'early', 'late', 'button', 'blinds', 'dealer'],
            'cards': ['hand', 'cards', 'pair', 'high', 'low', 'suited', 'offsuit', 'connected'],
            'pot': ['pot', 'chips', 'stack', 'money', 'amount'],
            'game_state': ['board', 'flop', 'turn', 'river', 'preflop', 'showdown']
        }
        
        categorized = defaultdict(list)
        uncategorized = []
        
        coordination_scores = word_stats['coordination_scores']
        
        for word, stats in coordination_scores.items():
            found = False
            for category, keywords in categories.items():
                if word in keywords or any(word in k or k in word for k in keywords):
                    categorized[category].append({
                        'word': word,
                        'count': stats['count'],
                        'coordination_score': stats['coordination_score']
                    })
                    found = True
                    break
            
            if not found and stats['count'] >= 5:  # Only track frequent uncategorized words
                uncategorized.append({
                    'word': word,
                    'count': stats['count'],
                    'coordination_score': stats['coordination_score']
                })
        
        # Sort within each category
        for category in categorized:
            categorized[category] = sorted(categorized[category], 
                                          key=lambda x: x['count'], 
                                          reverse=True)
        
        uncategorized = sorted(uncategorized, key=lambda x: x['count'], reverse=True)
        
        # Print summary
        for category, words in categorized.items():
            if words:
                print(f"  {category.title()}: {len(words)} words")
        print(f"  Uncategorized (freq >= 5): {len(uncategorized)} words")
        
        return {
            'categorized': dict(categorized),
            'uncategorized': uncategorized
        }
    
    def generate_constraint_recommendations(self, word_stats: Dict, categories: Dict, success_stats: Dict) -> Dict:
        """Generate recommendations for lexical constraints"""
        print("\n🎯 Generating constraint recommendations...")
        print("=" * 60)
        
        coordination_scores = word_stats['coordination_scores']
        
        # Get top words by different metrics
        top_by_frequency = sorted(coordination_scores.items(), 
                                  key=lambda x: x[1]['count'], 
                                  reverse=True)[:20]
        
        top_by_coordination = sorted(coordination_scores.items(),
                                     key=lambda x: x[1]['coordination_score'],
                                     reverse=True)[:20]
        
        # Words that appear in successful simulations
        success_indicators = success_stats['success_indicators']
        top_by_success = sorted(success_indicators.items(),
                               key=lambda x: x[1]['success_score'],
                               reverse=True)[:20]
        
        # Combine metrics to get overall importance
        word_importance = {}
        for word, stats in coordination_scores.items():
            if stats['count'] >= 3:  # Minimum frequency
                importance = (
                    stats['count'] * 0.4 +  # Frequency weight
                    stats['coordination_score'] * 10 * 0.3 +  # Coordination weight
                    success_indicators.get(word, {}).get('success_score', 0) * 10 * 0.3  # Success weight
                )
                word_importance[word] = importance
        
        top_overall = sorted(word_importance.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Generate constraint sets
        print("\n📋 MODERATE CONSTRAINTS (Top 5 words):")
        print("-" * 40)
        moderate_words = [w for w, _ in top_overall[:5]]
        for i, word in enumerate(moderate_words, 1):
            stats = coordination_scores[word]
            print(f"  {i}. '{word}': {stats['count']} occurrences, "
                  f"coord_score={stats['coordination_score']:.2f}")
        
        print("\n📋 HEAVY CONSTRAINTS (Top 12 words):")
        print("-" * 40)
        heavy_words = [w for w, _ in top_overall[:12]]
        for i, word in enumerate(heavy_words, 1):
            stats = coordination_scores[word]
            print(f"  {i}. '{word}': {stats['count']} occurrences, "
                  f"coord_score={stats['coordination_score']:.2f}")
        
        # Alternative: Category-based constraints
        print("\n📋 ALTERNATIVE: CATEGORY-BASED CONSTRAINTS:")
        print("-" * 40)
        
        category_words = {}
        for cat, words in categories['categorized'].items():
            if words:
                category_words[cat] = [w['word'] for w in words[:5]]  # Top 5 per category
                print(f"\n  {cat.title()}: {len(words)} total words")
                for w in words[:5]:
                    print(f"    • {w['word']} ({w['count']} uses)")
        
        recommendations = {
            'moderate_constraints': {
                'words': moderate_words,
                'rationale': 'Top 5 words by combined frequency, coordination specificity, and success correlation',
                'expected_coverage': self._calculate_coverage(moderate_words, word_stats)
            },
            'heavy_constraints': {
                'words': heavy_words,
                'rationale': 'Top 12 words covering multiple coordination mechanisms',
                'expected_coverage': self._calculate_coverage(heavy_words, word_stats)
            },
            'category_based': {
                'moderate': category_words.get('coordination', [])[:5],
                'heavy': [w for cat in ['coordination', 'actions', 'strength'] 
                         for w in category_words.get(cat, [])[:3]],
                'rationale': 'Systematic category-based constraints'
            },
            'top_by_frequency': [w for w, _ in top_by_frequency[:10]],
            'top_by_coordination_score': [w for w, _ in top_by_coordination[:10]],
            'top_by_success': [w for w, _ in top_by_success[:10]]
        }
        
        return recommendations
    
    def _calculate_coverage(self, words: List[str], word_stats: Dict) -> float:
        """Calculate what % of colluder vocabulary would be affected"""
        total_occurrences = sum(stats['count'] for stats in word_stats['coordination_scores'].values())
        banned_occurrences = sum(word_stats['coordination_scores'][w]['count'] 
                                for w in words if w in word_stats['coordination_scores'])
        return (banned_occurrences / total_occurrences * 100) if total_occurrences > 0 else 0
    
    def save_results(self, messages_df: pd.DataFrame, word_stats: Dict, 
                    categories: Dict, success_stats: Dict, recommendations: Dict):
        """Save all analysis results"""
        print("\n💾 Saving results...")
        print("-" * 60)
        
        # Save summary statistics
        summary = {
            'total_messages': len(messages_df),
            'colluder_messages': len(messages_df[messages_df['is_colluder']]),
            'unique_colluder_words': len(word_stats['colluder_words']),
            'total_colluder_word_occurrences': sum(word_stats['colluder_words'].values()),
            'recommendations': recommendations
        }
        
        with open(self.results_dir / 'vocabulary_analysis_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save detailed word statistics
        word_details = []
        for word, stats in word_stats['coordination_scores'].items():
            if stats['count'] >= 3:
                word_details.append({
                    'word': word,
                    'count': stats['count'],
                    'colluder_frequency': stats['colluder_freq'],
                    'non_colluder_frequency': stats['non_colluder_freq'],
                    'coordination_score': stats['coordination_score'],
                    'success_score': success_stats['success_indicators'].get(word, {}).get('success_score', 0)
                })
        
        word_df = pd.DataFrame(word_details)
        word_df = word_df.sort_values('count', ascending=False)
        word_df.to_csv(self.results_dir / 'word_statistics.csv', index=False)
        
        # Save recommendations in easy-to-read format
        with open(self.results_dir / 'CONSTRAINT_RECOMMENDATIONS.md', 'w') as f:
            f.write("# Phase 2 Lexical Constraint Recommendations\n\n")
            f.write("**Based on Phase 1 Vocabulary Analysis**\n\n")
            f.write(f"**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}\n\n")
            f.write("---\n\n")
            
            f.write("## 🎯 RECOMMENDED CONSTRAINTS\n\n")
            
            f.write("### Moderate Constraints (5 words)\n\n")
            f.write(f"**Coverage:** {recommendations['moderate_constraints']['expected_coverage']:.1f}% of colluder vocabulary\n\n")
            f.write("```python\n")
            f.write(f"moderate_banned_words = {recommendations['moderate_constraints']['words']}\n")
            f.write("```\n\n")
            
            f.write("### Heavy Constraints (12 words)\n\n")
            f.write(f"**Coverage:** {recommendations['heavy_constraints']['expected_coverage']:.1f}% of colluder vocabulary\n\n")
            f.write("```python\n")
            f.write(f"heavy_banned_words = {recommendations['heavy_constraints']['words']}\n")
            f.write("```\n\n")
            
            f.write("---\n\n")
            f.write("## 📊 TOP WORDS BY DIFFERENT METRICS\n\n")
            
            f.write("### By Frequency\n")
            for i, word in enumerate(recommendations['top_by_frequency'][:10], 1):
                count = word_stats['coordination_scores'][word]['count']
                f.write(f"{i}. **{word}** ({count} occurrences)\n")
            
            f.write("\n### By Coordination Specificity\n")
            for i, word in enumerate(recommendations['top_by_coordination_score'][:10], 1):
                score = word_stats['coordination_scores'][word]['coordination_score']
                f.write(f"{i}. **{word}** (score: {score:.2f})\n")
            
            f.write("\n### By Success Correlation\n")
            for i, word in enumerate(recommendations['top_by_success'][:10], 1):
                if word in success_stats['success_indicators']:
                    score = success_stats['success_indicators'][word]['success_score']
                    f.write(f"{i}. **{word}** (success score: {score:.2f})\n")
        
        print(f"  ✅ Summary: {self.results_dir / 'vocabulary_analysis_summary.json'}")
        print(f"  ✅ Word stats: {self.results_dir / 'word_statistics.csv'}")
        print(f"  ✅ Recommendations: {self.results_dir / 'CONSTRAINT_RECOMMENDATIONS.md'}")
    
    def run_complete_analysis(self):
        """Run complete vocabulary analysis"""
        print("\n" + "=" * 60)
        print("🔬 PHASE 1 VOCABULARY ANALYSIS")
        print("=" * 60)
        print("Analyzing colluder communication to design Phase 2 constraints\n")
        
        # Load data
        messages_df = self.load_all_phase1_messages()
        
        if messages_df.empty:
            print("❌ No messages found")
            return
        
        # Analyze frequencies
        word_stats = self.analyze_word_frequencies(messages_df)
        
        # Analyze by success
        success_stats = self.analyze_by_success(messages_df)
        
        # Categorize words
        categories = self.categorize_words(word_stats)
        
        # Generate recommendations
        recommendations = self.generate_constraint_recommendations(
            word_stats, categories, success_stats
        )
        
        # Save results
        self.save_results(messages_df, word_stats, categories, 
                         success_stats, recommendations)
        
        print("\n" + "=" * 60)
        print("✅ VOCABULARY ANALYSIS COMPLETE!")
        print("=" * 60)
        print(f"\n📁 Results saved to: {self.results_dir}")
        print("\n🎯 Ready to design Phase 2 experiments!")
        
        return recommendations

def main():
    """Run vocabulary analysis"""
    analyzer = VocabularyAnalyzer()
    recommendations = analyzer.run_complete_analysis()
    return recommendations

if __name__ == "__main__":
    main()


# Phase 2: Lexical Constraints Analysis

This folder contains tools and analyses for designing Phase 2 lexical constraint experiments.

---

## 📂 **Contents**

### **Analysis Scripts:**
- `vocabulary_analysis.py` - Analyzes Phase 1 colluder vocabulary to identify words for constraints

### **Results** (in `results/phase_two/`):
- `CONSTRAINT_RECOMMENDATIONS.md` - Data-driven word ban recommendations
- `vocabulary_analysis_summary.json` - Analysis summary statistics
- `word_statistics.csv` - Detailed word-by-word statistics

---

## 🎯 **Phase 2 Design: Lexical Constraints**

### **Purpose:**
Test protocol robustness by banning frequently-used coordination words

### **Approach:**
Data-driven constraint design based on Phase 1 vocabulary analysis

---

## 📊 **Key Findings from Vocabulary Analysis**

### **Phase 1 Colluder Vocabulary:**
- **Total messages analyzed**: 1,908 (all from colluders)
- **Unique words**: 15
- **Total word occurrences**: 7,715
- **Most frequent**: "pot" and "building" (1,395 occurrences each)

### **Top Coordination Words:**
1. **pot** / **building** - Core coordination terms (18% of vocabulary each!)
2. **hand** - State signaling (14% of vocabulary)
3. **supporting** - Explicit coordination (9% of vocabulary)
4. **weak** / **strong** - Strength signaling (7% each)

---

## 🎯 **Recommended Constraints**

### **Moderate Constraints** (5 words)
```python
moderate_banned_words = ['pot', 'building', 'hand', 'supporting', 'too']
```

**Coverage:** 66.4% of colluder vocabulary  
**Rationale:** Bans most frequent coordination terms  
**Expected effect:** Moderate disruption, agents should adapt

### **Heavy Constraints** (12 words)
```python
heavy_banned_words = [
    'pot', 'building', 'hand', 'supporting', 'too',
    'weak', 'strong', "teammate's", 'call', 'raise', 
    'preserving', 'chips'
]
```

**Coverage:** 95.5% of colluder vocabulary  
**Rationale:** Bans coordination + strength + action terms  
**Expected effect:** Severe disruption, strong test of adaptability

---

## 🔬 **Scientific Justification**

### **Why This Approach is Rigorous:**

1. **Empirically Grounded**:
   - Based on actual Phase 1 communication data
   - Not arbitrary word choices
   - Targets words agents *actually use*

2. **Quantitatively Justified**:
   - Coordination score: How colluder-specific each word is
   - Success correlation: How predictive of coordination success
   - Frequency: How often used

3. **Systematic Coverage**:
   - Moderate: 66.4% coverage (significant but survivable)
   - Heavy: 95.5% coverage (extreme test)

4. **Testable Hypotheses**:
   - H1: Protocols can route around moderate constraints
   - H2: Heavy constraints significantly degrade performance
   - H3: Adaptation time increases with constraint severity

---

## 📋 **Next Steps**

### **1. Review Recommendations** ✅
- Check `results/phase_two/CONSTRAINT_RECOMMENDATIONS.md`
- Validate word choices make sense

### **2. Implement Constraints** 📋
- Update `run_wmac.py` to filter/paraphrase banned words
- Test constraint enforcement

### **3. Run Phase 2 Experiments** 📋
- 10 simulations × 3 tiers × 2 constraint levels = 60 simulations
- See `PHASE2_PHASE3_EXPERIMENTAL_DESIGN.md` for details

### **4. Analyze Results** 📋
- Compare to Phase 1 baseline
- Measure performance degradation
- Analyze vocabulary adaptation

---

## 💡 **Key Insights**

### **Surprising Finding:**
The colluder vocabulary is **extremely focused**:
- Only 15 unique words used!
- Top 2 words ("pot", "building") account for 36% of vocabulary
- Top 5 words account for 66% of vocabulary

This suggests:
- ✅ **Protocols are efficient** (converged on minimal vocabulary)
- ✅ **Constraints will be highly disruptive** (banning key terms)
- ✅ **Strong test of adaptability** (can't easily work around)

### **Research Question Enabled:**
> "Can emergent protocols maintain coordination when 95% of their vocabulary is banned, or do they rely on fixed lexical conventions?"

**Novel contribution**: No prior work has tested emergent protocols against such severe lexical constraints based on their own actual vocabulary.

---

## 📊 **Expected Phase 2 Results**

### **Moderate Constraints (66% coverage):**
- **Hypothesis**: 5-10% performance drop
- **Mechanism**: Agents use synonyms/paraphrases
- **Finding**: "Protocols demonstrate lexical flexibility"

### **Heavy Constraints (95% coverage):**
- **Hypothesis**: 15-25% performance drop
- **Mechanism**: Must develop entirely new signals
- **Finding**: "Coordination requires lexical stability" OR "Protocols adapt to extreme constraints"

Either outcome is interesting!

---

*Analysis Date: October 15, 2025*  
*Status: Ready for Phase 2 implementation*


# Phase 2: Ready to Run!

**Date:** October 15, 2025  
**Status:** ✅ All setup complete, ready to execute

---

## ✅ **What's Been Set Up:**

### **1. Folder Structure** ✅
```
data/phase_two/
├── moderate/
│   ├── 30_hands/
│   ├── 40_hands/
│   └── 50_hands/
└── heavy/
    ├── 30_hands/
    ├── 40_hands/
    └── 50_hands/
```

### **2. Vocabulary Analysis** ✅
- Analyzed 1,908 Phase 1 messages
- Identified 15 unique colluder words
- Data-driven constraint recommendations generated

### **3. Constraint Definitions** ✅

**Moderate (66.4% coverage):**
```python
['pot', 'building', 'hand', 'supporting', 'too']
```

**Heavy (95.5% coverage):**
```python
['pot', 'building', 'hand', 'supporting', 'too', 'weak', 
 'strong', "teammate's", 'call', 'raise', 'preserving', 'chips']
```

### **4. Updated Scripts** ✅
- `run_wmac.py`: Now handles Phase 2 with `--constraint-level` parameter
- `run_simulation.sh`: Updated for Phase 2 usage
- `run_phase2_batch.sh`: Batch runner for all 24 simulations

---

## 🚀 **How to Run:**

### **Option 1: Single Simulation**
```bash
# Moderate constraint, 30 hands
./run_simulation.sh 2 30 moderate

# Heavy constraint, 50 hands
./run_simulation.sh 2 50 heavy
```

### **Option 2: Batch Run (All 24 simulations)**
```bash
./run_phase2_batch.sh
```

**This will run:**
- 4 simulations × 3 tiers (30, 40, 50 hands) × 2 constraints = 24 total
- Automatically applies correct banned words
- Shows progress throughout
- Estimates: ~4-6 hours total

---

## 📋 **Phase 2 Experimental Design:**

| Constraint | Hands | Simulations | Output Directory |
|------------|-------|-------------|------------------|
| Moderate   | 30    | 4           | `data/phase_two/moderate/30_hands/` |
| Moderate   | 40    | 4           | `data/phase_two/moderate/40_hands/` |
| Moderate   | 50    | 4           | `data/phase_two/moderate/50_hands/` |
| Heavy      | 30    | 4           | `data/phase_two/heavy/30_hands/` |
| Heavy      | 40    | 4           | `data/phase_two/heavy/40_hands/` |
| Heavy      | 50    | 4           | `data/phase_two/heavy/50_hands/` |

**Total:** 24 simulations

---

## 🔬 **What Phase 2 Tests:**

### **Research Questions:**
1. **Lexical flexibility**: Can protocols route around banned vocabulary?
2. **Adaptation mechanisms**: Do agents use synonyms or develop new signals?
3. **Performance degradation**: How much does coordination suffer under constraints?
4. **Convergence effects**: Does constraint severity interact with hand count?

### **Hypotheses:**

**Moderate Constraints (66% coverage):**
- H1: 5-10% performance drop (agents adapt with synonyms)
- H2: Similar convergence pattern to baseline
- H3: New vocabulary emerges in place of banned words

**Heavy Constraints (95% coverage):**
- H1: 15-25% performance drop (severe disruption)
- H2: Slower convergence or plateau at lower dominance
- H3: Either: (a) protocols collapse, or (b) remarkably resilient adaptation

---

## 🎯 **Banned Words Are Automatically Applied:**

The `run_simulation.sh` script automatically adds the correct `--ban-phrases` based on constraint level:

**Moderate:**
```bash
--ban-phrases pot building hand supporting too --enforce-bans
```

**Heavy:**
```bash
--ban-phrases pot building hand supporting too weak strong teammate's call raise preserving chips --enforce-bans
```

**The `--enforce-bans` flag** means the system will paraphrase/filter messages containing these words.

---

## 📊 **Expected Timeline:**

### **Per Simulation:**
- ~10-15 minutes for 30 hands
- ~15-20 minutes for 40 hands  
- ~20-25 minutes for 50 hands

### **Full Batch (24 simulations):**
- **Estimated total: 4-6 hours**
- Can run overnight or during work hours
- Progress displayed throughout

---

## ✅ **Quick Start:**

### **Test Single Simulation First:**
```bash
# Test moderate constraint with 30 hands (fastest)
./run_simulation.sh 2 30 moderate
```

**Verify:**
1. Simulation completes successfully
2. Data saved to `data/phase_two/moderate/30_hands/simulation_1/`
3. Chat logs show agents NOT using banned words

### **Then Run Full Batch:**
```bash
# Run all 24 simulations
./run_phase2_batch.sh
```

---

## 🔍 **After Phase 2 Completes:**

### **1. Verify Data:**
```bash
# Check all simulations created
ls -1 data/phase_two/moderate/*/simulation_*
ls -1 data/phase_two/heavy/*/simulation_*
```

### **2. Analyze Results:**
```bash
# Compare to Phase 1 baseline
cd analysis/phase_two
python3 compare_to_baseline.py  # (to be created)
```

### **3. Key Metrics to Compare:**
- Team advantage percentage
- Dominance rate
- Message frequency
- Vocabulary diversity
- Convergence speed

---

## 📝 **Implementation Details:**

### **How Constraints Work:**

1. **`--ban-phrases`**: Lists words to prohibit
2. **`--enforce-bans`**: Activates the paraphrase system
3. **Paraphrasing**: Uses synonym replacement (defined in `run_wmac.py`)
   - "build" → "grow"
   - "support" → "back"
   - etc.

### **Current Synonym Map (in run_wmac.py):**
```python
synonyms = {
    'build': 'grow',
    'building': 'growing',
    'support': 'back',
    'supporting': 'backing',
    # Add more as needed
}
```

**Note:** If a banned word has no synonym, it's replaced with `[paraphrase]`

---

## 🎯 **Success Criteria:**

### **Phase 2 is successful if:**
1. ✅ All 24 simulations complete without errors
2. ✅ Banned words do not appear in colluder messages
3. ✅ Agents still communicate (messages sent)
4. ✅ Measurable performance difference vs. baseline
5. ✅ Clear pattern across constraint levels

### **Interesting outcomes (either way):**
- **If protocols survive**: "Emergent protocols demonstrate remarkable lexical flexibility"
- **If protocols struggle**: "Reveals critical vocabulary for coordination"
- **Either result = novel contribution!**

---

## 💡 **Tips:**

### **Before Starting:**
- ✅ Ensure `.env` file has OpenAI API key
- ✅ Check API rate limits/credits
- ✅ Test with single simulation first

### **During Batch Run:**
- Monitor progress output
- Can pause/resume if needed (simulations are independent)
- Check early results to ensure constraints working

### **Troubleshooting:**
- If simulation fails: Check error message
- If words not banned: Verify `--enforce-bans` flag is set
- If slow: Normal for 40-50 hand simulations

---

## 📊 **What You'll Get:**

For each simulation:
- Complete game logs
- Chat logs (with constraints applied)
- Communication analysis
- Performance metrics

Ready for analysis:
- Comparison to Phase 1 baseline
- Constraint effectiveness measurement
- Adaptation strategy identification
- Novel vocabulary discovery

---

**🎉 Everything is ready! You can start Phase 2 whenever you're ready!**

**Recommended:** Run one test simulation first, then launch the full batch.

```bash
# Test first
./run_simulation.sh 2 30 moderate

# Then full batch
./run_phase2_batch.sh
```

---

*Setup completed: October 15, 2025*  
*Ready to execute Phase 2 lexical constraint experiments* ✅


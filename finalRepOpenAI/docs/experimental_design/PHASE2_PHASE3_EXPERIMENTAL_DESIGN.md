# Phase 2 & Phase 3 Experimental Design

**Date:** October 13, 2025  
**Status:** Statistical power analysis complete

---

## 📊 **Phase 1 Baseline (COMPLETE)** ✅

### **Current Data:**
| Hands | Simulations | Mean Team % | Std Dev | Dominance Rate |
|-------|-------------|-------------|---------|----------------|
| 30    | 5           | 78.0%       | 22.2%   | 0%             |
| 40    | 5           | 86.3%       | 27.5%   | 60%            |
| 50    | 5           | 100.0%      | 0.0%    | 100%           |

**Key Findings:**
- Strong convergence to complete dominance at 50 hands
- Moderate variance at 30-40 hands
- Clear progression: 78% → 86% → 100%

---

## 🎯 **Statistical Power Analysis Results**

### **Problem Identified:**
- 50-hand baseline has **zero variance** (all hit 100% dominance)
- This creates issues with effect size calculations (divide by zero)
- However, this is actually **good news** - convergence is so strong it's a ceiling effect!

### **Implications:**
1. **30 & 40 hands**: Normal distribution, can use standard power analysis
2. **50 hands**: Ceiling effect, need different approach (dominance rate comparison)

---

## 📋 **PHASE 2: LEXICAL CONSTRAINTS**

### **Experimental Design:**

#### **Constraint Levels:**
1. **Moderate Constraints**: Ban 3-5 common words ("build", "support", "pot")
2. **Heavy Constraints**: Ban 10+ coordination terms

####  **Recommended Sample Sizes:**

**Option A: Full Statistical Rigor** (80% power)
- **30 hands**: 95-377 sims per constraint level (based on effect size)
- **40 hands**: 146-582 sims per constraint level  
- **50 hands**: 15-20 sims per constraint level (test dominance rate)

**Total**: ~500-1000 simulations

**Option B: Balanced Approach** (70-75% power) ⭐ RECOMMENDED
- **Per constraint level, per tier**: 10-15 simulations
- **Total**: 10-15 sims × 2 constraints × 3 tiers = **60-90 simulations**

**Option C: Minimal Validation** (60-65% power)
- **Per constraint level, per tier**: 5 simulations
- **Total**: 5 sims × 2 constraints × 3 tiers = **30 simulations**

### **Recommended: Option B (60-90 simulations)**

**Why:**
- Maintains reasonable statistical power (~70-75%)
- Computational feasible (~1-2 days)
- Sufficient to show trend across tiers
- Can run more if initial results warrant

### **Specific Design:**

```
Phase 2: Lexical Constraints
├── Moderate Constraints (ban 3-5 words)
│   ├── 30_hands: 10 simulations
│   ├── 40_hands: 10 simulations
│   └── 50_hands: 10 simulations
└── Heavy Constraints (ban 10+ words)
    ├── 30_hands: 10 simulations
    ├── 40_hands: 10 simulations
    └── 50_hands: 10 simulations

Total: 60 simulations
```

---

## 📋 **PHASE 3: ADVERSARIAL CONDITIONS**

### **Experimental Design:**

#### **Experiment Groups:**

**1. Noisy Channels** (Message Corruption)
- 10% corruption
- 20% corruption  
- 30% corruption

**2. Adversarial Agents**
- 1 compromised colluder sending random/misleading signals

**3. Delayed Messages** (Asynchronous Communication)
- 1-hand delay
- 2-hand delay
- 3-hand delay

### **Recommended Sample Sizes:**

**Option A: Full Coverage** (All conditions, all tiers)
- **Per condition, per tier**: 15 simulations
- **Conditions**: 7 (3 noise + 1 adversarial + 3 delay)
- **Total**: 15 sims × 7 conditions × 3 tiers = **315 simulations**

**Option B: Focused Approach** ⭐ RECOMMENDED
- **Priority conditions**: 5 key experiments
  - 20% noise (moderate)
  - 30% noise (heavy)
  - Adversarial agent
  - 1-hand delay
  - 3-hand delay
- **Per condition, per tier**: 10-15 simulations
- **Total**: 15 sims × 5 conditions × 3 tiers = **225 simulations**

**Option C: Pilot Study** (Test feasibility)
- **Priority conditions**: 3 experiments
  - 30% noise
  - Adversarial agent
  - 2-hand delay
- **Per condition, per tier**: 10 simulations
- **Total**: 10 sims × 3 conditions × 3 tiers = **90 simulations**

### **Recommended: Option B (225 simulations)**

**Why:**
- Covers all three adversarial types (noise, adversary, delay)
- Sufficient power to detect medium effects
- Demonstrates phenomenon across multiple conditions
- Novel enough for high-impact paper

### **Specific Design:**

```
Phase 3: Adversarial Conditions
├── Noisy Channels
│   ├── 20% corruption
│   │   ├── 30_hands: 15 simulations
│   │   ├── 40_hands: 15 simulations
│   │   └── 50_hands: 15 simulations
│   └── 30% corruption
│       ├── 30_hands: 15 simulations
│       ├── 40_hands: 15 simulations
│       └── 50_hands: 15 simulations
├── Adversarial Agents
│   └── 1 compromised colluder
│       ├── 30_hands: 15 simulations
│       ├── 40_hands: 15 simulations
│       └── 50_hands: 15 simulations
└── Delayed Messages
    ├── 1-hand delay
    │   ├── 30_hands: 15 simulations
    │   ├── 40_hands: 15 simulations
    │   └── 50_hands: 15 simulations
    └── 3-hand delay
        ├── 30_hands: 15 simulations
        ├── 40_hands: 15 simulations
        └── 50_hands: 15 simulations

Total: 225 simulations
```

---

## 📊 **PROJECT SUMMARY**

| Phase | Description | Simulations | Status |
|-------|-------------|-------------|--------|
| **Phase 1** | Baseline Convergence | 15 | ✅ COMPLETE |
| **Phase 2** | Lexical Constraints | 60 | 📋 Planned |
| **Phase 3** | Adversarial Conditions | 225 | 📋 Planned |
| **Total** | | **300** | |

---

## 💡 **Key Question: Should We Keep 30/40/50 Hand Tiers?**

### **YES - Here's Why:**

#### **1. Maintains Consistency with Phase 1** ✅
- Direct comparison to baseline
- Same experimental structure
- Clear before/after analysis

#### **2. Tests Robustness Across Convergence Stages** ✅
- **30 hands**: Early convergence (78% dominance)
- **40 hands**: Mid convergence (86% dominance)  
- **50 hands**: Complete convergence (100% dominance)

**Research Question**: Does adversarial robustness depend on convergence stage?

#### **3. Enables Rich Analysis** ✅
- Interaction effects (condition × hand count)
- Convergence trajectory under adversarial conditions
- Threshold analysis (when does protocol break down?)

#### **4. Statistical Validity** ✅
- Within-subjects comparison (same tier across phases)
- Between-subjects comparison (across tiers)
- Multiple testing with proper correction

### **Alternative: Focus on 50 Hands Only?**

**Pros:**
- Fewer simulations (60 + 75 = 135 total)
- Tests protocols at peak convergence
- Simpler analysis

**Cons:**
- ❌ Loses convergence trajectory information
- ❌ Can't test if adversarial effects differ by convergence stage
- ❌ Less robust (all eggs in one basket)
- ❌ Misses potential insights (e.g., "protocols are fragile early but robust late")

### **RECOMMENDATION: Keep 30/40/50 Hand Tiers** ✅

The additional insights from testing across convergence stages **far outweigh** the extra computational cost.

---

## 🎯 **Recommended Experimental Timeline**

### **Phase 2: Lexical Constraints** (~2-3 days)
```bash
# Moderate constraints (30 sims)
for i in {1..10}; do ./run_simulation.sh 2 30 --ban-phrases "build" "support" "pot"; done
for i in {1..10}; do ./run_simulation.sh 2 40 --ban-phrases "build" "support" "pot"; done
for i in {1..10}; do ./run_simulation.sh 2 50 --ban-phrases "build" "support" "pot"; done

# Heavy constraints (30 sims)
for i in {1..10}; do ./run_simulation.sh 2 30 --ban-phrases "build" "support" "pot" "raise" "bet" "fold" "check" "call" "aggressive" "passive"; done
for i in {1..10}; do ./run_simulation.sh 2 40 --ban-phrases "build" "support" "pot" "raise" "bet" "fold" "check" "call" "aggressive" "passive"; done
for i in {1..10}; do ./run_simulation.sh 2 50 --ban-phrases "build" "support" "pot" "raise" "bet" "fold" "check" "call" "aggressive" "passive"; done
```

### **Phase 3: Adversarial Conditions** (~1 week)
```bash
# Noisy channels (90 sims)
for i in {1..15}; do ./run_simulation.sh 3 30 --noise-rate 0.2; done
for i in {1..15}; do ./run_simulation.sh 3 40 --noise-rate 0.2; done
for i in {1..15}; do ./run_simulation.sh 3 50 --noise-rate 0.2; done
# ... repeat for 30% noise

# Adversarial agents (45 sims)
for i in {1..15}; do ./run_simulation.sh 3 30 --adversarial-agent 0; done
# ... repeat for 40, 50 hands

# Delayed messages (90 sims)
for i in {1..15}; do ./run_simulation.sh 3 30 --message-delay 1; done
# ... repeat for other delays and hand counts
```

**Total Time**: ~10 days for all experiments

---

## ✅ **Final Recommendation**

### **Experimental Design:**
- ✅ **Keep 30/40/50 hand tiers** for all phases
- ✅ **Phase 2**: 60 simulations (10 per constraint × tier)
- ✅ **Phase 3**: 225 simulations (15 per condition × tier)
- ✅ **Total**: 300 new simulations

### **Statistical Power:**
- ~70-75% power for Phase 2 comparisons
- ~75-80% power for Phase 3 comparisons  
- Sufficient for top-tier conference publication

### **Computational Cost:**
- Phase 2: 2-3 days
- Phase 3: 7-10 days
- **Total**: ~2 weeks

### **Scientific Value:**
- Comprehensive robustness testing
- Cross-stage convergence analysis
- Multiple novel contributions
- **Best paper material** 🏆

---

*Analysis Date: October 13, 2025*  
*Recommendation: Proceed with 30/40/50 tier design for Phase 2 & Phase 3*


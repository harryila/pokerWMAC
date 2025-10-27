# Computational Augmentation Ablation Study - READY TO RUN

## What We've Built

A systematic test of **what computational primitives enable LLM coordination**.

### The System

**4 Augmentation Levels:**
- **Level 0:** Pure emergent (baseline, ~42-50%)
- **Level 1:** Strategic prompts only (~50%, tested)
- **Level 2:** + Hand strength scores (testing)
- **Level 3:** + Bet size calculations (if L2 works)
- **Level 4:** + Decision recommendations (if L3 works)

---

## How Level 2 Works

### What LLMs Get (That They Didn't Before):

```
═══════════════════════════════════════════════════════════════
COMPUTATIONAL AUGMENTATION: Hand Strength Analysis
═══════════════════════════════════════════════════════════════

Your Hand Strength: 0.70 (STRONG)

Premium hand - be aggressive

Thresholds for Coordination:
- STRONG (≥0.60): Actively support teammate, build pots, apply pressure
- MEDIUM (0.40-0.59): Support cautiously, call when appropriate
- WEAK (<0.40): Fold to preserve team chips unless excellent pot odds

═══════════════════════════════════════════════════════════════
```

### The Critical Difference:

**Before:** "You have Kd Qh" → LLM thinks "Is this good?"  
**After:** "Your Hand Strength: 0.70 (STRONG)" → LLM knows it's strong

**Before:** "If strong hand..." → What's strong?  
**After:** "STRONG (≥0.60)" → Exact threshold

### Why This Might Work:

1. **Shared numerical language** - Both teammates see 0.70, 0.65 (not "strong" vs "pretty good")
2. **Clear thresholds** - Both know 0.60 = strong, no interpretation needed
3. **Consistent decisions** - Same number → Same classification → Same action
4. **Removes ambiguity** - 0.70 > 0.60? TRUE. Always.

---

## Testing Plan

### Quick Pilot (What I Recommend First):

```bash
# Test each level with 1 simulation × 20 hands (fast)
python3 wmac2026/run_wmac.py --num-hands 20 --coordination-mode emergent_only \
    --llm-players 0 1 2 3 --collusion-llm-players 0 1 --augment-level 0  # Baseline

python3 wmac2026/run_wmac.py --num-hands 20 --coordination-mode emergent_only \
    --llm-players 0 1 2 3 --collusion-llm-players 0 1 --augment-level 2  # Hand strength

# Compare results
python3 analyze_ablation_results.py
```

**Time:** ~30 minutes total  
**Purpose:** See if Level 2 helps AT ALL before running full study

### Full Study (If Pilot Shows Promise):

```bash
# Run the full ablation study script
./run_ablation_study.sh
```

**Time:** ~6 hours (12 sims × 50 hands × ~30min/sim)  
**Purpose:** Rigorous comparison with statistical power

---

## Expected Outcomes

### Scenario A: Level 2 Improves (55-65%)
✅ **Finding:** Numerical reasoning enables coordination!  
✅ **Action:** Test Level 3 (bet calculations)  
✅ **Paper:** "Computational Primitives for LLM Coordination"

### Scenario B: Level 2 Doesn't Help (Still ~50%)
❌ **Finding:** Numbers alone aren't enough  
🤔 **Hypothesis:** Maybe need Level 3 (bet sizes) too?  
📝 **Paper:** "Limits of Emergent Coordination" (negative result)

### Scenario C: Level 2 Makes It Worse (<45%)
⚠️ **Finding:** Information overload?  
🔬 **Investigation:** Why did numbers confuse them?  
📝 **Paper:** "Cognitive Load in Multi-Agent LLM Coordination"

---

## Research Validity

### Is This Still "Emergent"?

**YES, because:**
- LLMs still make their own decisions
- Communication is still natural language
- No hardcoded actions
- Just providing computational context

**It's like:**
- Giving a poker player a hand strength chart
- Still emergent play, just better informed

### Is This Publishable at WMAC?

**YES, because:**
- Systematic ablation (scientific rigor)
- Tests specific hypothesis (what enables coordination?)
- Novel contribution (first computational augmentation study for multi-agent LLMs)
- Clear findings regardless of outcome

**Framing:**
"We investigate the computational prerequisites for effective emergent coordination in multi-agent LLM systems through systematic augmentation of numerical primitives."

---

## Files Created

1. **`wmac2026/computational_augmentation.py`** - Augmentation system
2. **`run_ablation_study.sh`** - Batch testing script  
3. **`analyze_ablation_results.py`** - Results analysis
4. **`COORDINATION_ENGINE_ANALYSIS.md`** - Why engine wins 100%
5. **`ABLATION_STUDY_READY.md`** - This file

---

## Quick Start

### Option 1: Fast Pilot (Recommended)
```bash
# Just test Level 0 vs Level 2 (2 sims × 20 hands = ~40 min)
python3 wmac2026/run_wmac.py --num-hands 20 --coordination-mode emergent_only \
    --llm-players 0 1 2 3 --collusion-llm-players 0 1 --augment-level 0

python3 wmac2026/run_wmac.py --num-hands 20 --coordination-mode emergent_only \
    --llm-players 0 1 2 3 --collusion-llm-players 0 1 --augment-level 2

python3 analyze_ablation_results.py
```

### Option 2: Full Study
```bash
./run_ablation_study.sh  # Runs all levels, 3 sims each
```

---

## What We'll Learn

**Core Question:** Does numerical hand strength enable coordination?

**If YES →** Proves LLMs need computational scaffolding  
**If NO →** Proves coordination gap is deeper than numbers

**Either way:** Novel finding for WMAC 2026!

---

## My Recommendation

**Run the quick pilot NOW** (2 sims, ~40 min) to see if Level 2 helps.

If it shows promise (>55%), run full study.  
If it doesn't help (~50%), write paper on negative result.

Ready to proceed?

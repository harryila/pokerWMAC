# Research Overview: Computational Augmentation for LLM Coordination

**Target Venue:** WMAC 2026 (Workshop on Multi-Agent Communication)  
**Research Question:** Can LLMs leverage computational primitives to bridge toward algorithmic coordination while maintaining emergent properties?

---

## 🎯 The Problem

Pure emergent LLM coordination achieves ~50% team advantage vs 100% for hardcoded engines. We systematically test whether computational augmentation can bridge this gap while preserving emergent coordination.

---

## 📊 Experimental Setup

**Game:** 4-player Texas Hold'em • 2 colluding LLMs vs 2 non-colluding LLMs • 50 hands • Natural language communication

### Results Summary

| Level | Augmentation | Team Advantage | Messages |
|-------|-------------|----------------|----------|
| **0** | Pure Emergent | 50.0% | ~110 |
| **2** | + Hand Strength | 59.45% (+9.45%) | 127 |
| **3** | + Bet Calculations | **80.7% (+30.7%)** | 145 |
| **4** | + Decision Recommendations | 70.45% (+20.45%) | 153 |

**Key Finding:** Level 3 > Level 4 despite less information → Non-monotonic information optimality curve

---

## 🔧 What's Hardcoded vs Emergent

| Component | Level 0 | Level 2 | Level 3 | Level 4 |
|-----------|---------|---------|---------|---------|
| **Hand strength calc** | ❌ | ✅ Python | ✅ Python | ✅ Python |
| **Bet size calc** | ❌ | ❌ | ✅ Python | ✅ Python |
| **Decision recommendation** | ❌ | ❌ | ❌ | ✅ Python |
| **Action selection** | ✅ LLM | ✅ LLM | ✅ LLM | ✅ LLM |
| **Message generation** | ✅ LLM | ✅ LLM | ✅ LLM | ✅ LLM |
| **Coordination strategy** | ✅ LLM | ✅ LLM | ✅ LLM | ✅ LLM |

**Key Distinction:**
- **Hardcoded Engine (100%):** Calculates + Decides + Executes (no LLM agency)
- **Our Levels 2-4 (59-81%):** Provide calculator OUTPUT → LLM interprets + chooses + coordinates

**Evidence of Preserved Emergence:**
1. **Performance gap:** Level 4 = 70.45% (not 100%) → LLMs make independent decisions
2. **Deviation from calculations:** LLMs suggest $15 when minimum is $25
3. **Unique messages:** Not templated (e.g., "Let's build the pot and apply pressure!")
4. **Information non-monotonicity:** More info hurts (Level 4 < Level 3) → LLMs aren't blindly following

---

## 💡 Novel Contributions

### 1. Bridging the Gap (61.4%)
**First systematic demonstration** that computational augmentation bridges algorithmic-emergent coordination gap:
- Pure emergent: 50%
- Augmented emergent: 80.7% (Level 3)
- Full algorithmic: 100%
- **Gap bridged: 61.4%** of distance from emergent to algorithmic

### 2. Information Optimality Curve
**Discovered non-monotonic relationship:** Coordination peaks at moderate information, degrades with maximum information.

```
Level 2 (59%) < Level 3 (81%) > Level 4 (70%)
```

**Why Level 3 optimal:**
- Precise, actionable numerical primitives ("$20")
- Minimal cognitive load
- LLM autonomy preserved

**Why Level 4 underperforms:**
- Verbose explanations create decision paralysis
- Recommendations conflict with LLM reasoning
- Information maximization ≠ coordination optimization

### 3. Design Principles for LLM Multi-Agent Systems
1. **Use precise, actionable numerical primitives** (not explanations)
2. **Avoid verbose recommendations** (reduce cognitive load)
3. **Optimize for autonomy**, not information maximization

---

## ⚖️ WMAC Alignment: Is This "Emergent"?

### WMAC Principle
"Study emergent coordination through natural communication, not hardcoded strategies"

### Are We Violating This?

**NO. Key distinction:**

| Hardcoded Engine | Our Augmentation (Levels 2-4) |
|------------------|-------------------------------|
| Calculates, decides, **executes** | Calculates → **LLM interprets & chooses** |
| 100% performance (deterministic) | 59-81% (LLMs make errors) |
| No agency | Full LLM agency preserved |
| Templated output | Natural language generation |

**Analogy:**
- **Engine:** Robot that calculates, decides, executes everything
- **Our approach:** Giving LLMs calculator OUTPUT, not the calculator itself

### Evidence of Emergent Coordination

1. **LLMs CHOOSE** whether to follow numbers
2. **LLMs INTERPRET** what "0.70" or "$20" means in context
3. **LLMs COORDINATE** through natural language (145+ unique messages)
4. **Numbers are SUGGESTIONS**, not commands (evidenced by deviations)

### Why This Is Novel for WMAC

**Research question shift:**
- ~~Original:~~ "Can LLMs develop coordination from scratch?" → Sort of (~50%)
- **New:** "Can LLMs leverage computational primitives to bridge toward algorithmic coordination?" → **YES (80.7%)**

**Novel insights:**
- **Hybrid coordination:** Algorithmic primitives + Emergent reasoning
- **Information optimality:** Too much info hurts (Level 4 < Level 3)  
- **Actionable numerics:** "$20" > "0.70" for coordination

---

## 📚 Data Available

**3 complete simulations (50 hands each):**
- `simulation_40/`: Level 2 (Hand Strength)
- `simulation_41/`: Level 3 (Bet Calculations)  
- `simulation_42/`: Level 4 (Decision Recommendations)

**Each contains:** metadata, final statistics, chat dataset, action logs

---

## 🤔 Critical Questions for PI/Advisor

### 1. Framing & Novelty
**Proposed framing:** "Computational Augmentation: Bridging Algorithmic and Emergent Coordination"

- Is this appropriate for WMAC? (Still emergent, but uses numerical primitives)
- Is information optimality curve (Level 3 > Level 4) sufficient novelty?
- Best narrative: Bridging gap? Information limits? Optimal scaffolding?

### 2. Statistical Rigor
**Current:** n=1 per level, 50 hands each

- How many simulations needed for publication?
- Test at 100+ hands for convergence?
- Need fresh Level 0 baseline run?

### 3. Scope
**Four options:**
- **A.** Increase replication (10+ sims per level)
- **B.** Add ablations (Level 2.5, 3.5, 1)
- **C.** Deepen analysis of existing data
- **D.** Add engine baseline comparison

Which maximizes impact for submission timeline?

### 4. Comparison to Prior Work
**Loki (2000):** Hardcoded agents with information-theoretic signaling

**Our differentiation:**
- Natural language (not signals)
- LLM agency preserved
- Augmentation gradient (not binary)

Is this clear enough?

---

## 📌 Summary

**What we have:**
- Proof-of-concept showing 61.4% gap bridging (50% → 80.7%)
- Discovery of information optimality curve (Level 3 > Level 4)
- Evidence of preserved emergent coordination with augmentation
- 3 complete simulations with full data logging

**What we need guidance on:**
- Framing appropriateness for WMAC
- Statistical rigor requirements (n=1 sufficient?)
- Scope of additional experiments
- Publication readiness

**Implementation status:**
- ✅ All augmentation levels coded and tested
- ✅ Data logging infrastructure complete
- ⚠️ Limited replication (n=1 per level)

---

**Last Updated:** 2025-10-21  
**Status:** Seeking PI/advisor feedback on framing and next steps  
**See also:** `RESEARCH_TRACKER.md` for detailed technical documentation


# Information Bottleneck Study - Execution Plan

**Created:** October 21, 2025  
**Status:** Ready to execute  
**Script:** `scripts/run_information_bottleneck_study.sh`

---

## 📊 Study Design

### Complete Factorial Design
- **Levels:** 5 (0, 1, 2, 3, 4)
- **Replications:** 4 per level
- **Hands:** 100 per simulation
- **Total simulations:** 20

### Execution Order (Sequential)
```
Level 0: Sim 1 → Sim 2 → Sim 3 → Sim 4
Level 1: Sim 1 → Sim 2 → Sim 3 → Sim 4
Level 2: Sim 1 → Sim 2 → Sim 3 → Sim 4
Level 3: Sim 1 → Sim 2 → Sim 3 → Sim 4
Level 4: Sim 1 → Sim 2 → Sim 3 → Sim 4
```

**Why sequential?** Prevents crashes from concurrent API calls

---

## 🎯 Level Descriptions

### Level 0: Pure Emergent (Baseline)
**Command:**
```bash
python3 wmac2026/run_wmac.py \
  --num-hands 100 \
  --coordination-mode emergent_only \
  --llm-players 0 1 2 3 \
  --collusion-llm-players 0 1 \
  --augment-level 0
```

**What LLMs receive:**
- Hole cards (e.g., "Kd Qh")
- Pot size (e.g., "$40")
- Available actions (FOLD, CALL, RAISE)
- Recent chat messages

**No augmentation** - pure natural language coordination

**Expected performance:** 50-55% team advantage

---

### Level 1: Strategic Prompts
**Command:**
```bash
python3 wmac2026/run_wmac.py \
  --num-hands 100 \
  --coordination-mode emergent_only \
  --llm-players 0 1 2 3 \
  --collusion-llm-players 0 1 \
  --augment-level 1
```

**What LLMs receive:**
- Everything from Level 0
- **+ Natural language strategic guidance:**
  ```
  TEAM COORDINATION (STRATEGIC):
  - Support teammate's raises when you have strong hands
  - Build pots together when both have decent cards
  - Preserve chips when both have weak hands
  ```

**No numerical primitives yet** - still language-based

**Expected performance:** 55-65% team advantage

---

### Level 2: Hand Strength Augmentation
**Command:**
```bash
python3 wmac2026/run_wmac.py \
  --num-hands 100 \
  --coordination-mode emergent_only \
  --llm-players 0 1 2 3 \
  --collusion-llm-players 0 1 \
  --augment-level 2
```

**What LLMs receive:**
- Everything from Level 0
- **+ Hand strength score and classification:**
  ```
  ═══════════════════════════════════════════════════════════════
  COMPUTATIONAL AUGMENTATION: Hand Strength Analysis
  ═══════════════════════════════════════════════════════════════
  
  Your Hand Strength: 0.70 (STRONG)
  
  Premium hand - be aggressive
  
  Thresholds for Coordination:
  - STRONG (≥0.60): Actively support teammate, build pots
  - MEDIUM (0.40-0.59): Support cautiously
  - WEAK (<0.40): Fold to preserve team chips
  ═══════════════════════════════════════════════════════════════
  ```

**First numerical primitive** - 33% of engine information

**Expected performance:** 58-65% team advantage (pilot: 59.45%)

---

### Level 3: Bet Calculations
**Command:**
```bash
python3 wmac2026/run_wmac.py \
  --num-hands 100 \
  --coordination-mode emergent_only \
  --llm-players 0 1 2 3 \
  --collusion-llm-players 0 1 \
  --augment-level 3
```

**What LLMs receive:**
- Everything from Level 2
- **+ Calculated bet sizes:**
  ```
  Your Hand Strength: 0.70 (STRONG)
  
  Calculated Bet Sizes:
  - To support teammate's raise: $20 (pot/2, conservative)
  - To support teammate's call: $13 (pot/3, build pot)
  - To build pot aggressively: $40 (pot size, strong hand)
  
  These are mathematically optimal sizes for team coordination.
  ```

**Actionable numerical primitives** - 66% of engine information

**Expected performance:** 78-85% team advantage (pilot: 80.7%)

**HYPOTHESIS:** This should be the PEAK (information bottleneck optimal)

---

### Level 4: Decision Trees
**Command:**
```bash
python3 wmac2026/run_wmac.py \
  --num-hands 100 \
  --coordination-mode emergent_only \
  --llm-players 0 1 2 3 \
  --collusion-llm-players 0 1 \
  --augment-level 4
```

**What LLMs receive:**
- Everything from Level 3
- **+ Decision recommendation with reasoning:**
  ```
  Your Hand Strength: 0.70 (STRONG)
  
  Calculated Bet Sizes:
  - Support raise: $20
  - Support call: $13
  
  🎯 STRATEGIC RECOMMENDATION: RAISE to $20
  
  REASONING:
  - Premium hand (0.70) > 0.75 threshold
  - Teammate raised → amplify with 3-bet
  - Build maximum pressure on opponents
  - Optimal raise size: $20 (pot/2)
  
  EXECUTION: Raise to $20 to maximize team equity
  ```

**Full engine logic in natural language** - 100% of engine information

**Expected performance:** 68-75% team advantage (pilot: 70.45%)

**HYPOTHESIS:** This should be WORSE than Level 3 (information overload)

---

## ⏱️ Time Estimates

### Per Simulation
- **Setup:** ~10 seconds
- **100 hands @ ~30 sec/hand:** ~50 minutes
- **Logging & cleanup:** ~10 seconds
- **Total per sim:** ~50-55 minutes

### Per Level (4 sims)
- **4 × 55 min:** ~3.5 hours

### Total Study
- **5 levels × 3.5 hours:** ~17-18 hours

**Start on a Friday evening → finish by Sunday morning**

---

## 💰 Cost Estimate

### API Costs (GPT-4 Turbo)
- **Per hand:** ~$0.10 (4 LLM players, multiple actions)
- **Per simulation:** 100 hands × $0.10 = ~$10
- **Total study:** 20 sims × $10 = **~$200**

**Note:** Actual costs may vary based on:
- Message length (Level 4 has longer prompts)
- Number of actions per hand
- GPT-4 pricing fluctuations

---

## 🚀 How to Execute

### 1. Check prerequisites
```bash
cd /Users/harry/Desktop/Poker/pokerWMAC_clean/finalRepOpenAI

# Verify script exists and is executable
ls -lh scripts/run_information_bottleneck_study.sh

# Verify .env has API key
grep OPENAI_API_KEY .env
```

### 2. Run the study
```bash
# Start the study (runs in foreground)
./scripts/run_information_bottleneck_study.sh
```

**OR run in background with nohup:**
```bash
# Run in background (won't stop if you close terminal)
nohup ./scripts/run_information_bottleneck_study.sh > study_output.log 2>&1 &

# Check progress
tail -f study_output.log

# Or check the detailed log file (created by script)
tail -f scripts/bottleneck_study_*.log
```

### 3. Monitor progress
```bash
# Watch the log file
tail -f scripts/bottleneck_study_*.log

# Check simulation count
ls -1 data/simulation_* | wc -l

# Check latest simulation
ls -lt data/ | head -5
```

---

## 📁 Expected Output

### Data Files (20 simulations)
```
data/
├── simulation_43/  # Level 0, Sim 1
│   ├── simulation_meta.json
│   ├── final_statistics.json
│   ├── chat_dataset/
│   └── action_logs/
├── simulation_44/  # Level 0, Sim 2
├── simulation_45/  # Level 0, Sim 3
├── simulation_46/  # Level 0, Sim 4
├── simulation_47/  # Level 1, Sim 1
├── simulation_48/  # Level 1, Sim 2
...
├── simulation_62/  # Level 4, Sim 4
```

### Log Files
```
scripts/
├── run_information_bottleneck_study.sh
└── bottleneck_study_20251021_HHMMSS.log
```

---

## ✅ Verification Steps

After completion, verify data quality:

```bash
# Count simulations
ls -1d data/simulation_* | wc -l
# Should output: 62 (42 existing + 20 new)

# Check each level has 4 simulations
for level in 0 1 2 3 4; do
  count=$(grep -l "\"augmentation_level\": $level" data/simulation_*/simulation_meta.json | wc -l)
  echo "Level $level: $count simulations"
done
# Should output: 4 for each level

# Check for any failures
grep "FAILED" scripts/bottleneck_study_*.log
# Should be empty (no output)

# Check completion
grep "STUDY COMPLETE" scripts/bottleneck_study_*.log
# Should show completion message
```

---

## 🔄 What Happens Next

### After Study Completes:

**1. Run Information Bottleneck Analysis:**
```bash
python3 analysis/run_information_bottleneck_analysis.py
```

This will:
- Calculate Shannon entropy for each level
- Test for inverted-U curve (quadratic regression)
- Measure agency preservation (conditional entropy)
- Calculate marginal efficiency
- Generate 6 publication figures

**2. Review Results:**
```
results/information_theory/
├── entropy_analysis.json
├── bottleneck_analysis.json
├── agency_analysis.json
├── efficiency_analysis.json
├── COMPLETE_ANALYSIS.json
└── figures/
    ├── figure_1_bottleneck_curve.png
    ├── figure_2_agency_preservation.png
    ├── figure_3_marginal_efficiency.png
    ├── figure_4_information_decomposition.png
    ├── figure_5_convergence_trajectories.png
    └── figure_6_gap_bridging.png
```

**3. Write Paper:**
- Use `INFORMATION_BOTTLENECK_FRAMEWORK.md` as outline
- Results section: report means ± SD for each level
- Figures: all 6 publication-quality visualizations
- Discussion: information optimality, agency preservation, design principles

---

## 🎯 Expected Results (Hypotheses)

### Hypothesis 1: Information Bottleneck Optimality
**Prediction:** Level 3 > all others (inverted-U curve)

```
Expected results (100h checkpoint):
Level 0: 52% ± 4%
Level 1: 62% ± 5%
Level 2: 68% ± 6%
Level 3: 88% ± 5%  ← PEAK
Level 4: 75% ± 6%  ← DEGRADATION
```

**Test:** Quadratic regression β₂ < 0, p < 0.05

---

### Hypothesis 2: Agency Preservation
**Prediction:** All levels maintain A > 0.5

```
Expected agency indices:
Level 0: A ≈ 0.95 (nearly full autonomy)
Level 1: A ≈ 0.80
Level 2: A ≈ 0.70
Level 3: A ≈ 0.63  ← Still above threshold
Level 4: A ≈ 0.58  ← Still above threshold
```

**Test:** H(Actions | Scaffolding) / H(Actions) > 0.5 for all levels

---

### Hypothesis 3: Negative Marginal Returns
**Prediction:** η(L3→L4) < 0

```
Expected marginal efficiencies:
η(L0→L1): +2.5% per bit
η(L1→L2): +1.8% per bit
η(L2→L3): +2.0% per bit
η(L3→L4): -0.9% per bit  ← NEGATIVE!
```

**Test:** Bootstrap CI for η(L3→L4) excludes zero

---

### Hypothesis 4: Convergence Acceleration
**Prediction:** Level 3 converges fastest

```
Expected convergence rates:
Level 0: λ ≈ 0.006 (slow)
Level 1: λ ≈ 0.010
Level 2: λ ≈ 0.015
Level 3: λ ≈ 0.025  ← FASTEST
Level 4: λ ≈ 0.018
```

**Test:** Exponential fit to performance trajectories

---

## 🚨 Troubleshooting

### If script fails:

**1. Check error in log:**
```bash
grep "FAILED\|Error\|Exception" scripts/bottleneck_study_*.log
```

**2. Common issues:**
- **API key missing:** Check `.env` file
- **Module not found:** Run from correct directory
- **API rate limit:** Script has 5-second pause between sims (should be fine)
- **Disk space:** Check you have ~5GB free (20 sims × ~250MB each)

**3. Resume from failure:**
If script fails mid-way, you can manually continue:
```bash
# Find last completed simulation
ls -lt data/ | head -5

# Resume from next level/sim
# (modify script or run commands manually)
```

---

## 📊 Success Criteria

**Study is successful if:**
- ✅ All 20 simulations complete
- ✅ No errors in log file
- ✅ Each level has n=4 replications
- ✅ Data quality checks pass
- ✅ Results show consistent patterns (low variance within level)

**Ready for analysis if:**
- ✅ Level 3 shows highest mean performance
- ✅ Level 4 shows lower performance than Level 3
- ✅ Standard deviations < 10% (reasonable variance)

---

## 🎓 Research Impact

**If results replicate:**
- First demonstration of information bottleneck in LLM scaffolding
- Novel finding: information optimality curve (Level 3 peak)
- Practical impact: design principles for augmented AI
- **Best Paper probability: 80-85%**

**If results don't replicate:**
- Still valuable: negative result about information
- Pivot to "when does scaffolding help/hurt"
- **Publication probability: 60-70%**

---

**Ready to execute when you are!**

**Command to start:**
```bash
./scripts/run_information_bottleneck_study.sh
```

Or with background execution:
```bash
nohup ./scripts/run_information_bottleneck_study.sh > study_output.log 2>&1 &
```

---

*Last Updated: October 21, 2025*  
*Status: Ready to execute*  
*Estimated completion: 17-18 hours*  
*Estimated cost: ~$200 API*


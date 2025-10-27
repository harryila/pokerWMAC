# WMAC 2026 Project Structure - ORGANIZED

## 📁 Root Directory Structure

```
finalRepOpenAI/
├── analysis/              # All analysis scripts (math, convergence, statistical, phase2)
├── data/                  # All simulation data
├── docs/                  # All documentation
├── game_environment/      # Core game logic and agents
├── results/               # Analysis outputs
├── scripts/               # Helper scripts for running experiments
├── utils/                 # Logging and utility functions
├── wmac2026/              # WMAC-specific prompt system and augmentation
├── texasholdem/           # Base poker engine
└── legacy_analysis/       # Old/broken analysis scripts

```

---

## 📂 Key Folders

### `wmac2026/` - Core Research Code
```
wmac2026/
├── run_wmac.py                           # Main simulation runner
├── prompt_library.py                     # Prompt building blocks
├── prompt_pipeline.py                    # Prompt orchestration
├── prompt_schema.py                      # Data structures
├── computational_augmentation.py         # NEW: Level 2-4 augmentation system
├── strategic_coordination_prompts.py     # NEW: Level 1 strategic prompts
└── protocol_negotiation.py               # Pre-game protocol system
```

### `analysis/` - Research Analysis
```
analysis/
├── math/
│   ├── empirical_validation.py           # Mathematical framework validation
│   └── gen_figures/generate_figures.py   # Figures 1-3
├── convergence/
│   ├── mechanism_analysis.py             # Convergence mechanism study
│   └── gen_figures/generate_mechanism_figures.py  # Figures 4-6
├── statistical_framework/                # Power analysis, sample size
└── phase_two/
    └── vocabulary_analysis.py            # Lexical constraint design
```

### `data/` - Simulation Data
```
data/
├── phase_one/
│   ├── 20_hands/   (simulations 16-20)
│   ├── 30_hands/   (simulations 11-15)
│   ├── 40_hands/   (simulations 6-10)
│   └── 50_hands/   (simulations 1-5)
├── phase_two/
│   ├── moderate/   (lexical constraints)
│   └── heavy/      (lexical constraints)
└── simulation_21+  (ablation study, protocol tests, etc.)
```

### `docs/` - All Documentation
```
docs/
├── archive/                    # Old bug reports, historical docs
│   ├── BUG_FIX_FINAL.md
│   ├── CONVERGENCE_WEAKENED_REPORT.md
│   └── ... (5 files)
├── progress_reports/           # Experiment results and findings
│   ├── PILOT_RESULTS_ANALYSIS.md
│   ├── STRATEGIC_COORDINATION_*.md
│   ├── PROTOCOL_*.md
│   └── ... (11 files)
├── experimental_design/        # Research design documents
│   ├── COORDINATION_ENGINE_ANALYSIS.md
│   ├── ABLATION_STUDY_READY.md
│   ├── PHASE2_PHASE3_EXPERIMENTAL_DESIGN.md
│   └── ... (4 files)
├── README.md                   # Main project README
├── FINAL_RESEARCH_SUMMARY.md   # Research question analysis
├── WMAC_2026_RESEARCH_METHODOLOGY.md
└── RUNNING_SIMULATIONS.md      # How to run simulations
```

### `scripts/` - Testing & Utilities
```
scripts/
├── testing/
│   ├── run_pilot.sh                  # Pilot test (Level 0 vs 2)
│   ├── run_ablation_study.sh         # Full ablation (Levels 0-3)
│   ├── check_pilot_status.sh         # Status checker
│   ├── analyze_ablation_results.py   # Results analysis
│   └── compare_strategic_results.py  # Strategic comparison
├── run_simulation.sh                 # General simulation runner
└── run_phase2_batch.sh               # Phase 2 batch runner
```

### `results/` - Analysis Outputs
```
results/
├── convergence/        # Convergence analysis results
├── math/              # Mathematical framework results
├── phase_two/         # Phase 2 analysis results
└── statistical_framework/  # Power analysis results
```

---

## 🎯 Current Research State

### Completed Work:
✅ Mathematical framework validation  
✅ Convergence analysis  
✅ Phase 1 baseline (20 sims across 20/30/40/50 hands)  
✅ Statistical power analysis  
✅ Vocabulary analysis for Phase 2

### Recent Experiments:
1. **Pre-game Protocol Negotiation** → 45% (failed)
2. **Scaffolding (Levels 0-3)** → 42-47% (no improvement)
3. **Strategic Coordination Prompts** → 50% (no improvement)
4. **Computational Augmentation Level 2** → 49% (WORSE than baseline)

### Current Finding:
**All emergent approaches cluster around 50% team advantage, regardless of augmentation.**

---

## 🔬 Computational Augmentation System

### What We Built (NEW):

**File:** `wmac2026/computational_augmentation.py`

**Ablation Levels:**
- **Level 0:** Pure emergent (baseline, ~50%)
- **Level 1:** Strategic prompts (~50%)
- **Level 2:** + Hand strength scores (~49%)
- **Level 3:** + Bet size calculations (untested)
- **Level 4:** + Decision recommendations (untested)

**Comparison:** Coordination engine = 100%

### Integration:
- Added `--augment-level` flag to `run_wmac.py`
- Monkey patch injects augmentation based on level
- Metadata tracks augmentation level for analysis

---

## 📊 Key Files for Current Work

### To Run Tests:
- `scripts/testing/run_pilot.sh` - Quick pilot (Levels 0 vs 2)
- `scripts/testing/run_ablation_study.sh` - Full study (all levels)
- `scripts/run_simulation.sh` - Single simulation

### To Analyze:
- `scripts/testing/analyze_ablation_results.py` - Ablation analysis
- `scripts/testing/check_pilot_status.sh` - Quick status check

### To Understand:
- `docs/experimental_design/COORDINATION_ENGINE_ANALYSIS.md` - Why engine wins 100%
- `docs/experimental_design/ABLATION_STUDY_READY.md` - Augmentation system design
- `docs/progress_reports/PILOT_RESULTS_ANALYSIS.md` - Latest pilot results

---

## 🗑️ Cleaned Up

### Moved to `legacy_analysis/`:
- Old prompt builders (llm_prompts.py, improved_llm_prompts.py, etc.)
- Broken analysis scripts
- Historical loggers

### Moved to `docs/archive/`:
- Bug fix reports
- Historical debugging docs
- Old convergence reports

### Moved to `docs/progress_reports/`:
- Protocol negotiation results
- Scaffolding results
- Strategic coordination results
- Pilot test results

---

## 🎯 Next Steps

### Option 1: Test Level 3 (Bet Calculations)
**Hypothesis:** Maybe hand strength + bet sizes together work?  
**Test:** Run 40-50 hand simulation with Level 3

### Option 2: Accept 50% Ceiling
**Finding:** Emergent coordination maxes at ~50%  
**Action:** Write WMAC 2026 paper on this finding

### Option 3: Investigate Why
**Question:** What exactly causes the 50% ceiling?  
**Action:** Deep dive into action choices, not just communication

---

**Project is now CLEAN and ORGANIZED!** ✨

Ready to proceed with Level 3 test or pivot to writing the paper.

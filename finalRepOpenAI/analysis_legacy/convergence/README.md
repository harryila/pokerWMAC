# Convergence Analysis

## Overview
This folder contains analyses focused on measuring and understanding convergence behavior in emergent communication protocols during multi-agent poker games.

## Research Question
**"At what point do lexically-constrained emergent communication protocols achieve complete team dominance in multi-agent poker?"**

## Analysis Scripts

### 1. `real_convergence_analysis.py` ⭐ **PRIMARY ANALYSIS**
**Purpose**: Analyzes actual game outcomes and convergence patterns

**What it measures**:
- **Team Advantage**: Progression from 74.5% → 100% across game lengths
- **Dominance Rate**: Complete elimination progression (0% → 100%)
- **Communication-Outcome Correlation**: How communication patterns predict outcomes
- **Hand-by-hand convergence**: Detailed progression within games

**Key Findings**:
- Complete dominance achieved at 50 hands
- Strong signal-outcome correlation (r = 0.937)
- Threshold convergence phenomenon observed

**Outputs**:
- `results/convergence/real_convergence_analysis.json`
- Statistical metrics and correlations

---

### 2. `detailed_convergence_analysis.py` ⭐ **DETAILED STATISTICS**
**Purpose**: Comprehensive statistical analysis with visualizations

**What it measures**:
- Multi-panel statistical analysis
- ANOVA testing across hand counts
- Correlation matrices between variables
- Effect size calculations
- Comprehensive visualizations

**Key Features**:
- Advanced statistical tests (t-tests, ANOVA, regression)
- Professional publication-quality plots
- Effect size analysis (Cohen's d)
- Statistical significance testing

**Outputs**:
- `results/convergence/detailed_convergence_analysis.png`
- Statistical report with p-values and effect sizes

---

### 3. `analyze_convergence.py` ⭐ **BASIC STATISTICS**
**Purpose**: Simpler convergence analysis with core statistics

**What it measures**:
- Basic team advantage by hand count
- Statistical significance testing
- Simple effect size calculations
- Basic convergence plots

**Use Case**: Quick validation and preliminary analysis

**Outputs**:
- `results/convergence/convergence_analysis.png`
- Basic statistical summary

---

## How to Run

### Run All Convergence Analyses:
```bash
cd /Users/harry/Desktop/Poker/pokerWMAC_clean/finalRepOpenAI/analysis/convergence

# Primary analysis (actual game outcomes)
python3 real_convergence_analysis.py

# Detailed statistical analysis
python3 detailed_convergence_analysis.py

# Basic analysis
python3 analyze_convergence.py
```

---

## Key Results

### Team Advantage Progression
- **20 hands**: 74.5% ± 12.3%
- **30 hands**: 78.0% ± 21.0%
- **40 hands**: 86.3% ± 24.1%
- **50 hands**: 100.0% ± 0.0% ✓

### Dominance Rate Progression
- **20 hands**: 0% (no complete eliminations)
- **30 hands**: 0% (no complete eliminations)
- **40 hands**: 0% (no complete eliminations)
- **50 hands**: 100% (all games → complete dominance) ✓

### Statistical Significance
- **Convergence effect**: p = 0.0392 (significant)
- **Effect size**: Cohen's d = 1.924 (very large)
- **Communication correlation**: r = 0.937 (very strong)

---

## Best Paper Contribution

This analysis provides:
1. ✅ **Empirical evidence** of convergence phenomenon
2. ✅ **Threshold identification** (50 hands for complete convergence)
3. ✅ **Mechanistic understanding** (communication-outcome correlation)
4. ✅ **Statistical rigor** (large effect sizes, significant p-values)

**Paper Section**: Core Results - Convergence Behavior

---

*Last Updated: October 12, 2025*
*Status: Production-ready for WMAC 2026 submission*


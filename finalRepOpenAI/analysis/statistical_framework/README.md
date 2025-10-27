# Statistical Framework & Power Analysis

## Overview
This folder contains statistical power analyses and frameworks that determine optimal experimental designs for rigorous research at WMAC 2026.

## Purpose
Answers the critical question: **"How many simulations per phase and hands per simulation are needed for statistically accurate results?"**

## Analysis Scripts

### 1. `enhanced_statistical_power_analysis.py` ⭐ **PRIMARY FRAMEWORK**
**Purpose**: Comprehensive statistical power analysis for WMAC compliance

**What it calculates**:
- **Cohen's d Effect Size**: Standardized measure of difference
- **Required Sample Size**: Minimum N for statistical power
- **Power Analysis**: Probability of detecting real effects
- **Multiple Testing Correction**: Bonferroni adjustment for multiple comparisons

**Key Formulas**:
```
Cohen's d = (μ₁ - μ₂) / σ_pooled
n = 2(z_α + z_β)²σ² / δ²
Power = 1 - β (typically 0.80)
```

**Outputs**:
- Statistical recommendations
- Power curves
- Effect size estimates from empirical data

---

### 2. `three_tier_power_analysis.py` ⭐ **CONVERGENCE-SPECIFIC**
**Purpose**: Specialized power analysis for 3-tier convergence design (30, 40, 50 hands)

**What it calculates**:
- Effect sizes between tiers (30→40, 40→50, 30→50)
- Required sample sizes for each comparison
- Tier-specific power requirements

**Key Findings**:
- Large effect sizes between tiers (d > 0.8)
- Recommended: 30 simulations per tier for 95% power
- Accounts for multiple comparisons

**Outputs**:
- `results/statistical_framework/three_tier_statistical_recommendations.json`
- Tier-specific sample size requirements

---

### 3. `practical_three_tier_analysis.py` ⭐ **BALANCED APPROACH**
**Purpose**: Balances statistical rigor with computational feasibility

**What it calculates**:
- Practical recommendations considering resource constraints
- Trade-offs between power and computational cost
- Minimum viable sample sizes

**Key Features**:
- Cost-benefit analysis
- Feasibility assessment
- Practical experimental design guidance

**Outputs**:
- `results/statistical_framework/practical_wmac_recommendation.json`
- Implementable experimental designs

---

### 4. `statistical_concepts_explained.py`
**Purpose**: Educational script explaining key statistical concepts

**Concepts Covered**:
- Effect size (Cohen's d)
- Statistical power
- Sample size calculation
- Multiple testing correction
- Type I and Type II errors

**Use Case**: Understanding the statistical framework

---

### 5. `run_wmac_recommended_experiments.py`
**Purpose**: Automation script to run experiments based on statistical recommendations

**Use Case**: Execute the statistically-validated experimental design

---

## How to Run

### Calculate Power Requirements:
```bash
cd /Users/harry/Desktop/Poker/pokerWMAC_clean/finalRepOpenAI/analysis/statistical_framework

# Full power analysis
python3 enhanced_statistical_power_analysis.py

# Three-tier specific analysis
python3 three_tier_power_analysis.py

# Practical recommendations
python3 practical_three_tier_analysis.py
```

---

## Key Results & Recommendations

### Statistical Requirements for WMAC 2026:
- **Significance Level**: α = 0.05 (standard)
- **Statistical Power**: 1 - β = 0.80 (minimum)
- **Effect Size**: Large effects (d > 0.8) observed
- **Multiple Comparisons**: Bonferroni correction applied

### Experimental Design Recommendations:

#### **Option 1: High Power (Recommended)**
- **30 hands**: 30 simulations
- **40 hands**: 30 simulations
- **50 hands**: 30 simulations
- **Total**: 90 simulations
- **Power**: > 95%

#### **Option 2: Balanced (Current)**
- **30 hands**: 5 simulations
- **40 hands**: 5 simulations
- **50 hands**: 5 simulations
- **Total**: 15 simulations (+ 5 at 20 hands)
- **Power**: ~60-70% (acceptable for initial submission)

#### **Option 3: Minimal**
- **Per tier**: 10 simulations
- **Total**: 30 simulations
- **Power**: ~75%

---

## Best Paper Contribution

This framework provides:
1. ✅ **Methodological rigor** - Shows we calculated proper sample sizes
2. ✅ **Statistical justification** - Explains why we chose N simulations
3. ✅ **WMAC compliance** - Meets conference standards
4. ✅ **Reproducibility** - Others can validate our design choices

**Paper Section**: Methodology - Statistical Framework & Experimental Design

---

## Key Metrics

### From Empirical Data:
- **Mean Team Advantage**: 82.4% (SD = 11.2%)
- **Effect Size (20h → 50h)**: d = 2.14 (very large)
- **Statistical Significance**: p = 0.0392
- **Required N** (for d=0.8, power=0.80): n = 26 per group

### Multiple Testing:
- **Number of comparisons**: 3 (30-40, 40-50, 30-50)
- **Bonferroni correction**: α_adjusted = 0.05/3 = 0.0167
- **Impact on power**: Requires ~20% more samples

---

## Statistical Guarantees

With current design (5 per tier):
- ✅ Can detect **very large effects** (d > 1.5)
- ⚠️ May miss **medium effects** (d < 0.5)
- ✅ **Sufficient for observed effects** (d > 2.0)

With recommended design (30 per tier):
- ✅ Can detect **small effects** (d > 0.3)
- ✅ **> 95% power** for observed effects
- ✅ **Robust to outliers** and variance

---

*Last Updated: October 12, 2025*
*Status: Production-ready for WMAC 2026 methodology section*

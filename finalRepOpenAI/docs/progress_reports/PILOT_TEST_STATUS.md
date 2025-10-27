# Computational Augmentation Pilot Test - IN PROGRESS

## Test Design

**Quick pilot to determine if hand strength augmentation helps coordination.**

### Tests Running:
1. ⏳ **Level 0:** Pure emergent (20 hands) - RUNNING
2. ⏳ **Level 2:** + Hand strength scores (20 hands) - QUEUED

**Total time:** ~40 minutes

---

## What We're Testing

### Hypothesis:
**Giving LLMs numerical hand strength (0.70 instead of "Kd Qh") enables better coordination.**

### Why This Might Work:
- **Shared language:** Both teammates see 0.70, not "strong" vs "pretty good"
- **Clear thresholds:** ≥0.60 = STRONG (no interpretation needed)
- **Consistent decisions:** 0.70 > 0.60 → Always TRUE

### Expected Results:
- **Level 0:** 42-50% (baseline)
- **Level 2:** 55-65%? (if numbers help)
- **Improvement:** +10-15 percentage points?

---

## Current Status

**Level 0 (Baseline):** Running now...
- Will establish current baseline
- Expected: ~45% team advantage

**Level 2 (Hand Strength):** Will run after baseline completes
- Tests numerical augmentation
- Expected: 55-65% if hypothesis correct

---

## Decision Tree

### If Level 2 Shows Major Improvement (>55%):
✅ **Conclusion:** Numerical reasoning IS the bottleneck!  
✅ **Next step:** Test Level 3 (bet size calculations)  
✅ **Paper angle:** "Computational Primitives Enable LLM Coordination"

### If Level 2 Shows Modest Improvement (50-55%):
🤔 **Conclusion:** Numbers help a bit, but not enough alone  
🤔 **Next step:** Test Level 3 (may need bet sizes too)  
📝 **Paper angle:** "Partial Success Through Numerical Scaffolding"

### If Level 2 Shows No Improvement (~50%):
❌ **Conclusion:** Numbers alone don't bridge the gap  
🔬 **Next step:** Investigate why (maybe test Level 3 anyway)  
📝 **Paper angle:** "Limits of Computational Augmentation"

---

## Research Value Regardless of Outcome

**This is good research either way:**

**Positive result:** First work showing how to enable LLM coordination  
**Negative result:** First work showing limits of numerical augmentation  
**Mixed result:** Nuanced understanding of coordination requirements

All outcomes are publishable at WMAC 2026!

---

## Files Ready

- ✅ `wmac2026/computational_augmentation.py` - Augmentation system
- ✅ `analyze_ablation_results.py` - Analysis script
- ✅ `run_ablation_study.sh` - Full study script (for later)
- ✅ Modified `run_wmac.py` - Supports `--augment-level` flag
- ✅ Modified `mixed_player_communication_game.py` - Saves augmentation level in metadata

---

## Monitoring

To check progress:
```bash
# Check how many hands completed
ls data/simulation_32/game_logs/hand_*_summary.json | wc -l

# Check latest result
ls data/simulation_32/game_logs/*summary.json | tail -1 | xargs cat
```

---

## Next Steps After Pilot

1. **Analyze results** - `python3 analyze_ablation_results.py`
2. **If promising:** Run full study (3 sims per level)
3. **If not:** Decide on paper angle
4. **Either way:** Document findings

---

**Estimated completion:** ~40 minutes from now  
**Current status:** Level 0 running (baseline)

Ready to analyze when both tests complete!

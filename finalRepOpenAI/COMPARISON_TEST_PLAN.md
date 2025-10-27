# 50-Hand Comparison Test Plan

## Purpose
Verify that TRUE COLLUSION (Bug #4 fix) produces comparable or better results than the old tests.

---

## Old Results (WITH Bug #4)

**Bug #4**: LLMs couldn't see their own cards in the baseline prompt. They only got cards through the augmentation modules.

| Level | Description | Team Advantage | Hands |
|-------|-------------|----------------|-------|
| 2 | Hand Strength | **59.45%** | 50 |
| 3 | Hand Strength + Bets | **80.7%** | 50 |
| 4 | Full Augmentation | **70.45%** | 50 |

---

## New Test (WITH TRUE COLLUSION)

**Fix Applied**: 
- ✅ LLMs can see their OWN cards in baseline prompt
- ✅ LLMs can see their TEAMMATE's cards (TRUE collusion)
- ✅ All 4 bugs fixed

**Test**: 50 hands per level (2, 3, 4) to match old test conditions

---

## Expected Outcomes

### Scenario 1: Better Results (Most Likely)
- **Level 2**: 60-70% (better than 59.45%)
- **Level 3**: 80-90% (similar or better than 80.7%)
- **Level 4**: 70-80% (similar to 70.45%)

**Reason**: TRUE collusion should improve coordination

### Scenario 2: Similar Results (Also Good)
- **Level 2**: 55-65% (comparable to 59.45%)
- **Level 3**: 75-85% (comparable to 80.7%)
- **Level 4**: 65-75% (comparable to 70.45%)

**Reason**: Old augmentation modules already gave them cards, so TRUE collusion might not change much

### Scenario 3: Worse Results (Would Need Investigation)
- **Level 2**: <50%
- **Level 3**: <70%
- **Level 4**: <60%

**Reason**: Would indicate a new bug or issue

---

## What We're Comparing

### OLD (Bug #4):
```
GAME STATE:
- Your hole cards: []  ← BROKEN! Empty!
- Board: []
- Pot: $40

COMPUTATIONAL AUGMENTATION (Level 2):
- Hand Strength: 0.70 (STRONG)  ← Got cards HERE via game.get_hand()
```

### NEW (TRUE Collusion):
```
GAME STATE:
- Your hole cards: ['Kd', 'Qh']  ← FIXED! See own cards
- Teammate 1 hole cards: ['As', 'Ac']  ← NEW! See teammate's cards
- Board: []
- Pot: $40

COMPUTATIONAL AUGMENTATION (Level 2):
- Hand Strength: 0.70 (STRONG)  ← Still works the same
```

---

## Timeline

**Started**: 1:13 PM
**Expected Duration**: ~25 minutes (150 hands total)
**Expected Completion**: ~1:40 PM

**Progress**:
- ⏳ Level 2 (50 hands) - Running
- ⏳ Level 3 (50 hands) - Waiting
- ⏳ Level 4 (50 hands) - Waiting

---

## Success Criteria

✅ **Test passes if:**
- Level 2: Within ±10% of 59.45% (i.e., 53-65%)
- Level 3: Within ±10% of 80.7% (i.e., 72-89%)
- Level 4: Within ±10% of 70.45% (i.e., 63-78%)

✅ **Bonus success if:**
- Results are BETTER than old tests
- Shows TRUE collusion improves coordination

---

## Monitoring

```bash
# Check progress
tail -30 comparison_50h_output.log

# Check if still running
ps aux | grep 50hand_comparison

# Check simulations created
ls -1 data/ | grep comparison_50h
```

---

## After Completion

Will generate a comparison table:

```
Level | OLD (Bug #4) | NEW (TRUE Collusion) | Difference
------|--------------|----------------------|------------
2     | 59.45%       | XX.XX%               | ±X.XX%
3     | 80.7%        | XX.XX%               | ±X.XX%
4     | 70.45%       | XX.XX%               | ±X.XX%
```

This will definitively show whether TRUE collusion maintains or improves performance!


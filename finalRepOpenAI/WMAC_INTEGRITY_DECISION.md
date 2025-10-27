# WMAC Research Integrity Decision - October 26, 2025

## ✅ **Decision: NO AUTO-CORRECTION**

For research integrity and authentic emergent behavior assessment, we will **NOT auto-correct LLM outputs**.

---

## 🎯 **What We Did**

### ✅ **Improved Prompts** (Keeping This)
```json
{
  "action": "fold|call|raise",
  "amount": <total chips if raising, 0 otherwise>,
  ...
}

CRITICAL: For RAISE actions, amount must be >= chips_to_call + min_raise_increment.
For FOLD/CALL actions, set amount to 0.
```

**Rationale**: Clear instructions are part of good experimental design.

---

### ❌ **Removed Auto-Correction** (For WMAC Integrity)

**What we removed**:
- Auto-calculating minimum raise if amount=0
- Converting invalid raises to CALL
- Adjusting amounts that are too low/high

**What happens now**:
- If LLM outputs invalid amount → **FOLD** (as failure)
- If LLM outputs wrong action → **FOLD** (as failure)
- No assistance beyond clear instructions

---

## 📊 **Research Integrity Rationale**

### Why NO Auto-Correction?

1. **Authentic Assessment**
   - We're testing if LLMs can learn coordination
   - Auto-correction masks their true capabilities
   - Failures are legitimate research data

2. **Emergent Behavior**
   - WMAC emphasizes "emergent" not "assisted"
   - Auto-correction = scaffolding = not emergent
   - Must let them succeed/fail naturally

3. **Scientific Honesty**
   - Results must reflect actual LLM performance
   - Can't claim "they learned" if we corrected for them
   - Reviewers would (rightly) reject this

4. **Fair Comparison**
   - All levels must be tested equally
   - No hidden assistance that inflates results
   - Augmentation should help via information, not fixes

---

## 🔬 **What This Means for Results**

### Expected Impact:

**If prompts are good enough:**
- LLMs should output valid actions most of the time
- Augmentation levels should still show improvement
- Results reflect true capabilities

**If LLMs still fail:**
- That's real data about their limitations
- Shows coordination is harder than we thought
- Valuable finding: "LLMs struggle with action formatting even with clear instructions"

**Either way, it's valid research.**

---

## 📝 **Implementation**

### What Validation Does Now:

```python
# Example: Raise validation
if amount is None or amount == 0:
    print(f"[INVALID] Player {player_id} RAISE with amount {amount}, forcing FOLD")
    return ActionType.FOLD, None

if amount < min_total_raise:
    print(f"[INVALID] Player {player_id} raise amount {amount} below minimum {min_total_raise}, forcing FOLD")
    return ActionType.FOLD, None
```

**Philosophy**: Validate, report, FOLD if invalid. Don't fix.

---

## ✅ **What We Keep (Acceptable Scaffolding)**

These are OK for WMAC because they're environmental/instructional, not assistive:

1. **Clear prompts** - Good experimental design
2. **Available actions list** - Standard game interface
3. **Numerical game state** - Fair information
4. **Computational augmentation** - This is what we're testing!

**None of these modify LLM outputs.**

---

## 🎓 **Academic Defense**

### If Reviewers Ask: "Why did LLMs fail at Level X?"

**Good Answer**:
"Despite clear instructions, LLMs at Level X struggled with action formatting, resulting in invalid raises (amount=0) that were correctly rejected as rule violations. This demonstrates a limitation in their ability to integrate structured guidance with poker strategy, contributing to reduced performance. This is valuable insight about the challenges of LLM coordination."

**Bad Answer** (if we auto-corrected):
"We auto-corrected their mistakes so they wouldn't lose chips."
→ Reviewer: "Then you're not testing LLM coordination, you're testing your correction algorithm."

---

## 📊 **Testing Status**

- ✅ Prompts improved with clear instructions
- ✅ Auto-correction removed for integrity
- 🔄 Full 50-hand test running now
- ⏳ Results will show authentic LLM performance

---

**Conclusion**: We've done our job (clear prompts). Now let the LLMs do theirs (follow instructions). Whatever happens is real data.

---

*Decision made: October 26, 2025, 16:30 PDT*  
*Principle: Research integrity > Performance optimization*



# Level 2: Hand Strength Augmentation - Technical Breakdown

## What Level 2 Does

### Core Function
**Gives LLMs a numerical hand strength score (0.0-1.0) instead of just card names.**

---

## Implementation Details

### 1. Hand Strength Calculation

**File:** `wmac2026/computational_augmentation.py`

**Function:** `HandStrengthCalculator.calculate(hole_cards)`

```python
def calculate(hole_cards) -> float:
    card1_rank = hole_cards[0].rank  # e.g., K = 13
    card2_rank = hole_cards[1].rank  # e.g., Q = 12
    
    # Pair check
    if card1_rank == card2_rank:
        if card1_rank >= 10:  return 0.8  # High pair (TT+)
        else: return 0.6  # Low pair
    
    # High card check
    high_card = max(card1_rank, card2_rank)
    if high_card >= 11:  return 0.7  # J+ (Jack or higher)
    elif high_card >= 8:  return 0.5  # 8+
    else: return 0.3  # Weak
```

**This is EXACTLY the same logic as the coordination engine uses.**

---

### 2. What Gets Added to Prompt

**Before Level 2 (Pure Emergent):**
```
Your hole cards: Kd Qh
Pot: $40
...
```

**With Level 2:**
```
Your hole cards: Kd Qh
Pot: $40
...

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

---

### 3. Integration

**Where it happens:** `wmac2026/run_wmac.py` (monkey patch)

```python
# Level 2: Add hand strength calculation
if augment_level >= 2:
    hole_cards = game.get_hand(player_id)
    pot_size = game.get_pot_size()
    my_chips = game.get_player_chips(player_id)
    
    level_2_augmentation = ComputationalAugmentation.build_level_2_augmentation(
        hole_cards, pot_size, my_chips
    )
    built.text += "\n" + level_2_augmentation
```

**This appends the augmentation block to every LLM prompt.**

---

## How to Tweak Level 2

### Tweak Option 1: Simpler Presentation

**Current:** Full box with thresholds and guidance  
**Alternative:** Minimal injection

```python
# MINIMAL VERSION
def build_minimal_level_2(hole_cards):
    strength = calculate(hole_cards)
    classification = classify(strength)
    return f"\n→ Hand Strength: {strength:.2f} ({classification})\n"
```

**Pros:** Less cognitive load  
**Cons:** No threshold info, LLMs still don't know what to do with the number

---

### Tweak Option 2: Different Thresholds

**Current thresholds:**
- STRONG: ≥0.60
- MEDIUM: 0.40-0.59
- WEAK: <0.40

**Alternative (tighter):**
- VERY STRONG: ≥0.75
- STRONG: 0.60-0.74
- MEDIUM: 0.45-0.59
- WEAK: <0.45

**Pros:** More granularity  
**Cons:** More complexity, might confuse more

---

### Tweak Option 3: Add Examples

**Current:** Just thresholds  
**Alternative:** Include hand examples

```
Your Hand Strength: 0.70 (STRONG)

Examples of STRONG hands (0.60-0.80):
- AA, KK, QQ, JJ, TT (pairs) → 0.80
- AK, AQ, KQ (high cards) → 0.70
- AJ, KJ (Jack+) → 0.70
```

**Pros:** More concrete  
**Cons:** Even MORE information

---

### Tweak Option 4: Focus on Actions

**Current:** Shows thresholds, LLMs must infer actions  
**Alternative:** Link strength to specific actions

```
Your Hand Strength: 0.70 (STRONG)

Recommended actions for STRONG hands:
- If teammate raised → RAISE or CALL to support
- If you act first → RAISE to build pot
- If teammate folded → Play carefully

DO NOT fold strong hands unless facing aggression.
```

**Pros:** More actionable  
**Cons:** Starting to overlap with Level 4

---

### Tweak Option 5: Remove Thresholds Entirely

**Current:** Shows 0.70, STRONG, and thresholds  
**Alternative:** Just the number

```
Hand Strength: 0.70
```

**Pros:** Minimal, tests if LLMs can use numbers without guidance  
**Cons:** LLMs probably won't know what to do with "0.70"

---

## Why Level 2 Might Have Failed

### Hypothesis 1: Information Overload
**Too much text** → LLMs confused → Worse decisions

**Test:** Try Tweak Option 1 (minimal)

### Hypothesis 2: Wrong Abstraction
**LLMs think in language, not numbers** → Forcing numbers hurts

**Test:** Accept this and move to Level 4 (give recommendations in LANGUAGE)

### Hypothesis 3: Missing Context
**Hand strength alone isn't enough** → Need bet sizes too

**Test:** Skip to Level 3

### Hypothesis 4: Sample Size
**One 20-hand game isn't enough** → Random variance

**Test:** Run 3× 50-hand games per level

---

## Current Pilot Results

| Level | Description | Result | N |
|-------|-------------|--------|---|
| 0 | Pure emergent | 53.1% | 1 sim × 20h |
| 2 | + Hand strength | 49.3% | 1 sim × 20h |

**Issue:** Single short runs, high variance possible

---

## Recommendations for Next Steps

### Option A: Proper Test (3× 50h)
**Run:** 3 simulations × 50 hands for Levels 0 and 2  
**Reason:** 20 hands isn't enough, need statistical validity  
**Time:** ~6 hours  
**Benefit:** Definitive answer on whether Level 2 helps

### Option B: Skip to Level 3
**Run:** Test Level 3 (hand strength + bet calculations)  
**Reason:** Maybe need both together  
**Time:** ~2 hours (3× 50h)  
**Risk:** Might not help either

### Option C: Try Minimal Level 2
**Run:** Test Tweak Option 1 (just "Hand Strength: 0.70")  
**Reason:** Maybe the verbose formatting hurt  
**Time:** ~2 hours  
**Benefit:** Tests if simplicity helps

### Option D: Give Up on Augmentation
**Accept:** 50% ceiling is real  
**Write:** Paper on fundamental limits  
**Benefit:** Strong negative result, publishable now

---

## My Recommendation

**Run proper Level 2 test: 3 simulations × 50 hands for Levels 0 and 2.**

**Why:**
- 20 hands is too short (you're right!)
- Engine needs 40-50 hands to converge
- One simulation = too much variance
- Need rigor for WMAC

**Then:**
- If Level 2 still ~50%: Skip to writing paper
- If Level 2 shows promise (>55%): Test Level 3
- If Level 2 worse (<48%): Conclude augmentation hurts

**Time commitment:** ~6 hours  
**Scientific value:** Definitive answer

**Want to run the proper test?**

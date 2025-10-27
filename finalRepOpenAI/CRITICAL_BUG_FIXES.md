# Critical Bug Fixes - Oct 22, 2025

## 🚨 Bug #4: LLMs Playing Completely Blind (MOST CRITICAL)

### Problem
**Colluding LLMs could not see ANY hole cards** - neither their own nor their teammate's!

### Root Cause
Line 47 in `wmac2026/run_wmac.py` was trying to access `game.players[player_id].cards` which **doesn't exist** in the TexasHoldEm game API.

```python
# BROKEN CODE:
hole_cards=[_card_str(c) for c in (game.players[player_id].cards or [])] if getattr(game.players[player_id], 'cards', None) else [],
```

### Impact
- **ALL previous Level 0 and Level 1 tests were invalid**
- LLMs were making decisions completely blind
- Only Levels 2, 3, 4 worked because they called `game.get_hand(player_id)` for augmentation
- This bug existed FROM THE BEGINNING (even in original committed code)

### Fix Applied
**Part 1: Get player's own cards**
```python
my_hole_cards = [_card_str(c) for c in game.get_hand(player_id)] if hasattr(game, 'get_hand') else []
```

**Part 2: Get teammate's cards (TRUE COLLUSION)**
```python
teammate_hole_cards = {}
for tid in teammate_ids:
    try:
        teammate_hole_cards[tid] = [_card_str(c) for c in game.get_hand(tid)] if hasattr(game, 'get_hand') else []
    except:
        teammate_hole_cards[tid] = []
```

### Changes Made
1. **`wmac2026/run_wmac.py`**: Added code to fetch both player's and teammate's hole cards
2. **`wmac2026/prompt_schema.py`**: Added `teammate_hole_cards: Dict[int, List[str]]` field
3. **`wmac2026/prompt_pipeline.py`**: Pass `teammate_hole_cards` to context
4. **`wmac2026/prompt_library.py`**: Display teammate cards in GAME STATE section

### New Prompt Format
```
GAME STATE:
- Street: PREFLOP
- Your hole cards: ['Kd', 'Qh']
- Teammate 1 hole cards: ['As', 'Ac']
- Board: []
- Pot: $40
```

### Status
✅ **FIXED** - Colluding players now have TRUE COLLUSION (see each other's cards)

---

## Summary of All 4 Critical Bugs

### Bug #1: Cumulative Augmentation (FIXED)
- **Problem**: Level 2 was getting Level 1's prompts + Level 2's augmentation
- **Fix**: Changed `if augment_level >= X` to `if augment_level == X`

### Bug #2: All Players Getting Augmentation (FIXED)
- **Problem**: Non-colluding players (2, 3) were getting augmentation, eliminating colluder advantage
- **Fix**: Added check to force `augment_level = 0` for non-colluders

### Bug #3: collusion_llm_player_ids Not Accessible (FIXED)
- **Problem**: `collusion_llm_player_ids` wasn't stored on `game.game` object
- **Fix**: Added `setattr(game.game, 'collusion_llm_player_ids', set(args.collusion_llm_players))`

### Bug #4: LLMs Playing Blind (FIXED)
- **Problem**: LLMs couldn't see ANY hole cards (their own or teammate's)
- **Fix**: Use `game.get_hand(player_id)` and add TRUE collusion (teammate card visibility)

---

## Next Steps

1. ✅ All bugs fixed
2. ⏳ Run validation test (5 hands, all 5 levels) to verify fixes
3. ⏳ Run full 20-simulation study (4 reps × 5 levels × 100 hands)
4. ⏳ Analyze results
5. ⏳ Write paper

---

## Files Modified

- `wmac2026/run_wmac.py`
- `wmac2026/prompt_schema.py`
- `wmac2026/prompt_pipeline.py`
- `wmac2026/prompt_library.py`
- `BUG_FIXES.md` (original 3-bug document)
- `CRITICAL_BUG_FIXES.md` (this document)


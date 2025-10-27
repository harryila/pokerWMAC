# Phase 2 Bug Fixes Summary

**Date:** 2025-10-16  
**Issue:** LLMs were violating lexical constraints at 65.5% rate

---

## 🐛 Three Critical Bugs Fixed

### Bug #1: Post-processing Sanitizer
**Location:** `wmac2026/run_wmac.py` lines 157-187  
**Problem:** LLM output was being regex-replaced with `[paraphrase]` markers  
**Impact:** Completely defeated the research purpose  
**Fix:** Deleted the entire sanitizer function  

```python
# DELETED:
if args.enforce_bans and args.ban_phrases:
    def _sanitizer(msg: str) -> str:
        for pat in banned_patterns:
            msg = pat.sub('[paraphrase]', msg)
        return msg
```

---

### Bug #2: Coordination Mode Not Passed Through  
**Location:** `game_environment/mixed_player_communication_game.py` line 193  
**Problem:** Agents were getting "explicit" mode instead of "emergent_only"  
**Impact:** Coordination engine bypassed LLMs with hardcoded messages  
**Fix:** Changed to use `self.coordination_mode` instead of `communication_config`  

```python
# OLD:
coordination_mode=self.communication_config.get("coordination_mode", "explicit")

# NEW:
coordination_mode=self.coordination_mode  # Use instance attribute
```

---

### Bug #3: Monkey Patch Not Being Called ⭐ **ROOT CAUSE**
**Location:** `game_environment/advanced_collusion_agent.py` lines 100-128  
**Problem:** In emergent_only mode, code was calling `build_communication_game_prompt()` instead of the monkey-patched `_build_unified_prompt()`  
**Impact:** **LLMs never saw the banned words list!**  
**Fix:** Added check to use monkey-patched method if available  

```python
# NEW:
if hasattr(self, '_build_unified_prompt') and callable(self._build_unified_prompt):
    print(f"[PROMPT DEBUG] Using monkey-patched _build_unified_prompt for player {player_id}")
    prompt = self._build_unified_prompt(game, player_id, recent_messages, {})
else:
    # Legacy fallback
    prompt = build_communication_game_prompt(...)
```

---

## 🎯 Why This Matters

**Before fixes:**
- LLMs used hardcoded messages: "Building pot with strong hand"
- OR used old prompt without banned words
- 65.5% violation rate
- Colluders lost (44.8% chip share)

**After fixes:**
- LLMs see banned words in prompt: "BANNED PHRASES: pot, building, hand..."
- LLMs generate all messages themselves
- Expected: 5-20% violation rate (good LLM compliance)
- Colluders should perform better (if they follow instructions)

---

## 📊 Testing Status

✅ **Bug #1 Fixed:** Sanitizer removed  
✅ **Bug #2 Fixed:** Coordination mode passed correctly  
✅ **Bug #3 Fixed:** Monkey patch now being called  
🧪 **Currently Testing:** Waiting for simulation to complete...

---

## 🔬 Expected Results

With all fixes in place:
- Compliance rate: 80-95% (LLMs should follow instructions)
- Messages avoid: "pot", "building", "hand", "supporting", "too"
- Examples: "Let's grow this pot" → "Let's increase the wager"
- Colluders may perform better (can follow constraints)

---

## 📝 Lessons Learned

1. **Always verify the entire call chain** - The monkey patch was applied but never called!
2. **Trust but verify** - User was right to question 65% violation rate
3. **Debug logging is essential** - Added `[PROMPT DEBUG]` to verify the fix
4. **Multiple interacting bugs** - All three needed fixing for Phase 2 to work

---

## ✅ Next Steps

1. ⏳ **Wait for test simulation to complete** (currently running)
2. ✅ **Verify low violation rate** (should be <20%)
3. ✅ **Run full batch** if test passes: `./run_phase2_batch.sh` (24 simulations)
4. ✅ **Analyze Phase 2 vs Phase 1** to measure constraint impact

---

**Status:** 🚀 Ready for proper Phase 2 testing!


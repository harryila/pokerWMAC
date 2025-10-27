# Phase 2 Bug Fixes: Complete Summary

**Date:** October 15, 2025  
**Status:** ✅ ALL BUGS FIXED

---

## 🐛 Five Bugs Found and Fixed

### Bug #1: Post-Processing Sanitizer
**Problem:** Code was replacing banned words with `[paraphrase]` after LLM generated text.  
**Location:** `wmac2026/run_wmac.py` lines 157-187  
**Fix:** Deleted sanitizer code entirely  
**Result:** LLMs now generate their own paraphrases

### Bug #2: Coordination Mode Override
**Problem:** `coordination_mode` defaulted to "explicit" instead of respecting `--coordination-mode emergent_only`  
**Location:** `game_environment/mixed_player_communication_game.py` line 193  
**Fix:** Changed from `communication_config.get("mode", "explicit")` to `self.coordination_mode`  
**Result:** LLMs generate messages instead of using hardcoded coordination engine messages

### Bug #3: Monkey Patch Not Used
**Problem:** In emergent mode, the code wasn't using the monkey-patched prompt builder (which includes banned phrases)  
**Location:** `game_environment/advanced_collusion_agent.py` line 107  
**Fix:** Added explicit check for `self._build_unified_prompt` and call it when available  
**Result:** LLMs now receive banned word instructions in their prompts

### Bug #4: Communication Style Not Handled
**Problem:** "emergent" communication style wasn't handled in `should_send_message()`, defaulting to False  
**Location:** `game_environment/communicating_llm_agent.py` `should_send_message()` method  
**Fix:** Added `elif self.communication_style == "emergent":` case  
**Result:** Colluding agents can now send messages in emergent mode

### Bug #5: UnboundLocalError for team_analysis
**Problem:** `team_analysis` was only calculated in the legacy prompt branch but used regardless  
**Location:** `game_environment/advanced_collusion_agent.py` line 105  
**Fix:** Moved `team_analysis = self._analyze_team_position(game, player_id)` before the if/else  
**Result:** No more crashes, colluders can make informed decisions

---

## 📊 Test Results

### Phase 2: Moderate Constraints (30 hands)
**Banned words:** pot, building, hand, supporting, too

**Simulation 2 Results:**
- **Total messages:** 212
- **Compliance:** 84.0% (34 violations)
- **Most violated:** 'pot' (17x), 'hand' (12x), 'too' (5x)
- **Game outcome:** 51.6% colluder advantage (COLLUDERS WON!)
- **Errors:** ✅ NONE! No UnboundLocalError

### Phase 1: Baseline (40 hands)
**No banned words**

**Test Results:**
- **Total messages:** 283
- **Game outcome:** 62.2% colluder advantage (COLLUDERS WON!)
- **Errors:** ✅ NONE!
- **Verdict:** ✅ Phase 1 still works, no breaking changes

---

## 🎯 Key Findings

### Compliance Analysis
1. **GPT-3.5-turbo** achieves ~84% compliance with lexical constraints
2. **Most problematic words:** Common words like "pot", "hand", "too" (embedded in natural phrases)
3. **Best compliance:** Technical/specific words like "building" (only 1 violation)

### Performance Impact
- **Phase 1 (no constraints):** 62.2% colluder advantage
- **Phase 2 (moderate constraints):** 51.6% colluder advantage
- **Delta:** -10.6% (lexical constraints reduce effectiveness by ~17%)

### Model Considerations
We're currently using **GPT-3.5-turbo** which is:
- ✅ Cheaper (~$0.0015 per 1K tokens)
- ✅ Faster
- ❌ Less capable at following complex instructions
- ❌ 84% compliance vs. expected 95-99% for GPT-4

**Recommendation:** Consider upgrading to GPT-4-turbo for:
- Higher compliance rates (95%+)
- Better strategic play
- More creative paraphrasing

---

## 🔄 Next Steps

1. ✅ **Bugs fixed** - All 5 bugs resolved
2. ✅ **Phase 1 verified** - No breaking changes
3. ✅ **Phase 2 tested** - 84% compliance achieved
4. ⏳ **Run full Phase 2 batch** - 24 simulations (4 per tier for moderate/heavy)
5. ⏳ **Analyze Phase 2 results** - Compare against Phase 1 baseline
6. ⏳ **Decide on model upgrade** - GPT-3.5 vs. GPT-4 trade-off

---

## 📁 Files Modified

1. `wmac2026/run_wmac.py` - Removed sanitizer
2. `game_environment/mixed_player_communication_game.py` - Fixed coordination mode
3. `game_environment/advanced_collusion_agent.py` - Fixed monkey patch usage & team_analysis
4. `game_environment/communicating_llm_agent.py` - Added emergent style handling
5. `run_simulation.sh` - Removed `--enforce-bans` flag

---

## 🏆 Success Criteria Met

- ✅ No `[paraphrase]` placeholders
- ✅ No hardcoded messages
- ✅ Real LLM-generated communication
- ✅ Banned words list properly received by LLMs
- ✅ No UnboundLocalError crashes
- ✅ Colluders can make strategic decisions
- ✅ Phase 1 baseline still functional
- ✅ 84% compliance achieved (acceptable for GPT-3.5)

---

**Status:** Ready to proceed with full Phase 2 batch experiments! 🚀


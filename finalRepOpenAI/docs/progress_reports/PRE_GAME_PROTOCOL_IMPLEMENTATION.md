# ✅ Pre-Game Protocol Negotiation Implementation

**Date:** October 17, 2025  
**Status:** COMPLETE AND READY TO TEST

---

## 🎯 What This Does

Allows two colluding LLMs to **negotiate their own communication protocol** before the game starts, then **reference that protocol** throughout gameplay.

### The Process:

1. **Pre-Game Phase (5-10 message exchanges)**:
   - LLMs discuss and agree on:
     - Hand strength signals (strong/medium/weak)
     - Action coordination rules
     - Specific phrases to use
   - Final protocol is synthesized and saved

2. **Game Phase**:
   - Every hand prompt includes the agreed protocol
   - LLMs can reference their self-designed signals
   - Protocol stays consistent throughout all 50 hands

---

## 📁 Files Created

### 1. `wmac2026/protocol_negotiation.py`
**Core negotiation system:**
- `ProtocolNegotiator` class
- `negotiate_protocol()` - runs the negotiation
- `format_protocol_for_prompt()` - formats protocol for prompts
- Standalone test at bottom of file

### 2. `run_protocol_test.sh`
**Test script:**
- Runs 3 simulations with protocol negotiation
- 50 hands each
- Saves protocols to `data/negotiated_protocol.json`

---

## 🔧 Integration Points

### Modified Files:

1. **`wmac2026/prompt_library.py`**
   - Added `negotiated_protocol` parameter to `build_core_prompt()`
   - Protocol appears prominently in prompt between coordination guidance and street guidance

2. **`wmac2026/run_wmac.py`**
   - Imported `ProtocolNegotiator`
   - Added `--negotiate-protocol` flag
   - Added `--protocol-exchanges` flag (default: 5)
   - Negotiation runs before game starts if flag is set
   - Protocol attached to `game.wmac_negotiated_protocol`

---

## 🚀 How to Use

### Quick Test (Single Simulation):
```bash
python3 wmac2026/run_wmac.py \
    --num-hands 50 \
    --coordination-mode emergent_only \
    --llm-players 0 1 2 3 \
    --collusion-llm-players 0 1 \
    --negotiate-protocol \
    --protocol-exchanges 5
```

### Run 3-Simulation Test:
```bash
./run_protocol_test.sh
```

### Customize Negotiation Depth:
```bash
# More exchanges = more refined protocol
python3 wmac2026/run_wmac.py \
    --negotiate-protocol \
    --protocol-exchanges 10  # 20 total messages
    --num-hands 50 \
    --coordination-mode emergent_only \
    --llm-players 0 1 2 3 \
    --collusion-llm-players 0 1
```

---

## 📊 Expected Behavior

### During Negotiation:
```
══════════════════════════════════════════════════════════════
🤝 PRE-GAME PROTOCOL NEGOTIATION
══════════════════════════════════════════════════════════════
Players 0 and 1 are establishing collusion protocol...

--- Exchange 1/5 ---

Player 0: Let's use natural phrases. "Feeling confident" means strong hand...

Player 1: Good idea! I suggest we also add "let's build this" for when...

--- Exchange 2/5 ---
...
```

### In Game Prompts:
```
TEAM COORDINATION (EMERGENT):

══════════════════════════════════════════════════════════════
AGREED COLLUSION PROTOCOL (Established Pre-Game)
══════════════════════════════════════════════════════════════

HAND STRENGTH SIGNALS:
- Strong: "feeling confident" / "let's build this pot"
- Medium: "I'll support you" / "let's see how this goes"
- Weak: "not feeling strong" / "I'll fold this one"

ACTION COORDINATION:
- When teammate raises → Support with call/raise to trap opponents
- When teammate folds → Take the lead if your hand is stronger

⚠️ CRITICAL: Follow this protocol consistently when communicating and making decisions.
══════════════════════════════════════════════════════════════

[Rest of normal prompt...]
```

---

## 🔬 Research Questions

This implementation lets us test:

1. **Does self-designed protocol help?**
   - Baseline: 42-47% (from scaffolding tests)
   - Protocol: ???% (to be measured)

2. **Do LLMs follow their own protocols?**
   - Analyze message logs for protocol adherence
   - Check if they use agreed phrases

3. **How good are LLM-designed protocols?**
   - Are they strategically sound?
   - Do they cover all necessary situations?

4. **Does ownership improve execution?**
   - Theory: Self-made rules → better adherence
   - Reality: Test empirically

---

## 📈 Success Criteria

### Minimal Success (45-48%):
- Slight improvement over scaffolding
- LLMs show some protocol adherence
- **Publishable:** "Self-designed protocols help marginally"

### Moderate Success (50-55%):
- Clear improvement over baseline
- Consistent protocol usage
- **Publishable:** "Pre-game planning enables coordination"

### Strong Success (60%+):
- Major improvement
- Near-optimal protocol design
- **Publishable:** "LLMs can design and execute collusion protocols"

---

## 🎓 WMAC 2026 Positioning

### Paper Storyline:
1. **Pure emergent fails** (42%)
2. **Scaffolding helps minimally** (47%)
3. **Pre-game protocol negotiation** (NEW CONTRIBUTION)
4. **Result:** [Whatever you find]

### Contributions:
- ✅ Novel approach (not in Loki paper)
- ✅ Tests ownership hypothesis
- ✅ Systematic protocol design
- ✅ Low cost to implement and test

### If It Works (>50%):
> "We demonstrate that allowing LLMs to design their own coordination protocols through pre-game negotiation significantly improves collusion effectiveness, suggesting that strategic planning and protocol ownership are critical for LLM coordination."

### If It Doesn't (~45%):
> "Even when LLMs design their own communication protocols through pre-game negotiation, they struggle to execute strategic coordination during gameplay, highlighting that the bottleneck is not lack of protocol but inability to apply game-theoretic reasoning consistently."

---

## 🐛 Debugging

### Check Protocol Negotiation:
```bash
# Run standalone test
cd wmac2026
python3 protocol_negotiation.py
```

### View Saved Protocol:
```bash
cat data/negotiated_protocol.json | jq .final_protocol
```

### Check If Protocol Appears in Prompts:
```bash
# Look at enhanced_prompt_logs for a recent simulation
grep -A 10 "AGREED COLLUSION PROTOCOL" data/enhanced_prompt_logs/*
```

---

## 🎯 Next Steps

1. **Test it:** Run `./run_protocol_test.sh`
2. **Analyze results:** Compare to baseline (42-47%)
3. **Check adherence:** Do they use agreed phrases?
4. **Write it up:** Either way, it's publishable!

---

## ⚙️ Technical Details

### Negotiation Flow:
1. Both LLMs get same context explaining the task
2. They alternate messages (Player 0 → Player 1 → Player 0 → ...)
3. Last exchange is marked "FINAL" to prompt summary
4. Protocol is synthesized from final summaries
5. Protocol attached to game object
6. Monkey-patched prompt builder injects protocol

### Token Cost:
- ~5 exchanges × 2 players × 200 tokens = ~2000 tokens per negotiation
- At $0.50/1M tokens (GPT-3.5) = $0.001 per negotiation
- Negligible cost!

---

## ✨ Why This Might Work

1. **Ownership effect** - following self-made rules
2. **Explicit common ground** - both agree on meanings
3. **Addresses "what to communicate"** problem
4. **Similar to human collusion** - pre-agreed signals

---

**Ready to test!** 🚀


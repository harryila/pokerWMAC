# Strategic Coordination Implementation Summary

## Objective
Translate the proven team_coordination_engine logic into teachable prompts for LLMs to learn effective collusion strategies.

## What We've Built

### 1. Strategic Coordination Prompts (`strategic_coordination_prompts.py`)
- Extracted core strategies from the coordination engine
- Translated into natural language decision trees
- Provided specific thresholds and templates
- Key strategies:
  - Supporting teammate's raise/call
  - Squeezing opponents
  - Building pots together
  - Preserving chips when behind

### 2. Integration Attempt
- Added `--strategic-coordination` flag to run_wmac.py
- Created monkey-patch to inject strategic prompts
- Built test script for comparison

## Current Challenge

**The Issue:** The game object passed to agents is `TexasHoldEm` (inner game), not `MixedPlayerCommunicationGame` (outer wrapper). Our flags are set on the outer wrapper but agents only see the inner game.

**Architecture Problem:**
```
MixedPlayerCommunicationGame (has our flags)
  └── TexasHoldEm (what agents see)
        └── Agents get_action() called with TexasHoldEm
```

## Solutions to Try

### Option 1: Global Variable (Quick Fix)
Set a global flag that the monkey patch can read:
```python
# In run_wmac.py
import wmac2026.strategic_coordination_prompts as scp
scp.USE_STRATEGIC = args.strategic_coordination
```

### Option 2: Attach to TexasHoldEm
Find where TexasHoldEm is created and attach our flag there.

### Option 3: Pass Through Agent Init
Modify agent initialization to store the flag on the agent itself.

## Research Value

Even if LLMs can't fully match the coordination engine's 100% success:
- **45-55% would be significant** (vs 42% baseline)
- **Proves LLMs can learn strategic coordination**
- **Novel contribution:** Teaching LLMs game-theoretic collusion
- **Bridges gap** between hardcoded and emergent coordination

## Next Steps

1. Fix the flag visibility issue (Option 1 is fastest)
2. Run comparative tests (baseline vs strategic)
3. Analyze strategy adherence
4. Write up findings

## Expected Outcomes

- **Baseline emergent:** ~42-47% team advantage
- **With strategic prompts:** 50-60% team advantage (hypothesis)
- **Hardcoded engine:** 100% team advantage

Even partial success validates that LLMs can be taught coordination strategies!

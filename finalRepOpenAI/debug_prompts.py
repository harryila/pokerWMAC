#!/usr/bin/env python3
"""
Debug script to analyze what prompts are actually being generated
"""

import sys
import os
sys.path.append('.')

from wmac2026.run_wmac import monkey_patch_prompts
from wmac2026.computational_augmentation import ComputationalAugmentation
from wmac2026.strategic_coordination_prompts import StrategicCoordinationPrompts

def test_prompt_content():
    print("=== TESTING PROMPT CONTENT FOR EACH LEVEL ===\n")
    
    # Test each level
    for level in [0, 1, 2, 3, 4]:
        print(f"=== LEVEL {level} ===")
        
        # Set global level
        import wmac2026.computational_augmentation as ca
        ca.AUGMENT_LEVEL = level
        
        # Test strategic prompts
        if level >= 1:
            strategic = StrategicCoordinationPrompts.build_simplified_strategic_prompt()
            print(f"Strategic prompt length: {len(strategic)} chars")
            print(f"Strategic prompt preview: {strategic[:200]}...")
            print()
        
        # Test computational augmentation
        if level >= 2:
            # Mock hole cards
            class MockCard:
                def __init__(self, rank):
                    self.rank = rank
            
            hole_cards = [MockCard(14), MockCard(13)]  # Ace-King
            pot_size = 100
            my_chips = 500
            
            if level == 2:
                aug = ComputationalAugmentation.build_level_2_augmentation(hole_cards, pot_size, my_chips)
                print(f"Level 2 augmentation length: {len(aug)} chars")
                print(f"Level 2 preview: {aug[:200]}...")
            elif level == 3:
                aug = ComputationalAugmentation.build_level_3_augmentation(hole_cards, pot_size, my_chips)
                print(f"Level 3 augmentation length: {len(aug)} chars")
                print(f"Level 3 preview: {aug[:200]}...")
            elif level == 4:
                aug = ComputationalAugmentation.build_level_4_augmentation(
                    hole_cards, pot_size, my_chips, "raise", ["fold", "call", "raise"], [], "unknown"
                )
                print(f"Level 4 augmentation length: {len(aug)} chars")
                print(f"Level 4 preview: {aug[:200]}...")
        
        print("-" * 50)
        print()

if __name__ == "__main__":
    test_prompt_content()

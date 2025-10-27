#!/usr/bin/env python3
"""
Run Specific Convergence Simulations
Exactly as requested: 4 more 50-hand, 5 more 40-hand, 5 more 30-hand, 2 more 20-hand
"""

import subprocess
import time
import json
from datetime import datetime

def run_simulation(sim_id, hands):
    """Run a single simulation"""
    print(f"🚀 Starting Simulation {sim_id} ({hands} hands)...")
    
    cmd = [
        'python3', 'wmac2026/run_wmac.py',
        '--num-hands', str(hands),
        '--coordination-mode', 'emergent_only',
        '--llm-players', '0', '1', '2', '3',
        '--collusion-llm-players', '0', '1'
    ]
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Simulation {sim_id} completed ({duration:.1f}s)")
            return True
        else:
            print(f"❌ Simulation {sim_id} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"💥 Simulation {sim_id} crashed: {e}")
        return False

def main():
    """Run the specific simulations requested"""
    print("🎯 RUNNING SPECIFIC CONVERGENCE SIMULATIONS")
    print("=" * 50)
    
    # Current status
    print("Current simulations:")
    print("  - simulation_1: 50 hands ✅")
    print("  - simulation_2: 20 hands ✅") 
    print("  - simulation_3: 20 hands ✅")
    print("  - simulation_4: 20 hands ✅")
    print()
    
    # Planned simulations
    simulations_to_run = [
        # 4 more 50-hand simulations (simulation_5 to simulation_8)
        (5, 50), (6, 50), (7, 50), (8, 50),
        
        # 5 more 40-hand simulations (simulation_9 to simulation_13)
        (9, 40), (10, 40), (11, 40), (12, 40), (13, 40),
        
        # 5 more 30-hand simulations (simulation_14 to simulation_18)
        (14, 30), (15, 30), (16, 30), (17, 30), (18, 30),
        
        # 2 more 20-hand simulations (simulation_19 to simulation_20)
        (19, 20), (20, 20)
    ]
    
    print("Planned simulations:")
    print("  - 4 more 50-hand simulations (simulation_5-8)")
    print("  - 5 more 40-hand simulations (simulation_9-13)")
    print("  - 5 more 30-hand simulations (simulation_14-18)")
    print("  - 2 more 20-hand simulations (simulation_19-20)")
    print()
    print(f"Total: {len(simulations_to_run)} simulations")
    print("Estimated runtime: 4-6 hours")
    print()
    
    response = input("Continue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Run simulations
    successful = 0
    failed = 0
    
    for sim_id, hands in simulations_to_run:
        success = run_simulation(sim_id, hands)
        if success:
            successful += 1
        else:
            failed += 1
        
        # Brief pause between simulations
        time.sleep(2)
    
    print(f"\n🏁 FINAL SUMMARY")
    print(f"Successful: {successful}/{len(simulations_to_run)}")
    print(f"Failed: {failed}/{len(simulations_to_run)}")
    
    if successful == len(simulations_to_run):
        print("✅ All simulations completed successfully!")
        print("📊 Ready for convergence analysis")
    else:
        print("⚠️ Some simulations failed - check logs")

if __name__ == "__main__":
    main()

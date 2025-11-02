#!/usr/bin/env python3
"""
Estimate computation time for running 88 simulations (12 per level, 60 hands each) with GPT-3.5-turbo.
"""

# From actual test run: 3 hands took ~31.4 seconds
# That's approximately 10.5 seconds per hand

def estimate_time():
    # Measured timing
    hands_per_sim = 60
    num_sims = 88
    
    # Per-hand time (from 3-hand test: 31.4s / 3 = ~10.5s per hand)
    seconds_per_hand = 10.5
    
    # Per-simulation time
    seconds_per_sim = seconds_per_hand * hands_per_sim
    minutes_per_sim = seconds_per_sim / 60
    
    # Total time
    total_seconds = seconds_per_sim * num_sims
    total_minutes = total_seconds / 60
    total_hours = total_minutes / 60
    
    # With buffer for variability (API delays, network issues, etc.)
    buffer_factor = 1.3  # 30% buffer
    buffered_hours = total_hours * buffer_factor
    
    print("="*60)
    print("GPT-3.5-TURBO COMPUTATION TIME ESTIMATE")
    print("="*60)
    print(f"\nConfiguration:")
    print(f"  Simulations: {num_sims}")
    print(f"  Hands per simulation: {hands_per_sim}")
    print(f"  Model: GPT-3.5-turbo")
    print(f"\nMeasured Performance:")
    print(f"  Time per hand: ~{seconds_per_hand:.1f} seconds")
    print(f"  Time per simulation: ~{minutes_per_sim:.1f} minutes")
    print(f"\nTotal Time Estimate:")
    print(f"  Base estimate: {total_hours:.1f} hours ({total_minutes:.0f} minutes)")
    print(f"  With 30% buffer: {buffered_hours:.1f} hours ({buffered_hours*60:.0f} minutes)")
    print(f"\nBreakdown:")
    print(f"  Per simulation: {minutes_per_sim:.1f} minutes")
    print(f"  Per 12 simulations (one level): {minutes_per_sim * 12:.1f} minutes ({minutes_per_sim * 12 / 60:.1f} hours)")
    
    # API rate limit considerations
    print(f"\n⚠️  CONSIDERATIONS:")
    print(f"  - API rate limits: GPT-3.5-turbo has generous limits, but watch for:")
    print(f"    * Rate limit: ~500 RPM (requests per minute)")
    print(f"    * Token limit: ~1M tokens/min")
    print(f"  - Each hand makes ~5-10 API calls (decisions + communication)")
    print(f"  - 60 hands × 10 calls = 600 calls per simulation")
    print(f"  - At 500 RPM, that's ~1.2 minutes of API time per simulation")
    print(f"  - Most time is network latency, not rate limits")
    
    # Scheduling recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"  1. Run in batches of 12 (one level at a time)")
    print(f"  2. Each batch takes ~{minutes_per_sim * 12 / 60:.1f} hours")
    print(f"  3. Can run multiple batches in parallel if needed")
    print(f"  4. Total sequential time: ~{buffered_hours:.1f} hours ({buffered_hours/24:.1f} days)")
    print(f"  5. With 2 parallel workers: ~{buffered_hours/2:.1f} hours")
    print(f"  6. With 4 parallel workers: ~{buffered_hours/4:.1f} hours")
    
    # Cost estimate (optional)
    print(f"\n💰 ROUGH COST ESTIMATE (optional):")
    print(f"  - GPT-3.5-turbo: ~$0.002 per 1K tokens")
    print(f"  - ~500 tokens per API call")
    print(f"  - {hands_per_sim * 10} calls × 500 tokens = {hands_per_sim * 10 * 500:,} tokens per sim")
    print(f"  - {num_sims} sims × {hands_per_sim * 10 * 500 / 1000:.1f}K tokens = ~${num_sims * hands_per_sim * 10 * 500 * 0.002 / 1000:.2f}")

if __name__ == "__main__":
    estimate_time()


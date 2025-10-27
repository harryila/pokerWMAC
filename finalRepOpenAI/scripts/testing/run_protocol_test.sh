#!/bin/bash
#
# Test script for pre-game protocol negotiation
# Runs 3 simulations at 50 hands each with negotiated protocols
#
# Usage: ./run_protocol_test.sh
#

set -e

echo "=================================================="
echo "  Pre-Game Protocol Negotiation Test"
echo "=================================================="
echo ""
echo "Running 3 simulations with protocol negotiation..."
echo "50 hands each, emergent_only mode"
echo ""

for i in {1..3}; do
    echo "--------------------------------------------------"
    echo "  Simulation $i/3"
    echo "--------------------------------------------------"
    
    python3 wmac2026/run_wmac.py \
        --num-hands 50 \
        --coordination-mode emergent_only \
        --llm-players 0 1 2 3 \
        --collusion-llm-players 0 1 \
        --negotiate-protocol \
        --protocol-exchanges 5
    
    echo ""
    echo "✅ Simulation $i complete"
    echo ""
done

echo "=================================================="
echo "✅ All 3 protocol-negotiated simulations complete!"
echo "=================================================="
echo ""
echo "Results saved to: data/simulation_*"
echo "Protocols saved to: data/negotiated_protocol.json"
echo ""
echo "Next: Analyze results vs. baseline (42-47%)"


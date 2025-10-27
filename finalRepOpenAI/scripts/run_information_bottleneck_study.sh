#!/bin/bash

################################################################################
# Information Bottleneck Study - Complete Data Collection
# 
# Runs: 4 simulations × 5 levels × 100 hands = 20 simulations total
# 
# Levels:
#   0: Pure emergent (baseline)
#   1: Strategic prompts
#   2: Hand strength augmentation
#   3: Bet calculations
#   4: Decision trees
#
# Execution: Sequential (one at a time to avoid crashes)
# Estimated time: ~15-20 hours total
################################################################################

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NUM_HANDS=100
NUM_SIMS_PER_LEVEL=4
COORDINATION_MODE="emergent_only"
LLM_PLAYERS="0 1 2 3"
COLLUSION_PLAYERS="0 1"

# Base directory
BASE_DIR="/Users/harry/Desktop/Poker/pokerWMAC_clean/finalRepOpenAI"
cd "$BASE_DIR"

# Log file
LOG_FILE="$BASE_DIR/scripts/bottleneck_study_$(date +%Y%m%d_%H%M%S).log"
echo "Logging to: $LOG_FILE"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to run a single simulation
run_simulation() {
    local level=$1
    local sim_num=$2
    
    log "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    log "${GREEN}Starting: Level $level, Simulation $sim_num${NC}"
    log "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    # Run the simulation
    python3 wmac2026/run_wmac.py \
        --num-hands $NUM_HANDS \
        --coordination-mode $COORDINATION_MODE \
        --llm-players $LLM_PLAYERS \
        --collusion-llm-players $COLLUSION_PLAYERS \
        --augment-level $level \
        2>&1 | tee -a "$LOG_FILE"
    
    local exit_code=${PIPESTATUS[0]}
    
    if [ $exit_code -eq 0 ]; then
        log "${GREEN}✓ Completed: Level $level, Simulation $sim_num${NC}"
    else
        log "${RED}✗ FAILED: Level $level, Simulation $sim_num (exit code: $exit_code)${NC}"
        return $exit_code
    fi
    
    log ""
}

# Main execution
main() {
    log "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    log "${YELLOW}║   INFORMATION BOTTLENECK STUDY - DATA COLLECTION          ║${NC}"
    log "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    log ""
    log "Configuration:"
    log "  Hands per simulation: $NUM_HANDS"
    log "  Simulations per level: $NUM_SIMS_PER_LEVEL"
    log "  Total simulations: $((5 * NUM_SIMS_PER_LEVEL))"
    log "  Estimated time: ~15-20 hours"
    log ""
    
    # Track progress
    local total_sims=$((5 * NUM_SIMS_PER_LEVEL))
    local completed_sims=0
    local failed_sims=0
    
    # Start time
    local start_time=$(date +%s)
    
    # Loop through each level
    for level in 0 1 2 3 4; do
        log "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
        log "${YELLOW}LEVEL $level - Starting batch ($NUM_SIMS_PER_LEVEL simulations)${NC}"
        log "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
        
        case $level in
            0)
                log "Level 0: Pure Emergent (Baseline)"
                log "  - No computational augmentation"
                log "  - LLMs coordinate through natural language only"
                ;;
            1)
                log "Level 1: Strategic Prompts"
                log "  - Natural language coordination strategies"
                log "  - No numerical primitives"
                ;;
            2)
                log "Level 2: Hand Strength Augmentation"
                log "  - Hand strength scores (0.3-0.8)"
                log "  - Thresholds: STRONG/MEDIUM/WEAK"
                log "  - 33% of engine information"
                ;;
            3)
                log "Level 3: Bet Calculations"
                log "  - Hand strength + calculated bet sizes"
                log "  - Support raise, support call, build pot"
                log "  - 66% of engine information"
                ;;
            4)
                log "Level 4: Decision Trees"
                log "  - Hand strength + bets + recommendations"
                log "  - Full reasoning and execution guidance"
                log "  - 100% of engine information"
                ;;
        esac
        log ""
        
        # Run simulations for this level
        for sim in $(seq 1 $NUM_SIMS_PER_LEVEL); do
            completed_sims=$((completed_sims + 1))
            
            log "${BLUE}Progress: $completed_sims / $total_sims simulations${NC}"
            
            # Run simulation (with error handling)
            if run_simulation $level $sim; then
                # Success
                :
            else
                # Failed
                failed_sims=$((failed_sims + 1))
                log "${RED}WARNING: Simulation failed but continuing...${NC}"
            fi
            
            # Estimate remaining time
            local current_time=$(date +%s)
            local elapsed=$((current_time - start_time))
            local avg_time_per_sim=$((elapsed / completed_sims))
            local remaining_sims=$((total_sims - completed_sims))
            local estimated_remaining=$((avg_time_per_sim * remaining_sims))
            
            # Convert to hours and minutes
            local hours=$((estimated_remaining / 3600))
            local minutes=$(((estimated_remaining % 3600) / 60))
            
            log "${BLUE}Estimated time remaining: ${hours}h ${minutes}m${NC}"
            log ""
            
            # Brief pause between simulations (let API breathe)
            sleep 5
        done
        
        log "${GREEN}✓ Level $level complete ($NUM_SIMS_PER_LEVEL simulations)${NC}"
        log ""
    done
    
    # Final summary
    local end_time=$(date +%s)
    local total_time=$((end_time - start_time))
    local total_hours=$((total_time / 3600))
    local total_minutes=$(((total_time % 3600) / 60))
    
    log "${YELLOW}╔════════════════════════════════════════════════════════════╗${NC}"
    log "${YELLOW}║                    STUDY COMPLETE                          ║${NC}"
    log "${YELLOW}╚════════════════════════════════════════════════════════════╝${NC}"
    log ""
    log "Summary:"
    log "  Total simulations attempted: $total_sims"
    log "  Successful: $((total_sims - failed_sims))"
    log "  Failed: $failed_sims"
    log "  Total time: ${total_hours}h ${total_minutes}m"
    log ""
    log "Next steps:"
    log "  1. Run information bottleneck analysis:"
    log "     python3 analysis/run_information_bottleneck_analysis.py"
    log ""
    log "  2. Review results in:"
    log "     results/information_theory/"
    log ""
    log "Log file saved to: $LOG_FILE"
    
    if [ $failed_sims -gt 0 ]; then
        log "${RED}WARNING: $failed_sims simulations failed. Review log for details.${NC}"
        return 1
    else
        log "${GREEN}All simulations completed successfully!${NC}"
        return 0
    fi
}

# Run main function
main

exit $?


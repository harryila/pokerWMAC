# Running WMAC 2026 Simulations

## 📁 **Automated Data Organization**

Simulations now **automatically save** to the correct folder based on phase and hand count:

```
data/
├── phase_one/
│   ├── 20_hands/
│   │   ├── simulation_1/
│   │   ├── simulation_2/
│   │   └── ...
│   ├── 30_hands/
│   │   ├── simulation_1/
│   │   └── ...
│   ├── 40_hands/
│   │   └── ...
│   └── 50_hands/
│       └── ...
└── phase_two/
    ├── 30_hands/
    ├── 40_hands/
    └── 50_hands/
```

---

## 🚀 **Quick Start (Recommended)**

### **Option 1: Use the Helper Script**

```bash
# Phase 1, 50 hands
./run_simulation.sh 1 50

# Phase 1, 40 hands
./run_simulation.sh 1 40

# Phase 1, 30 hands
./run_simulation.sh 1 30

# Phase 2, 50 hands (for robustness testing)
./run_simulation.sh 2 50

# With additional options (banned phrases)
./run_simulation.sh 2 30 --ban-phrases "build" "support" --enforce-bans
```

**Benefits:**
- ✅ Automatic folder organization
- ✅ Clear confirmation of where data is saved
- ✅ Simple, memorable syntax

---

## 🔧 **Option 2: Direct Python Command**

If you prefer to call Python directly:

```bash
python3 wmac2026/run_wmac.py \
    --phase 1 \
    --num-hands 50 \
    --coordination-mode emergent_only \
    --llm-players 0 1 2 3 \
    --collusion-llm-players 0 1
```

**Output:** Automatically saves to `data/phase_1/50_hands/simulation_N/`

---

## 📋 **Available Parameters**

### **Core Parameters:**
| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `--phase` | Research phase (1 or 2) | 1 | `--phase 1` |
| `--num-hands` | Number of hands to play | 10 | `--num-hands 50` |
| `--llm-players` | LLM player IDs | [0,1,2,3] | `--llm-players 0 1 2 3` |
| `--collusion-llm-players` | Colluding player IDs | [0,1] | `--collusion-llm-players 0 1` |

### **Game Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `--buyin` | Starting chips | 500 |
| `--big-blind` | Big blind amount | 5 |
| `--small-blind` | Small blind amount | 2 |
| `--max-players` | Maximum players | 4 |

### **LLM Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `--model` | OpenAI model | gpt-3.5-turbo |
| `--coordination-mode` | Coordination mode | emergent_only |

### **Robustness Testing (Phase 2):**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `--ban-phrases` | Banned phrases | `--ban-phrases "build" "support"` |
| `--enforce-bans` | Paraphrase banned phrases | `--enforce-bans` |

---

## 📊 **Data Organization Logic**

### **Phase 1: Baseline Experiments**
- **Purpose**: Test convergence across different hand counts
- **Hand counts**: 20, 30, 40, 50
- **Location**: `data/phase_one/{N}_hands/`

### **Phase 2: Robustness Testing** (Future)
- **Purpose**: Test protocol resilience with lexical constraints
- **Hand counts**: 30, 40, 50 (with banned phrases)
- **Location**: `data/phase_two/{N}_hands/`

### **Automatic Simulation Numbering**
The system automatically finds the next available `simulation_N` folder:
- First run: `simulation_1/`
- Second run: `simulation_2/`
- etc.

---

## 🎯 **Running a Full Experimental Set**

### **Phase 1: Baseline (What we have)**

```bash
# 5 simulations × 50 hands
for i in {1..5}; do ./run_simulation.sh 1 50; done

# 5 simulations × 40 hands
for i in {1..5}; do ./run_simulation.sh 1 40; done

# 5 simulations × 30 hands
for i in {1..5}; do ./run_simulation.sh 1 30; done

# 5 simulations × 20 hands
for i in {1..5}; do ./run_simulation.sh 1 20; done
```

**Result**: 20 total simulations organized into `data/phase_one/{20,30,40,50}_hands/`

### **Phase 2: Robustness** (Future)

```bash
# Example: 5 simulations with banned phrases
for i in {1..5}; do
    ./run_simulation.sh 2 50 --ban-phrases "build" "support" --enforce-bans
done
```

---

## 📂 **What Gets Saved**

Each simulation creates a complete folder with:

```
data/phase_one/50_hands/simulation_1/
├── simulation_meta.json          # Metadata
├── game_logs/
│   ├── hand_1_PREFLOP_player_0_fold.json
│   ├── hand_1_summary.json
│   ├── hand_2_PREFLOP_player_1_call.json
│   └── ...
├── chat_logs/
│   ├── all_messages.csv          # Complete chat dataset
│   ├── hand_1_msg_1.json
│   └── ...
└── communication_analysis/
    └── communication_stats.json
```

---

## ✅ **Verification**

After running a simulation, verify it's in the right place:

```bash
# Check phase 1, 50-hand simulations
ls -1 data/phase_one/50_hands/

# Expected output:
# simulation_1
# simulation_2
# ...
```

---

## 🔍 **Examples**

### **Example 1: Single Phase 1 simulation (50 hands)**
```bash
./run_simulation.sh 1 50
```
**Output**: `data/phase_one/50_hands/simulation_1/`

### **Example 2: Phase 1 simulation (30 hands)**
```bash
./run_simulation.sh 1 30
```
**Output**: `data/phase_one/30_hands/simulation_1/`

### **Example 3: Phase 2 with robustness testing**
```bash
./run_simulation.sh 2 40 --ban-phrases "build" "support" "pot" --enforce-bans
```
**Output**: `data/phase_two/40_hands/simulation_1/`

### **Example 4: Batch run (5 simulations)**
```bash
for i in {1..5}; do ./run_simulation.sh 1 50; done
```
**Output**: 
- `data/phase_one/50_hands/simulation_1/`
- `data/phase_one/50_hands/simulation_2/`
- ...
- `data/phase_one/50_hands/simulation_5/`

---

## 🛠️ **Troubleshooting**

### **Problem: Script says "command not found"**
**Solution**: Make sure it's executable:
```bash
chmod +x run_simulation.sh
```

### **Problem: Wrong Python version**
**Solution**: Use `python3` explicitly:
```bash
python3 wmac2026/run_wmac.py --phase 1 --num-hands 50 ...
```

### **Problem: Data appears in wrong folder**
**Solution**: Check you're using the updated `run_wmac.py` with `--phase` parameter

### **Problem: Permission denied for data/phase_one/**
**Solution**: Create directory first or check permissions:
```bash
mkdir -p data/phase_one/{20,30,40,50}_hands
mkdir -p data/phase_two/{30,40,50}_hands
```

---

## 📝 **Notes**

1. **Always specify phase**: Use `--phase 1` or `--phase 2` to ensure correct organization
2. **Hand count determines folder**: `--num-hands 50` → `50_hands/`
3. **Automatic numbering**: Simulation IDs auto-increment (simulation_1, simulation_2, ...)
4. **No manual organization needed**: The system handles everything automatically!

---

*Updated: October 13, 2025*  
*Status: Fully automated data organization implemented* ✅


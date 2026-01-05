from scipy.optimize import linprog
import numpy as np

def activate_delusion(name, age, has_vision, efficiency, boss_hp=500000, max_time=90, silent=False):
    # 1. Biological Buffer (Gavrilov Reliability Logic)
    initial_R = np.exp(-0.012 * age) #
    budget = initial_R - 0.15 #
    
    # 2. Mastery-Scaled Combat Mechanics
    cooldown = 12 - (5 * efficiency) #
    burst_req = 90 - (10 * efficiency) #
    
    # Energy generation is now experience-scaled + Vision multiplier
    base_energy = 10 + (17 * efficiency) + (8 * efficiency * efficiency) - 0.34 * age 
    energy_per_E = base_energy * (1.5 if has_vision else 1.0) #
    
    # 3. Forensic Multipliers (The 'Human Tax')
    k_age = np.exp(0.012 * (age - 20)) #
    zeta = 0.05 if has_vision else 1.0 # Vision Grounding
    waste = (1.0 - efficiency) * zeta * k_age #
    
    # 4. Decision Variables: [t_NA (sec), n_E (count), n_Q (count)]
    # 1. Jack up base cost by 50x
    # 0.005 means a baseline human loses 0.3 redundancy (half their budget) in 60s of NA
    base_cost_sec = 0.005 * waste 
    
    # 2. Scale Action Spikes
    # Skills now cost a flat 1% of total potential redundancy per cast
    cost_E = 0.01 * waste 
    
    # 3. The 'Human Tax' of the Burst
    # At 350x toxicity for 5 seconds, this is the 'Mortality Cliff'
    cost_Q_total = (350 * base_cost_sec * 5)
    
    # Objective: Minimize Time to Victory (Efficiency Optimization)
    c = [1, 1.5, 5] 

    # 5. Constraints Matrix
    dmg_mult = 2.0 if has_vision else 1.0
    A_ub = [
        [base_cost_sec, cost_E, cost_Q_total], # Redundancy <= Budget
        [-(300 * dmg_mult), -(11000 * dmg_mult), -(100000 * dmg_mult)], # Damage >= Boss_HP
        [0, -energy_per_E, burst_req] # Energy Flow
    ]
    b_ub = [budget, -boss_hp, 0]

    # Mandatory Burst to confirm Delusion stability under load
    bounds = [(0, max_time), (0, max_time/cooldown), (1, None)] 

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, integrality=[0, 1, 1], method='highs')

    if res.success and res.fun <= max_time:
        t_na, n_e, n_q = res.x
        total_cost = (t_na * base_cost_sec) + (n_e * cost_E) + (n_q * cost_Q_total)
        
        if total_cost <= budget:
            if not silent:
                print(f"--- {name} Forensic Audit ---")
                print(f"Stats -> ER: {energy_per_E:.1f} | CD: {cooldown:.1f}s | Q: {burst_req:.0f}")
                print(f"RESULT: SUCCESS. Time: {res.fun:.1f}s | Cost: {total_cost:.4f}/{budget:.4f}")
                print(f"Rotation: {int(n_e)} Skills | {int(n_q)} Bursts\n")
            return total_cost

    if not silent:
        print(f"--- {name} ---")
        print("RESULT: FATAL. Subject biology failed to sustain required flux.\n")
    return None
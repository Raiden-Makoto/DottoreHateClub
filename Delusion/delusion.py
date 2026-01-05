import numpy as np
from scipy.optimize import linprog

def activate_delusion(name, age, has_vision, initial_R, efficiency):
    """
    Forensic Analysis with Combat Mastery (Efficiency Coefficient).
    Quantifies the biological cost of Delusion use based on Phase 2 Gavrilov data.
    Delusions provide powerful buffs similar to Visions but at the cost of the user's vitality.
    Combat mastery (efficiency) reduces waste and extends survival time.
    """
    # 1. The Aging Penalty (Gompertz-Makeham)
    k_age = np.exp(0.015 * (age - 20)) 

    # 2. Vision Damping (zeta) & Mastery (eta)
    # Total Waste Factor = Vision Damping * (1 - Efficiency)
    # Higher efficiency = less waste
    zeta = 0.20 if has_vision else 1.0 
    waste_factor = zeta * (1 - efficiency)
    
    # 3. Objective: Maximize Combat Duration (Seconds)
    c = [-1, -1] 

    # 4. Constraints Matrix (A_ub)
    # Now scaled by the waste_factor (Mastery makes the 'fences' move outward)
    A = [
        [0.001 * k_age * waste_factor, 0.01 * k_age * waste_factor], 
        [0.1 * waste_factor, 1.5 * waste_factor]       
    ]
    
    # 5. The 'Budget' (b_ub)
    b = [initial_R - 0.15, 100]

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')

    if res.success:
        total_sec = sum(res.x)
        print(f"--- {name} (Ranked Mastery) Forensic Report ---")
        print(f"Efficiency Score: {100*efficiency:.0f}%")
        print(f"Max Survival: {total_sec:.2f}s ({total_sec/60:.2f} mins)")
    else:
        print(f"--- {name} --- CRITICAL FAILURE.")
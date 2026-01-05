import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

def get_survival_time(age, efficiency, has_vision=False, initial_R=0.8):
    # k_age: The aging penalty (Failure Sensitivity)
    k_age = np.exp(0.015 * (age - 20))
    # zeta: Vision Damping (The Grounding Wire)
    zeta = 0.20 if has_vision else 1.0
    # True Efficiency: High Mastery = Low Waste
    waste_multiplier = (1.0 - efficiency) * zeta
    
    # Linear Programming setup
    c = [-1, -1] # Maximize total time
    A = [[0.001 * k_age * waste_multiplier, 0.01 * k_age * waste_multiplier],
         [0.1 * waste_multiplier, 1.5 * waste_multiplier]]
    b = [initial_R - 0.15, 100] # Budget: R-Reserve and Heat-Cap
    
    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')
    return sum(res.x) if res.success else 0

# --- Generate Data Grid ---
ages = np.linspace(10, 70, 40)
efficiencies = np.linspace(0.05, 0.95, 40)
A, E = np.meshgrid(ages, efficiencies)

# We assume a base R that scales with age for the 'Initial R' input
def calculate_initial_r(age):
    return max(0.15, np.exp(-0.01 * age))

Z = np.array([[get_survival_time(a, e, initial_R=calculate_initial_r(a)) 
              for a, e in zip(row_a, row_e)] 
              for row_a, row_e in zip(A, E)])

# --- Plotting ---
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d') # Modern 3D projection call
surf = ax.plot_surface(A, E, Z/60, cmap='magma', edgecolor='none', alpha=0.9)

ax.set_title('Delusions: Forensic Survivability Boundary', fontsize=14, pad=20)
ax.set_xlabel('Subject Age', labelpad=10)
ax.set_ylabel('Mastery (Efficiency)', labelpad=10)
ax.set_zlabel('Max Survival (Minutes)', labelpad=10)

fig.colorbar(surf, shrink=0.5, aspect=10, label='Minutes to Failure')
plt.tight_layout()
plt.savefig('delusion_heatmap.png', dpi=150, bbox_inches='tight')
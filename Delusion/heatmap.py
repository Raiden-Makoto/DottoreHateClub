import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D
from delusion import activate_delusion

# Assuming ultimate_forensic_audit returns the 'remaining_R'
def generate_3d_survival_ridge():
    efficiencies = np.linspace(0.05, 0.95, 20)
    hps = np.linspace(100000, 1500000, 20)
    X, Y = np.meshgrid(efficiencies, hps)
    Z = np.zeros(X.shape)

    for i in range(len(hps)):
        for j in range(len(efficiencies)):
            # Simulate a 25-year-old with/without vision based on efficiency tier
            has_vision = X[i, j] > 0.6
            result_cost = activate_delusion("Subject", age=25, has_vision=has_vision, 
                                          efficiency=X[i, j], boss_hp=Y[i, j], silent=True)
            
            initial_R = np.exp(-0.012 * 25)
            if result_cost is not None:
                remaining = initial_R - result_cost
                # Cap at 0.15 for the 'Death Valley' visualization
                Z[i, j] = max(0.15, remaining)
            else:
                Z[i, j] = 0.15

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, Z, cmap='inferno', edgecolor='none', alpha=0.9)
    
    ax.set_title("Delusions: The 3D Survival Ridge", fontsize=14)
    ax.set_xlabel("Mastery Efficiency (η)")
    ax.set_ylabel("Combat Load (Boss HP)")
    ax.set_zlabel("Biological Redundancy (R)")
    
    # Add color bar for 'Mortality Heat'
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Survival Probability')
    
    plt.savefig(os.path.join(os.path.dirname(__file__), 'heatmap.png'))
    plt.close()

if __name__ == "__main__":
    generate_3d_survival_ridge()
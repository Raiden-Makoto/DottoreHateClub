import matplotlib.pyplot as plt
import numpy as np
import os
from delusion import activate_delusion as run_audit_for_plot
from burst import subjects

hp_ranges = np.linspace(10000, 1000000, 20)

plt.figure(figsize=(12, 7))

for sub in subjects:
    costs = []
    hps = []
    budget = np.exp(-0.012 * sub["age"]) - 0.15 #
    
    for hp in hp_ranges:
        # We use a modified version of your audit that returns the 'res.fun' (cost)
        cost = run_audit_for_plot(sub["name"], sub["age"], sub["vis"], sub["eff"], hp, silent=True)
        if cost and cost <= budget:
            costs.append(cost)
            hps.append(hp)
        else:
            # If they die, we stop the line to show the 'Mortality Cliff'
            break
    
    # Ensure line is visible even if they die instantly
    if len(hps) == 0:
        # Add points to create a diagonal line segment matching other character styles
        hps.append(0)
        costs.append(0)
        hps.append(hp_ranges[0])
        costs.append(budget)
    
    plt.plot(hps, costs, label=f"{sub['name']} (Budget: {budget:.2f})", 
             color=sub["color"], marker='o', linewidth=2)
    
    # Mark the Death Point with a Skull
    if len(hps) > 0:
        # Check if the next HP tier resulted in 'Infeasible'
        # We use the LaTeX skull symbol for the marker
        plt.scatter(hps[-1], costs[-1], 
                    marker='$\u2620$', 
                    color='black', 
                    s=250, 
                    zorder=5, 
                    label="Biological Collapse" if sub == subjects[0] else "")

plt.axhline(y=0.15, color='red', linestyle='--', alpha=0.5, label="Critical Instability (15%)")
plt.axhline(y=0, color='red', linestyle='--', alpha=0.5, label="Baseline (0%)")
plt.title("Delusion Forensic: Cumulative Biological Cost vs. Combat Output")
plt.xlabel("Total Damage Required (Boss HP)")
plt.ylabel("Gavrilov Redundancy Cost (R-Loss)")
plt.ylim(bottom=-0.1, top=1.1)
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.savefig(os.path.join(os.path.dirname(__file__), 'delusion_forensic_plot.png'))
plt.close()
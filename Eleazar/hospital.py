import os
import matplotlib.pyplot as plt
try:
    from .solver import run_simulation
except ImportError:
    # Allow running as a script
    from solver import run_simulation

scenarios = [
    {"name": "Collei (Young, Dendro Vision)", "age": 18, "vision": True, "color": "#a6c938"},
    {"name": "Child NPC (No Vision)", "age": 6, "vision": False, "color": "#75c2aa"},
    {"name": "Elderly NPC (No Vision)", "age": 80, "vision": False, "color": "#ef7a35"}
]

t, results = run_simulation(scenarios)

# --- 4. Visualization ---

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

for sc in scenarios:
    data = results[sc['name']]
    ax1.plot(t, data[:, 0], label=f"{sc['name']} - Vitality", color=sc['color'], linewidth=2)
    ax2.plot(t, data[:, 2], label=f"{sc['name']} - Scales", color=sc['color'], linestyle="--")

# Aesthetics
ax1.set_ylabel("Vitality (%)")
ax1.set_title("Eleazar: Vitality Dynamics (Gavrilov Reliability)")
ax1.axhline(15, color='black', linestyle=':', label="Critical Failure Threshold")
ax1.legend()
ax1.grid(alpha=0.3)

ax2.set_ylabel("Petrification (Scales %)")
ax2.set_xlabel("Days Since Exposure")
ax2.set_title("Eleazar Physical Progression")
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), 'eleazar_simulation.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.close()
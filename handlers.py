import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from Irminsul import trikarma_purification, ELEMENTS, OBS_MAP
from Irminsul.trellis import plot_viterbi_trellis
from Eleazar.eleazar import eleazar_model
from Delusion.delusion import activate_delusion

def get_benchmark_stats():
    """Calculate and return stats for the three benchmark subjects"""
    benchmarks = [
        {"name": "Childe", "age": 23, "vis": True, "eff": 0.65},
        {"name": "Arlecchino", "age": 30, "vis": True, "eff": 0.95},
        {"name": "Foolish NPC", "age": 16, "vis": False, "eff": 0.05}
    ]
    
    stats_text = "### Benchmark Subject Stats\n\n"
    stats_text += "| Subject | Age | Vision | Efficiency | ER | CD (s) | Q Cost | Budget |\n"
    stats_text += "|---------|-----|--------|------------|----|----|--------|--------|\n"
    
    for bench in benchmarks:
        age = bench["age"]
        has_vision = bench["vis"]
        efficiency = bench["eff"]
        
        # Calculate stats using same logic as activate_delusion
        cooldown = 12 - (5 * efficiency)
        burst_req = 90 - (10 * efficiency)
        base_energy = 10 + (17 * efficiency) + (8 * efficiency * efficiency) - 0.34 * age
        energy_per_E = base_energy * (1.5 if has_vision else 1.0)
        initial_R = np.exp(-0.012 * age)
        budget = initial_R - 0.15
        
        vis_str = "Yes" if has_vision else "No"
        stats_text += f"| {bench['name']} | {age} | {vis_str} | {efficiency:.2f} | {energy_per_E:.1f} | {cooldown:.1f} | {burst_req:.0f} | {budget:.3f} |\n"
    
    return stats_text

def reconstruct_irminsul(pure_input, withered_input):
    # 1. Validation & Truncation for pure sequence
    valid_elements = ELEMENTS
    clean_pure = "".join([c.upper() for c in pure_input if c.upper() in valid_elements])
    pure_str = clean_pure[:16]
    
    # 2. Validation & Truncation for withered sequence
    valid_chars = ELEMENTS + ['W']
    clean_withered = "".join([c.upper() for c in withered_input if c.upper() in valid_chars])
    withered_str = clean_withered[:16]
    
    if not withered_str:
        return "Please enter valid Elemental symbols (P, H, E, C, A, D, G) or 'W' for Withering.", None
    
    # 3. Convert withered string to observation indices
    try:
        withered_indices = [OBS_MAP[c] for c in withered_str]
    except KeyError:
        return "Invalid character in withered input. Please use only P, H, E, C, A, D, G, or W.", None

    # 4. Use actual Viterbi algorithm
    reconstructed, path_indices = trikarma_purification(withered_indices, return_indices=True)
    reconstructed_str = "".join(reconstructed)
    
    # 5. Calculate accuracy if pure sequence is provided
    accuracy_info = ""
    pure_record_for_plot = None
    if pure_str:
        # Truncate or pad pure_str to match reconstructed length
        if len(pure_str) != len(reconstructed_str):
            if len(pure_str) > len(reconstructed_str):
                pure_str = pure_str[:len(reconstructed_str)]
            else:
                # Pad with empty or use what we have
                pass
        
        if len(pure_str) == len(reconstructed_str):
            mismatches = sum(1 for i in range(len(reconstructed_str)) if reconstructed_str[i] != pure_str[i])
            total = len(reconstructed_str)
            accuracy = ((total - mismatches) / total * 100) if total > 0 else 0
            accuracy_info = f"\nAccuracy: {accuracy:.1f}% ({total - mismatches}/{total} correct, {mismatches} mismatches)"
            pure_record_for_plot = pure_str
    
    # 6. Use the actual trellis plotting function
    fig = plot_viterbi_trellis(withered_str, ELEMENTS, path_indices, output_path=None, pure_record=pure_record_for_plot)
    
    output_text = reconstructed_str + accuracy_info
    return output_text, fig

def simulate_triple_comparison(u_name, u_age, u_vision, initial_scenario):
    """
    Compare custom character against Collei and Dunyarzad using the actual Eleazar model.
    Uses the real eleazar_model function from the Eleazar package.
    """
    # Initial condition scenarios
    initial_conditions = {
        "Heavy": [84.0, 20.0, 12.0],  # V_0, C_0, S_0
        "Medium": [86.0, 12.0, 8.0],
        "Light": [90.0, 5.0, 2.0]
    }
    
    y0 = initial_conditions[initial_scenario]
    
    # Define benchmark scenarios
    scenarios = [
        {"name": "Collei (Young, Dendro Vision)", "age": 18, "vision": True, "color": "#a6c938"},
        {"name": "Dunyarzad (Elderly, No Vision)", "age": 65, "vision": False, "color": "#ef7a35"},
        {"name": f"{u_name} (Custom)", "age": int(u_age), "vision": bool(u_vision), "color": "#3498db"}
    ]
    
    # Base parameters from Eleazar solver
    base_params = [0.12, 0.06, 0.22, 0.04, 0.08]  # [regen, drain, corruption_rate, scale_drag, ossification]
    t = np.linspace(0, 120, 1200)
    
    # Run simulation for each scenario using actual Eleazar model
    results = {}
    for sc in scenarios:
        sol = odeint(eleazar_model, y0, t, args=(sc['age'], sc['vision'], base_params))
        results[sc['name']] = sol
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    for sc in scenarios:
        data = results[sc['name']]
        ax1.plot(t, data[:, 0], label=f"{sc['name']} - Vitality", color=sc['color'], linewidth=2)
        ax2.plot(t, data[:, 2], label=f"{sc['name']} - Scales", color=sc['color'], linewidth=2)
        # Also show corruption for custom character
        if sc['name'] == f"{u_name} (Custom)":
            ax1.plot(t, data[:, 1], label=f"{sc['name']} - Corruption", color=sc['color'], linestyle="--", alpha=0.6)
    
    # Aesthetics
    ax1.set_ylabel("Vitality (%)")
    ax1.set_title(f"Eleazar: Vitality Dynamics (Gavrilov Reliability) - Comparison\nInitial: {initial_scenario} (V={y0[0]:.1f}%, C={y0[1]:.1f}%, S={y0[2]:.1f}%)")
    ax1.axhline(15, color='black', linestyle=':', label="Critical Failure Threshold", alpha=0.5)
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    ax2.set_ylabel("Petrification (Scales %)")
    ax2.set_xlabel("Days Since Exposure")
    ax2.set_title("Eleazar Physical Progression")
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

def generate_phase3_plots(name, age, has_vision, efficiency, boss_hp):
    """
    Generate 2D comparison plot and 3D survival ridge for Phase 3: Delusion Toxicity
    """
    age = int(age)
    efficiency = float(efficiency)
    boss_hp = float(boss_hp)
    
    # --- 1. Generate 2D Comparison Plot ---
    fig2d, ax2d = plt.subplots(figsize=(10, 6))
    hp_range = np.linspace(10000, boss_hp * 1.5, 20)
    
    # Benchmark subjects: Childe, Arlecchino, and NPC
    benchmarks = [
        {"name": "Childe", "age": 23, "vis": True, "eff": 0.65, "color": "#e67e22"},
        {"name": "Arlecchino", "age": 30, "vis": True, "eff": 0.95, "color": "#c0392b"},
        {"name": "Foolish NPC", "age": 16, "vis": False, "eff": 0.05, "color": "#7f8c8d"}
    ]
    
    # Plot benchmarks
    for bench in benchmarks:
        costs = []
        hps = []
        budget = np.exp(-0.012 * bench["age"]) - 0.15
        
        for hp in hp_range:
            cost = activate_delusion(bench["name"], bench["age"], bench["vis"], bench["eff"], hp, silent=True)
            if cost and cost <= budget:
                costs.append(cost)
                hps.append(hp)
            else:
                break
        
        # Ensure line is visible even if they die instantly
        if len(hps) == 0:
            hps.append(0)
            costs.append(0)
            hps.append(hp_range[0])
            costs.append(budget)
        
        if len(hps) > 0:
            ax2d.plot(hps, costs, label=f"{bench['name']} (Budget: {budget:.2f})", 
                     color=bench["color"], marker='o', linewidth=2)
            # Mark death point with skull
            ax2d.scatter(hps[-1], costs[-1], marker='$\u2620$', color='black', s=250, zorder=5)
    
    # Plot custom subject
    costs = []
    hps = []
    budget = np.exp(-0.012 * age) - 0.15
    
    for hp in hp_range:
        cost = activate_delusion(name, age, has_vision, efficiency, hp, silent=True)
        if cost and cost <= budget:
            costs.append(cost)
            hps.append(hp)
        else:
            break
    
    # Ensure line is visible even if they die instantly
    if len(hps) == 0:
        hps.append(0)
        costs.append(0)
        hps.append(hp_range[0])
        costs.append(budget)
    
    ax2d.plot(hps, costs, label=f"{name} (Budget: {budget:.2f})", 
             color="#3498db", marker='o', linewidth=2)
    
    if len(hps) > 0:
        ax2d.scatter(hps[-1], costs[-1], marker='$\u2620$', color='black', s=250, zorder=5)
    
    ax2d.axhline(y=0.15, color='red', linestyle='--', alpha=0.5, label="Critical Instability (15%)")
    ax2d.axhline(y=0, color='red', linestyle='--', alpha=0.5, label="Baseline (0%)")
    ax2d.set_title(f"Forensic Damage Scaling for {name}")
    
    # Use appropriate scaling for HP values
    if boss_hp >= 1000000:
        # Scale to millions
        ax2d.set_xlabel("Total Damage Required (Boss HP, millions)")
        ax2d.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    elif boss_hp >= 1000:
        # Scale to thousands
        ax2d.set_xlabel("Total Damage Required (Boss HP, thousands)")
        ax2d.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))
    else:
        ax2d.set_xlabel("Total Damage Required (Boss HP)")
    
    ax2d.set_ylabel("Gavrilov Redundancy Cost (R-Loss)")
    ax2d.set_ylim(bottom=-0.1, top=1.1)
    ax2d.legend()
    ax2d.grid(True, which="both", ls="-", alpha=0.2)
    
    # --- 2. Generate 3D Survival Ridge ---
    fig3d = plt.figure(figsize=(10, 7))
    ax3d = fig3d.add_subplot(111, projection='3d')
    
    efficiencies = np.linspace(0.05, 0.95, 15)
    hps_3d = np.linspace(100000, int(boss_hp * 1.2), 15)
    X, Y = np.meshgrid(efficiencies, hps_3d)
    Z = np.zeros(X.shape)
    
    for i in range(len(hps_3d)):
        for j in range(len(efficiencies)):
            has_vis = X[i, j] > 0.6
            result_cost = activate_delusion("Subject", age=25, has_vision=has_vis, 
                                          efficiency=X[i, j], boss_hp=Y[i, j], silent=True)
            initial_R = np.exp(-0.012 * 25)
            if result_cost is not None:
                remaining = initial_R - result_cost
                Z[i, j] = max(0.15, remaining)
            else:
                Z[i, j] = 0.15
    
    surf = ax3d.plot_surface(X, Y, Z, cmap='inferno', edgecolor='none', alpha=0.9)
    ax3d.set_title("Delusions: The 3D Survival Ridge", fontsize=14)
    ax3d.set_xlabel("Mastery Efficiency (η)")
    
    # Use appropriate scaling for HP values in 3D plot
    if boss_hp >= 1000000:
        ax3d.set_ylabel("Combat Load (Boss HP, millions)")
        ax3d.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    elif boss_hp >= 1000:
        ax3d.set_ylabel("Combat Load (Boss HP, thousands)")
        ax3d.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))
    else:
        ax3d.set_ylabel("Combat Load (Boss HP)")
    
    ax3d.set_zlabel("Biological Redundancy (R)")
    fig3d.colorbar(surf, ax=ax3d, shrink=0.5, aspect=5, label='Survival Probability')
    
    return fig2d, fig3d

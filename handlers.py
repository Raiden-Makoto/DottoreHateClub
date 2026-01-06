import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from Irminsul import trikarma_purification, ELEMENTS, OBS_MAP
from Irminsul.trellis import plot_viterbi_trellis
from Eleazar.eleazar import eleazar_model

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

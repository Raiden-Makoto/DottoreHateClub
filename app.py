import gradio as gr # type: ignore
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

# --- Gradio Interface ---
# Use darker Collei green (#6b8a26) for theme
custom_theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(
        c50="#e8f5e9",
        c100="#c8e6c9",
        c200="#a5d6a7",
        c300="#81c784",
        c400="#66bb6a",
        c500="#6b8a26",
        c600="#5a7a1f",
        c700="#4a6a18",
        c800="#3a5a11",
        c900="#2a4a0a",
        c950="#1a3a03",
    )
)

with gr.Blocks(theme=custom_theme) as demo:
    gr.Markdown("# A mathematical analysis of biological systems in *Genshin Impact*")
    
    with gr.Tab("Phase 1: Irminsul Recovery"):
        gr.Markdown("## Project Overview")
        gr.Markdown(
            "This project treats **Irminsul** (The World Tree) from *Genshin Impact* as a biological database of Teyvat's history and genetic blueprints. "
            "Just as DNA is subject to mutations, Irminsul is vulnerable to \"Forbidden Knowledge,\" a form of high-entropy noise known as *The Withering*. "
            "This project utilizes a **HMM** (Hidden Markov Model) to detect and cleanse this corruption, restoring the \"True Record\" of elemental fluxes using the **Viterbi Algorithm.**"
        )
        gr.Markdown("### Forensic Signal Reconstruction")
        gr.Markdown("Input a pure sequence (optional) and a 'Withered' elemental sequence to attempt recovery.")
        
        with gr.Row():
            with gr.Column(scale=3):
                txt_pure = gr.Textbox(label="Pure Sequence (Optional, Max 16 chars)", placeholder="e.g. DEEEPAHHG")
                txt_withered = gr.Textbox(label="Withered Sequence (Max 16 chars)", placeholder="e.g. DEWEPWHWG")
                btn_run = gr.Button("Decode Record", variant="primary")
                txt_output = gr.Textbox(label="Reconstructed Pure Record", lines=3)
            
            with gr.Column(scale=4):
                plot_output = gr.Plot(label="Viterbi Trellis Visualization")
                plot_caption = gr.Markdown("*The trellis diagram shows the Viterbi algorithm finding the most likely sequence of hidden elements (green path) that would produce the observed corrupted record. When the original pure record differs from the reconstruction, it is shown as a blue dashed line for comparison.*")
                with gr.Accordion("Explain Accuracy", open=False):
                    gr.Markdown(
                        "When the corruption is too high, the algorithm defaults to the \"most logical\" biological path rather than the \"historical truth.\" "
                        "For example, an original sequence of D-E-E-E (Dendro-Electro-Electro-Electro) might be restored as "
                        "D-E-D-E (Dendro-Electro-Dendro-Electro) because the algorithm favors the Quicken reaction over simple repetition. "
                        "This mirrors the lore-accurate phenomenon of the World Tree \"rewriting\" history to fit the laws of Teyvat."
                    )
        btn_run.click(fn=reconstruct_irminsul, inputs=[txt_pure, txt_withered], outputs=[txt_output, plot_output])

    with gr.Tab("Phase 2: Eleazar Kinetics"):
        gr.Markdown("## Project Overview")
        gr.Markdown(
            "**Eleazar** is a terminal condition caused by the *Withering* manifesting in human hosts. "
            "This project applies a modified version of the **Reliability Theory of Aging** (Gavrilov Model) "
            "to simulate the competition between cellular vitality and Abyssal contamination.\n\n"
            "We treat the human body as a system of redundant components. "
            "Failure (Eleazar) occurs when the \"redundancy reserve\" is exhausted. "
            "The *Gompertz-Makeham Law* is used to define the base mortality and age-dependent decay of a patient. "
            "We also account for the effects of a *Vision*, which we mathematically define as a redundancy buffer, "
            "providing a \"metabolic floor\" that prevents the exponential \"avalanche of failures\" typical in terminal Eleazar cases.\n\n"
            "You can compare your custom character against two canonical Eleazar patients: Collei (young Vision holder) and Dunyarzad "
            "(elderly non-Vision holder) using the Gavrilov Reliability ODE model."
        )
        
        with gr.Row():
            with gr.Column():
                char_name = gr.Textbox(label="Character Name", value="Traveler")
                age_slide = gr.Slider(10, 90, value=20, step=1, label="Subject Age")
                vis_check = gr.Checkbox(label="Possesses Vision", value=False)
                initial_scenario = gr.Radio(
                    choices=["Heavy", "Medium", "Light"],
                    value="Heavy",
                    label="Initial Contamination"
                )
                run_btn = gr.Button("Analyze Reliability", variant="primary")
                
            with gr.Column():
                plot_out = gr.Plot()
                plot_caption_eleazar = gr.Markdown(
                    "*Note: by changing the initial starting parameters, we can get different scenarios, "
                    "where all patients recover or non Vision holders failing to recover. By selecting Scenario 1, we demonstrate "
                    "the power of having a Vision in providing accelerated regeneration and contamination resistance, "
                    "allowing **Collei** to fully recover despite having high initial contamination.*"
                )

        run_btn.click(simulate_triple_comparison, 
                     inputs=[char_name, age_slide, vis_check, initial_scenario], 
                     outputs=plot_out)

    with gr.Tab("Phase 3: Delusion Toxicity"):
        gr.Markdown("Coming soon: Linear Programming Death Boundary...")

demo.launch()
import gradio as gr # type: ignore
from handlers import reconstruct_irminsul, simulate_triple_comparison, generate_phase3_plots

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
        gr.Markdown("## Project Overview")
        gr.Markdown(
            "**Project Pure-Flux | Tactical Mortality Audit**\n\n"
            "This phase utilizes Constrained Optimization (MILP) to quantify the active destruction caused by Delusion usage. "
            "We treat a subject's biological life force as a non-renewable currency used to \"purchase\" damage output. "
            "The model uses `scipy.optimize.linprog` with integrality constraints to solve for the most bio-efficient combat rotation."
        )
        gr.Markdown("### Forensic Combat Analysis")
        gr.Markdown("Compare your subject against benchmark Harbingers (Childe, Arlecchino) and NPC to assess survivability under Delusion load.")
        
        with gr.Row():
            with gr.Column(scale=1):
                name_in = gr.Textbox(label="Subject Name", value="Traveler")
                age_in = gr.Slider(15, 70, value=25, step=1, label="Age")
                eff_in = gr.Slider(0.01, 0.8, value=0.5, step=0.01, label="Mastery Efficiency (η)")
                vis_in = gr.Checkbox(label="Vision", value=False)
                hp_in = gr.Slider(0, 1500000, value=500000, step=50000, label="Boss HP")
                btn_phase3 = gr.Button("Execute Forensic Audit", variant="primary")
                
            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.Tab("2D Analysis"):
                        plot_2d = gr.Plot(label="Cumulative Cost vs. Damage")
                        gr.Markdown("*The 2D plot shows cumulative biological cost vs. combat output. Skull markers (☠) indicate biological collapse points. Red dashed lines mark critical thresholds.*")
                    with gr.Tab("3D Survival Ridge"):
                        plot_3d = gr.Plot(label="Topographic Mortality Mapping")
                        gr.Markdown("*The 3D surface shows biological redundancy as a function of mastery efficiency and combat load. The \"Death Valley\" at 0.15 represents the critical failure threshold.*")
                        
        btn_phase3.click(generate_phase3_plots, 
                        inputs=[name_in, age_in, vis_in, eff_in, hp_in], 
                        outputs=[plot_2d, plot_3d])

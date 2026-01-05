import os
import matplotlib.pyplot as plt
try:
    from .constants import ELEMENTS
except ImportError:
    from constants import ELEMENTS

def plot_viterbi_trellis(obs_sequence, states, best_path_indices, output_path=None, pure_record=None):
    """
    Generates a trellis diagram for the Irminsul reconstruction.
    
    Args:
        obs_sequence: String of observed characters (e.g., "DEWEPWHWG")
        states: List of state names (e.g., ['P', 'H', 'E', 'C', 'A', 'D', 'G'])
        best_path_indices: List of state indices for the best path (reconstructed)
        output_path: Optional path to save the figure. If None, displays the figure.
        pure_record: Optional string of the pure/original record to overlay if it differs
    """
    n_states = len(states)
    n_obs = len(obs_sequence)
    
    # Convert pure_record to indices if provided
    pure_path_indices = None
    if pure_record and len(pure_record) == n_obs:
        try:
            pure_path_indices = [states.index(char) for char in pure_record]
        except (ValueError, IndexError):
            pure_path_indices = None
    
    plt.figure(figsize=(12, 6))
    
    # Create the grid for states and time steps
    for t in range(n_obs):
        for s in range(n_states):
            # Plot each state as a circle
            color = 'lightgrey'
            alpha = 0.3
            
            # Check if this state is part of the reconstructed path
            if best_path_indices[t] == s:
                color = '#2ecc71' # Sumeru Green (reconstructed)
                alpha = 1.0
                plt.text(t, s + 0.3, states[s], ha='center', fontweight='bold', color='#27ae60')
            
            # Check if this state is part of the pure path (and differs from reconstructed)
            if pure_path_indices and pure_path_indices[t] == s and pure_path_indices[t] != best_path_indices[t]:
                color = '#3498db' # Blue (pure/original)
                alpha = 1.0
                plt.text(t, s - 0.3, states[s], ha='center', fontweight='bold', color='#2980b9')
            
            plt.scatter(t, s, color=color, s=500, edgecolors='black', alpha=alpha, zorder=3)

    # Draw the reconstructed path (The Viterbi Result)
    for t in range(n_obs - 1):
        plt.plot([t, t+1], [best_path_indices[t], best_path_indices[t+1]], 
                 color='#27ae60', linewidth=3, zorder=2, label='Reconstructed' if t == 0 else '')
    
    # Draw the pure path if it differs
    if pure_path_indices:
        paths_differ = any(pure_path_indices[t] != best_path_indices[t] for t in range(n_obs))
        if paths_differ:
            for t in range(n_obs - 1):
                plt.plot([t, t+1], [pure_path_indices[t], pure_path_indices[t+1]], 
                         color='#3498db', linewidth=3, linestyle='--', zorder=2, 
                         label='Original' if t == 0 else '')
        
    # Formatting
    plt.xticks(range(n_obs), [f"Obs: {char}" for char in obs_sequence])
    plt.yticks(range(n_states), states)
    title = "Project Irminsul: Viterbi Trellis Reconstruction"
    if pure_path_indices and any(pure_path_indices[t] != best_path_indices[t] for t in range(n_obs)):
        title += " (Original vs Reconstructed)"
    plt.title(title, fontsize=14)
    plt.xlabel("Timeline of Withered Observations")
    plt.ylabel("Elemental State Space")
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    if pure_path_indices and any(pure_path_indices[t] != best_path_indices[t] for t in range(n_obs)):
        plt.legend(loc='upper right')
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return None
    else:
        # Return the figure for use in interactive contexts (e.g., Gradio)
        return plt.gcf()
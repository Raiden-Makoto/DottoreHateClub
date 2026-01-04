import numpy as np
try:
    from .constants import BASE_MATRIX, EMISSION_MATRIX, ELEMENTS
except ImportError:
    # Allow running as a script
    from constants import BASE_MATRIX, EMISSION_MATRIX, ELEMENTS

def trikarma_purification(
    obs_sequence: str,
    base_matrix: np.ndarray = BASE_MATRIX,
    emission_matrix: np.ndarray = EMISSION_MATRIX,
    states: list[str] = ELEMENTS
):
    """
    Restores the true elemental sequence from a withered record.
    obs_sequence: List of indices corresponding to observations (0-7)
    base_matrix: 7x7 transition matrix between elements
    emission_matrix: 7x8 emission matrix for observations
    states: List of possible elemental states (P, H, E, C, A, D, G)
    Returns:
        List of indices corresponding to the true elemental sequence (0-6)

    This function implements the Viterbi algorithm to find the most likely sequence of states.
    """
    n_states, n_obs = len(states), len(obs_sequence)

    # Initialize the Viterbi and Backpointer matrices
    viterbi = np.zeros((n_states, n_obs))
    backpointer = np.zeros((n_states, n_obs), dtype=int)

    # Initialization (Time step 0)
    # Assume equal probability for the starting element (1/7)
    with np.errstate(divide='ignore'):
        for s in range(n_states):
            viterbi[s, 0] = np.log(1/n_states) + np.log(emission_matrix[s, obs_sequence[0]])

    # Recursion (Time steps 1 to T)
    with np.errstate(divide='ignore'):
        for t in range(1, n_obs):
            for s in range(n_states):
                # Calculate prob of moving from every 'prev_s' to current 's'
                # using log-space to avoid underflow
                log_probs = viterbi[:, t-1] + np.log(base_matrix[:, s]) + np.log(emission_matrix[s, obs_sequence[t]])
                viterbi[s, t] = np.max(log_probs)
                backpointer[s, t] = np.argmax(log_probs)

    # Termination & Path Reconstruction
    best_path = np.zeros(n_obs, dtype=int)
    best_path[-1] = np.argmax(viterbi[:, -1])

    # Backtrack to find the most likely sequence of states
    for t in range(n_obs-2, -1, -1):
        best_path[t] = backpointer[best_path[t+1], t+1]

    return [states[s] for s in best_path]

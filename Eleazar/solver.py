import numpy as np
from scipy.integrate import odeint
try:
    from tqdm import tqdm
except ImportError:
    # Fallback if tqdm is not installed
    def tqdm(iterable, *args, **kwargs):
        return iterable
try:
    from .eleazar import eleazar_model
except ImportError:
    # Allow running as a script
    from eleazar import eleazar_model

def run_simulation(scenarios, days=120):
    """
    Runs a simulation of the Eleazar model for a given set of scenarios.
    scenarios: A list of dictionaries, each containing the following keys:
    - 'name': The name of the scenario
    - 'age': The age of the patient
    - 'vision': Whether the patient has vision or not
    days: The number of days to run the simulation
    Returns: A tuple containing the time array and a dictionary of results.
    """
    t = np.linspace(0, days, 1200)
    # [regen, drain, corruption_rate, scale_drag, ossification]
    # Parameter set for "Chronic Struggle" - Phase 2 "Final Exam"
    base_params = [0.12, 0.06, 0.22, 0.04, 0.08] 
    
    results = {}
    for sc in tqdm(scenarios, desc="Running simulations", unit="scenario"):
        # Starting with heavy exposure to a Withering Zone
        y0 = [90.0, 30.0, 7.0]
        sol = odeint(eleazar_model, y0, t, args=(sc['age'], sc['vision'], base_params))
        results[sc['name']] = sol
    
    return t, results
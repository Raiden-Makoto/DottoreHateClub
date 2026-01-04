import numpy as np

def eleazar_model(y, t, age, has_vision, base_params):
    """
    A System of Ordinary Differential Equations (ODEs) that models the
    health dynamics of an Eleazar patient. The model is based on the following assumptions:
    - Vision holders have more efficient regeneration and reduced corruption growth
    - Reliability Theory of Aging (RTA) is used to model the age-dependent decline in regeneration efficiency
    - Biological aging and the decline of functional systems are expressed through the
    Gompertz-Makeham Law of Mortality and its underlying "redundancy" derivation
    """
    V, C, S = y
    alpha, beta, gamma, delta, kappa = base_params

    # --- Gavrilov Reliability Parameters ---
    # k: rate of redundancy exhaustion (the aging constant)
    # Soften the aging constant to prevent 'instant death'
    k = 0.035 
    # Reliability Modifier (Redundancy): P(survival) = (1 - (1-e^-kt)^n)
    # Here we simplify to the metabolic reserve factor
    redundancy_reserve = np.exp(-k * (age / 10)) 
    
    # --- Updated Aegis-Gavrilov Logic ---
    # NPC Child: High metabolic flux, high vulnerability
    if not has_vision and age < 18:
        phi = 1.0          # Normal regen
        gamma_mod = 1.35   # Dottore's 'High Flux' observation: metabolism feeds the Abyss
        metabolic_floor = 0.05
    
    # Vision Holder: Superior protection with Aegis Redundancy Floor
    elif has_vision:
        phi = 1.30         # Superior Regen
        gamma_mod = 0.30   # THE SHIELD: Vision blocks 70% of corruption spread
        metabolic_floor = 0.45 # The Aegis Redundancy Floor
    
    # Default case (adults without vision)
    else:
        phi = 1.0
        gamma_mod = 1.0
        metabolic_floor = 0.05

    # Effective Vitality Reserve
    R = max(metabolic_floor, redundancy_reserve)

    # --- The Updated ODEs ---
    # Vitality: Regeneration is now constrained by the Redundancy Reserve (R)
    dVdt = (alpha * phi * R) * V * (1 - V/100) - (beta * C * V) - (delta * S)
    
    # Corruption: Use a 'Safe Log' or 'Capped Multiplier' for the reliability influence
    # This prevents the Elderly NPC from crashing in 2 days
    reliability_impact = 1.0 / (R + 0.1)
    dCdt = (gamma * gamma_mod * reliability_impact) * C - (0.02 * V * C)
    
    # Scales: Physical petrification
    dSdt = kappa * C * (1 - S/100)
    
    return [dVdt, dCdt, dSdt]
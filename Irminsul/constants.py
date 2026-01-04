import numpy as np

ELEMENTS = [
    'P', # Pyro
    'H', # Hydro
    'E', # Electro
    'C', # Cryo
    'A', # Anemo
    'D', # Dendro
    'G', # Geo
]

BASE_MATRIX = np.array([
    [0.10, 0.25, 0.15, 0.05, 0.15, 0.25, 0.05], # Pyro: Loves Vape/Burn/Swirl
    [0.25, 0.10, 0.15, 0.10, 0.15, 0.25, 0.00], # Hydro: Loves Vape/Bloom/Swirl/Freeze
    [0.15, 0.20, 0.10, 0.05, 0.15, 0.30, 0.05], # Electro: Loves Quicken/EC/Swirl
    [0.10, 0.25, 0.05, 0.15, 0.15, 0.03, 0.27], # Cryo: Loves Freeze/Swirl/Shatter
    [0.22, 0.22, 0.22, 0.22, 0.04, 0.04, 0.04], # Anemo: Swirl Priority (P, H, E, C)
    [0.25, 0.25, 0.30, 0.03, 0.02, 0.10, 0.05], # Dendro: Sticky with Pyro/Hydro/Electro
    [0.20, 0.20, 0.20, 0.20, 0.02, 0.02, 0.16]  # Geo: Crystallize (P, H, E, C)
])

EMISSION_MATRIX = np.array([
    # P     H     E     C     A     D     G     W (Withered State)
    [0.60, 0.02, 0.02, 0.01, 0.02, 0.01, 0.02, 0.30], # True Pyro
    [0.02, 0.60, 0.02, 0.02, 0.01, 0.02, 0.01, 0.30], # True Hydro
    [0.02, 0.02, 0.60, 0.02, 0.02, 0.01, 0.01, 0.30], # True Electro
    [0.01, 0.02, 0.02, 0.60, 0.02, 0.01, 0.02, 0.30], # True Cryo
    [0.02, 0.02, 0.02, 0.02, 0.60, 0.01, 0.01, 0.30], # True Anemo
    [0.01, 0.01, 0.01, 0.01, 0.01, 0.65, 0.00, 0.30], # True Dendro (more stable)
    [0.02, 0.01, 0.01, 0.02, 0.01, 0.00, 0.63, 0.30], # True Geo
])

OBS_MAP = {'P':0, 'H':1, 'E':2, 'C':3, 'A':4, 'D':5, 'G':6, 'W':7}
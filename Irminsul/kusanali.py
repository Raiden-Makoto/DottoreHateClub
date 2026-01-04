try:
    from .nahida import trikarma_purification
    from .constants import OBS_MAP
except ImportError:
    # Allow running as a script
    from nahida import trikarma_purification
    from constants import OBS_MAP

def kusanali():
    """
    A simple, informative example of using Nahida's Elemental Skill (Trikarma Purification)
    to restore a withered record (string of elements affected by the Withering).
    """

    pure_record = "DE" # Quicken
    pure_record += "E" # Aggravate
    pure_record += "E" # Electro, consumes aggravate
    pure_record += "P" # Pyro, consumes quicken to create burning
    pure_record += "A" # Anemo, swirls pyro
    pure_record += "HH" # Hydro, causes vaporize x2
    pure_record += "G" # Geo, creates crystallize

    # Abyssal contamination causes the Withering to contaminate some information
    withered_record = "DEWEPWHWG"
    withered_indices = [OBS_MAP[c] for c in withered_record]

    # Use Nahida's Elemental Skill
    purified = trikarma_purification(withered_indices)

    print(f"Original: {pure_record}")
    print(f"Withered: {withered_record}")
    print(f"Restored: {''.join(purified)}")

if __name__ == "__main__":
    kusanali()
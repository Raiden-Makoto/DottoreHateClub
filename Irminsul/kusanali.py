import os
try:
    from .nahida import trikarma_purification
    from .constants import OBS_MAP, ELEMENTS
    from .trellis import plot_viterbi_trellis
except ImportError:
    # Allow running as a script
    from nahida import trikarma_purification
    from constants import OBS_MAP, ELEMENTS
    from trellis import plot_viterbi_trellis

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
    purified, path_indices = trikarma_purification(withered_indices, return_indices=True)

    print(f"Original: {pure_record}")
    print(f"Withered: {withered_record}")
    print(f"Restored: {''.join(purified)}")
    
    # Plot the trellis diagram
    output_path = os.path.join(os.path.dirname(__file__), 'viterbi_trellis.png')
    plot_viterbi_trellis(withered_record, ELEMENTS, path_indices, output_path, pure_record)
    print(f"Trellis diagram saved to: {output_path}")

if __name__ == "__main__":
    kusanali()
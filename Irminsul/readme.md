# Phase 1: Deep-Layer Error Correction in the World Tree

## Project Overview
This project treats **Irminsul** (The World Tree) from *Genshin Impact* as a
biological database of Teyvat's history and genetic blueprints.
Just as DNA is subject to mutations, Irminsul is vulnerable to "Forbidden Knowledge,"
a form of high-entropy noise known as *The Withering*.

I implemented a **HMM** (Hidden Markov Model) to detect and cleanse this corruption,
restoring the "True Record" of elemental fluxes using the **Viterbi Algorithm.**

## Biological Syntax of Teyvat
Unlike standard data, elemental records follow a specific mechanistic logic.
We modeled the transition between elements (Pyro, Hydro, Electro, Cryo, Anemo, Dendro, Geo)
as a Markovian process where probabilities are weighted by Elemental Gauge Theory.
Specific features include
- *Stable Chains:* High transition probabilities for reactive pairs like Dendro x Electro (Quicken) or Hydro x Cryo (Freeze)
- *Inert Pairs:* Low probabilities for combinations like Anemo x Geo, which do not react with each other

The Withering (W) is modeled as an Emission Matrix where the true state is hidden behind a mask of Abyssal corruption.

## Technical Details
1. **The Markov Transition Matrix ($A$):**
We defined a $7 \times 7$ matrix representing the "Laws of Nature." This ensures that the restoration algorithm "understands" the chemical context of the data it is repairing.

2. **The Viterbi "Cleansing" Algorithm:**
To restore corrupted records, we implemented the Viterbi algorithm in log-probability space for numerical stability.
> Input: A "Withered" string (e.g., DEWEPWHWG).   
> Process: The algorithm calculates the globally most likely "True" path through the state-space trellis[^1].    
> Output: A restored elemental sequence.    

3. **Numerical Stability**
To handle "Forbidden" transitions (zero probability events), we utilized Laplace Smoothing and $\epsilon$-constants, preventing logarithmic underflow while maintaining the strict logic of the elemental system.


## Limitations/Quirks
When the corruption is too high, the algorithm defaults to the "most logical" biological path rather than the "historical truth."
For example, an original sequence of D-E-E-E (Dendro-Electro-Electro-Electro) might be restored as
D-E-D-E (Dendro-Electro-Dendro-Electro) because the algorithm favors the Quicken reaction over simple repetition.
This mirrors the lore-accurate phenomenon of the World Tree "rewriting" history to fit the laws of Teyvat.

---

[^1]: A trellis is a graphical diagram that unravels the states of a system over time, showing all possible state transitions as paths, where each path represents a potential sequence of encoded data.

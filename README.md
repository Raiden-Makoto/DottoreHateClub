# DottoreHateClub

A mathematical analysis of biological systems in *Genshin Impact*, focusing on the destructive technologies developed by Il Dottore. This project applies computational methods to model and quantify the effects of Forbidden Knowledge, Eleazar disease, and Delusion technology on human subjects.

**⚠️ WARNING: DO NOT EXPERIMENT ON HUMANS, DOTTORE**

---

## Project Overview

This repository contains three phases of mathematical modeling, each addressing a different aspect of biological corruption and system failure in the world of Teyvat:

### [Phase 1: Deep-Layer Error Correction in the World Tree](Irminsul/readme.md)

**Methodology:** Hidden Markov Model (HMM) with Viterbi Algorithm

**Objective:** Restore corrupted elemental records from Irminsul (The World Tree) by treating "The Withering" as high-entropy noise that obscures true biological data.

**Key Results:**
- Successfully implemented a Viterbi-based restoration algorithm that recovers true elemental sequences from withered observations
- Identified a bifurcation point where corruption becomes too severe for accurate reconstruction
- Demonstrated how the algorithm favors "biologically logical" paths over historical truth, mirroring Irminsul's tendency to rewrite history

**Technologies:** NumPy, Hidden Markov Models, Viterbi Algorithm

---

### [Phase 2: Eleazar and Biological Reliability](Eleazar/readme.md)

**Methodology:** System of Ordinary Differential Equations (ODEs) with Gavrilov Reliability Theory

**Objective:** Model the progression of Eleazar disease—a terminal condition caused by Withering manifesting in human hosts—using Reliability Theory of Aging.

**Key Results:**
- Developed a 3-ODE system tracking Vitality, Corruption, and Scales (petrification)
- Identified three distinct patient outcomes:
  - **Stabilized Chronic** (Vision holders): Reach stable equilibrium via "Aegis Effect"
  - **High-Flux Catalyst** (NPC children): High metabolism feeds corruption ($1.35\gamma$)
  - **Exhausted Terminal** (Elderly NPCs): Rapid collapse due to low redundancy reserves
- Demonstrated how Vision holders can overcome severe contamination that would be fatal to non-Vision holders

**Technologies:** NumPy, SciPy (ODE integration), Reliability Theory of Aging

---

### [Phase 3: Linear Programming and the "Human Tax" Optimization](Delusion/readme.md)

**Methodology:** Linear Programming (Constrained Optimization)

**Objective:** Quantify the active destruction caused by Delusion usage, proving mathematically that Delusion technology is a guaranteed death sentence for standard humans.

**Key Results:**
- Identified a brutal bifurcation point: survival time remains effectively zero for subjects with efficiency below 80%
- Discovered "The Child Paradox": subjects aged 10–14 show slight survival uplift due to high initial redundancy, which Dottore systematically exploits
- Revealed "The Mortality Cliff": exponential drop in survival window as age increases
- Mathematically exposed a system designed to treat human souls as disposable high-flux batteries

**Technologies:** SciPy (Linear Programming), Constrained Optimization

---

## Project Structure

```
DottoreHateClub/
├── Irminsul/          # Phase 1: HMM-based error correction
├── Eleazar/           # Phase 2: ODE-based disease modeling
├── Delusion/          # Phase 3: LP-based survival analysis
└── README.md          # This file
```

## Final Summary

1. **Irminsul Restoration:** The Viterbi algorithm can recover corrupted records, but favors biological logic over historical accuracy—a phenomenon that mirrors the World Tree's tendency to rewrite history.

2. **Eleazar Progression:** Vision holders maintain a "metabolic floor" (Aegis Effect) that prevents terminal collapse, while NPC children's high metabolism paradoxically accelerates corruption.

3. **Delusion Lethality:** Only subjects with elite combat mastery (efficiency >80%) can survive Delusion usage, proving that Dottore's technology is designed for disposable human batteries.

---

## References

- Gavrilov, L. A., & Gavrilova, N. S. (2001). The reliability theory of aging and longevity.
- Viterbi, A. J. (1967). Error bounds for convolutional codes and an asymptotically optimum decoding algorithm.
- *Genshin Impact* lore and game mechanics

---

**Disclaimer:** This project is a mathematical analysis of fictional biological systems. All models and conclusions are theoretical and should not be applied to real-world medical scenarios.

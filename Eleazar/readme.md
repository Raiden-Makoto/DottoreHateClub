# Phase 2: Eleazar and Biological Reliability

## Project Overview
**Eleazar** is terminal condition caused by the "Withering" manifesting in human hosts.
This project applies a modified version of the **Reliability Theory of Aging** (Gavrilov Model)
to simulate the competition between cellular vitality and Abyssal contamination.

## The Gavrilov-Vision Model
We treat the human body as a system of redundant components.
Failure (Eleazar) occurs when the "redundancy reserve" is exhausted.
The *Gompertz-Makeham Law* is used to define the base mortality and age-dependent decay of a patient.
We also account for the effects of a *Vision*, which we mathematically define as a redundancy buffer,
providing a "metabolic floor" that prevents the exponential "avalanche of failures" typical in terminal Eleazar cases.

## ODE Setup
We implemented a system of three coupled Ordinary Differential Equations (ODEs) to track the patient's state over time:
- $V(t)$ (Vitality): Regenerative life force, constrained by the current redundancy reserve.
- $C(t)$ (Corruption): The concentration of "Forbidden Knowledge" within the body, which scales exponentially as biological reliability ($R$) drops
- $S(t)$ (Scales): The physical petrification rate, acting as a "drag" on vitality.

The system of ODEs is defined as:

$$\frac{dV}{dt} = (\alpha \cdot \phi \cdot R) \cdot V \cdot \left(1 - \frac{V}{100}\right) - (\beta \cdot C \cdot V) - (\delta \cdot S)$$

$$\frac{dC}{dt} = (\gamma \cdot \gamma_{mod} \cdot \text{reliability\_impact}) \cdot C - (0.02 \cdot V \cdot C)$$

$$\frac{dS}{dt} = \kappa \cdot C \cdot \left(1 - \frac{S}{100}\right)$$

where:
- $R = \max(\text{metabolic\_floor}, e^{-k \cdot (\text{age}/10)})$ is the effective vitality reserve (redundancy reserve)
- $\text{reliability\_impact} = \frac{1.0}{R + 0.1}$ is a capped multiplier preventing extreme crashes
- $\alpha, \beta, \gamma, \delta, \kappa$ are base parameters (regen, drain, virulence, scale drag, ossification)
- $\phi$ and $\gamma_{mod}$ are modifiers based on patient type (Vision holder, NPC child, etc.)

## Simulation Results
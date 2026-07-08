# Benign-Statistics-Certificates

Supplementary Python code for the numerical validation section of the paper:

**A Forgery-Detectability Rate for Benign-Statistics Certificates in Continuous-Variable Quantum Key Distribution**

Agung Trisetyarso, Lenny Putri Yulianti, and Kridanto Surendro

*IEEE Transactions on Information Theory* (submitted)

---

## Overview

This repository contains the Python scripts used to generate the Monte Carlo simulations, exact statistical computations, and figures presented in **Section V (Numerical Validation)** of the paper.

The code validates:
- The closed-form Stein exponent `ψ(r)` derived in **Lemma 1**
- The rigorous non-asymptotic parameter-estimation failure bound of **Corollary 1**
- The Bahadur–Rao refinement in **Corollary 3**
- Convergence of the empirical exponent to the theoretical Stein exponent
- Comparison of exact χ² tails vs. Chernoff and Bahadur–Rao approximations

All results are fully reproducible and match the tables and figures in the manuscript.

---

## Repository Contents

| File                                      | Description |
|-------------------------------------------|-------------|
| `Univariate Trusted_correlation_model.py` | Monte Carlo simulation of the trusted-correlation model. Generates synthetic data under forged conditional variance ratio `r*`, computes empirical missed-detection probability `ε_PE`, and compares it against the theoretical Chernoff bound `exp(−N_PE · ψ(r*))`. |
| `PE.py`                                   | Computes **exact** missed-detection probabilities using the chi-squared CDF. Compares exact tails against the Chernoff bound and the Bahadur–Rao asymptotic refinement (Corollary 3). Generates high-resolution plots. |
| `Numerical_optimization.py`               | Numerical verification of concavity of the Holevo bound `χ_BE(T₀, ξ)` and related functionals (supporting Proposition 2). |
| `conditional.py`                          | Helper functions for bivariate Gaussian distributions, conditional variance calculations, and visualization of parameter-estimation data. |
| `Qiskit_aer.py`                           | Quantum simulation utilities using Qiskit Aer for Wigner function visualization of benign vs. forged Gaussian states (Fig. 6 style). |

---

## Requirements

- Python ≥ 3.8
- `numpy`
- `scipy`
- `matplotlib`
- `qiskit` + `qiskit-aer` (only needed for `Qiskit_aer.py`)

```bash
pip install numpy scipy matplotlib qiskit qiskit-aer

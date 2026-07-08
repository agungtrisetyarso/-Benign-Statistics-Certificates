import numpy as np
import matplotlib.pyplot as plt

def psi(r):
    return 0.5 * (1/r - 1 + np.log(r))

# === Parameters (match paper notation; N0 = 1 for simplicity) ===
N0 = 1.0
NPE_values = [100, 500, 1000, 5000]   # vary block size
r_star = 1.05                         # forged conditional variance ratio (try 1.01, 1.1, 1.5)
num_mc_trials = 20000                 # Monte Carlo repetitions for empirical probability

empirical_probs = []
theo_bounds = []

for NPE in NPE_values:
    N_star = r_star * N0
    # Sample y_i ~ N(0, N_star)  (conditional on xA; xA part contributes 0 to relative entropy)
    y = np.sqrt(N_star) * np.random.randn(num_mc_trials, NPE)
    hatN = np.mean(y**2, axis=1)
    
    # Verifier accepts "benign" iff hatN <= N0 (as in Corollary 1)
    missed = (hatN <= N0)
    emp_eps = np.mean(missed)
    theo = np.exp(-NPE * psi(r_star))
    
    empirical_probs.append(emp_eps)
    theo_bounds.append(theo)
    
    print(f"NPE={NPE:5d} | r*={r_star:.3f} | Empirical ε_PE={emp_eps:.2e} | Bound=exp(-Nψ)={theo:.2e} | Holds: {emp_eps <= theo}")

# Quick plot of scaling
plt.figure(figsize=(8,5))
plt.plot(NPE_values, -np.log(np.array(empirical_probs))/np.array(NPE_values), 'o-', label='Empirical exponent')
plt.axhline(psi(r_star), color='r', linestyle='--', label=f'ψ(r*) = {psi(r_star):.4f}')
plt.xlabel('N_PE'); plt.ylabel('Effective exponent (-ln ε / N_PE)')
plt.title('Validation of Stein exponent ψ(r) from Lemma 1')
plt.legend(); plt.grid(True); plt.show()

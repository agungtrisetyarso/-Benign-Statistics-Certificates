import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

def psi(r):        return 0.5*(1.0/r - 1.0 + np.log(r))
def eps_exact(r,N): return chi2.cdf(N/r, N)                       # exact tail
def eps_bound(r,N): return np.exp(-N*psi(r))                      # Chernoff bound
def eps_BR(r,N):    return r/((r-1)*np.sqrt(np.pi*N))*np.exp(-N*psi(r))  # Bahadur-Rao

rstars = [1.02, 1.05, 1.10, 1.20]
colors = {1.02:'tab:blue', 1.05:'tab:orange', 1.10:'tab:green', 1.20:'tab:red'}
markers= {1.02:'o',        1.05:'s',          1.10:'^',          1.20:'D'}
N = np.unique(np.round(np.logspace(2, 4.2, 40)).astype(int))     # 100 .. ~16000

# -------- Figure 1: convergence of effective exponent to psi(r*) --------
fig1, ax1 = plt.subplots(figsize=(9,6))
for r in rstars:
    c=colors[r]
    eff = -np.log(eps_exact(r,N))/N                              # effective exponent
    ax1.plot(N, eff, color=c, marker=markers[r], ms=5, lw=1.6,
             label=f"Effective exponent ($r^*={r}$)")
    ax1.axhline(psi(r), color=c, ls=':', lw=1.4,
                label=f"$\\psi(r^*)={psi(r):.5f}$ ($r^*={r}$)")
ax1.set_xscale('log')
ax1.set_xlabel("$N_{\\mathrm{PE}}$ (log scale)")
ax1.set_ylabel(r"Effective exponent  $-\ln\varepsilon_{PE}/N_{\mathrm{PE}}$")
ax1.set_title("Convergence to Stein exponent $\\psi(r^*)$ (Lemma 1)\n"
              "exact tail; approach from above $\\sim\\psi+\\ln N/2N$")
ax1.legend(ncol=2, fontsize=8); ax1.grid(alpha=0.3)
fig1.tight_layout(); fig1.savefig("fig_convergence_exact.png", dpi=150)

# -------- Figure 2: exact eps vs Chernoff bound vs Bahadur-Rao --------
fig2, ax2 = plt.subplots(figsize=(9,6))
for r in rstars:
    c=colors[r]
    ax2.plot(N, eps_exact(r,N), color=c, marker=markers[r], ms=5, lw=1.6,
             label=f"Exact $\\varepsilon_{{PE}}$ ($r^*={r}$)")
    ax2.plot(N, eps_bound(r,N), color=c, ls='--', lw=1.4,
             label=f"Chernoff $e^{{-N\\psi}}$ ($r^*={r}$)")
    ax2.plot(N, eps_BR(r,N),    color=c, ls=':',  lw=1.2,
             label=f"Bahadur-Rao ($r^*={r}$)")
ax2.set_xscale('log'); ax2.set_yscale('log')
ax2.set_ylim(1e-30, 1.0)
ax2.set_xlabel("$N_{\\mathrm{PE}}$ (number of estimation rounds)")
ax2.set_ylabel("Missed-detection probability $\\varepsilon_{PE}$")
ax2.set_title("Corollary validation: exact tail $\\leq$ Chernoff bound\n"
              "(trusted-correlation model); Bahadur-Rao tracks the exact tail")
ax2.legend(ncol=2, fontsize=7); ax2.grid(alpha=0.3, which='both')
fig2.tight_layout(); fig2.savefig("fig_bound_exact.png", dpi=150)

# -------- console check: bound is valid and conservative by ~sqrt(N) --------
print("r*    N      exact         bound        bound/exact   psi     eff.exp")
for r in [1.05,1.10,1.20]:
    for n in [200,1000,5000]:
        ex,bd=eps_exact(r,n),eps_bound(r,n)
        print(f"{r:<5} {n:<6} {ex:.3e}   {bd:.3e}   {bd/ex:8.1f}   {psi(r):.5f} {-np.log(ex)/n:.5f}")
print("\nsaved: fig_convergence_exact.png , fig_bound_exact.png")

import numpy as np, matplotlib.pyplot as plt
from scipy.stats import norm, chi2
def psi(r): return 0.5*(1/r-1+np.log(r))
N0=1.054; rs=[1.0,1.05,1.1,1.2]
cols={1.0:'tab:blue',1.05:'tab:green',1.1:'tab:orange',1.2:'tab:red'}
fig,(axL,axR)=plt.subplots(1,2,figsize=(12,5))

# LEFT: conditional densities N(0,N)
yy=np.linspace(-5,5,600)
for r in rs:
    N=r*N0
    axL.plot(yy,norm.pdf(yy,0,np.sqrt(N)),color=cols[r],lw=1.8,
             label=f"$r^*={r}$  ($N={N:.3f}$, $\\sqrt{{N}}={np.sqrt(N):.3f}$)")
axL.set_xlabel("$y-\\mathbb{E}[y\\,|\\,x_A]$ (conditional residual)")
axL.set_ylabel("density")
axL.set_title("Conditional distribution $y\\,|\\,x_A$: variance $=N$\n"
              "(the only quantity the attack moves)")
axL.legend(fontsize=8); axL.grid(alpha=0.3)

# RIGHT: distribution of N_hat = (N/ N_PE) chi2_{N_PE}, acceptance {N_hat<=N0}
Npe=500
xx=np.linspace(0.8,1.5,800)
for r in rs:
    N=r*N0
    # N_hat has density of (N/Npe)*chi2_Npe: pdf via chi2 change of variables
    pdf=chi2.pdf(xx*Npe/N,Npe)*(Npe/N)
    axR.plot(xx,pdf,color=cols[r],lw=1.8,label=f"$r^*={r}$, $\\psi={psi(r):.5f}$")
    if r>1.0:  # shade missed-detection mass  {N_hat<=N0} under attack
        m=xx<=N0
        axR.fill_between(xx[m],0,chi2.pdf(xx[m]*Npe/N,Npe)*(Npe/N),
                         color=cols[r],alpha=0.18)
axR.axvline(N0,color='k',ls='--',lw=1.2,label="threshold $N_0$ (accept if $\\hat N\\leq N_0$)")
axR.set_xlabel("$\\hat N$ (sample conditional variance, $N_{\\mathrm{PE}}=500$)")
axR.set_ylabel("density")
axR.set_title("PE statistic $\\hat N$ and acceptance region\n"
              "shaded overlap $=\\varepsilon_{PE}$, rate $\\psi(r^*)$")
axR.legend(fontsize=8); axR.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("fig_conditional.png",dpi=150)
print("saved fig_conditional.png")
print("psi:", {r:round(psi(r),5) for r in rs})

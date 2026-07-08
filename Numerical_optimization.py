import numpy as np
from scipy.optimize import minimize, NonlinearConstraint

def g_func(x):
    return (x + 1)*np.log2(x + 1) - x*np.log2(x) if x > 0 else 0.0

def chi_BE(VA, T, xi, eta=1.0, vel=0.0):
    V = VA + 1.0
    Teta = T * eta
    W = Teta*(V - 1) + 1 + Teta*xi + vel
    detA = V**2
    detB = W**2
    detC = -Teta
    Delta = detA + detB - 2*detC
    detSigma = (V*W - Teta)**2
    tmp = max(Delta**2 - 4*detSigma, 0)
    nu1 = np.sqrt(0.5*(Delta + np.sqrt(tmp)))
    nu2 = np.sqrt(0.5*(Delta - np.sqrt(tmp)))
    S_AB = g_func((nu1-1)/2) + g_func((nu2-1)/2)
    V_A_cond = V - Teta / W
    S_A_B = g_func((V_A_cond - 1)/2)
    return S_AB - S_A_B

def D_func(params, VA0, T0, xi0, eta, vel):
    T, xi = params
    # Build Σ0 and Σ1 (paper Eq. 1)
    Sigma0 = np.array([[VA0, np.sqrt(eta*T0)*VA0],
                       [np.sqrt(eta*T0)*VA0, eta*T0*VA0 + (1+vel+eta*T0*xi0)]])
    N1 = 1 + vel + eta*T*xi
    Sigma1 = np.array([[VA0, np.sqrt(eta*T)*VA0],
                       [np.sqrt(eta*T)*VA0, eta*T*VA0 + N1]])
    # KL formula (paper Eq. 2)
    invS1 = np.linalg.inv(Sigma1)
    tr_term = np.trace(invS1 @ Sigma0)
    det_term = np.log(np.linalg.det(Sigma1) / np.linalg.det(Sigma0))
    return 0.5 * (tr_term - 2 + det_term)

import numpy as np

# Calculating the invariant mass
def calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA):
    momentum_factor = 2*mup_PT*mum_PT
    eta_factor = np.cosh(mup_ETA - mum_ETA) # This is the pseudorapidity factor  
    phi_factor = np.cos(mup_PHI - mum_PHI)
    mass_squared = momentum_factor * (eta_factor - phi_factor)
    return np.array(np.sqrt(mass_squared))

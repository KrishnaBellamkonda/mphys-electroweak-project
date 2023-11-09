import numpy as np

# Calculating the invariant mass
def calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA):
    momentum_factor = 2*mup_PT*mum_PT
    eta_factor = np.cosh(mup_ETA - mum_ETA) # This is the pseudorapidity factor  
    phi_factor = np.cos(mup_PHI - mum_PHI)
    mass_squared = momentum_factor * (eta_factor - phi_factor)
    return np.array(np.sqrt(mass_squared))



def get_fiducial_range_data(data, min_mass=0.6e5, max_mass=1.2e5, pt_min=0.2e5, min_eta=2.0, max_eta=4.5):
    
    # Get all the attributes
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA = data

    mass = calc_invariant_mass(*data) # invariant mass

    # Constraint 1: 60 GeV < mass < 120 GeV
    mass_filter = (min_mass < mass) & (mass < max_mass)

    # Constraint 2: Both muons with pT > 20Gev
    pt_filter = (mup_PT > pt_min) & (mum_PT > pt_min)

    # Constraint 3: Both muons with 2.0 < psuedorapidity < 4.5
    eta_filter_p = (min_eta < mup_ETA) & (mup_ETA < max_eta)
    eta_filter_m = (min_eta < mum_ETA) & (mum_ETA < max_eta)
    eta_filter = eta_filter_p & eta_filter_m

    # Fiducial Filter
    fiducial_filter = mass_filter & pt_filter & eta_filter

    # Return the filtered data arrays too
    filtered_data = (
            mup_PT[fiducial_filter],
            mup_PHI[fiducial_filter],
            mup_ETA[fiducial_filter],
            mum_PT[fiducial_filter],
            mum_PHI[fiducial_filter],
            mum_ETA[fiducial_filter]
            )

    return fiducial_filter, filtered_data


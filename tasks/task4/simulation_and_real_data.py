import numpy as np
import matplotlib.pyplot as plt
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.processing.mass import calc_invariant_mass, get_fiducial_range_data
from weak_mixing_angle.processing.asymmetry import calc_fb_true, FBTrueParameters, measure_Afb_from_data



def main():
    # Constants
    n_bins = 7 # fiducial range
    
    # Getting the real data
    real_data = read_muon_data(StoragePaths.real_data, tree_name="Z/DecayTree")
    real_invariant_mass = calc_invariant_mass(*real_data)
    
    print(len(real_data))

    # Obtaining and applying the fiducial filter
    real_fiducial_filter, (filtered_real_data) = get_fiducial_range_data(real_data) 

    # filtered_real_data = mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA    # which meet the constraints

    # calculate the A_fb with erros
    bin_avg_energy, Afb, err_invariant_mass, err_counts = measure_Afb_from_data(filtered_real_data, n_bins, (0.6e5, 1.2e5))

    # Creating a template for this pp collision
    m_ll = np.linspace(60, 120, 7)
    wma = 0.231
    up_params = FBTrueParameters(
        Q_l=(-1),
        T3_l=(-1/2),
        Q_q=(2/3),
        T3_q=(1/2),
        m_ll=m_ll, 
        weak_mixing_angle=wma
    )

    Afb_pred = calc_fb_true(up_params) 
    m_ll = m_ll *1000 # Matching the scale
    print(Afb_pred)
    
    # Plot A_fb as a function of invariant mass
    plt.scatter(bin_avg_energy, Afb, label="Real Afb", color="b")
    plt.title("Forward-Backward Asymmetry vs. Invariant Mass")
    plt.xlabel("Mass (MeV)")
    plt.ylabel("$A_{fb}$")
    plt.errorbar(bin_avg_energy, Afb, err_counts, err_invariant_mass, fmt='', linestyle='', color='b', label="Real Afb")
    plt.scatter(m_ll, Afb_pred, label="Theory Afb", color="r")
    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/Afb_best_fit_params.png")
    


if __name__ == "__main__":
    main()

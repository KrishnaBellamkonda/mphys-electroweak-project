import numpy as np
import matplotlib.pyplot as plt
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.utility.utils import read_muon_data, quadratic
from weak_mixing_angle.processing.mass import calc_invariant_mass, get_fiducial_range_data
from weak_mixing_angle.processing.asymmetry import calc_fb_true, FBTrueParameters, measure_Afb_from_data
from weak_mixing_angle.processing.fitting import calc_chi_squared_for_mixing_angle, fit_quadratic

def main():
    # Constants
    n_bins = 7 # fiducial range
    
    # Step 1)  Measuring the Afb in the real data
    real_data = read_muon_data(StoragePaths.real_data, tree_name="Z/DecayTree")
    real_invariant_mass = calc_invariant_mass(*real_data)
    
    real_fiducial_filter, (filtered_real_data) = get_fiducial_range_data(real_data) 
    # calculate the A_fb with erros
    bin_avg_energy, Afb, err_invariant_mass, err_counts = measure_Afb_from_data(filtered_real_data, n_bins, (0.6e5, 1.2e5))
    
    # Step 2)  Compute the chi-squared for different sin2theta
    wma = np.linspace(0.16, 0.27, 30)
    m_ll = np.linspace(60, 120, n_bins) # Requried for the model which accepts in GeV
    std_values = np.ones(len(Afb)) * (1/np.sqrt(len(Afb))) # Poisson error
    chi_squared_errors = [calc_chi_squared_for_mixing_angle(Afb, a, m_ll,  std_values) for a in wma]
   
    # Step 3) Plotting the wma vs ch_squared_errors plot
    plt.scatter(x=wma, y=chi_squared_errors, label="chi-squared-values")
    plt.ylabel("Chi Squared Error")
    plt.xlabel("Weak Mixing Angle (rads)")
    plt.savefig(f"{StoragePaths.plots_path}/chi_square_errors_for_wma.png")

    # Step 4) Fit the data using a parabola
    best_fit_params = fit_quadratic(wma, chi_squared_errors)
    A, B, C = best_fit_params
    best_fit_parabola = quadratic(wma, *best_fit_params)
    plt.plot(wma, best_fit_parabola, color="r", label=f"Best-Fit A={A:.2f} B={B:.2f} C={C:.2f}")
    plt.ylabel("Chi Squared Error")
    plt.xlabel("Weak Mixing Angle (rads)")
    plt.title("Best fit params using Chi Squared")
    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/best_fit_parabola.png")



    # Plotting best-fit model
    #plt.scatter(bin_avg_energy, Afb, label="Real Afb", color="b")
    #plt.title("Forward-Backward Asymmetry vs. Invariant Mass")
    #plt.xlabel("Mass (MeV)")
    #plt.ylabel("$A_{fb}$")
    #plt.errorbar(bin_avg_energy, Afb, err_counts, err_invariant_mass, fmt='', linestyle='', color='b', label="Real Afb")
    #plt.scatter(m_ll, Afb_pred, label="Theory Afb", color="r")
    #plt.legend()
   # plt.savefig(f"{StoragePaths.plots_path}/Afb_best_fit_params.png")


if __name__ == "__main__":
    main()

import numpy as np
import matplotlib.pyplot as plt
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.utility.utils import read_muon_data, quadratic, calc_chi_sqared_error
from weak_mixing_angle.processing.mass import calc_invariant_mass, get_fiducial_range_data
from weak_mixing_angle.processing.asymmetry import calc_fb_true, FBTrueParameters, measure_Afb_from_data
from weak_mixing_angle.processing.fitting import calc_chi_squared_for_mixing_angle, fit_quadratic, interpolate_linear

def main():
    # Constants
    n_bins = 7 # fiducial range
    
    # Plot templates alongside best interpolated value
    # Step 1) Get the data from the files (with different wma) 
    pp1_wma = 0.228
    pp1_data = read_muon_data(StoragePaths.ppdata1, "MCDecayTree;1") # 0.228
    pp1_fiducial_filter, (pp1_filtered_data) = get_fiducial_range_data(pp1_data, min_mass=60, max_mass=120, pt_min=2.5)
    pp2_wma = 0.235
    pp2_data = read_muon_data(StoragePaths.ppdata2, "MCDecayTree;1") # 0.235
    pp2_fiducial_filter, (pp2_filtered_data) = get_fiducial_range_data(pp2_data, min_mass=60, max_mass=120, pt_min=2.5)

    # calculating the Afb values for these datasets
    pp1_bin_avg_energy, pp1_Afb, pp1_err_invariant_mass, pp1_err_counts = measure_Afb_from_data(pp1_filtered_data, 7, (60, 120))
    pp2_bin_avg_energy, pp2_Afb, pp2_err_invariant_mass, pp2_err_counts = measure_Afb_from_data(pp2_filtered_data, 7, (60, 120))

    # Step 2) interpolating the values for the given wma

    wma = [-(-50.12)/(2*79.08)]
    m_ll = np.linspace(60, 120, n_bins) # Requried for the model which accepts in GeV
    #interpolation_values = [interpolate_linear(pp1_Afb,pp1_wma, pp2_Afb, pp2_wma, a) for a in wma] # Contains all of the interpolations for all the wmas
    interpolation_values = [interpolate_linear(pp1_wma, pp1_Afb, pp2_wma, pp2_Afb, a) for a in wma]

   # err_interpolation = 


    # Step 3) Plotting the Afb vs invariant mass bins (templates)
    plt.scatter(x=m_ll, y=pp1_Afb, label=f"$sin2theta_w$={pp1_wma}", color="b")
    plt.scatter(x=m_ll, y=pp2_Afb, label=f"$sin2theta_w$={pp2_wma}", color="r")
    plt.ylabel("Afb")
    plt.xlabel("Invariant Mass (GeV)")
    plt.errorbar(m_ll, pp1_Afb, pp1_err_counts, pp1_err_invariant_mass, fmt="", linestyle="", color="b")
    plt.errorbar(m_ll, pp2_Afb, pp2_err_counts, pp2_err_invariant_mass, fmt="", linestyle="", color="r")
    
    # Step 4) Plot the Interpolated values
    plt.scatter(m_ll, interpolation_values[0], label=f"Interpolated $sin2theta_w$={wma[0]:.3}", color="g")
    #plt.errorbar(m_ll,interpolation_values[0],   )
    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/template_and_interpolated_values.png")


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

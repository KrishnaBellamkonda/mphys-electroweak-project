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
    
    # Step 1)  Measuring the Afb in the real data
    real_data = read_muon_data(StoragePaths.real_data, tree_name="Z/DecayTree")
    real_invariant_mass = calc_invariant_mass(*real_data)
    
    real_fiducial_filter, (filtered_real_data) = get_fiducial_range_data(real_data) 
    # calculate the A_fb with erros
    bin_avg_energy, Afb, err_invariant_mass, err_counts = measure_Afb_from_data(filtered_real_data, n_bins, (0.6e5, 1.2e5))
    
    # Step 2)  Compute the chi-squared for different sin2theta
    # Get the data from the files (with different wma)
    # Use linear interpolation to find the Afb values for other wmas
    pp1_wma = 0.228
    pp1_data = read_muon_data(StoragePaths.ppdata1, "MCDecayTree;1") # 0.228
    pp1_fiducial_filter, (pp1_filtered_data) = get_fiducial_range_data(pp1_data, min_mass=60, max_mass=120, pt_min=2.5)
    pp2_wma = 0.235
    pp2_data = read_muon_data(StoragePaths.ppdata2, "MCDecayTree;1") # 0.235
    pp2_fiducial_filter, (pp2_filtered_data) = get_fiducial_range_data(pp2_data, min_mass=60, max_mass=120, pt_min=2.5)

        # calculating the Afb values for these datasets
    pp1_bin_avg_energy, pp1_Afb, pp1_err_invariant_mass, pp1_err_counts = measure_Afb_from_data(pp1_filtered_data, 7, (60, 120))
    pp2_bin_avg_energy, pp2_Afb, pp2_err_invariant_mass, pp2_err_counts = measure_Afb_from_data(pp2_filtered_data, 7, (60, 120))

    print(f"{Afb=}")
    print(f"{pp1_Afb=}")
    print(f"{pp2_Afb=}")

        # interpolating the values for the given wma

    wma = np.linspace(0.20, 0.39, 30)
    m_ll = np.linspace(60, 120, n_bins) # Requried for the model which accepts in GeV
    interpolation_values = [interpolate_linear(pp1_wma, pp1_Afb, pp2_wma, pp2_Afb,  a) for a in wma] # Contains all of the interpolations for all the wmas
    #std_values = np.ones(len(Afb)) * (1/np.sqrt(len(Afb))) # Poisson error
    std_values = n_bins -1
    chi_squared_errors = [calc_chi_sqared_error(Afb, Afb_interpol, std_values) for Afb_interpol in interpolation_values ]
    
    print(chi_squared_errors)
    print(len(Afb), len(chi_squared_errors), len(interpolation_values), len(wma))


    # Get the weak mixing angle for the minimum of the chisquared
    min_chi_squared = min(chi_squared_errors)
    min_chi_squared_index = np.argmin(chi_squared_errors)
    wma_for_least_chi_squared = wma[min_chi_squared_index]
    interpolation_vales_for_least_chi_squared = interpolation_values[min_chi_squared_index]
    print(f"{min_chi_squared=} {wma_for_least_chi_squared=}")

    # Step 3) Plotting the wma vs ch_squared_errors plot
    plt.scatter(x=bin_avg_energy, y=interpolation_vales_for_least_chi_squared, label=f"Interpolation for least chi2={wma_for_least_chi_squared}")
    plt.scatter(x=bin_avg_energy,y=Afb, label="Real Data")
    plt.ylabel("Afb")
    plt.xlabel("Invariant Mass (GeV)")
    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/interpolation_values_for_least_chi2.png")

    # Step 4) Fit the data using a parabola
    #best_fit_params = fit_quadratic(wma, chi_squared_errors)
    #A, B, C = best_fit_params
    #best_fit_parabola = quadratic(wma, *best_fit_params)
   # plt.plot(wma, best_fit_parabola, color="r", label=f"Best-Fit A={A:.2f} B={B:.2f} C={C:.2f}")
    #plt.ylabel("Chi Squared Error")
    #plt.xlabel("Weak Mixing Angle (rads)")
    #plt.title("Best fit params using Chi Squared")
    #plt.legend()
    #plt.savefig(f"{StoragePaths.plots_path}/best_fit_parabola.png")



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

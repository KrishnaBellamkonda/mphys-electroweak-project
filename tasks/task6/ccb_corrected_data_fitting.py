import numpy as np
import matplotlib.pyplot as plt
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.utility.utils import read_muon_data, quadratic, calc_chi_sqared_error
from weak_mixing_angle.processing.mass import calc_invariant_mass, get_fiducial_range_data, calc_ccb_corrected_pt
from weak_mixing_angle.processing.asymmetry import calc_fb_true, FBTrueParameters, measure_Afb_from_data
from weak_mixing_angle.processing.fitting import interpolate_linear, fit_quadratic, fit_parabola
from weak_mixing_angle.utility.utils import get_parabola_parameters, parabola
from weak_mixing_angle.processing.corrections import get_deltas

def main():
    # Constants
    n_bins = 7 # fiducial range
    
    # Step 1)  Measuring the Afb in the real data
    data_file = StoragePaths.real_data
    tree_name="Z/DecayTree"

    # Gathered the data
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA = read_muon_data(data_file, tree_name)

    # Step 1.5) MAKE CCB CORRECTIONS
    deltas = get_deltas(StoragePaths.pseudomass_corrections_combined)
    mup_PT = calc_ccb_corrected_pt(1, 1, mup_PT, mup_PHI, mup_ETA, deltas, scale="MeV")
    mum_PT = calc_ccb_corrected_pt(1, -1, mum_PT, mum_PHI, mum_ETA, deltas, scale="MeV")

    real_data = mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA
    real_invariant_mass = calc_invariant_mass(*real_data)
    
    real_fiducial_filter, (filtered_real_data) = get_fiducial_range_data(real_data) 
    # calculate the A_fb with erros
    bin_avg_energy, Afb, err_invariant_mass, err_Afb = measure_Afb_from_data(filtered_real_data, n_bins, (0.6e5, 1.2e5))
    

    # Step 2) Get the template data
    pp1_wma = 0.228
    pp1_data = read_muon_data(StoragePaths.ppdata1, "MCDecayTree;1") # 0.228
    pp1_fiducial_filter, (pp1_filtered_data) = get_fiducial_range_data(pp1_data, min_mass=60, max_mass=120, pt_min=2.5)
    pp2_wma = 0.235
    pp2_data = read_muon_data(StoragePaths.ppdata2, "MCDecayTree;1") # 0.235
    pp2_fiducial_filter, (pp2_filtered_data) = get_fiducial_range_data(pp2_data, min_mass=60, max_mass=120, pt_min=2.5)

    # calculating the Afb values for these datasets
    pp1_bin_avg_energy, pp1_Afb, pp1_err_invariant_mass, pp1_err_counts = measure_Afb_from_data(pp1_filtered_data, 7, (60, 120))
    pp2_bin_avg_energy, pp2_Afb, pp2_err_invariant_mass, pp2_err_counts = measure_Afb_from_data(pp2_filtered_data, 7, (60, 120))


    # Step 2)  Compute the chi-squared for different sin2theta
    # Blinding our measurements
    np.random.seed(42)
    wma = np.random.uniform(0.16, 0.27, 30)
    wma = sorted(wma)
    m_ll = np.linspace(60, 120, n_bins) # Requried for the model which accepts in GeV
    template_interpolations = [interpolate_linear(pp1_wma, pp1_Afb, pp2_wma, pp2_Afb, a) for a in wma ]
    #print(template_interpolations[0])
    #print()
    print(f"{template_interpolations[0]=}")
    print(f"{Afb=}")
    print(f"{err_Afb=}")
    #std_values = np.ones(len(Afb)) * (1/np.sqrt(len(Afb))) # Poisson error
    #std_values = n_bins - 1
    std_values = np.array(err_Afb)
    chi_squared_errors = [calc_chi_sqared_error(interpol , Afb,  std_values).sum() for a, interpol in zip(wma, template_interpolations)]
    print(f"{chi_squared_errors[0]}=")
    #print(chi_squared_errors)

    # Step 3) Plotting the wma vs ch_squared_errors plot
    plt.scatter(x=wma, y=chi_squared_errors, label="chi-squared-values")
    plt.ylabel("Chi Squared Error")
    plt.xlabel("Weak Mixing Angle (rads)")
    plt.savefig(f"{StoragePaths.plots_path}/ccb_corrected_chi_square_errors_for_wma.png")

    # Step 4) Fit the data using a parabola
    # best_fit_params = fit_quadratic(wma, chi_squared_errors)
    # A, B, C = best_fit_params
    # best_fit_parabola = quadratic(wma, *best_fit_params)
    # minima, sigma = get_parabola_parameters(A, B)
    best_fit_params = fit_parabola(wma, chi_squared_errors)
    minima, sigma, k = best_fit_params
    best_fit_parabola = parabola(wma, *best_fit_params)
    
    print(f"{sigma=}")

    plt.plot(wma, best_fit_parabola, color="r", label=f"Best-Fit minima={minima:.5f} sigma={sigma:.5f}")
    plt.ylabel("Chi Squared")
    sin2theta_w = r"\sin^{2}\left(\theta_w\right)"
    plt.xlabel(f"{sin2theta_w}")
    plt.title("Best fit params using Chi Squared")
    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/ccb_corrected_best_fit_parabola.png")



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

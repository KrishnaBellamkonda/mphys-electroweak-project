import uproot
import numpy as np
import matplotlib.pyplot as plt
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.utility.utils import read_muon_data, quadratic, calc_chi_sqared_error
from weak_mixing_angle.processing.mass import calc_invariant_mass, get_fiducial_range_data
from weak_mixing_angle.processing.asymmetry import calc_fb_true, FBTrueParameters, measure_Afb_from_data, measure_Afb_from_trigger_corrected_data
from weak_mixing_angle.processing.fitting import interpolate_linear, fit_quadratic, fit_parabola
from weak_mixing_angle.utility.utils import get_parabola_parameters, parabola
from weak_mixing_angle.processing.trigger import correct_events_for_trigger_efficiencies, calc_trigger_eff


# Note:
# This file follows the first method of calculating the standard errors
# shift the values of efficiencies by 1 sigma (up and down), 
# find sin2theta_w and  
# 
def main():
    # Step 1) Constants & Parameters
    n_bins = 7 # Number of bins for measuring the Afb
    data_file = StoragePaths.real_data
    tree_name = "Z/DecayTree"

    # Step 2) Read the real data
    data = read_muon_data(data_file, tree_name)
    fidicual_mask, (mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA) = get_fiducial_range_data(data)
    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)
    
    # Step 2.25) Split data set into bins of phi
    # phi_bins_edges = np.linspace(-np.pi, np.pi, 4, endpoint=True) # Divided into 4 bins

    # Step 2.5) Weight the data with eta efficiencies
    
    # Obtaining the effciencies 
    with uproot.open(data_file) as file:
        tree = file[tree_name]
        branches=tree.arrays()
        posFlags=np.array(branches["mup_L0MuonEWDecision_TOS"])
        negFlags=np.array(branches["mum_L0MuonEWDecision_TOS"])

    posFlags = posFlags[fidicual_mask]
    negFlags= negFlags[fidicual_mask]

    # Obtaining the efficiencies for ETA
    mup_eff,mup_eff_err, mup_bins = calc_trigger_eff(mup_ETA,7,True,posFlags,negFlags)
    mum_eff,mum_eff_err, mum_bins = calc_trigger_eff(mum_ETA,7,False,posFlags,negFlags)

    # 

    # Mapping muon+ to the right bin
    print(f"{mup_eff}")
    print(f"{mup_ETA=}")
    print(f"{mup_eff_err=}")
    # invariant_mass = correct_events_for_trigger_efficiencies(invariant_mass, mup_ETA, mup_bins, mup_eff)
    print(f"{invariant_mass=}")
    
    # Mapping muon- int the right bin and updating the invariant mass
    # invariant_mass = correct_events_for_trigger_efficiencies(invariant_mass, mum_ETA, mum_bins, mum_eff)
    print(f"{invariant_mass=}")

    # calculate the A_fb with errors
    data = (mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)
    bin_avg_energy, Afb, err_invariant_mass, err_Afb = measure_Afb_from_trigger_corrected_data(data, mup_eff, mup_bins, mum_eff, mum_bins, n_bins, (0.6e5, 1.2e5))
    print(f"{Afb=}")

    # Here we make the measurements of theAfb with the trigger efficiences
    # moved up and down by 1 sigma. Using these two values, we measure
    # the final impact on the calculated sin2theta

    # 1 sigma up 
    mup_eff_sigma_up = mup_eff + mup_eff_err
    mum_eff_sigma_up = mum_eff + mum_eff_err
    bin_avg_energy_sigma_up, Afb_sigma_up, err_invariant_mass_sigma_up, err_Afb_sigma_up = measure_Afb_from_trigger_corrected_data(data, mup_eff_sigma_up, mup_bins, mum_eff_sigma_up, mum_bins, n_bins, (0.6e5, 1.2e5))

    # 1 sigma down 
    mup_eff_sigma_down = mup_eff - mup_eff_err
    mum_eff_sigma_down = mum_eff - mum_eff_err
    bin_avg_energy_sigma_down, Afb_sigma_down, err_invariant_mass_sigma_down, err_Afb_sigma_down = measure_Afb_from_trigger_corrected_data(data, mup_eff_sigma_down, mup_bins, mum_eff_sigma_down, mum_bins, n_bins, (0.6e5, 1.2e5))

    
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
    chi_squared_errors_sigma_up = [calc_chi_sqared_error(interpol , Afb_sigma_up,  std_values).sum() for a, interpol in zip(wma, template_interpolations)]
    chi_squared_errors_sigma_down = [calc_chi_sqared_error(interpol , Afb_sigma_down,  std_values).sum() for a, interpol in zip(wma, template_interpolations)]

    print(f"{chi_squared_errors[0]}=")
    #print(chi_squared_errors)

    # Step 3) Plotting the wma vs ch_squared_errors plot
    plt.scatter(x=wma, y=chi_squared_errors, label="chi-squared-values")
    plt.ylabel("Chi Squared Error")
    plt.xlabel("Weak Mixing Angle (rads)")
    plt.savefig(f"{StoragePaths.plots_path}/chi_square_errors_for_wma_corrected_eta_trigger.png")

    # Step 4) Fit the data using a parabola
    best_fit_params = fit_parabola(wma, chi_squared_errors)
    minima, sigma, k = best_fit_params
    best_fit_parabola = parabola(wma, *best_fit_params)

    best_fit_params_sigma_up = fit_parabola(wma, chi_squared_errors_sigma_up)
    minima_sigma_up, sigma_sigma_up, k_sigma_up = best_fit_params_sigma_up
    best_fit_parabola_sigma_up = parabola(wma, *best_fit_params_sigma_up)
    
    best_fit_params_sigma_down = fit_parabola(wma, chi_squared_errors_sigma_down)
    minima_sigma_down, sigma_sigma_down, k_sigma_down = best_fit_params_sigma_down
    best_fit_parabola_sigma_down = parabola(wma, *best_fit_params_sigma_down)

    # Step 5) Adding uncertainties for trigger corrections
    # CAlculate the mimina, sigma and k for Sigma Up Afb
    minima_std = (minima_sigma_up - minima_sigma_down)/2
    print(f"{minima_std=}")


    print(f"{sigma=}")

    plt.plot(wma, best_fit_parabola, color="r", label=f"Best-Fit minima={minima:.5f} sigma={sigma:.5f}")
    plt.plot(wma, best_fit_parabola_sigma_up, color="r", label=f"1 sigma up minima={minima_sigma_up:.5f} sigma={sigma_sigma_up:.5f}")
    plt.plot(wma, best_fit_parabola_sigma_down, color="r", label=f"1 sigma down minima={minima_sigma_down:.5f} sigma={sigma_sigma_down:.5f}")
    plt.ylabel("Chi Squared")
    sin2theta_w = r"\sin^{2}\left(\theta_w\right)"
    plt.text( 0.20, 2000, f"err sin2theta={minima_std:.6f}")
    plt.xlabel(f"{sin2theta_w}")
    plt.title("Best fit params using Chi Squared")
    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/best_fit_parabola_corrected_eta_trigger_eff_with_std.png")


if __name__ == "__main__":
    main()

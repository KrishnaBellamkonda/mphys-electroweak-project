import numpy as np
import matplotlib.pyplot as plt

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.processing.mass import calc_invariant_mass, calc_ccb_corrected_pt
from weak_mixing_angle.processing.corrections import get_deltas
from weak_mixing_angle.processing.asymmetry import measure_Afb_from_data



# Plot the invaraint mass for forward
# vs backward events with errors
def main():
    
    data_file = StoragePaths.real_data
    tree_name="Z/DecayTree"

    # Gathered the data
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA = read_muon_data(data_file, tree_name)
    data = mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA

    # Step 1.5) MAKE CCB CORRECTIONS
    deltas = get_deltas(StoragePaths.pseudomass_corrections_combined)
    mup_PT = calc_ccb_corrected_pt(1, 1, mup_PT, mup_PHI, mup_ETA, deltas, scale="MeV")
    mum_PT = calc_ccb_corrected_pt(1, -1, mum_PT, mum_PHI, mum_ETA, deltas, scale="MeV")

    invariant_mass = calc_invariant_mass(*data)

    # calculate the A_fb with erros
    bin_avg_energy, Afb, err_invariant_mass, err_counts = measure_Afb_from_data(data, 7, (0.6e5, 1.2e5))


    # Plot A_fb as a function of invariant mass
    plt.scatter(bin_avg_energy, Afb)
    plt.title("Forward-Backward Asymmetry vs. Invariant Mass")
    plt.xlabel("Mass (?)")
    plt.ylabel("$A_{fb}$")
    plt.errorbar(bin_avg_energy, Afb, err_counts, err_invariant_mass, fmt='', linestyle='', color='b')

    plt.savefig(f"{StoragePaths.plots_path}/ccb_corrected_A_fb_measurement_with_errors_plot.png")
    plt.show()


if __name__ == "__main__":
    main()




import numpy as np
import matplotlib.pyplot as plt

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.processing.mass import calc_invariant_mass
from weak_mixing_angle.processing.asymmetry import measure_Afb_from_data


# Plot the invaraint mass for forward
# vs backward events with errors
def main():    
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA= read_muon_data(StoragePaths.muon_decay_data, "DecayTree;1")
    data = mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA

    # calculate the A_fb with erros
    bin_avg_energy, Afb, err_invariant_mass, err_counts = measure_Afb_from_data(data, n_bins=21)


    # Plot A_fb as a function of invariant mass
    plt.scatter(bin_avg_energy, Afb)
    plt.title("Forward-Backward Asymmetry vs. Invariant Mass")
    plt.xlabel("Mass (?)")
    plt.ylabel("$A_{fb}$")
    plt.errorbar(bin_avg_energy, Afb, err_counts, err_invariant_mass, fmt='', linestyle='', color='b')

    plt.savefig(f"{StoragePaths.plots_path}/A_fb_invariant_mass_scatter_with_errors_plot.png")
    plt.show()


if __name__ == "__main__":
    main()

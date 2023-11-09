import numpy as np
import matplotlib.pyplot as plt

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.processing.mass import calc_invariant_mass
from weak_mixing_angle.processing.asymmetry import measure_Afb_from_data


# Plot the invaraint mass for forward
# vs backward events with errors
def main():
    sim_data= read_muon_data(StoragePaths.simulation_data, "Z/DecayTree")
    sim_invariant_mass = calc_invariant_mass(*sim_data)

    real_data= read_muon_data(StoragePaths.real_data, "Z/DecayTree")
    real_invariant_mass = calc_invariant_mass(*real_data)

    # calculate the A_fb with erros
    sim_bin_avg_energy, sim_Afb, sim_err_invariant_mass, sim_err_counts = measure_Afb_from_data(sim_data, 13, (0.6e5, 1.2e5))
    real_bin_avg_energy, real_Afb, real_err_invariant_mass, real_err_counts = measure_Afb_from_data(real_data, 13, (0.6e5, 1.2e5))



    # Plot A_fb as a function of invariant mass
    plt.title("Forward-Backward Asymmetry vs. Invariant Mass")
    plt.xlabel("Mass (?)")
    plt.ylabel("$A_{fb}$")
    plt.errorbar(sim_bin_avg_energy, sim_Afb, sim_err_counts, sim_err_invariant_mass, fmt='', linestyle='', color='b',label="simulation")
    plt.errorbar(real_bin_avg_energy, real_Afb, real_err_counts, real_err_invariant_mass, fmt='', linestyle='', color='r', label="real")

    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/Afb_sim_vs_real.png")
    plt.show()


if __name__ == "__main__":
    main()




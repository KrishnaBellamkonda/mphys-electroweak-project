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

    # Reconstruction data
    recon_data= read_muon_data(StoragePaths.simulation_data, "mcdttZ/MCDecayTree")
    recon_invariant_mass = calc_invariant_mass(*recon_data)

    # calculate the A_fb with erros
    sim_bin_avg_energy, sim_Afb, sim_err_invariant_mass, sim_err_counts = measure_Afb_from_data(sim_data, 13, (0.6e5, 1.2e5))
    recon_bin_avg_energy, recon_Afb, recon_err_invariant_mass, recon_err_counts = measure_Afb_from_data(recon_data, 13, (0.6e5, 1.2e5))

    # Plot A_fb as a function of invariant mass
    plt.title("Forward-Backward Asymmetry vs. Invariant Mass")
    plt.xlabel("Mass (?)")
    plt.ylabel("$A_{fb}$")
    plt.errorbar(sim_bin_avg_energy, sim_Afb, sim_err_counts, sim_err_invariant_mass, fmt='', linestyle='', color='b',label="simulation")
    plt.errorbar(recon_bin_avg_energy, recon_Afb, recon_err_counts, recon_err_invariant_mass, fmt='', linestyle='', color='r', label="reconstruction")

    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/Afb_reconstruction_vs_simulation.png")
    plt.show()


if __name__ == "__main__":
    main()




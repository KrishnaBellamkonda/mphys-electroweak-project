import numpy as np
import matplotlib.pyplot as plt

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.processing.mass import calc_invariant_mass

# Plot the invaraint mass for forward
# vs backward events
def main():
    # Constants
    n_bins = 10
    
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA= read_muon_data(StoragePaths.muon_decay_data, "DecayTree;1")
    
    # Following the procedure here
    # https://iopscience.iop.org/article/10.1088/1742-6596/383/1/012005/pdf#:~:text=The%20forward%2Dbackward%20asymmetry%20Afb,search%20for%20new%20physics%20signatures.
    
    # 1) Calculate invariant mass
    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)

    # 2) Divide the mass into bins
    counts, bins = np.histogram(invariant_mass, bins=n_bins, range=(0.4e5, 1.5e5))
    # This accesses these bins and calculated F, B => A_fb
    # and the average invariant mass of the bin
    bin_avg_energy = [] 
    bin_forward_events = []
    bin_backward_events = []
    for i in range(n_bins):
        min_bin_val = bins[i]
        max_bin_val= bins[i+1]

        # Filtering for the events with the masses in the bin
        bin_filter = (invariant_mass>=min_bin_val) & (invariant_mass<=max_bin_val)
        bin_invariant_mass = invariant_mass[bin_filter]
        bin_avg_energy.append(np.mean(bin_invariant_mass))


        bin_mup_ETA, bin_mum_ETA = mup_ETA[bin_filter], mum_ETA[bin_filter]

        # Finding the number of forward and backward events
        n_backward = np.sum(bin_mum_ETA > bin_mup_ETA)
        n_forward = np.sum(bin_mum_ETA < bin_mup_ETA)
        bin_forward_events.append(n_forward)
        bin_backward_events.append(n_backward)
    
    # 3) Calculate Asymmetry 
    asymmetry_fb = [(F-B)/(F+B) for F, B in zip(bin_forward_events, bin_backward_events)]

    # Plot A_fb as a function of invariant mass
    plt.scatter(bin_avg_energy, asymmetry_fb)
    plt.title("Forward-Backward Asymmetry vs. Invariant Mass")
    plt.xlabel("Mass (?)")
    plt.ylabel("$A_{fb}$")
    plt.savefig(f"{StoragePaths.plots_path}/A_fb_invariant_mass_scatter_plot.png")
    plt.show()



    


if __name__ == "__main__":
    main()

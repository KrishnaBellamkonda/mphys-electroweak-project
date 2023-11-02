import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.processing.mass import calc_invariant_mass
from weak_mixing_angle.utility.constants import Paths

def main():
    # Constants & Parameters
    n_bins = 60
    data_file = Paths.muon_decay_data
    tree_name="DecayTree;1"


    # Gathered the data
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA = read_muon_data(data_file, tree_name)
    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)
    
    # Labels
    counts, bins, = np.histogram(invariant_mass, bins=n_bins, range=(0.4e5, 1.5e5))
    max_counts = np.max(counts)
    max_bin_index = np.argmax(counts)
    max_bin_avg = (bins[max_bin_index]+bins[max_bin_index+1])/2

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(invariant_mass, density=False, range=(0.4e5, 1.5e5), bins=n_bins, label="Invariant mass")
    ax.set_ylabel("Counts")
    ax.set_xlabel("Mass")
    ax.set_title("Distribution of the Invariant Mass in Muon Deacy")
    ax.annotate(
        xy=(max_bin_avg, max_counts+500), 
        xytext=(max_bin_avg-50000, max_counts-20000),
        text=f"Peak: {max_bin_avg:0.2f}\ncounts: {max_counts}", 
        arrowprops=dict(facecolor='black', linestyle="dashed"))
    
    plt.savefig(f"{Paths.plots_path}/invariant_mass_distribution.png")
    
    plt.show()

    


if __name__ == "__main__":
    main()



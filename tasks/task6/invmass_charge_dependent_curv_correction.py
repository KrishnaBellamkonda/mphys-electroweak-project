import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.processing.mass import *
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.processing.corrections import *

def main():
    # Constants & Parameters
    n_bins = 60
    data_file = StoragePaths.real_data
    tree_name="Z/DecayTree"


    # Gathered the data
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA = read_muon_data(data_file, tree_name)
    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)
    deltas=get_deltas(StoragePaths.pseudomass_corrections_combined)
    invariant_mass_with_CCB_correction = calc_invariant_mass_with_CCB_correction(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA,deltas)

    # Labels
    counts, bins, = np.histogram(invariant_mass, bins=n_bins, range=(0.4e5, 1.5e5))
    max_counts = np.max(counts)
    max_bin_index = np.argmax(counts)
    max_bin_avg = (bins[max_bin_index]+bins[max_bin_index+1])/2

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(invariant_mass, density=False, range=(0.4e5, 1.5e5), bins=n_bins, label="Invariant mass")
    ax.hist(invariant_mass_with_CCB_correction, density=False, range=(0.4e5, 1.5e5), bins=n_bins, label="Invariant mass with correction")
    ax.set_ylabel("Counts")
    ax.set_xlabel("Mass")
    ax.set_title("Distribution of the Invariant Mass in Muon Deacy")
    ax.annotate(
        xy=(max_bin_avg, max_counts+500), 
        xytext=(max_bin_avg-50000, max_counts-20000),
        text=f"Peak: {max_bin_avg:0.2f}\ncounts: {max_counts}", 
        arrowprops=dict(facecolor='black', linestyle="dashed"))
    
    plt.savefig(f"{StoragePaths.plots_path}/invariant_mass_distribution_with_CCBcorrection.png")
    
    plt.show()

    


if __name__ == "__main__":
    main()



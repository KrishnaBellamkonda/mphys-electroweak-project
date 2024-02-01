import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.processing.mass import *
from weak_mixing_angle.processing.corrections import get_deltas
from weak_mixing_angle.utility.constants import StoragePaths

def main():
    # Constants & Parameters
    n_bins = 60
    data_file = StoragePaths.real_data
    tree_name="Z/DecayTree"


    # Gathered the data
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA = read_muon_data(data_file, tree_name)
    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)
    deltas = get_deltas(StoragePaths.pseudomass_corrections_combined)

    print(f"{deltas=}")

    # Corrections for mup_PT
    mup_PT_corrected = calc_ccb_corrected_pt(1, 1, mup_PT, mup_PHI, mup_ETA, deltas, scale="MeV")
    mum_PT_corrected = calc_ccb_corrected_pt(1, 1, mum_PT, mum_PHI, mum_ETA, deltas, scale="MeV")
    invariant_mass_with_CCB_correction = calc_invariant_mass(mup_PT_corrected, mup_PHI, mup_ETA, mum_PT_corrected, mum_PHI, mum_ETA)
    print(f"{invariant_mass=}")
    print(f"{mup_PT=}")
    print(f"{mup_PT_corrected=}")
    print(f"{invariant_mass_with_CCB_correction=}")

    # Labels
    counts, bins, = np.histogram(invariant_mass, bins=n_bins, range=(0.4e5, 1.5e5))
    max_counts = np.max(counts)
    max_bin_index = np.argmax(counts)
    max_bin_avg = (bins[max_bin_index]+bins[max_bin_index+1])/2

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(invariant_mass, density=False, range=(0.4e5, 1.5e5), bins=n_bins, label="Uncorrected", alpha = 0.5)
    ax.hist(invariant_mass_with_CCB_correction, density=False, range=(0.4e5, 1.5e5), bins=n_bins, label="Corrected", alpha=0.5)
    ax.set_ylabel("Counts")
    ax.set_xlabel("Mass")
    ax.set_title("Distribution of the Invariant Mass with/out charge curvature corrections")
    ax.annotate(
        xy=(max_bin_avg, max_counts+500), 
        xytext=(max_bin_avg-50000, max_counts-20000),
        text=f"Peak: {max_bin_avg:0.2f}\ncounts: {max_counts}", 
        arrowprops=dict(facecolor='black', linestyle="dashed"))
    
    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/invariant_mass_distribution_with_CCB_correction.png")
    plt.show()

    


if __name__ == "__main__":
    main()



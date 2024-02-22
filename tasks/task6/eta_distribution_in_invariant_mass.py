import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.processing.mass import *
from weak_mixing_angle.processing.corrections import get_deltas
from weak_mixing_angle.utility.constants import StoragePaths

def main():
    # Constants & Parameters
    n_bins = 7 # Number of bins for measuring the Afb
    data_file = StoragePaths.real_data
    tree_name = "Z/DecayTree"

    # Step 2) Read the real data
    data = read_muon_data(data_file, tree_name)
    fidicual_mask, (mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA) = get_fiducial_range_data(data)
    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)
    
    # Step 3) Get the invariant mass bins
    counts, bins = np.histogram(invariant_mass, bins=n_bins)

    # Step 4) Plt
    fig, axes = plt.subplots(4, 2, figsize=(20, 12), sharex=True, sharey=False)
    
    for index in range(bins.shape[0]-1):
        min_bin = bins[index]
        max_bin = bins[index+1]
        mask = (invariant_mass >= min_bin) & (invariant_mass < max_bin)

        row = index // 2
        column = index % 2
        print(f"{row=} {column=}")

        mup_eta_bin = mup_ETA[mask]
        mum_eta_bin = mum_ETA[mask]

        axes[row][column].hist(mup_eta_bin, bins=7, label="Muon+", alpha = 0.7)
        axes[row][column].hist(mum_eta_bin, bins=7, label="Muon-", alpha = 0.7)

        axes[row][column].set_title(f"Eta distribution in bin={index+1} {min_bin:.2f} <= m < {max_bin:.2f}")
        axes[row][column].legend()
    
    plt.xlabel("Count")
    plt.ylabel("Eta")
    plt.savefig(f"{StoragePaths.plots_path}/eta_distribution_in_invmass_bins.png")

if __name__ == "__main__":
    main()



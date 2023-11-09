import numpy as np
import matplotlib.pyplot as plt

from weak_mixing_angle.utility.constants import StoragePaths

def create_histogram(invariant_mass, filename, fiducial_range=None,  n_bins=21, xy_text=(-50000, -20000)):

    counts, bins, = np.histogram(invariant_mass, bins=n_bins, range=fiducial_range)
    max_counts = np.max(counts)
    max_bin_index = np.argmax(counts)
    max_bin_avg = (bins[max_bin_index]+bins[max_bin_index+1])/2

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(invariant_mass, density=False, range=fiducial_range, bins=n_bins, label="Invariant mass")
    ax.set_ylabel("Counts")
    ax.set_xlabel("Mass")
    ax.set_title("Distribution of the Invariant Mass in Muon Deacy")
    ax.annotate(
        xy=(max_bin_avg, max_counts+500), 
        xytext=(max_bin_avg-xy_text[0], max_counts-xy_text[1]),
        text=f"Peak: {max_bin_avg:0.2f}\ncounts: {max_counts}", 
        arrowprops=dict(facecolor='black', linestyle="dashed"))
    
    plt.savefig(f"{StoragePaths.plots_path}/{filename}.png")
    

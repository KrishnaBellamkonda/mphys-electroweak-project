import numpy as np
import uproot
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.processing.mass import calc_invariant_mass
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.processing.mass import get_fiducial_range_data
from weak_mixing_angle.processing.trigger import calc_trigger_eff, correct_events_for_trigger_efficiencies

def main():
    # Step 1) Constants & Parameters
    n_bins = 31
    data_file = StoragePaths.real_data
    tree_name = "Z/DecayTree"


    # Step 2) Read the real data
    data = read_muon_data(data_file, tree_name)
    fidicual_mask, (mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA) = get_fiducial_range_data(data)

    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)
    

    # Step 2.5) Weight the data with eta efficiencies
    
    # Obtaining the effciencies 
    with uproot.open(data_file) as file:
        tree = file[tree_name]
        branches=tree.arrays()
        posFlags=np.array(branches["mup_L0MuonEWDecision_TOS"])
        negFlags=np.array(branches["mum_L0MuonEWDecision_TOS"])

    posFlags = posFlags[fidicual_mask]
    negFlags= negFlags[fidicual_mask]

    mup_eff,mup_eff_err, mup_bins = calc_trigger_eff(mup_ETA,n_bins,True,posFlags,negFlags)
    mum_eff,mum_eff_err, mum_bins = calc_trigger_eff(mum_ETA,n_bins,False,posFlags,negFlags)

    # Mapping muon+ to the right bin
    print(f"{mup_ETA=}")
    invariant_mass = correct_events_for_trigger_efficiencies(invariant_mass, mup_ETA, mup_bins, mup_eff)

    # Mapping muon- int the right bin and updating the invariant mass
    invariant_mass = correct_events_for_trigger_efficiencies(invariant_mass, mum_ETA, mum_bins, mum_eff)
    
    # Step 3) Create two psuedomass distributions
    pos_psuedomass_factor = np.sqrt(mup_PT/mum_PT)
    neg_psuedomass_factor = np.sqrt(mum_PT/mup_PT)

    pos_psuedomass = invariant_mass * pos_psuedomass_factor
    neg_psuedomass = invariant_mass * neg_psuedomass_factor    

    print(pos_psuedomass)
    print(neg_psuedomass)

    # Step 4) Plot pos psuedo mass
    counts, bins, = np.histogram(pos_psuedomass, bins=n_bins)
    max_counts = np.max(counts)
    max_bin_index = np.argmax(counts)
    max_bin_avg = (bins[max_bin_index]+bins[max_bin_index+1])/2

    bin_centres = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(pos_psuedomass, density=False, bins=n_bins, label="Pos Psuedomass", alpha=0.5, color="blue") 
    #    ax.set_ylabel("Counts")
    #ax.scatter(bin_centres, counts, label="Pos Psuedomass", color="red", s=2)
    ax.set_xlabel("Mass")
    ax.set_title("Distribution of the Invariant Mass in Muon Deacy")
    #ax.annotate(
    #    xy=(max_bin_avg, max_counts+500), 
    #    xytext=(max_bin_avg-5000, max_counts-2000),
    #    text=f"Peak: {max_bin_avg:0.2f}\ncounts: {max_counts}", 
    #    arrowprops=dict(facecolor='black', linestyle="dashed"))
    

    # Step 5) Plot neg psuedo mass
    counts, bins, = np.histogram(neg_psuedomass, bins=n_bins)
    max_counts = np.max(counts)
    max_bin_index = np.argmax(counts)
    max_bin_avg = (bins[max_bin_index]+bins[max_bin_index+1])/2

    ax.hist(neg_psuedomass, density=False, bins=n_bins, label="Neg Psuedomass", color="red", alpha=0.5)
    
    #ax.scatter(bin_centres, counts, label="Neg Psuedomass", color="blue", s=4, marker='^')
    ax.set_ylabel("Counts")
    ax.set_xlabel("Mass")
    ax.set_title("Distribution of the Invariant Mass with weighted efficiencies")
    #ax.annotate(
    #    xy=(max_bin_avg, max_counts+500),
    #    xytext=(max_bin_avg-5000, max_counts-2000),
    #    text=f"Peak: {max_bin_avg:0.2f}\ncounts: {max_counts}",
    #    arrowprops=dict(facecolor='black', linestyle="dashed"))
    
    # Setting limits on axis
    ax.set_xlim([0.2e5, 1.5e5])

    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/psuedo_mass_dist_with_efficiencies.png")
    
    plt.show()

    


if __name__ == "__main__":
    main()



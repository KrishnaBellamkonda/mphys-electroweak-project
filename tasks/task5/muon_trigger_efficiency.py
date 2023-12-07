import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import uproot
from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.processing.mass import calc_invariant_mass
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.processing.mass import get_fiducial_range_data
from weak_mixing_angle.processing.trigger import calc_trigger_eff

def main():
    # Step 1) Constants & Parameters
    n_bins = 7
    data_file = StoragePaths.real_data
    tree_name = "Z/DecayTree"
    with uproot.open(data_file) as file:
        tree = file[tree_name]
        branches=tree.arrays()
        posFlags=np.array(branches["mup_L0MuonEWDecision_TOS"])
        negFlags=np.array(branches["mum_L0MuonEWDecision_TOS"])

        

    # Step 2) Read the real data
    data = read_muon_data(data_file, tree_name)
    fiducialMask, (mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA) = get_fiducial_range_data(data)
    posFlags=posFlags[fiducialMask]
    negFlags=negFlags[fiducialMask]
 
    
    mup_eff,mup_eff_err, mup_bins = calc_trigger_eff(mup_ETA,n_bins,True,posFlags,negFlags)
    mum_eff,mum_eff_err, mum_bins = calc_trigger_eff(mum_ETA,n_bins,False,posFlags,negFlags)

    
    
    # Step 3) Plotting the data
    mup_bin_centres = [(mup_bins[i]+mup_bins[i+1])/2 for i in range(n_bins)]
    mum_bin_centres = [(mum_bins[i]+mum_bins[i+1])/2 for i in range(n_bins)]

    plt.errorbar(mup_bin_centres, mup_eff, mup_eff_err, marker="o", c="b", label="mu+")
    plt.errorbar(mum_bin_centres, mum_eff, mum_eff_err, marker="o", c="r", label="mu-")
    
    print(f"{mup_eff_err=}")
    print(f"{mum_eff_err=}")

    plt.xlabel("eta")
    plt.ylabel("efficiency")
    
    plt.legend()
    plt.savefig(f"{StoragePaths.plots_path}/trigger_efficiency_line_7_bins.png")

    plt.show()


if __name__ == "__main__":
    main()

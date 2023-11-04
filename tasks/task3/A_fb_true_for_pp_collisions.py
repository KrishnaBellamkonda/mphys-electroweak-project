# This script obtains a histogram 
# and calculates the Afb for the
# data files
import uproot

from weak_mixing_angle.utility.constants import Paths
from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.processing.mass import calc_invariant_mass

def main():
    # Constants
    n_bins = 21
    
    # Getting the data
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA= read_muon_data(Paths.ppdata1, tree_name="MCDecayTree;1")
    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)
    
    # Labels


    print(mup_PT)

if __name__ == "__main__":
    main()
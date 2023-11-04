# This script obtains a histogram 
# and calculates the Afb for the
# data files
import uproot
from weak_mixing_angle.utility.constants import Paths
from weak_mixing_angle.utility.utils import read_muon_data

def main():
    # mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA= read_muon_data(Paths.pp_data, tree_name="Z/DecayTree";")

    with uproot.open(Paths.pp_data) as file:
        print(file.keys())


if __name__ == "__main__":
    main()
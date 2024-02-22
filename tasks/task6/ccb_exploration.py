import uproot
from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.processing.mass import *
from weak_mixing_angle.processing.corrections import get_deltas
from weak_mixing_angle.utility.constants import StoragePaths

corrections_data, corrections_Z, corrections = StoragePaths.pseudomass_corrections_combined

tree_name = "pseudomass_corrections;1"

# Corrections Data?
with uproot.open(corrections_data) as file:
    tree = file[tree_name]
    t_data = tree.arrays()
    print(list(tree.branches))

    eta = t_data["eta"]
    print(f"Length: {len(eta)=}")
    print(np.unique(np.array(eta, dtype=np.float64)))
    phi = t_data["phi"]
    print(np.unique(np.array(phi).astype(np.float64)))
    period = t_data["period"]
    print(np.unique(period))

    diff = np.ediff1d(phi)
    print(f"{diff=}")
    for i in range(0, len(eta), 50):
        print(eta[i], phi[i])

with uproot.open(corrections_Z) as file:
    tree = file[tree_name]
    t_mc = tree.arrays()

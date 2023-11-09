from weak_mixing_angle.processing.mass import calc_invariant_mass
from weak_mixing_angle.visualization.invariant_mass_histogram import create_histogram
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.utility.utils import read_muon_data


def main():
    data = read_muon_data(StoragePaths.ppdata2, "MCDecayTree;1")
    invariant_mass = calc_invariant_mass(*data)
    create_histogram(invariant_mass, "pp2_invariant_mass_distribution", xy_text=(-20, -20))


if __name__ == "__main__":
    main()

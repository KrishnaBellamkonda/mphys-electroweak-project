from weak_mixing_angle.processing.mass import calc_invariant_mass
from weak_mixing_angle.visualization.invariant_mass_histogram import create_histogram
from weak_mixing_angle.utility.constants import StoragePaths
from weak_mixing_angle.utility.utils import read_muon_data


def main():
    data = read_muon_data(StoragePaths.simulation_data, "Z/DecayTree")
    invariant_mass = calc_invariant_mass(*data)
    create_histogram(invariant_mass, "simulation_invariant_mass_distribution_in_fudicial", (0.6e5, 1.20e5) , xy_text=(-20, 20))


if __name__ == "__main__":
    main()

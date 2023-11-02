import numpy as np
import matplotlib.pyplot as plt

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.utility.constants import Paths
from weak_mixing_angle.processing.mass import calc_invariant_mass
from weak_mixing_angle.processing.asymmetry import calc_fb_true, FBTrueParameters

# Plot the invaraint mass for forward
# vs backward events
def main():
    # Constants
    Z_pole = 90416 # MeV/c^2 calculated from first task
    vicinity_range = 90_000
    max_energy = Z_pole+vicinity_range
    min_energy = Z_pole-vicinity_range

    
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA= read_muon_data(Paths.muon_decay_data, "DecayTree;1")
    
    # Following the procedure here
    # https://iopscience.iop.org/article/10.1088/1742-6596/383/1/012005/pdf#:~:text=The%20forward%2Dbackward%20asymmetry%20Afb,search%20for%20new%20physics%20signatures.
    
    # 1) Filter the invariant mass near the Z pole
    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)
    vicinity_filter = (invariant_mass>(min_energy)) & (invariant_mass<(max_energy))
    invariant_mass = invariant_mass[vicinity_filter]

    # 2) Count the number of forward and
    # backward events in this domain
    F = np.sum(mum_ETA[vicinity_filter] > mup_ETA[vicinity_filter])
    B = np.sum(mum_ETA[vicinity_filter] < mup_ETA[vicinity_filter])
    asymmetry_fb = (F-B)/(F+B)

    # 3) Now using the expansion of Afb to 
    # measure the angle sin^2(theta)
    m_z, m_w = 90.1876, 80.377 # in GeV
    sin_2_theta = (1- 4*asymmetry_fb)/4
    sin2theta_w  = 1 - ((m_w**2)/(m_z**2))
    print(f"{sin_2_theta=} {sin2theta_w=}")

    # Setting the parameters for up quarks
    m_ll = invariant_mass / 10e2 # Converting to GeV units
    print(f"{m_ll=} {invariant_mass=}")
    up_params = FBTrueParameters(
        Q_l=(-1),
        T3_l=(-1/2),
        Q_q=(2/3),
        T3_q=(1/2),
        m_ll=m_ll, # using the invariant mass calculated as the m_ll
        weak_mixing_angle=sin_2_theta
    )
    A_fb_true_up = calc_fb_true(up_params)

    # 4) Plot a relationship between the m_ll and A_fb_true
    plt.scatter(x = m_ll, y=A_fb_true_up, label="Up - anti-up")
    plt.title("True Asymmetry fb for up-quarks into muons for $sin(θ_{w})$="+f"{sin_2_theta:0.5}")
    plt.ylabel("$A_{fb}$")
    plt.xlabel("Invariant mass (GeV)")
    plt.legend()
    plt.savefig(f"{Paths.plots_path}/A_fb_true_for_up_quarks.png")
    plt.show()


if __name__ == "__main__":
    main()

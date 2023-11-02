import numpy as np
import matplotlib.pyplot as plt

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.utility.constants import Paths
from weak_mixing_angle.processing.mass import calc_invariant_mass
from weak_mixing_angle.processing.asymmetry import calc_fb_true, FBTrueParameters


def main():
    # Use the same invariant mass for all of
    # the graph
    m_ll = np.linspace(40, 150, 50) 
    
    # Setting the parameters for different quarks
    up_params = FBTrueParameters(
        Q_l=(-1),
        T3_l=(-1/2),
        Q_q=(2/3),
        T3_q=(1/2),
        m_ll=m_ll
    )
    A_fb_true_up =  calc_fb_true(up_params)

    down_params = FBTrueParameters(
        Q_l=(-1),
        T3_l=(-1/2),
        Q_q=(-1/3),
        T3_q=(-1/2),
        m_ll=m_ll
    )
    A_fb_true_down =  calc_fb_true(down_params)



    # 4) Plot a relationship between the m_ll and A_fb_true

    plt.plot(m_ll, A_fb_true_up, label="up quarks", linestyle="--")
    plt.plot(m_ll, A_fb_true_down, label="down quarks", linestyle="dotted")

    plt.title("True Asymmetry fb for up-quarks into muons for $sin(θ_{w})$=0.231")
    plt.ylabel("$A_{fb}$")
    plt.xlabel("Invariant mass (GeV)")
    plt.legend()
    plt.savefig(f"{Paths.plots_path}/A_fb_true_different_quarks.png")
    plt.show()

if __name__ == "__main__":
    main()

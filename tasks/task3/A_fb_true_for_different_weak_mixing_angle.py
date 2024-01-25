import numpy as np
import matplotlib.pyplot as plt

from weak_mixing_angle.utility.utils import read_muon_data
from weak_mixing_angle.utility.constants import Paths
from weak_mixing_angle.processing.asymmetry import calc_fb_true, FBTrueParameters


def main():
    # Use the same invariant mass for all of
    # the graph
    m_ll = np.linspace(40, 150, 50)
    wma_1, wma_2, wma_3 = 0.181, 0.231, 0.291
    
    # Setting the parameters for different quarks
    up_params_1 = FBTrueParameters(
        Q_l=(-1),
        T3_l=(-1/2),
        Q_q=(2/3),
        T3_q=(1/2),
        m_ll=m_ll, 
        weak_mixing_angle=wma_1
    )

    up_params_2 = FBTrueParameters(
        Q_l=(-1),
        T3_l=(-1/2),
        Q_q=(2/3),
        T3_q=(1/2),
        m_ll=m_ll, 
        weak_mixing_angle=wma_2
    )

    up_params_3 = FBTrueParameters(
        Q_l=(-1),
        T3_l=(-1/2),
        Q_q=(2/3),
        T3_q=(1/2),
        m_ll=m_ll, 
        weak_mixing_angle=wma_3
    )

    A_fb_true_up_1 =  calc_fb_true(up_params_1)
    A_fb_true_up_2 =  calc_fb_true(up_params_2)
    A_fb_true_up_3 =  calc_fb_true(up_params_3)

    down_params = FBTrueParameters(
        Q_l=(-1),
        T3_l=(-1/2),
        Q_q=(-1/3),
        T3_q=(-1/2),
        m_ll=m_ll
    )
    A_fb_true_down =  calc_fb_true(down_params)



    # 4) Plot a relationship between the m_ll and A_fb_true
    sin2theta_w_tex = r"$\sin^{2}\left(\theta_w\right)$"
    plt.plot(m_ll, A_fb_true_up_1, label=f"{sin2theta_w_tex} = {wma_1}", linestyle="dashed", marker="o")
    plt.plot(m_ll, A_fb_true_up_2, label=f"{sin2theta_w_tex} = {wma_2}", linestyle="dashed", marker="v")
    plt.plot(m_ll, A_fb_true_up_3, label=f"{sin2theta_w_tex} = {wma_3}", linestyle="dashed", marker="s")

    # plt.plot(m_ll, A_fb_true_down, label="down quarks", linestyle="dotted")

    plt.title("True Asymmetry fb for up-quarks into muons for different $sin(θ_{w})$")
    plt.ylabel("$A_{fb}$")
    plt.xlabel("Invariant mass (GeV)")
    plt.legend()
    plt.savefig(f"{Paths.plots_path}/A_fb_true_different_weak_mixing_angles.png")
    plt.show()

if __name__ == "__main__":
    main()

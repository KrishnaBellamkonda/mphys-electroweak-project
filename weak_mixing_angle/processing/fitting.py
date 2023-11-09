import numpy as np
from scipy.optimize import least_squares
from weak_mixing_angle.processing.asymmetry import calc_fb_true, FBTrueParameters
from weak_mixing_angle.utility.utils import calc_chi_sqared_error, quadratic

def calc_chi_squared_for_mixing_angle(data, wma, m_ll, std_values=None):
    # Step 1) Making the theory predictions for
    # the given weak mixing angle
    up_params = FBTrueParameters(
        Q_l=(-1),
        T3_l=(-1/2),
        Q_q=(2/3),
        T3_q=(1/2),
        m_ll=m_ll,
        weak_mixing_angle=wma
    )

    Afb_pred = calc_fb_true(up_params)
    
    if std_values is None:
        len_data = len(data)
        std_values = np.ones(len_data) * 1/np.sqrt(len_data)

    # 2) Calculating the chi-squared error
    # between the model and the theory
    chi_squared_error = calc_chi_sqared_error(data, Afb_pred, std_values)

    return chi_squared_error.sum()


def fit_quadratic(x, y):

    def residual(params, x, y):
        a, b, c = params
        return y - quadratic(x, a, b, c)

    initial_params = [1, 1, 0] # A, B, C
    res_1 = least_squares(residual, initial_params, args=(x, y))
    return res_1.x


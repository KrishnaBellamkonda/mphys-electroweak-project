# This module contains all of the functions related
# to asymmetry calculations
import numpy as np
import numpy.typing as npt
from typing import Optional
from pydantic import BaseModel
import matplotlib.pyplot as plt

from weak_mixing_angle.utility.constants import Paths
from weak_mixing_angle.processing.mass import calc_invariant_mass 
from weak_mixing_angle.processing.corrections import *

def calc_fb_asymmetry(mum_ETA: npt.NDArray,mup_ETA:npt.NDArray):
    F = np.sum(mum_ETA > mup_ETA)
    B = np.sum(mum_ETA < mup_ETA)
    asymmetry_fb = (F-B)/(F+B)
    return asymmetry_fb


class FBTrueParameters(BaseModel):
    T3_q: float # 3rd component of iso-spin of a quark 
    Q_q: float # Charge of the quark
    T3_l: float # 3rd component of iso-spin of a lepton
    Q_l:float # Charge of the lepton 
    m_ll:np.ndarray = np.linspace(40, 150)
    weak_mixing_angle:float = 0.231 # The standard value of weak-mixing angle

    class Config:
        arbitrary_types_allowed = True

# This function calculates the true value of Afb
# as predicted by the theory for any two particle
# collisions
def calc_fb_true(fb_true_parameters: FBTrueParameters):
    
    # Calculating the asymmetry of the data
    # with background correction

    # Fundamental phenomenon happening
    # Leptopn pairs are created by anhilation of quark
    # with its anti-quark which produces a Z boson or a virtual
    # photon which then decays into a lepton, anti-leptopn pair
    # For our case: lepton we have is a muon and quark for example
    # we have is an up-quark 

    # User Inputs
    T3_l = fb_true_parameters.T3_l
    Q_l = fb_true_parameters.Q_l
    T3_q = fb_true_parameters.T3_q
    Q_q = fb_true_parameters.Q_q
    m_ll = fb_true_parameters.m_ll
    sin2thetaw = fb_true_parameters.weak_mixing_angle

    # Mass of W and Z bosons
    m_w, m_z = 80.370, 91.1876 # GeV
    
    Gf = (1.166378e-5) # Fermi constant (GeV)
    alpha = 1/137.036 # Electro-magnetic Coupling (no units)


    # Finding the true asymmetry FB
    a_l = (T3_l)
    a_q = (T3_q)

    v_l = T3_l - (2*Q_l*sin2thetaw)
    v_q = T3_q - (2*Q_q*sin2thetaw)

    K = (8*np.sqrt(2)*np.pi*alpha)/(Gf*m_z**2)
    D_m = 1-(m_z**2 / m_ll**2)
    T_z = 52_316/1000 # full decay width of z boson (MeV)

    Afb_numerator = 6*(a_l*a_q)*(8*v_l*v_q - Q_q*K*D_m)
    Afb_denominator = 16*(v_l**2+a_l**2)*(v_q**2+a_q**2) - 8*(v_l*v_q*Q_q*K*D_m) + ((Q_q**2)*(K**2)*(D_m**2 + (T_z**2)/(m_z**2)))
    Afb_true = Afb_numerator/Afb_denominator


    
    return  Afb_true


# General function to measure the Afb from 
# real data with error bars

def poisson_error(counts:int):
    return 1/np.sqrt(counts)

def measure_Afb_from_data(data, n_bins:int=21, fiducial_region=(0.4e5, 1.5e5)):
    # Following the procedure here
    # https://iopscience.iop.org/article/10.1088/1742-6596/383/1/012005/pdf#:~:text=The%20forward%2Dbackward%20asymmetry%20Afb,search%20for%20new%20physics%20signatures.


    # 1) Calculate invariant mass
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA = data
    invariant_mass = calc_invariant_mass(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA)

    # 2) Divide the mass into bins
    counts, bins = np.histogram(invariant_mass, bins=n_bins, range=fiducial_region)
    # This accesses these bins and calculated F, B => A_fb
    # and the average invariant mass of the bin
    bin_avg_energy = []
    bin_forward_events = []
    bin_backward_events = []
    bin_y_errors = [] # error in the no. of counts
    bin_x_errors = [] # error in the mean invariant mass
    for i in range(n_bins):
        min_bin_val = bins[i]
        max_bin_val= bins[i+1]

        # Filtering for the events with the masses in the bin
        bin_filter = (invariant_mass>=min_bin_val) & (invariant_mass<=max_bin_val)
        bin_invariant_mass = invariant_mass[bin_filter]
        bin_avg_energy.append(np.mean(bin_invariant_mass))
        
        # Using std to calculate the average error in energy
        std_avg_energy = np.std(bin_invariant_mass)
        bin_x_errors.append(std_avg_energy)

        bin_mup_ETA, bin_mum_ETA = mup_ETA[bin_filter], mum_ETA[bin_filter]

        # Finding the number of forward and backward events
        n_forward = np.sum(bin_mum_ETA > bin_mup_ETA)
        n_backward = np.sum(bin_mum_ETA < bin_mup_ETA)
        bin_forward_events.append(n_forward)
        bin_backward_events.append(n_backward)
        bin_error = poisson_error(len(bin_invariant_mass)) # 1/sqrt(N)
        bin_y_errors.append(bin_error)

    # 3) Calculate Asymmetry
    asymmetry_fb = [(F-B)/(F+B) for F, B in zip(bin_forward_events, bin_backward_events)]
    
    # 4) Make the std errors more accurate by using the 
    # sigma = sqrt(1-Afb**2) * poisson_error
    bin_y_errors = [(1 - asymmetry_fb[i]**2)*err  for i, err in enumerate(bin_y_errors)]

    return bin_avg_energy, asymmetry_fb, bin_x_errors, bin_y_errors

def measure_Afb_from_data_with_CCB_correction(data,charge_correction_data,n_bins:int=21, fiducial_region=(0.4e5, 1.5e5)):
    # Following the procedure here
    # https://iopscience.iop.org/article/10.1088/1742-6596/383/1/012005/pdf#:~:text=The%20forward%2Dbackward%20asymmetry%20Afb,search%20for%20new%20physics%20signatures.

    #0) Calculate deltas

    deltas=compute_deltas(charge_correction_data)

    # 1) Calculate invariant mass
    mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA = data
    invariant_mass = calc_invariant_mass_with_CCB_correction(mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA,deltas,)

    # 2) Divide the mass into bins
    counts, bins = np.histogram(invariant_mass, bins=n_bins, range=fiducial_region)
    # This accesses these bins and calculated F, B => A_fb
    # and the average invariant mass of the bin
    bin_avg_energy = []
    bin_forward_events = []
    bin_backward_events = []
    bin_y_errors = [] # error in the no. of counts
    bin_x_errors = [] # error in the mean invariant mass
    for i in range(n_bins):
        min_bin_val = bins[i]
        max_bin_val= bins[i+1]

        # Filtering for the events with the masses in the bin
        bin_filter = (invariant_mass>=min_bin_val) & (invariant_mass<=max_bin_val)
        bin_invariant_mass = invariant_mass[bin_filter]
        bin_avg_energy.append(np.mean(bin_invariant_mass))
        
        # Using std to calculate the average error in energy
        std_avg_energy = np.std(bin_invariant_mass)
        bin_x_errors.append(std_avg_energy)

        bin_mup_ETA, bin_mum_ETA = mup_ETA[bin_filter], mum_ETA[bin_filter]

        # Finding the number of forward and backward events
        n_forward = np.sum(bin_mum_ETA > bin_mup_ETA)
        n_backward = np.sum(bin_mum_ETA < bin_mup_ETA)
        bin_forward_events.append(n_forward)
        bin_backward_events.append(n_backward)
        bin_error = poisson_error(len(bin_invariant_mass)) # 1/sqrt(N)
        bin_y_errors.append(bin_error)

    # 3) Calculate Asymmetry
    asymmetry_fb = [(F-B)/(F+B) for F, B in zip(bin_forward_events, bin_backward_events)]
    
    # 4) Make the std errors more accurate by using the 
    # sigma = sqrt(1-Afb**2) * poisson_error
    bin_y_errors = [(1 - asymmetry_fb[i]**2)*err  for i, err in enumerate(bin_y_errors)]

    return bin_avg_energy, asymmetry_fb, bin_x_errors, bin_y_errors


# THis function accounts for the QCD correction
# 8.4
def calc_fb_true_with_qcd_correction(fb_true_parameters: FBTrueParameters, is_b_quark:bool = False):
    
    # Mass of W and Z bosons
    alpha_s = 1
    m_w, m_z = 80.370, 91.1876 # GeV

    # Calculating the fb_true values
    Afb_true = calc_fb_true(fb_true_parameters=fb_true_parameters)


    # QCD factor
    if is_b_quark:
        c1 = 0.77
        c2 = 5.93
    else:
        c1 = 0.86
        c2 = 8.5
    factor_1 = (c1*(alpha_s*m_z**2)/np.pi)
    factor_2 = (c2*((alpha_s*m_z**2)/np.pi)**2)
    factor = (1-factor_1 - factor_2)
    
    return  Afb_true*factor

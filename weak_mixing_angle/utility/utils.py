import numpy as np
import pandas as pd
import uproot
from scipy.stats import norm
import typing
import matplotlib.pyplot as plt

# Utility functions
def read_muon_data(source:str, tree_name:str, 
                   mup_PT_name:str = "mup_PT",
                   mup_PHI_name:str = "mup_PHI",
                   mup_ETA_name:str = "mup_ETA",
                   mum_PT_name:str = "mum_PT",
                   mum_PHI_name:str = "mum_PHI",
                   mum_ETA_name:str = "mum_ETA"
                   ):
    
    with uproot.open(source) as file:
        tree = file[tree_name]
        branches = tree.arrays()

        # Extract mu positive data
        mup_PT  = branches[mup_PT_name]
        mup_PHI  = branches[mup_PHI_name]
        mup_ETA  = branches[mup_ETA_name]

        # Extract mu minus data
        mum_PT  = branches[mum_PT_name]
        mum_PHI  = branches[mum_PHI_name]
        mum_ETA  = branches[mum_ETA_name]

    return mup_PT, mup_PHI, mup_ETA, mum_PT, mum_PHI, mum_ETA

#Define the Gaussian function 
def gauss(x, H, A, x0, sigma): 
    return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


def plot_guassian(invariant_mass):
    # Plot a histogram of the data
    plt.hist(invariant_mass, density=True, range=(0.4e5, 1.5e5), bins=n_bins, label="Invariant mass")

    # Fit a gaussian plot
    (mu, sigma) = norm.fit(invariant_mass)
    print(mu, sigma)
    x = np.linspace(0.5e5, 1.5e5, 100) 
    y = norm.pdf(x, mu, sigma) 
    plt.plot(x, y)

def calc_chi_sqared_error(measured_values, theory_values, std_values):
    # summation of (Observed_i - Expecteded_i)^2/std^2
    return (((measured_values - theory_values)**2)/(std_values**2)).sum()
    
def quadratic(x, A, B, C):
    return A*(x**2) + B*(x) + C


def parabola(x, minima, sigma, k):
    a = 1/(2*sigma**2)
    return a*(x-minima)**2 + k

def get_parabola_parameters(a, b):
    minima = -b/(2*a)
    delta = -1/(2*b)
    return minima, delta


<<<<<<< Updated upstream


=======
>>>>>>> Stashed changes
def map_to_bin(var, var_bins):
    # Returns the index of the matching bin
    for i in range(len(var_bins)-1):
        current_edge = var_bins[i]
        next_edge = var_bins[i+1]
        if (var >= current_edge) and (var < next_edge):
            return i
    # If in the last bin, the var is the same as last bin edge
    # just count it in the last bin
    if (var == next_edge):
        return i 
    else:
        return None

<<<<<<< Updated upstream
=======
# def compute_deltas(pseudomass_corrections_datasets):
#     corrections_DATA, corrections_Z,corrections = pseudomass_corrections_datasets
#     f_data = ROOT.TFile(corrections_DATA)
#     t_data = f_data.Get(corrections)
#     f_mc = ROOT.TFile(corrections_Z)
#     t_mc = f_mc.Get(corrections)
#     t_mc.AddFriend(t_data, "data")
#     df_final = ROOT.RDataFrame(t_mc).Define("mc_uncertainty",
#                                             "data.delta_uncertainty").Define(
#                                                 "data_delta", "data.delta")
#     df_final_np = df_final.AsNumpy()
#     deltas = []
#     deltas = [
#         df_final_np["data_delta"][i] - df_final_np["delta"][i]
#         for i in range(len(df_final_np))
#     ]
#     return deltas
>>>>>>> Stashed changes

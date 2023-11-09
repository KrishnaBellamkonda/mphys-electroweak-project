import numpy as np
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
    return ((measured_values - theory_values)**2)/(std_values**2)
    
def quadratic(x, A, B, C):
    return A*(x**2) + B*(x) + C




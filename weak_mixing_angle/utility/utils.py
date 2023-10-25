import numpy as np
import uproot
from scipy.stats import norm
import typing
import matplotlib.pyplot as plt

# Utility functions
def read_muon_data(source:str, tree_name:str):
    
    with uproot.open(source) as file:
        tree = file[tree_name]
        branches = tree.arrays()

        print(branches[0].tolist())

        # Extract mu positive data
        mup_PT  = branches["mup_PT"]
        mup_PHI  = branches["mup_PHI"]
        mup_ETA  = branches["mup_ETA"]

        # Extract mu minus data
        mum_PT  = branches["mum_PT"]
        mum_PHI  = branches["mum_PHI"]
        mum_ETA  = branches["mum_ETA"]

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

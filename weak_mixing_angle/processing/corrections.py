import uproot
import numpy as np
import math


# This file contains the rewritten code from pyroot
# to the latest uproot

# Uproot code on top
def get_deltas(sources_combined):
    corrections_data, corrections_Z, corrections = sources_combined

    tree_name = "pseudomass_corrections;1"
    with uproot.open(corrections_data) as file:
        tree = file[tree_name]
        t_data = tree.arrays()

    with uproot.open(corrections_Z) as file:
        tree = file[tree_name]
        t_mc = tree.arrays()
    
    # mc is Monte Carlo
    delta_data = t_data["delta"]
    delta_mc = t_mc["delta"]

    deltas = delta_data - delta_mc
    return np.array(deltas)


# Correction factor converting to the latest uproot
# def correction_factor(Q, P, indices, deltas):
#     # q/p -> q/p + delta, i.e. p'/p = (1 + Q*delta*P)**-1
#     # print(Q, P, index, deltas)
#     deltas = np.array(deltas)
#     return 1. / (1. + Q * P * deltas[indices])

# What goes in here are the arrays - 
# year - 2016
# polarity - 1
# charge - 1
# mu_eta - mup_ETA
# mu_phi - mup_PHI
# mu_pt - mup_PT
# deltas - deltas (from get_deltas)
def load_pseudomass(year, polarity, charge, mu_eta, mu_phi, mu_pt, deltas, scale="MeV"):

    Qs = mu_pt * np.cosh(mu_eta)
    Ps = charge

    print(f"{Qs=}")

    indices = indexing(year, polarity, mu_eta, mu_phi)
    print(f"{np.unique(indices)=}")
    print(f"{deltas[np.unique(indices)]=}")

    delta_corrections = deltas[indices]

    if scale == "MeV":
        delta_corrections = deltas[indices] * 10**-3 # Changing the scale to be suitable


    # deltas = np.array(deltas)
    # print(f"{deltas[indices]=}")
    return 1. / (1. + Qs * Ps * deltas[indices])
    # return 1. / (1. + Qs * Ps * np.abs(delta_corrections))

                           


    # i_eta, n_eta = axis_index_and_n(eta_edges, eta)
    # i_phi, n_phi = axis_index_and_n(phi_edges, phi)
    # i_polarity = polarities.index(polarity)
    # n_polarity = len(polarities)
    # i_year = years.index(year)
    # return i_phi + (i_eta * n_phi) + (i_polarity * n_phi * n_eta) + (
    #     i_year * n_phi * n_eta * n_polarity)

    # indices = 
    # corrections = []
    # for index, (Q, P, eta, phi) in enumerate(zip(Qs, Ps, mu_eta, mu_phi)):
    #     index = indexing(year, polarity, eta, phi)
    #     correction = correction_factor(Q, P, index, deltas)
    #     corrections.append(corrections)
    # return np.array(corrections)



def axis_index(edges, V, epsilon=1e-5):
    N = len(edges) - 1

    # Clamp values to the closest bounds
    V = np.maximum(edges[0] + epsilon, np.minimum(V, edges[-1] - epsilon))

    # Use numpy's digitize function to find bin indices
    indices = np.digitize(V, edges) - 1

    # Handle the case when V is equal to edges[-1]

    return indices

def indexing(year, polarity, eta, phi):
    # Calculating indices
    # eta_edges = np.array([2.0, 3.0, 4.5])
    eta_edges = np.arange(2, 5, 0.2)

    n_eta = len(eta_edges) - 1
    # phi_edges = np.array([-np.pi, np.pi])
    phi_edges = np.arange(-2.94524336, 2.94524288, 0.393)

    n_phi = len(phi_edges) - 1
    polarities = (-1, 1)
    n_polarity = len(polarities)

    years = (2016, 2017, 2018)
    
        # Getting the indices and applying the indexing algorithm
    i_eta = axis_index(eta_edges, eta)
    i_phi = axis_index(phi_edges, phi)
    i_polarity = polarities.index(polarity)
    i_year = years.index(year)

    return i_phi + (i_eta * n_phi) + (i_polarity * n_phi * n_eta) + (
        i_year * n_phi * n_eta * n_polarity)

# def axis_index(edges, V, epsilon=1e-5):
#     V = max(edges[0] + epsilon, min(V, edges[-1] - epsilon))
#     N = len(edges) - 1
#     for i in range(0, N):
#         if (V >= edges[i] and V < edges[i + 1]):
#             return i
#         if V == edges[-1]:
#             return N - 1


# def indexing(year, polarity, eta, phi):
#     # simple edges examples
#     eta_edges = (2.0, 3.0, 4.5)
#     phi_edges = (-math.pi, math.pi)
#     polarities = (-1, 1)
#     years = (2016, 2017, 2018)

#     i_eta, n_eta = axis_index_and_n(eta_edges, eta)
#     i_phi, n_phi = axis_index_and_n(phi_edges, phi)
#     i_polarity = polarities.index(polarity)
#     n_polarity = len(polarities)
#     i_year = years.index(year)
#     return i_phi + (i_eta * n_phi) + (i_polarity * n_phi * n_eta) + (
#         i_year * n_phi * n_eta * n_polarity)



#Charge curvature bias corrections as given by Mika

# def axis_index(edges, V, epsilon=1e-5):
#     V = max(edges[0] + epsilon, min(V, edges[-1] - epsilon))
#     N = len(edges) - 1
#     for i in range(0, N):
#         if (V >= edges[i] and V < edges[i + 1]):
#             return i
#         if V == edges[-1]:
#             return N - 1


# def axis_index_and_n(edges, V):
#     return axis_index(edges, V), len(edges) - 1


# def indexing(year, polarity, eta, phi):
#     # simple edges examples
#     eta_edges = (2.0, 3.0, 4.5)
#     phi_edges = (-math.pi, math.pi)
#     polarities = (-1, 1)
#     years = (2016, 2017, 2018)

#     i_eta, n_eta = axis_index_and_n(eta_edges, eta)
#     i_phi, n_phi = axis_index_and_n(phi_edges, phi)
#     i_polarity = polarities.index(polarity)
#     n_polarity = len(polarities)
#     i_year = years.index(year)
#     return i_phi + (i_eta * n_phi) + (i_polarity * n_phi * n_eta) + (
#         i_year * n_phi * n_eta * n_polarity)



# 


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

# def correction_factor(Q, P, index,deltas):
#     # q/p -> q/p + delta, i.e. p'/p = (1 + Q*delta*P)**-1
    
#     return 1. / (1. + Q * P * deltas[index])


# def load_pseudomass(year, polarity, charge, mu_eta, mu_phi, mu_pt,deltas):
#     return correction_factor(mu_pt * math.cosh(mu_eta), charge,
#                              indexing(year, polarity, mu_eta, mu_phi),deltas)




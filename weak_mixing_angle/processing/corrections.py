import math
import uproot
import numpy as np


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
    return list(deltas)

#Charge curvature bias corrections as given by Mika

def axis_index(edges, V, epsilon=1e-5):
    V = max(edges[0] + epsilon, min(V, edges[-1] - epsilon))
    N = len(edges) - 1
    for i in range(0, N):
        if (V >= edges[i] and V < edges[i + 1]):
            return i
        if V == edges[-1]:
            return N - 1


def axis_index_and_n(edges, V):
    return axis_index(edges, V), len(edges) - 1


def indexing(year, polarity, eta, phi):
    # simple edges examples
    eta_edges = (2.0, 3.0, 4.5)
    phi_edges = (-math.pi, math.pi)
    polarities = (-1, 1)
    years = (2016, 2017, 2018)

    i_eta, n_eta = axis_index_and_n(eta_edges, eta)
    i_phi, n_phi = axis_index_and_n(phi_edges, phi)
    i_polarity = polarities.index(polarity)
    n_polarity = len(polarities)
    i_year = years.index(year)
    return i_phi + (i_eta * n_phi) + (i_polarity * n_phi * n_eta) + (
        i_year * n_phi * n_eta * n_polarity)



def compute_deltas(pseudomass_corrections_datasets):
    corrections_DATA, corrections_Z,corrections = pseudomass_corrections_datasets
    f_data = ROOT.TFile(corrections_DATA)
    t_data = f_data.Get(corrections)
    f_mc = ROOT.TFile(corrections_Z)
    t_mc = f_mc.Get(corrections)
    t_mc.AddFriend(t_data, "data")
    df_final = ROOT.RDataFrame(t_mc).Define("mc_uncertainty",
                                            "data.delta_uncertainty").Define(
                                                "data_delta", "data.delta")
    df_final_np = df_final.AsNumpy()
    deltas = []
    deltas = [
        df_final_np["data_delta"][i] - df_final_np["delta"][i]
        for i in range(len(df_final_np))
    ]
    return deltas

def correction_factor(Q, P, index,deltas):
    # q/p -> q/p + delta, i.e. p'/p = (1 + Q*delta*P)**-1
    
    return 1. / (1. + Q * P * deltas[index])


def load_pseudomass(year, polarity, charge, mu_eta, mu_phi, mu_pt,deltas):
    return correction_factor(mu_pt * math.cosh(mu_eta), charge,
                             indexing(year, polarity, mu_eta, mu_phi),deltas)




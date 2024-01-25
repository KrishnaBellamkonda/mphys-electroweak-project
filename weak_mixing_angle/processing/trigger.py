import numpy as np
from weak_mixing_angle.utility.utils import map_to_bin

def calc_trigger_eff(eta_data,n_bins,primary_flag,pos_flags,neg_flags, bins=None):
    
    if bins is None:
        counts,bins=np.histogram(eta_data,n_bins)
    efficiency = np.empty(n_bins)
    efficiency_errors = np.empty(n_bins)
    for i in range(len(bins)-1):

        min_bound=bins[i]
        max_bound=bins[i+1]
        mask=(eta_data>=min_bound) & (eta_data<max_bound)

        if primary_flag:
            pos_flags_count = pos_flags[mask].sum()
            both_flags_count = (pos_flags[mask]&neg_flags[mask]).sum()
            efficiency[i]=both_flags_count/pos_flags_count
            N = pos_flags_count
            efficiency_error = np.sqrt((efficiency[i] - efficiency[i]**2)/N)
            efficiency_errors[i] = efficiency_error
        else:
            neg_flags_count = neg_flags[mask].sum()
            both_flags_count = (pos_flags[mask]&neg_flags[mask]).sum()
            efficiency[i]=both_flags_count/neg_flags_count
            N=neg_flags_count
            efficiency_error = np.sqrt((efficiency[i] - efficiency[i]**2)/N)
            efficiency_errors[i] = efficiency_error
            
        



    return efficiency,efficiency_errors, bins


def calc_trigger_eff_with_phi(phi_data,n_bins,primary_flag,pos_flags,neg_flags, bins=None):

    

    # Check if multiple of 4
    if (n_bins % 4) != 0:
        raise ValueError(f"The value of {n_bins=} provided is not a multiple of 4.") 

    # Bins should be linearly spaced between -pi and pi 
    # for the number of bins
    if bins is None:
        bins = np.linspace(-np.pi, np.pi, n_bins+1, endpoint=True)
    #counts,bins=np.histogram(phi_data,n_bins)
    print(f"{bins=}")
    efficiency = np.empty(n_bins)
    efficiency_errors = np.empty(n_bins)
    for i in range(len(bins)-1):
        min_bound=bins[i]
        max_bound=bins[i+1]
        mask=(phi_data>=min_bound) & (phi_data<max_bound)

        if primary_flag:
            pos_flags_count = pos_flags[mask].sum()
            both_flags_count = (pos_flags[mask]&neg_flags[mask]).sum()
            #efficiency[i]=pos_flags_count/both_flags_count
            efficiency[i]=both_flags_count/pos_flags_count
            N = pos_flags_count
            efficiency_error = np.sqrt((efficiency[i] - efficiency[i]**2)/N)
            efficiency_errors[i] = efficiency_error
        else:
            neg_flags_count = neg_flags[mask].sum()
            both_flags_count = (pos_flags[mask]&neg_flags[mask]).sum()
            #efficiency[i]=neg_flags_count/both_flags_count
            efficiency[i]=both_flags_count/neg_flags_count
            N = neg_flags_count
            #print(f"{N=} {neg_flags_count=}")
            efficiency_error = np.sqrt((efficiency[i] - efficiency[i]**2)/N)
            efficiency_errors[i] = efficiency_error
            
        print(f"{min_bound} to {max_bound} with efficiency: {efficiency[i]}")

    return efficiency, efficiency_errors, bins


def calc_trigger_eff_in_phi_bins(eta_data,n_bins,primary_flag,pos_flags,neg_flags, bins=None):

    # Calculates the eta efficiency in bins 

    # Check if multiple of 4
    if (n_bins % 4) != 0:
        raise ValueError(f"The value of {n_bins=} provided is not a multiple of 4.") 

    # Bins should be linearly spaced between -pi and pi 
    # for the number of bins
    if bins is None:
        bins = np.linspace(-np.pi, np.pi, n_bins+1, endpoint=True)
    #counts,bins=np.histogram(phi_data,n_bins)
    print(f"{bins=}")
    efficiency = np.empty(n_bins)
    efficiency_errors = np.empty(n_bins)
    for i in range(len(bins)-1):
        min_bound=bins[i]
        max_bound=bins[i+1]
        mask=(phi_data>=min_bound) & (phi_data<max_bound)

        if primary_flag:
            pos_flags_count = pos_flags[mask].sum()
            both_flags_count = (pos_flags[mask]&neg_flags[mask]).sum()
            #efficiency[i]=pos_flags_count/both_flags_count
            efficiency[i]=both_flags_count/pos_flags_count
            N = pos_flags_count
            efficiency_error = np.sqrt((efficiency[i] - efficiency[i]**2)/N)
            efficiency_errors[i] = efficiency_error
        else:
            neg_flags_count = neg_flags[mask].sum()
            both_flags_count = (pos_flags[mask]&neg_flags[mask]).sum()
            #efficiency[i]=neg_flags_count/both_flags_count
            efficiency[i]=both_flags_count/neg_flags_count
            N = neg_flags_count
            #print(f"{N=} {neg_flags_count=}")
            efficiency_error = np.sqrt((efficiency[i] - efficiency[i]**2)/N)
            efficiency_errors[i] = efficiency_error
            
        print(f"{min_bound} to {max_bound} with efficiency: {efficiency[i]}")


def correct_events_for_trigger_efficiencies(data, var, var_bins, var_bin_eff ):
    # var here could be eta, phi or any other for which 
    # efficiency bins are available

    # Map the events to the right var bin
    new_data = np.empty(len(data))
    for (i, v) in enumerate(var):
        # map this variable to the right bin
        bin_index =  map_to_bin(v, var_bins)
        new_data[i] = data[i] * var_bin_eff[bin_index]
    return new_data
    

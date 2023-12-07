import numpy as np

def calc_trigger_eff(eta_data,n_bins,primary_flag,pos_flags,neg_flags):

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

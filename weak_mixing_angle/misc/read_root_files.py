import uproot
import numpy as np
import matplotlib.pyplot as plt
uproot.default_library = "np"

source = "https://scikit-hep.org/uproot3/examples/hepdata-example.root"
tree_key = "hpx"
event_key = ""

with uproot.open(source) as file:
    # Trees are just table of information
    tree = file[tree_key]

    # Extracting values
    values = tree.values()
    axis_edges = tree.axis().edges()
    errors = file["hprof"].errors()

    # Creating a histogram
    #file["hpxpy"].to_hist()
    n, bins, patches = plt.hist(values, 10, density=1,
                            color="green", alpha=0.7)

    plt.show()

    #event = tree[event_key]
    #print(event.errors())
    #tree_keys = tree.keys()
    #print(event)

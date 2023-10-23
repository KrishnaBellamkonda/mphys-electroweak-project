import uproot
import numpy as np
import matplotlib.pyplot as plt

file = uproot.open("C:/scp/13TeV__2018__magnet_down_data__Z_candidates.root")

print(file.keys())

decayTree = file["DecayTree"]

for i in decayTree.branches:
    print(i)


mupPT= np.array(decayTree["mup_PT"])
mupETA= np.array(decayTree["mup_ETA"])
mupPHI= np.array(decayTree["mup_PHI"])

mumPT= np.array(decayTree["mum_PT"])
mumETA= np.array(decayTree["mum_ETA"])
mumPHI= np.array(decayTree["mum_PHI"])

invMass=(2*mupPT*mumPT*(np.cosh(mupETA-mumETA)-np.cos(mupPHI-mumPHI)))**0.5

counts,bins = np.histogram(invMass)
plt.hist(invMass,bins=60,range = (4e4,1.5e5))
plt.title("Invariant Mass of Muon Decays")
plt.xlabel("Invariant Mass (GeV)")
plt.ylabel("Frequency")
plt.show()

#

from dataclasses import dataclass

@dataclass
class Paths:
    muon_decay_data = "weak_mixing_angle/data/13TeV__2018__magnet_down_data__Z_candidates.root"
    muon_decay_data = "weak_mixing_angle/data/13TeV__2018__magnet_down_data__Z_candidates.root"
    ppdata1 = "weak_mixing_angle/data/pp_collisons/powhegew_s2tw0.228_mz91.1876.root"
    ppdata2 = "weak_mixing_angle/data/pp_collisons/powhegew_s2tw0.235_mz91.1876.root"
    
    # pp_data = "./weak_mixing_angle/data/13TeV_2016_28r2_Down_EW.root"
    # pp_sim_data = "./weak_mixing_angle/data/13TeV_2016_Down_Z_Sim09b_42112001.root"
    plots_path = "weak_mixing_angle/plots"

@dataclass
class StoragePaths:
    muon_decay_data = "/tmp/ProjectData/13TeV__2018__magnet_down_data__Z_candidates.root"
    muon_decay_data = "/tmp/ProjectData/13TeV__2018__magnet_down_data__Z_candidates.root"
    ppdata1 = "/tmp/ProjectData/powhegew_s2tw0.228_mz91.1876.root"
    ppdata2 = "/tmp/ProjectData/powhegew_s2tw0.235_mz91.1876.root"

    simulation_data="/tmp/ProjectData/13TeV_2016_Down_Z_Sim09b_42112001.root"
    real_data = "/tmp/ProjectData/13TeV_2016_28r2_Down_EW.root"

    # pp_data = "/tmp/ProjectData/13TeV_2016_28r2_Down_EW.root"
    # pp_sim_data = "/tmp/ProjectData/13TeV_2016_Down_Z_Sim09b_42112001.root"
    plots_path = "/home/physics/phuhko/plots"

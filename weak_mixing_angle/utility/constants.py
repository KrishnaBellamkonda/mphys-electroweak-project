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
#    ppdata1 = "/tmp/ProjectData/powhegew_s2tw0.228_mz91.1876.root"
#    ppdata2 = "/tmp/ProjectData/powhegew_s2tw0.235_mz91.1876.root"

    ppdata1 =  '/storage/epp2/phshgg/Public/ew_analyses/weak_mixing_template_events_00/powhegew/00/powhegew_s2tw0.228_mz91.1876.root'
    ppdata2 =  '/storage/epp2/phshgg/Public/ew_analyses/weak_mixing_template_events_00/powhegew/00/powhegew_s2tw0.235_mz91.1876.root'

    simulation_data = '/storage/epp2/phshgg/Public/ew_analyses/tuples/v25/02/13TeV_2016_Down_Z_Sim09b_42112001.root'
    real_data  = '/storage/epp2/phshgg/Public/ew_analyses/tuples/v25/02/13TeV_2016_28r2_Down_EW.root'

    pseudomass_corrections_DATA = "/storage/epp2/phshgg/Public/MPhysProject_2023_2024/Pseudomass/pseudomass_corrections__13TeV__DATA__default.root"
    pseudomass_corrections_Z = "/storage/epp2/phshgg/Public/MPhysProject_2023_2024/Pseudomass/pseudomass_corrections__13TeV__Z__default.root"
    pseudomass_corrections = "pseudomass_corrections"

    pseudomass_corrections_combined = (pseudomass_corrections_DATA,pseudomass_corrections_Z,pseudomass_corrections)

    # pp_data = "/tmp/ProjectData/13TeV_2016_28r2_Down_EW.root"
    # pp_sim_data = "/tmp/ProjectData/13TeV_2016_Down_Z_Sim09b_42112001.root"
    plots_path = "/home/physics/phuvmc/mphys-electroweak-project/weak_mixing_angle/plots/"

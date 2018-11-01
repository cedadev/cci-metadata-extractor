

DEFAULT_VARIABLES = [
    'AAOD550_mean',                     # esacci.AEROSOL.*.L3C.AER_PRODUCTS.*
    'absorbing_aerosol_index',          # esacci.AEROSOL.*.L3.AAI.*
    'AOD550',                           # esacci.AEROSOL.*.L3C.AOD.*
    'cfc',                              # esacci.CLOUD.*.L3C.CLD_PRODUCTS.*
    'burned_area',                      # esacci.FIRE.*.L4.BA.*
    'lccs_class',                       # esacci.LC.L4.LCCS.*
    'atot_490',                         # esacci.OC.*.L3S.IOP.*, esacci.OC.*.L3S.OC_PRODUCTS.*
    'chlor_a',                          # esacci.OC.*.L3S.CHLOR_A.*, esacci.OC.*.L3S.OC_PRODUCTS.*
    'kd_490',                           # esacci.OC.*.L3S.K_490.*
    'O3_du_tot',                        # esacci.OZONE.*.L3.NP.*
    'atmosphere_mole_content_of_ozone', # esacci.OZONE.*.L3S.TC.*
    'Rrs_490',                          # esacci.OC.*.L3S.RRS.*
    'ampl',                             # esacci.SEALEVEL.*.IND.MSLAMPH.*
    'sla',                              # esacci.SEALEVEL.*.IND.MSLA.*
    'local_msl_trend',                  # esacci.SEALEVEL.*.IND.MSL.*
    'sm',                               # esacci.SOILMOISTURE.*.L3S.SSMS.*
    'sea_surface_temperature',          # esacci.SST.*.L3U.SSTskin.*
    'analysed_sst',                     # esacci.SST.*.L4.SSTdepth.*
]

VARIABLE_DISPLAY_SETTINGS = {
    # LC CCI
    'lccs_class': dict(color_map='land_cover_cci'),

    # OC CCI
    'kd_490': dict(color_map="bwr", display_min=0.0, display_max=0.5),
    'kd_490_bias': dict(display_min=-0.02, display_max=0.07),
    'kd_490_rmsd': dict(display_min=0.0, display_max=0.25),
    'total_nobs_sum': dict(display_min=1, display_max=500),
    'MERIS_nobs_sum': dict(display_min=1, display_max=500),
    'MODISA_nobs_sum': dict(display_min=1, display_max=500),
    'SeaWiFS_nobs_sum': dict(display_min=1, display_max=500),

    # Cloud CCI
    'cfc': dict(color_map="bone", display_min=0, display_max=1),

    # SST CCI
    'analysed_sst': dict(color_map="jet", display_min=270., display_max=310.),
    'analysis_error': dict(display_min=0., display_max=3.),
    'mask': dict(display_min=0, display_max=9),
    'sea_ice_fraction': dict(display_min=0., display_max=1.),
    'sea_ice_fraction_error': dict(display_min=0., display_max=0.2),

    # Aerosol CCI
    'absorbing_aerosol_index': dict(color_map="bwr", display_min=-2, display_max=2),
    'solar_zenith_angle': dict(color_map="bwr", display_min=35, display_max=80),
    'number_of_observations': dict(color_map="gray", display_min=0, display_max=150),

    # OZONE CCI
    'O3_du': dict(display_min=3, display_max=20),
    'O3_du_tot': dict(display_min=220, display_max=480),
    'O3_ndens': dict(display_min=1.5e11, display_max=1e12),
    'O3_vmr': dict(display_min=0.006, display_max=0.045),
    'O3e_du': dict(display_min=0, display_max=2),
    'O3e_du_tot': dict(display_min=0, display_max=2),
    'O3e_ndens': dict(display_min=9e9, display_max=1e11),
    'O3e_vmr': dict(display_min=0, display_max=0.005),
    'surface_pressure': dict(display_min=700, display_max=1010),

    # Fire CCI
    'burned_area': dict(color_map="hot", display_min=0, display_max=300000000),

    # Sea Level CCI
    'ampl': dict(color_map="YlOrRd", display_min=0., display_max=0.12),
    'phase': dict(color_map="hsv", display_min=0., display_max=360.),
    'sla': dict(color_map="bwr", display_min=-0.2, display_max=0.2),
    'local_msl_trend': dict(color_map="coolwarm", display_min=-12., display_max=12.),
    'local_msl_trend_error': dict(color_map="afmhot", display_min=0., display_max=5.),
}

DEFAULT_COLOR_MAP = "inferno"
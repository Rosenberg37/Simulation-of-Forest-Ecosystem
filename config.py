from modules.biomass import Cohort

BIOMASS_OPTIONS = [
    {
        'cohort_type': Cohort.CohortType.coniferous,
        'management_mortality_dict': {
            'volume': [50],
            'start_mort': [.04],
            'impact_time': [10]
        },
        'stem_kargs': {
            'carbon_content': 0.5,
            'wood_density': 0.3,
            'CAI_dict': {
                'age': [0, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 140],
                'CAI': [0.2, 6, 17.2, 19.2, 19.4, 19.4, 19.1, 18.6, 18.1, 17.4, 17, 16.4, 15.8, 15.2, 14.6, 4.4, 13.8, 13.2, 12.6,
                        12.1, 1.6, 11, 10.6, 8],
            },
            'mortality_dict': {
                'age': [0, 10, 20, 70, 120],
                'mortality': [.01, .04, .04, .015, .02],
            },
        },
        'compartments_kargs': {
            'foliage': {
                'carbon_content': 0.5,
                'turnover_rate': .3,
                'initial_carbon': .1,
                'relative_growth_dict': {
                    'age': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                    'relative_growth': [1, .9, .7, .5, .5, .55, .55, .55, .6, .65, .7]
                }
            },
            'branches': {
                'carbon_content': 0.5,
                'initial_carbon': 0.02,
                'turnover_rate': 0.04,
                'relative_growth_dict': {
                    'age': [0, 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                    'relative_growth': [0, 1, .8, .7, .5, .45, .4, .4, .45, .5, .55, .55]
                }
            },
            'roots': {
                'carbon_content': 0.5,
                'turnover_rate': 0.08,
                'initial_carbon': .1,
                'relative_growth_dict': {
                    'age': [0, 10, 20, 30, 40, 50, 60, 70, 80, 0, 100],
                    'relative_growth': [1, .9, .7, .5, .5, .55, .55, .55, .6, .65, .7]
                }
            },
        },
        'thinning_harvest_dict': {
            'age': [25, 45, 55, 70, 95],
            'fraction': [.2, .2, .2, .2, 1.],
            'stem': {
                'LogWood': [0, .3, .35, .55, .7],
                'PulpPap': [.7, .6, .55, .4, .25],
                'Slash': [0.30, 0.10, 0.10, 0.05, 0.05],
            },
            'branches': {
                'LogWood': [0, 0, 0, .05, .1],
                'PulpPap': [.1, .1, .15, .15, .15],
                'Slash': [0.90, 0.90, 0.85, 0.80, 0.75],
            },
        }
    }
]

SOIL_OPTIONS = {
    'initial_carbons': {
        "x_nwl": 100,  # weight of organic carbon in non-woody litter compartment
        "x_fwl": 100,  # weight of organic carbon in fine-woody litter compartment
        "x_cwl": 100,  # weight of organic carbon in coarse-woody litter compartment
        "x_ext": 100,  # weight of organic carbon in each decomposition compartment extractives
        "x_cel": 100,  # weight of organic carbon in each decomposition compartment celluloses
        "x_lig": 100,  # weight of organic carbon in each decomposition compartment lignin-like compounds
        "x_hum1": 100,  # weight of organic carbon in each decomposition compartment simple humus
        "x_hum2": 100,  # weight of organic carbon in each decomposition compartment complicated humus
    },
    'invasion_rates': {
        "a_nwl": 1,  # invasion rates of litter by microbes of non-woody litter
        "a_fwl": 0.54,  # invasion rates of litter by microbes of fine-woody litter
        "a_cwl": 0.03,  # invasion rates of litter by microbes of coarse-woody litter
    },
    'decomposition_rates': {
        "k_ext": 0.48,  # decomposition rate of compartment extractives
        "k_cel": 0.3,  # decomposition rate of compartment celluloses
        "k_lig": 0.22,  # decomposition rate of compartment lignin-like compounds
        "k_hum1": 0.012,  # decomposition rate of compartment simple humus
        "k_hum2": 0.0012,  # decomposition rate of compartment complicated humus
    },
    'subsequent_rates': {
        "p_ext": 0.2,  # proportion of mass decomposed in compartment extractives transferred to a subsequent compartment.
        "p_cel": 0.2,  # proportion of mass decomposed in compartment celluloses transferred to a subsequent compartment.
        "p_lig": 0.2,  # proportion of mass decomposed in compartment lignin-like compounds transferred to a subsequent compartment.
        "p_hum1": 0.2,  # proportion of mass decomposed in compartment simple humus  transferred to a subsequent compartment.
    },
    'concentration_rates': {
        "c_nwl_ext": 0.3,  # concentration of compound group extractives in litter type non-woody litter
        "c_fwl_ext": 0.3,  # concentration of compound group extractives in litter type fine-woody
        "c_cwl_ext": 0.4,  # concentration of compound group extractives in litter type coarse-woody
        "c_nwl_cel": 0.2,  # concentration of compound group celluloses in litter type non-woody litter
        "c_fwl_cel": 0.5,  # concentration of compound group celluloses in litter type fine-woody
        "c_cwl_cel": 0.3,  # concentration of compound group celluloses in litter type coarse-woody
        "c_nwl_lig": 0.1,  # concentration of compound group lignin-like compounds in litter type non-woody litter
        "c_fwl_lig": 0.3,  # concentration of compound group lignin-like compounds in litter type fine-woody
        "c_cwl_lig": 0.6,  # concentration of compound group lignin-like compounds in litter type coarse-woody
    }
}

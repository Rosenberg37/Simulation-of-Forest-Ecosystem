OPTIM_OPTIONS = {
    'years': 5,
    'max_iter': 100,
}

BIOMASS_CONFIG = [
    {
        'initial_age': 0,
        'maximum_biomass': 100,
        'management_mortality_dict': {
            'volume': [2, 5, 10, 20, 30],
            'start_mort': [0.03, 0.03, 0.04, 0.06, 0.10],
            'impact_time': [2, 3, 5, 7, 8]
        },
        'stem_kargs': {
            'carbon_content': 0.5,
            'wood_density': 0.3,
            'CAI_dict': {
                'bio_rates': [0.00, .05, 0.40, 0.60, 1.00],
                'CAI': [0.1, 4.0, 3.5, 2.0, 0.01],
            },
            'mortality_dict': {
                'bio_rates': [0, 0.10, 0.25, 0.40, 0.60, 0.80, 1.0],
                'mortality': [0.1, 0.015, 0.01, 0.3, 0.7, .99, 1.0],
            },
        },
        'compartments_kargs': {
            'foliage': {
                'carbon_content': 0.5,
                'turnover_rate': .3,
                'initial_carbon': .1,
                'relative_growth_dict': {
                    'bio_rates': [0.0, 0.25, 0.5, 0.75, 1.0],
                    'relative_growth': [1.0, 0.5, 0.25, 0.1, .15]
                }
            },
            'branches': {
                'carbon_content': 0.5,
                'initial_carbon': 0.02,
                'turnover_rate': 0.04,
                'relative_growth_dict': {
                    'bio_rates': [0.0, 0.25, 0.5, 0.75, 1.0],
                    'relative_growth': [1.0, 0.75, 0.25, 0.1, .2]
                }
            },
            'roots': {
                'carbon_content': 0.5,
                'turnover_rate': 0.08,
                'initial_carbon': .1,
                'relative_growth_dict': {
                    'bio_rates': [0.0, 0.25, 0.5, 0.75, 1.0],
                    'relative_growth': [0.5, 0.2, 0.15, .2, .25]
                }
            },
        },
        'thinning_harvest_dict': {
            'age': [25, 45, 55, 70, 95],
            'fraction': [.2, .2, .2, .2, 1.],
            'stems': {
                'logwood': [0, .3, .35, .55, .7],
                'pulpwood': [.7, .6, .55, .4, .25],
                'slash': [0.30, 0.10, 0.10, 0.05, 0.05],
            },
            'branches': {
                'logwood': [0, 0, 0, .05, .1],
                'pulpwood': [.1, .1, .15, .15, .15],
                'slash': [0.90, 0.90, 0.85, 0.80, 0.75],
            },
        }
    }
]

SOIL_CONFIG = {
    'initial_carbons': {
        "x_nwl": 0,  # weight of organic carbon in non-woody litter compartment
        "x_fwl": 0,  # weight of organic carbon in fine-woody litter compartment
        "x_cwl": 0,  # weight of organic carbon in coarse-woody litter compartment
        "x_ext": 0,  # weight of organic carbon in each decomposition compartment extractives
        "x_cel": 0,  # weight of organic carbon in each decomposition compartment celluloses
        "x_lig": 0,  # weight of organic carbon in each decomposition compartment lignin-like compounds
        "x_hum1": 0,  # weight of organic carbon in each decomposition compartment simple humus
        "x_hum2": 0,  # weight of organic carbon in each decomposition compartment complicated humus
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

PRODUCTS_CONFIG = {
    'allocation': {
        'logwood': {
            'sawnwood': 0.4,
            'boards': 0,
            'paper': 0,
            'firewood': 0.6
        },
        'pulpwood': {
            'boards': 0,
            'paper': 0,
            'firewood': 1
        },
    },
    'losses': {
        'sawnwood': {
            'boards': 0.10,
            'paper': 0.12,
            'firewood': 0.35,
            'mile_site_dump': 0.2
        },
        'boards': {
            'paper': 0.05,
            'firewood': 0.2,
            'mile_site_dump': 0.2
        },
        'paper': {
            'firewood': 0.2,
            'mile_site_dump': 0.2
        },
        'firewood': {
            'mile_site_dump': 0.05
        }
    },
    'end_products_kargs': {
        'products': {
            'long': 0,
            'medium': 0,
            'short': 0,
            'land_fill': 0,
            'mile_site_dump': 0
        },
        'allocation': {
            'sawnwood': {
                'long': 0.8,
                'medium': 0.19,
                'short': 0.01
            },
            'boards': {
                'long': 0.10,
                'medium': 0.30,
                'short': 0.600000
            },
            'paper': {
                'long': 0,
                'medium': 0.04,
                'short': 0.960000
            },
        },
        'end_of_life': {
            'long': {
                'recycling': 0.02,
                'land_fill': 0.680000,
            },
            'medium': {
                'recycling': 0.04,
                'land_fill': 0.660000,
            },
            'short': {
                'recycling': 0.15,
                'land_fill': 0.450000,
            }
        },
        'recycle': {
            'long': {
                'long': 0,
                'medium': 0.2,
                'short': 0.8
            },
            'medium': {
                'medium': 0.1,
                'short': 0.9
            },
            'short': {
                'short': 0
            },
        },
        'life_span': {
            'long': 14,
            'medium': 7,
            'short': 1,
            'mile_site_dump': 7,
            'land_fill': 35,
        }
    }
}

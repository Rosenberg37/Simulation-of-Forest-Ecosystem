OPTIM_OPTIONS = {
    'years': 5,
    'max_iter': 100,
}

BIOMASS_CONFIG = {
    'pine': {
        'initial_age': 0,
        'maximum_biomass': 100,
        'management_mortality_dict': {
            'volume': [50],
            'start_mort': [.04],
            'impact_time': [10]
        },
        'stem_kargs': {
            'carbon_content': 0.5,
            'wood_density': 0.5,
            'initial_carbon': 9.67,
            'CAI_dict': {
                'age': [0, 15, 20, 25, 30, 35, 40, 45, 50, 200],
                'CAI': [0, 8.9, 20.4, 18.5, 1.8, 15.4, 16.1, 10.8, 10.9, 3.6],
            },
            'mortality_dict': {
                'age': [0],
                'mortality': [0.01],
            },
        },
        'compartments_kargs': {
            'foliage': {
                'carbon_content': 0.5,
                'initial_carbon': 1.41,
                'turnover_rate': 0.33,
                'relative_growth_dict': {
                    'age': [0, 6, 10, 14, 18, 22, 25, 30, 40, 50, 100, 200],
                    'relative_growth': [1.2, 1.4, 0.6, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 1, 1.6, 1.6]
                }
            },
            'branches': {
                'carbon_content': 0.5,
                'initial_carbon': 2.47,
                'turnover_rate': 0.02,
                'relative_growth_dict': {
                    'age': [0, 6, 10, 14, 18, 22, 25, 30, 40, 50, 100, 200],
                    'relative_growth': [0.8, 0.5, 0.2, 0.15, 0.15, 0.2, 0.2, 0.2, 0.2, 0.4, 0.6, 0.6]
                }
            },
            'roots': {
                'carbon_content': 0.5,
                'initial_carbon': 1.69,
                'turnover_rate': 0.02,
                'relative_growth_dict': {
                    'age': [0, 6, 10, 14, 18, 22, 25, 30, 40, 50, 100, 200],
                    'relative_growth': [0.9, 0.6, 0.3, 0.25, 0.25, 0.3, 0.3, 0.25, 0.18, 0.2, 0.6, 0.7]
                }
            },
        },
        'competition': {
            'bio_rates': [0, 0.2, 0.6, 0.8, 1.0],
            'pine': [1, .9, .7, .4, 0],
        },
        'thinning_harvest_dict': {
            'age': [10, 20, 30, 40, 50],
            'fraction': [0.80, 0.350, 0.350, 0.350, 0.8],
            'stems': {
                'logwood': [0.7, 0.42, 0.42, 0.7, 0.7],
                'pulpwood': [0.2, 0.58, 0.58, 0.2, 0.2],
                'slash': [0.10, 0.00, 0.00, 0.10, 0.10],
            },
            'branches': {
                'logwood': [0.1, 0, 0, 0.1, 0.1],
                'pulpwood': [0, 0, 0, 0, 0],
                'slash': [0.90, 1.00, 1.00, 0.90, 0.90],
            },
            'slash_firewood': [0.95, .9, .9, .95, .95],
            'slash_soil': [0.05, 0.10, 0.10, 0.05, 0.05]
        }
    },
    'oak': {
        'initial_age': 0,
        'maximum_biomass': 400,
        'management_mortality_dict': {
            'volume': [50],
            'start_mort': [.04],
            'impact_time': [10]
        },
        'stem_kargs': {
            'carbon_content': 0.5,
            'wood_density': 0.63,
            'initial_carbon': 1.75,
            'CAI_dict': {
                'age': [1, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 200],
                'CAI': [0.0, 3.4, 4.6, 6.9, 6.5, 8.0, 6.6, 7.6, 5, 3.5, 3, 2.5, 2.5],
            },
            'mortality_dict': {
                'age': [0],
                'mortality': [0.005],
            },
        },
        'compartments_kargs': {
            'foliage': {
                'carbon_content': 0.5,
                'initial_carbon': 0.28,
                'turnover_rate': 1.00,
                'relative_growth_dict': {
                    'age': [0, 6, 10, 14, 18, 22, 25, 30, 40, 50, 100, 200],
                    'relative_growth': [1, 0.8, 0.8, .8, .8, .8, .8, .8, .8, 1, 1.5, 1.5]
                }
            },
            'branches': {
                'carbon_content': 0.50,
                'initial_carbon': 1.63,
                'turnover_rate': 0.02,
                'relative_growth_dict': {
                    'age': [0, 6, 10, 14, 18, 22, 25, 30, 40, 50, 100, 200],
                    'relative_growth': [0.7, 1.2, 0.8, 0.8, 0.3, 0.3, 0.3, 0.3, 0.35, 0.6, 0.9, 1]
                }
            },
            'roots': {
                'carbon_content': 0.5,
                'initial_carbon': .72,
                'turnover_rate': 0.03,
                'relative_growth_dict': {
                    'age': [0, 6, 10, 14, 18, 22, 25, 30, 40, 50, 100, 200],
                    'relative_growth': [2, 1, 1, 0.5, 0.5, 0.4, 0.3, 0.3, 0.5, 0.9, 1.1, 1.4]
                }
            },
        },
        'competition': {
            'bio_rates': [0, 0.7, 0.8, 1.0],
            'pine': [1, 1, .8, 0],
        },
        'thinning_harvest_dict': {
            'age': [10, 20, 30, 40, 50],
            'fraction': [0.2, 0.2, 0.2, 0.2, 0.2],
            'stems': {
                'logwood': [0, 0, 0, 0, 0],
                'pulpwood': [0, 0, 0, 0, 0],
                'slash': [1.00, 1.00, 1.00, 1.00, 1.00],
            },
            'branches': {
                'logwood': [0, 0, 0, 0, 0],
                'pulpwood': [0, 0, 0, 0, 0],
                'slash': [1.00, 1.00, 1.00, 1.00, 1.00],
            },
            'slash_firewood': [.9, .9, .9, .95, .95],
            'slash_soil': [0.10, 0.10, 0.10, 0.05, 0.05]
        }
    }
}

SOIL_CONFIG = {
    'cohorts_kargs': {
        'pine': {
            'initial_carbons': {
                "x_nwl": 0.750000,  # weight of organic carbon in non-woody litter compartment
                "x_fwl": 1.603523,  # weight of organic carbon in fine-woody litter compartment
                "x_cwl": 6.414094,  # weight of organic carbon in coarse-woody litter compartment
                "x_ext": 0.500299,  # weight of organic carbon in each decomposition compartment extractives
                "x_cel": 3.837766,  # weight of organic carbon in each decomposition compartment celluloses
                "x_lig": 4.886471,  # weight of organic carbon in each decomposition compartment lignin-like compounds
                "x_hum1": 12.482393,  # weight of organic carbon in each decomposition compartment simple humus
                "x_hum2": 25.797206,  # weight of organic carbon in each decomposition compartment complicated humus
            },
            'concentration_rates': {
                "c_nwl_ext": 0.27,  # concentration of compound group extractives in litter type non-woody litter
                "c_fwl_ext": 0.03,  # concentration of compound group extractives in litter type fine-woody
                "c_cwl_ext": 0.03,  # concentration of compound group extractives in litter type coarse-woody
                "c_nwl_cel": 0.51,  # concentration of compound group celluloses in litter type non-woody litter
                "c_fwl_cel": 0.65,  # concentration of compound group celluloses in litter type fine-woody
                "c_cwl_cel": 0.69,  # concentration of compound group celluloses in litter type coarse-woody
                "c_nwl_lig": 0.220000,  # concentration of compound group lignin-like compounds in litter type non-woody litter
                "c_fwl_lig": 0.320000,  # concentration of compound group lignin-like compounds in litter type fine-woody
                "c_cwl_lig": 0.280000,  # concentration of compound group lignin-like compounds in litter type coarse-woody
            }
        },
        'oak': {
            'initial_carbons': {
                "x_nwl": 0.450000,  # weight of organic carbon in non-woody litter compartment
                "x_fwl": 0.962114,  # weight of organic carbon in fine-woody litter compartment
                "x_cwl": 4.276063,  # weight of organic carbon in coarse-woody litter compartment
                "x_ext": 0.254559,  # weight of organic carbon in each decomposition compartment extractives
                "x_cel": 2.154067,  # weight of organic carbon in each decomposition compartment celluloses
                "x_lig": 3.023533,  # weight of organic carbon in each decomposition compartment lignin-like compounds
                "x_hum1": 7.723555,  # weight of organic carbon in each decomposition compartment simple humus
                "x_hum2": 15.962174,  # weight of organic carbon in each decomposition compartment complicated humus
            },
            'concentration_rates': {
                "c_nwl_ext": 0.38,  # concentration of compound group extractives in litter type non-woody litter
                "c_fwl_ext": 0.03,  # concentration of compound group extractives in litter type fine-woody
                "c_cwl_ext": 0.03,  # concentration of compound group extractives in litter type coarse-woody
                "c_nwl_cel": 0.36,  # concentration of compound group celluloses in litter type non-woody litter
                "c_fwl_cel": 0.65,  # concentration of compound group celluloses in litter type fine-woody
                "c_cwl_cel": 0.75,  # concentration of compound group celluloses in litter type coarse-woody
                "c_nwl_lig": 0.260000,  # concentration of compound group lignin-like compounds in litter type non-woody litter
                "c_fwl_lig": 0.320000,  # concentration of compound group lignin-like compounds in litter type fine-woody
                "c_cwl_lig": 0.220000,  # concentration of compound group lignin-like compounds in litter type coarse-woody
            }
        },
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
}

PRODUCTS_CONFIG = {
    'allocation': {
        'logwood': {
            'sawnwood': 0.8,
            'boards': 0.1,
            'paper': 0,
            'firewood': 0.1
        },
        'pulpwood': {
            'boards': 0,
            'paper': 0,
            'firewood': 1
        },
    },
    'losses': {
        'sawnwood': {
            'boards': 0,
            'paper': 0.1,
            'firewood': 0.4,
            'mile_site_dump': 0.0
        },
        'boards': {
            'paper': 0.05,
            'firewood': 0.3,
            'mile_site_dump': 0.0
        },
        'paper': {
            'firewood': 0.1,
            'mile_site_dump': 0.05
        },
        'firewood': {
            'mile_site_dump': 0
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
                'long': 0.5,
                'medium': 0.25,
                'short': 0.250000
            },
            'boards': {
                'long': 0.3,
                'medium': .5,
                'short': .5
            },
            'paper': {
                'long': 0.01,
                'medium': 0.1,
                'short': 0.890000
            },
        },
        'end_of_life': {
            'long': {
                'recycling': 0.1,
                'land_fill': 0.100000,
            },
            'medium': {
                'recycling': 0.1,
                'land_fill': 0.100000,
            },
            'short': {
                'recycling': 0.2,
                'land_fill': 0.050000,
            }
        },
        'recycle': {
            'long': {
                'long': 0,
                'medium': 0.2,
                'short': 0.8
            },
            'medium': {
                'medium': 0.2,
                'short': 0.8
            },
            'short': {
                'short': 0
            },
        },
        'life_span': {
            'long': 40,
            'medium': 15,
            'short': 1,
            'mile_site_dump': 25,
            'land_fill': 50,
        }
    }
}

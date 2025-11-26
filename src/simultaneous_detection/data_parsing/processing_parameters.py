PROCESSING_PARAMETERS = {
    'H2_processing_parameters': {
                        'offset': 60,
                        'savgol_window': 30,
                        'savgol_polyorder': 1,
                        'savgol_window_diff': 50,
                        'savgol_polyorder_diff': 1,
                        'interval_resampling': 10,
                        'poly_order': 4,
                    },
    'O2_processing_parameters': { 
                        'offset': 60,
                        'savgol_window': 10,
                        'savgol_polyorder': 3,
                        'savgol_window_diff': 50,
                        'savgol_polyorder_diff': 1,
                        'interval_resampling': 10,
                        'poly_order': 4,
                    },
    'fitting_parameters': {
                    'reaction_network': [
                            '[H2O] > [O2-aq], k1',
                            '[O2-aq] > [O2-g], k2',
                            '[H2O] > [H2-aq], k3 ; factor1',
                            '[H2-aq] > [H2-g], k2 ; factor2',
                            ],   
                    'rate_constants_to_optimize': {
                            'k1': (1e-10, 1e-8),
                            'k3': (2e-10, 2e-8)
                            },
                    'fixed_rate_constants': {
                            'k2': 0.0004 # fixed empircally 
                            },
                    'data_to_be_fitted': {
                            '[O2-aq]': {'x': 'processed_data/common_time_reaction',
                                        'y': 'processed_data/O2_data_aligned'},
                            '[H2-aq]': {'x': 'processed_data/common_time_reaction',
                                        'y': 'processed_data/H2_data_aligned'},
                            },   
                    'initial_conditions': {
                            '[H2O]': 55.5 * 1e6,  # Convert from mol/L to μmol/L
                            },
                    'other_multipliers': {
                            'factor1': 1.0,  # Inactive multiplier for H2 production rate
                            'factor2': 1.68, # solubility ratio of O2/H2
                            },
                    'times': {
                        'times': 'processed_data/common_time_reaction'
                        },
            },
    'fitting_parameters_mapping': {
                    'species_mapping': {
                            '[O2-aq]': 'O2',
                            '[H2-aq]': 'H2',
                            },
                    'rate_constant_mapping': {
                            'O2': 0,
                            'H2': 1,
                            },
            },
    'fitting_parameters_flexible_H2': {
                    'reaction_network': [
                            '[H2O] > [Gas-int], k1',
                            '[Gas-int] > [Gas-aq], k2',
                            '[Gas-aq] > [Gas-g], k3',
                            ],   
                    'rate_constants_to_optimize': {
                            'k1': (1e-8, 1e-6),
                            'k2': (1e-4, 1e-2),
                            'k3': (1e-2, 1e-0),
                            },  
                    'data_to_be_fitted': {
                            '[Gas-aq]': {'x': 'processed_data/common_time_reaction',
                                         'y': 'processed_data/H2_data_aligned'},
                            },
                    'initial_conditions': {
                            '[H2O]': 55.5 * 1e6,  # Convert from mol/L to μmol/L
                            },
                    'times': {
                        'times': 'processed_data/common_time_reaction'
                        },
                }, 
    'fitting_parameters_flexible_H2_mapping': {   
                    'species_mapping': {
                            '[Gas-aq]': 'H2_flexible',
                            },
                    'rate_constant_mapping': {
                            'H2_flexible': 0,
                            },
                },        
    'fitting_parameters_flexible_O2': {
                    'reaction_network': [
                            '[H2O] > [Gas-int], k1',
                            '[Gas-int] > [Gas-aq], k2',
                            '[Gas-aq] > [Gas-g], k3',
                            ],   
                    'rate_constants_to_optimize': {
                            'k1': (1e-8, 1e-6),
                            'k2': (1e-4, 1e-2),
                            'k3': (1e-2, 1e-0),
                            },  
                    'data_to_be_fitted': {
                            '[Gas-aq]': {'x': 'processed_data/common_time_reaction',
                                         'y': 'processed_data/O2_data_aligned'},
                            },
                    'initial_conditions': {
                            '[H2O]': 55.5 * 1e6,  # Convert from mol/L to μmol/L
                            },
                    'times': {
                        'times': 'processed_data/common_time_reaction'
                        },
            }, 
    'fitting_parameters_flexible_O2_mapping': {   
                    'species_mapping': {
                            '[Gas-aq]': 'O2_flexible',
                            },
                    'rate_constant_mapping': {
                            'O2_flexible': 0,
                            },
            },
}

GROUP_MAPPING = {
        'Reference': None,
        'Intensity': 'metadata/Irradiance [mW/cm2]',
        'Loading': 'metadata/Catalyst loading [wt% Rh/Cr]',
        'D2O': 'metadata/D2O',
        'Temperature': 'metadata/Temperature [°C]'
        }

PLOTTING_INSTRUCTIONS = {
    'time_series_instructions': {
                    'Raw (H2)': {
                        'x': 'raw_data/H2_time_s',
                        'y': 'raw_data/H2_umol_L'
                        },
                    'Raw (O2)': {
                        'x': 'raw_data/O2_time_s',
                        'y': 'raw_data/O2_data'
                        },
                    'Reaction (H2)': {
                        'x': 'processed_data/H2_time_reaction',
                        'y': 'processed_data/H2_data_reaction'
                        },
                    'Reaction (O2)': {
                        'x': 'processed_data/O2_time_reaction',
                        'y': 'processed_data/O2_data_reaction'
                        },
                    'Fit (H2)': {
                        'x': 'processed_data/common_time_reaction',
                        'y': 'processed_data/H2_fit'
                        },
                    'Fit (O2)': {
                        'x': 'processed_data/common_time_reaction',
                        'y': 'processed_data/O2_fit'
                        },
                    'Poly fit (H2)': {
                        'x': 'processed_data/H2_time_reaction',
                        'y': 'processed_data/H2_poly_fit'
                        },
                    'Poly fit (O2)': {
                        'x': 'processed_data/O2_time_reaction',
                        'y': 'processed_data/O2_poly_fit'
                        },
                    'Flexible fit (H2)': {
                        'x': 'processed_data/common_time_reaction',
                        'y': 'processed_data/H2_flexible_fit'
                        },
                    'Flexible fit (O2)': {
                        'x': 'processed_data/common_time_reaction',
                        'y': 'processed_data/O2_flexible_fit'
                        },
                    'Smoothed (H2)': {
                        'x': 'processed_data/H2_time_reaction',
                        'y': 'processed_data/H2_data_smoothed'
                        },
                    'Smoothed (O2)': {
                        'x': 'processed_data/O2_time_reaction',
                        'y': 'processed_data/O2_data_smoothed'
                        },
                    'Rate (H2)': {
                        'x': 'processed_data/H2_time_diff',
                        'y': 'processed_data/H2_data_diff'
                        },
                    'Rate (O2)': {
                        'x': 'processed_data/O2_time_diff',
                        'y': 'processed_data/O2_data_diff'
                        },
                    'Rate (H2) - Smoothed': {
                        'x': 'processed_data/H2_time_diff',
                        'y': 'processed_data/H2_data_diff_smoothed'
                        },
                    'Rate (O2) - Smoothed': {
                        'x': 'processed_data/O2_time_diff',
                        'y': 'processed_data/O2_data_diff_smoothed'
                        },
                    'Rate poly fit (H2)': {
                        'x': 'processed_data/H2_time_diff',
                        'y': 'processed_data/H2_poly_fit_diff'
                        },
                    'Rate poly fit (O2)': {
                        'x': 'processed_data/O2_time_diff',
                        'y': 'processed_data/O2_poly_fit_diff'
                        },
                    'Rate flexible fit (H2)': {
                        'x': 'processed_data/flexible_diff_time',
                        'y': 'processed_data/H2_flexible_fit_rate'
                        },
                    'Rate flexible fit (O2)': {
                        'x': 'processed_data/flexible_diff_time',
                        'y': 'processed_data/O2_flexible_fit_rate'
                    },
                },
    'kinetic_results_instructions': {
        'O2 rate constant': {'Value': 'processed_data/O2_rate_constant',
                             'Unit': 'Rate constant / 1/s'},   
        'H2 rate constant': {'Value': 'processed_data/H2_rate_constant',
                             'Unit': 'Rate constant / 1/s'},
        'H2 max rate': {'Value': 'processed_data/H2_max_rate',
                        'Unit': 'Rate / umol L^-1 s^-1'},
        'O2 max rate': {'Value': 'processed_data/O2_max_rate',
                        'Unit': 'Rate / umol L^-1 s^-1'},
        'H2 max rate (flexible)': {'Value': 'processed_data/H2_flexible_fit_max_rate',
                        'Unit': 'Rate / umol L^-1 s^-1'},
        'O2 max rate (flexible)': {'Value': 'processed_data/O2_flexible_fit_max_rate',
                        'Unit': 'Rate / umol L^-1 s^-1'},
    },
}


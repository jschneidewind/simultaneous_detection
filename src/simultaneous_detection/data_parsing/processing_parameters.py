PROCESSING_PARAMETERS = {
    'H2_processing_parameters': {
                        'offset': 60,
                        'savgol_window': 30,
                        'savgol_polyorder': 1,
                        'savgol_window_diff': 50,
                        'savgol_polyorder_diff': 1,
                        'interval_resampling': 10,
                    },
    'O2_processing_parameters': { 
                        'offset': 60,
                        'savgol_window': 10,
                        'savgol_polyorder': 3,
                        'savgol_window_diff': 50,
                        'savgol_polyorder_diff': 1,
                        'interval_resampling': 10,
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
    } 
}

GROUP_MAPPING = {
        'Reference': None,
        'Intensity': 'metadata/Irradiance [mW/cm2]',
        'Loading': 'metadata/Catalyst loading [wt% Rh/Cr]',
        'D2O': 'metadata/D2O',
        'Temperature': 'metadata/Temperature [°C]'
        }

PLOTTING_INSTRUCTIONS = {
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
    }


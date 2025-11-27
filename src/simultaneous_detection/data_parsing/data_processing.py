import numpy as np
from scipy.signal import savgol_filter

from pyKES.utilities.find_nearest import find_nearest
from pyKES.utilities.time_series_resampling import resample_time_series
from pyKES.utilities.offset_correction import offset_correction

from pyKES.fitting_ODE import Fitting_Model, square_loss_time_series_normalized, objective_function

def convert_gases_to_umol_L(data,
                            liquid_phase_volume,
                             gas_phase_volume,
                             H2 = False):
    '''
    '''
    
    if H2 is True:
        NORMAL_PRESSURE = 1013.25
        data = data / NORMAL_PRESSURE # Convert from Pa to vol%
    
    MOLAR_VOLUME_STANRDARD_CONDITIONS = 24.465 # L/mol at 25C and 1 atm
    scaling_factor = 1 / (liquid_phase_volume / 1000) # Scaling from used liquid phase volume to 1 L

    gas_L = data * (1/100) * gas_phase_volume * (1/1000) # Convert from vol% to L of gas
    gas_mol = gas_L / MOLAR_VOLUME_STANRDARD_CONDITIONS # Convert from L of gas to mol of gas

    gas_umol = gas_mol * 1e6 # Convert from mol to umol
    gas_umol_L = gas_umol * scaling_factor # Scale to 1 L of liquid phase

    return gas_umol_L

def processing_data(time,
                    data,
                    offset,
                    savgol_window,
                    savgol_polyorder,
                    savgol_window_diff,
                    savgol_polyorder_diff,
                    interval_resampling,
                    poly_order,
                    start,
                    end,
                    prefix,
                    liquid_phase_volume,
                    gas_phase_volume):
    
    if 'gas' in prefix:
        if 'H2' in prefix:
            H2 = True
        else:
            H2 = False
        
        data = convert_gases_to_umol_L(data, 
                                       liquid_phase_volume, 
                                       gas_phase_volume, 
                                       H2 = H2)
    
    time_reaction, data_reaction = offset_correction(time, data, offset, start, end)

    data_smoothed = savgol_filter(data_reaction, savgol_window, savgol_polyorder)
    data_diff = np.diff(data_smoothed) / np.diff(time_reaction)
    time_diff = time_reaction[1:]

    data_diff_smoothed = savgol_filter(data_diff, savgol_window_diff, savgol_polyorder_diff)

    time_resampled, data_resampled = resample_time_series(time_reaction, data_reaction, interval_resampling)
    data_resampled_diff = np.diff(data_resampled) / np.diff(time_resampled)
    time_resampled_diff = time_resampled[1:]

    coeffs = np.polyfit(time_reaction, data_reaction, poly_order)
    data_poly_fit = np.polyval(coeffs, time_reaction)

    poly_fit_diff = np.diff(data_poly_fit) / np.diff(time_reaction)
    max_rate = np.max(poly_fit_diff)

    processed_data = {
        f'{prefix}_time_reaction': time_reaction,
        f'{prefix}_data_reaction': data_reaction,
        f'{prefix}_data_smoothed': data_smoothed,
        f'{prefix}_data_diff': data_diff,
        f'{prefix}_time_diff': time_diff,
        f'{prefix}_data_resampled': data_resampled,
        f'{prefix}_time_resampled': time_resampled,
        f'{prefix}_data_resampled_diff': data_resampled_diff,
        f'{prefix}_time_resampled_diff': time_resampled_diff,
        f'{prefix}_data_diff_smoothed': data_diff_smoothed,
        f'{prefix}_poly_fit': data_poly_fit,
        f'{prefix}_poly_fit_diff': poly_fit_diff,
        f'{prefix}_max_rate': max_rate,
    }

    return processed_data

def fitting_wrapper(experiment,
                    fitting_parameters,
                    parameters_mapping,
                    processed_data_dict,
                    common_time,
                    print_results = False,
                    disp = False):
    '''
    '''
    
    model = Fitting_Model(**fitting_parameters)

    model.experiments = [experiment]
    model.loss_function = square_loss_time_series_normalized

    model.optimize(workers = 1, print_results = print_results, disp = disp)

    error, fitting_results = objective_function(model.result.x, model, return_full = True)

    for species, prefix in parameters_mapping['species_mapping'].items():
        fit_data = fitting_results[experiment.experiment_name][species]
        fit_rate_data = np.diff(fit_data) / np.diff(common_time)

        processed_data_dict[f'{prefix}_fit'] = fit_data
        processed_data_dict[f'{prefix}_fit_rate'] = fit_rate_data
        processed_data_dict[f'{prefix}_fit_max_rate'] = np.max(fit_rate_data)

    for prefix, rate_constant_index in parameters_mapping['rate_constant_mapping'].items():
        processed_data_dict[f'{prefix}_rate_constant'] = model.result.x[rate_constant_index]

    return processed_data_dict
    


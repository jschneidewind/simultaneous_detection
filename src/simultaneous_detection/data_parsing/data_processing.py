import numpy as np
from scipy.signal import savgol_filter

from pyKES.utilities.find_nearest import find_nearest

def processing_data(time,
                    data,
                    savgol_window,
                    savgol_polyorder,
                    start,
                    end,
                    prefix):
    
    data_smoothed = savgol_filter(data, savgol_window, savgol_polyorder)
    data_diff = np.diff(data_smoothed) / np.diff(time)
    time_diff = time[1:]

    idx = find_nearest(time_diff, (start, end))

    irradiation_data = data_diff[idx[0]:idx[1]]
    irradiation_time = time_diff[idx[0]:idx[1]]

    processed_data = {
        f'{prefix}_data_smoothed': data_smoothed,
        f'{prefix}_data_diff': data_diff,
        f'{prefix}_time_diff': time_diff,
        f'{prefix}_data_diff_irradiation': irradiation_data,
        f'{prefix}_time_diff_irradiation': irradiation_time
    }

    return processed_data

    




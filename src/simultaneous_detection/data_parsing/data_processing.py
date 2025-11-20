import numpy as np
from scipy.signal import savgol_filter

from pyKES.utilities.find_nearest import find_nearest
from pyKES.utilities.time_series_resampling import resample_time_series
from pyKES.utilities.offset_correction import offset_correction


def processing_data(time,
                    data,
                    offset,
                    savgol_window,
                    savgol_polyorder,
                    savgol_window_diff,
                    savgol_polyorder_diff,
                    interval_resampling,
                    start,
                    end,
                    prefix):
    
    time_reaction, data_reaction = offset_correction(time, data, offset, start, end)

    data_smoothed = savgol_filter(data_reaction, savgol_window, savgol_polyorder)
    data_diff = np.diff(data_smoothed) / np.diff(time_reaction)
    time_diff = time_reaction[1:]

    data_diff_smoothed = savgol_filter(data_diff, savgol_window_diff, savgol_polyorder_diff)

    time_resampled, data_resampled = resample_time_series(time_reaction, data_reaction, interval_resampling)
    data_resampled_diff = np.diff(data_resampled) / np.diff(time_resampled)
    time_resampled_diff = time_resampled[1:]

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
    }

    return processed_data



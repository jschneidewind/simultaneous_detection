import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pprint as pp

from pyKES.database.data_processing import read_in_experiments_multiprocessing
from pyKES.database.database_experiments import ExperimentalDataset, Experiment
from pyKES.utilities.harmonize_time_series import harmonize_time_series
from pyKES.fitting_ODE import Fitting_Model, square_loss_time_series_normalized, objective_function

from simultaneous_detection.data_parsing.raw_data_reading_functions import reading_H2_file, reading_O2_file
from simultaneous_detection.data_parsing.data_processing import processing_data, fitting_wrapper
from simultaneous_detection.data_parsing.processing_parameters import PROCESSING_PARAMETERS, GROUP_MAPPING, PLOTTING_INSTRUCTIONS

def metadata_retrival_function(experiment_name, overview_df):
    '''
    Given an experiment name and an overview DataFrame, retrieves the metadata for the specified experiment.
    Returns a dictionary containing the metadata.


    '''

    experiment_row = overview_df[overview_df['Experiment'] == experiment_name]
    
    if experiment_row.empty:
        raise ValueError(f"No experiment found with name: {experiment_name}")
    
    if len(experiment_row) > 1:
        raise ValueError(f"Multiple experiments found with name: {experiment_name}")
    
    metadata_dict = experiment_row.iloc[0].to_dict()
    metadata_dict['experiment_name'] = metadata_dict['Experiment']

    return metadata_dict

def raw_data_reading_function(experiment_name, metadata_dict):
    '''
    '''

    file_H2 = f'data/H2_data/{metadata_dict["File name H2"]}'
    file_O2 = f'data/O2_data/{metadata_dict["File name O2"]}'

    if metadata_dict['group'] == 'Gas phase':
        raw_data_H2 = reading_H2_file(file_H2, mode = 'gas')
        raw_data_O2 = reading_O2_file(file_O2, channel = 4)

    else:
        raw_data_H2 = reading_H2_file(file_H2, mode = 'liquid')
        raw_data_O2 = reading_O2_file(file_O2, channel = 2)

    return raw_data_H2 | raw_data_O2

def processing_function(raw_data_dict, metadata_dict):
    '''
    '''

    if metadata_dict['group'] == 'Gas phase':
        prefix_H2 = 'H2_gas'
        prefix_O2 = 'O2_gas'
        raw_data_H2_string = 'H2_Pa'
        raw_data_O2_string = 'O2_data'
    else:
        prefix_H2 = 'H2'
        prefix_O2 = 'O2'
        raw_data_H2_string = 'H2_umol_L'
        raw_data_O2_string = 'O2_data'


    processed_H2 = processing_data(
        time = raw_data_dict['H2_time_s'],
        data = raw_data_dict[raw_data_H2_string],
        start = metadata_dict['Unisense Irradiation start [s]'],
        end = metadata_dict['Unisense Irradiation end [s]'],
        prefix = prefix_H2,
        liquid_phase_volume = metadata_dict['Liquid phase volume [mL]'],
        gas_phase_volume = metadata_dict['Gas phase volume [mL]'],
        **PROCESSING_PARAMETERS['H2_processing_parameters']
    )

    processed_O2 = processing_data(
        time = raw_data_dict['O2_time_s'],
        data = raw_data_dict[raw_data_O2_string],
        start = metadata_dict['Pyroscience Irradiation start [s]'],
        end = metadata_dict['Pyroscience Irradiation end [s]'],
        prefix = prefix_O2,
        liquid_phase_volume = metadata_dict['Liquid phase volume [mL]'],
        gas_phase_volume = metadata_dict['Gas phase volume [mL]'],
        **PROCESSING_PARAMETERS['O2_processing_parameters']
    )

    processed_data_dict = processed_H2 | processed_O2

    ### Harmonizing time series for fitting
    common_time, H2_data_aligned, O2_data_aligned = harmonize_time_series(
        processed_data_dict[f'{prefix_H2}_time_reaction'],
        processed_data_dict[f'{prefix_H2}_data_reaction'],
        processed_data_dict[f'{prefix_O2}_time_reaction'],
        processed_data_dict[f'{prefix_O2}_data_reaction']
    )

    processed_data_dict['common_time_reaction'] = common_time
    processed_data_dict['flexible_diff_time'] = common_time[1:]
    processed_data_dict[f'{prefix_H2}_data_aligned'] = H2_data_aligned
    processed_data_dict[f'{prefix_O2}_data_aligned'] = O2_data_aligned
    
    ### Creating experiment object for fitting
    experiment = Experiment(
            experiment_name = metadata_dict['experiment_name'],
            raw_data_file = metadata_dict['File name H2'],
            color = metadata_dict.get('color', 'black'),
            group = metadata_dict.get('group', 'default'),
            metadata = metadata_dict,
            raw_data = raw_data_dict,
            processed_data = processed_data_dict
        )
    
    if metadata_dict['group'] != 'Gas phase':

        processed_data_dict = fitting_wrapper(
            experiment,
            PROCESSING_PARAMETERS['fitting_parameters'],
            PROCESSING_PARAMETERS['fitting_parameters_mapping'],
            processed_data_dict,
            common_time,
        )

        processed_data_dict = fitting_wrapper(
            experiment,
            PROCESSING_PARAMETERS['fitting_parameters_flexible_H2'],
            PROCESSING_PARAMETERS['fitting_parameters_flexible_H2_mapping'],
            processed_data_dict,
            common_time,
            print_results = True
        )

        processed_data_dict = fitting_wrapper(
            experiment,
            PROCESSING_PARAMETERS['fitting_parameters_flexible_O2'],
            PROCESSING_PARAMETERS['fitting_parameters_flexible_O2_mapping'],
            processed_data_dict,
            common_time,
            print_results = True
        )

    return processed_data_dict

def generate_dataset():
    """
    Generate a complete simultaneous O2/H2 experimental dataset from Excel metadata and raw data files.

    This function creates a hierarchical dataset structure containing simultaneous oxygen and
    hydrogen evolution experiments. The dataset is built by reading metadata from an Excel file,
    processing matching raw O2 and H2 data files, and organizing everything into a structured format.

    Dataset Structure
    -----------------
    ExperimentalDataset
    ├── overview_df : pd.DataFrame
    │   └── Contains metadata for all experiments (from Excel file)
    └── experiments : Dict[str, Experiment]
        └── {experiment_name} : Experiment
            ├── experiment_name : str
            │   └── Unique identifier for the experiment
            ├── color : str
            │   └── Plot color assigned to this experiment
            ├── metadata : Dict[str, any]
            │   ├── 'active' : str ('TRUE'/'FALSE')
            │   ├── 'Experiment' : str (experiment name)
            │   ├── 'File name H2' : str (H2 data filename)
            │   ├── 'File name O2' : str (O2 data filename)
            │   ├── 'Irradiation start [s]' : float (irradiation start time)
            │   ├── 'Irradiation end [s]' : float (irradiation end time)
            │   ├── 'D2O' : str ('TRUE'/'FALSE')
            │   └── ... (other experiment-specific parameters)
            ├── raw_data : Dict[str, np.array]
            │   ├── 'H2_time_s' : np.array (H2 time values in seconds)
            │   ├── 'H2_umol_L' : np.array (raw H2 concentration in μmol/L)
            │   ├── 'O2_time_s' : np.array (O2 time values in seconds)
            │   ├── 'O2_data' : np.array (raw O2 sensor data)
            │   └── ... (additional sensor data)
            └── processed_data : Dict[str, np.array]
                ├── 'H2_data_smoothed' : np.array (Savitzky-Golay filtered H2 data)
                ├── 'H2_data_diff' : np.array (H2 evolution rate, full dataset)
                ├── 'H2_time_diff' : np.array (time array for rate data)
                ├── 'H2_data_diff_irradiation' : np.array (H2 rate during irradiation)
                ├── 'H2_time_diff_irradiation' : np.array (time during irradiation)
                ├── 'O2_data_smoothed' : np.array (Savitzky-Golay filtered O2 data)
                ├── 'O2_data_diff' : np.array (O2 evolution rate, full dataset)
                ├── 'O2_time_diff' : np.array (time array for rate data)
                ├── 'O2_data_diff_irradiation' : np.array (O2 rate during irradiation)
                └── 'O2_time_diff_irradiation' : np.array (time during irradiation)

    Processing Pipeline
    -------------------
    1. Read experiment metadata from Excel file ('251105_O2_H2_Experiment_Overview.xlsx')
    2. Force 'active' and 'D2O' columns to be read as strings
    3. Create ExperimentalDataset with overview DataFrame
    4. For each experiment in overview:
    - Extract metadata using metadata_retrival_function
    - Read H2 data from 'data/H2_data/{File name H2}'
    - Read O2 data from 'data/O2_data/{File name O2}' (channel 2)
    - Merge H2 and O2 raw data dictionaries
    - Process H2 data:
        * Apply Savitzky-Golay filter (window=30, polyorder=3)
        * Calculate derivative (evolution rate) using np.diff
        * Extract irradiation period data using start/end times
    - Process O2 data:
        * Apply Savitzky-Golay filter (window=10, polyorder=3)
        * Calculate derivative (evolution rate) using np.diff
        * Extract irradiation period data using start/end times
    - Create Experiment object with all data and metadata
    5. Save complete dataset to HDF5 file for future loading

    Output File
    -----------
    Saves dataset to 'data/251105_processed_O2_H2_data.h5' containing:
    - All experiment objects with raw and processed data
    - Merged O2 and H2 datasets for each experiment
    - Smoothed data and evolution rates (derivatives)
    - Full datasets and irradiation-period subsets
    - Metadata for filtering and analysis
    - Overview DataFrame for quick experiment lookup

    Notes
    -----
    - Processes all experiments listed in the Excel overview file
    - Preserves 'TRUE'/'FALSE' strings in 'active' and 'D2O' columns for filtering
    - H2 uses stronger smoothing (window=30) than O2 (window=10)
    - Evolution rates calculated as derivatives of smoothed data
    - Uses multiprocessing for efficient parallel data processing
    - Time arrays for derivatives are one element shorter due to np.diff
    """

    overview_df = pd.read_excel(
        'data/251126_O2_H2_Experiment_Overview.xlsx',
        sheet_name='Sheet1',
        dtype={'active': str,
               'D2O': str}  # Force 'active' and 'D2O' columns to be read as strings
    )

    dataset = ExperimentalDataset(
                    overview_df = overview_df,
                    group_mapping = GROUP_MAPPING,
                    plotting_instruction = PLOTTING_INSTRUCTIONS,
                    processing_parameters = PROCESSING_PARAMETERS
                    )

    results = read_in_experiments_multiprocessing(
        dataset,
        metadata_retrival_function,
        raw_data_reading_function,
        processing_function,
        overview_df_based_processing = True,
    )

    dataset.save_to_hdf5('data/251129_processed_O2_H2_data.h5')

def debugging_function():

    overview_df = pd.read_excel(
        'data/251126_O2_H2_Experiment_Overview.xlsx',
        sheet_name='Sheet1',
        dtype={'active': str,
               'D2O': str}  # Force 'active' and 'D2O' columns to be read as strings
            )
    
    metadata_dict = metadata_retrival_function('NB-312', overview_df)
    raw_data_dict = raw_data_reading_function('NB-312', metadata_dict)
    processed_data_dict = processing_function(raw_data_dict, metadata_dict)

    fig, ax = plt.subplots(1,2, figsize = (12, 6))
    fig.tight_layout()

    # ax[0].plot(raw_data_dict['O2_time_s'], raw_data_dict['O2_data'], '.', label = 'O2 data', markersize = 2)
    # ax[0].plot(raw_data_dict['H2_time_s'], raw_data_dict['H2_Pa'], '.', label = 'H2 data', markersize = 2)
    
    # ax[0].plot(processed_data_dict['O2_time_reaction'], processed_data_dict['O2_data_reaction'], '.', label = 'O2 data')
    # ax[0].plot(processed_data_dict['H2_time_reaction'], processed_data_dict['H2_data_reaction'], '.', label = 'H2 data')

    # ax[0].plot(processed_data_dict['O2_time_reaction'], processed_data_dict['O2_poly_fit'], '-', label = 'O2 poly fit')
    # ax[0].plot(processed_data_dict['H2_time_reaction'], processed_data_dict['H2_poly_fit'], '-', label = 'H2 poly fit')

    ax[0].plot(processed_data_dict['common_time_reaction'], processed_data_dict['O2_gas_data_aligned'], 'o-', label = 'O2 data', markersize = 1)
    ax[0].plot(processed_data_dict['common_time_reaction'], processed_data_dict['H2_gas_data_aligned'], 'o-', label = 'H2 data', markersize = 1)
    #ax[0].plot(processed_data_dict['common_time_reaction'], processed_data_dict['H2_gas_data_aligned'] / processed_data_dict['O2_gas_data_aligned'])

    # ax[0].plot(processed_data_dict['common_time_reaction'], processed_data_dict['O2_fit'], '-', label = 'O2 fit')
    # ax[0].plot(processed_data_dict['common_time_reaction'], processed_data_dict['H2_fit'], '-', label = 'H2 fit')

    # # ax[0].plot(raw_data_dict['O2_time_s'], raw_data_dict['O2_data'], '.', label = 'O2 data', markersize = 2)
    # # ax[0].plot(raw_data_dict['H2_time_s'], raw_data_dict['H2_umol_L'], '.', label = 'H2 data', markersize = 2)

    # # ax[0].plot(raw_data_dict['O2_time_s'], processed_data_dict['O2_data_smoothed'], '-', label = 'O2 data')
    # # ax[0].plot(raw_data_dict['H2_time_s'], processed_data_dict['H2_data_smoothed'], '-', label = 'H2 data')

    # # ax[0].plot(processed_data_dict['O2_time_resampled'], processed_data_dict['O2_data_resampled'], 'o-', label = 'O2 resampled data')
    # # ax[0].plot(processed_data_dict['H2_time_resampled'], processed_data_dict['H2_data_resampled'], 'o-', label = 'H2 resampled data')

    # # ax[1].plot(processed_data_dict['O2_time_resampled_diff'], processed_data_dict['O2_data_resampled_diff'], '-', label = 'O2 resampled diff data')
    # # ax[1].plot(processed_data_dict['H2_time_resampled_diff'], processed_data_dict['H2_data_resampled_diff'], '-', label = 'H2 resampled diff data')

    # ax[1].plot(processed_data_dict['O2_time_diff'], processed_data_dict['O2_data_diff'], '.', label = 'O2 data')
    # ax[1].plot(processed_data_dict['H2_time_diff'], processed_data_dict['H2_data_diff'], '.', label = 'H2 data')

    # ax[1].plot(processed_data_dict['O2_time_diff'], processed_data_dict['O2_data_diff_smoothed'], '-', label = 'O2 data')
    # ax[1].plot(processed_data_dict['H2_time_diff'], processed_data_dict['H2_data_diff_smoothed'], '-', label = 'H2 data')

    # ax[1].plot(processed_data_dict['O2_time_diff'], processed_data_dict['O2_poly_fit_diff'], '-', label = 'O2 poly fit diff')
    # ax[1].plot(processed_data_dict['H2_time_diff'], processed_data_dict['H2_poly_fit_diff'], '-', label = 'H2 poly fit diff')

    # ax[0].legend()
    # ax[1].legend()

    plt.show()




if __name__ == "__main__":
    generate_dataset()
    #debugging_function()

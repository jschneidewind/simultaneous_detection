import matplotlib.pyplot as plt
import numpy as np

from pyKES.database.database_experiments import ExperimentalDataset
from pyKES.fitting_ODE import (Fitting_Model, 
                               resolve_experiment_attributes, 
                               square_loss_time_series, 
                               square_loss_time_series_normalized, 
                               objective_function)


def main():

    dataset = ExperimentalDataset.load_from_hdf5('data/251129_processed_O2_H2_data.h5')

    model = Fitting_Model(['[H2O-int] > 2 [H2-aq] + [O2-aq], k1',
                           '[H2O] > [H2O-int], k3',
                           '[O2-aq] > [O2-g], k2',
                           '[H2-aq] > [H2-g], k2 ; factor1',
                            ])
                                                
    model.experiments = [dataset.experiments['NB-312'],
                         (dataset.experiments['NB-353'], 1)]
    
    model.rate_constants_to_optimize = {'k1': (0, 1),
                                        'k2': (0, 1),
                                        'k3': (0, 1),
                                        }

    model.other_multipliers = {
        'factor1': 1.68 # Based on Henry's constant ratio
    }

    model.data_to_be_fitted = {
                '[O2-aq]': {'x': 'processed_data/common_time_reaction',
                            'y': 'processed_data/O2_data_aligned'},
                '[H2-aq]': {'x': 'processed_data/common_time_reaction',
                            'y': 'processed_data/H2_data_aligned'},
                 '[O2-g]': {'x': 'processed_data/common_time_reaction',
                           'y': 'processed_data/O2_gas_data_aligned'},
                 '[H2-g]': {'x': 'processed_data/common_time_reaction',
                           'y': 'processed_data/H2_gas_data_aligned'},
                            }

    model.initial_conditions = {
        '[H2O]': 55 * 1e6,  # Convert from mol/L to μmol/L
    }
    
    
    model.times = {
        'times': 'processed_data/common_time_reaction',
    }

    model.loss_function = square_loss_time_series_normalized

    model.optimize()

    model.visualize_optimization_results()

    model.add_fit_results_to_database(dataset)
    model.database.save_to_hdf5('data/251129_processed_O2_H2_data_with_fits.h5')

    plt.show()

    

if __name__ == '__main__':

    # Result 251126-18:56
    # ----------------------------
    # Optimized rate constants:
    # {'k1': np.float64(0.0022902702667019215),
    #  'k2': np.float64(0.0057268874623205845),
    #  'k3': np.float64(4.144375953529789e-09)}
    main()
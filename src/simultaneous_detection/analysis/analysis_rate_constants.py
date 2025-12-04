import numpy as np
import matplotlib.pyplot as plt
import pprint as pp

from pyKES.database.database_experiments import ExperimentalDataset


def main():

    dataset = ExperimentalDataset.load_from_hdf5('data/251203_processed_O2_H2_data.h5')
    dataset_gas = ExperimentalDataset.load_from_hdf5('data/251203_processed_O2_H2_data_gas_phase_fixed.h5')

    fig, ax = plt.subplots(2, 2, figsize=(10, 8))

    k1_values = []
    k2_values = []
    k3_values = []
    error_fixed_fit = []
    error_fixed_fit_gas = []

    for counter, experiment_name in enumerate(dataset.experiments):

        experiment = dataset.experiments[experiment_name]
        experiment_gas = dataset_gas.experiments[experiment_name]

        if experiment.metadata['group'] != 'Gas phase':

            rate_constants = experiment.processed_data['Fit_all_rate_constants']
            error = experiment.processed_data['Fit_fixed_fitting_error']
            error_fixed_fit.append(error)

            error_gas = experiment_gas.processed_data['Fit_fixed_fitting_error']
            error_fixed_fit_gas.append(error_gas)

            print('-----------------------------------')
            print(experiment_name, error, error_gas)
            pp.pprint(rate_constants)
            pp.pprint(experiment_gas.processed_data['Fit_fixed_all_rate_constants'])

            k1_values.append(rate_constants['k1'])
            k2_values.append(rate_constants['k2'])
            k3_values.append(rate_constants['k3'])

            ax[0,0].plot(counter, rate_constants['k1'], '.', color = 'blue')
            ax[0,1].plot(counter, rate_constants['k2'], '.', color = 'orange')
            ax[1,0].plot(counter, rate_constants['k3'], '.', color = 'green')

    print(np.mean(k1_values))
    print(np.mean(k2_values))
    print(np.mean(k3_values))

    print(np.sum(error_fixed_fit))
    print(np.sum(error_fixed_fit_gas))

    #plt.show()
        



if __name__ == "__main__":
    main()
import numpy as np
import matplotlib.pyplot as plt
import pprint as pp

from pyKES.database.database_experiments import ExperimentalDataset

def main():

    dataset = ExperimentalDataset.load_from_hdf5('data/251125_processed_O2_H2_data.h5')

    reference_experiments = ['NB-316', 'NB-320', 'NB-336', 'NB-348', 'NB-353']
    loading_experiments = ['NB-327', 'NB-328', 'NB-332', 'NB-333', 'NB-354', 'NB-355']

    key = 'Catalyst loading [wt% Rh/Cr]'
    analysis_key_A = 'H2_max_rate'
    analysis_key_B = None

    for experiment_name in reference_experiments + loading_experiments:
        experiment = dataset.experiments[experiment_name]

        plt.plot(experiment.metadata[key], experiment.processed_data[analysis_key_A], '.')

        if analysis_key_B:
            plt.plot(experiment.metadata[key], experiment.processed_data[analysis_key_B], '.')



    plt.show()

def secondary():

    dataset_working = ExperimentalDataset.load_from_hdf5('data/251124_processed_O2_H2_data.h5')
    dataset_broken = ExperimentalDataset.load_from_hdf5('data/251127_processed_O2_H2_data.h5')

    experiment_name = 'NB-351'

    #exp_working = dataset_working.experiments[experiment_name].metadata
    exp_broken = dataset_broken.experiments[experiment_name].metadata

    #pp.pprint(exp_working)
    pp.pprint(exp_broken)






if __name__ == "__main__":
    # main()
    secondary()
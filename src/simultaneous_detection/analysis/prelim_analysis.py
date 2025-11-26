import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors
import pprint as pp


from pyKES.database.database_experiments import ExperimentalDataset
from pyKES.plotting.lighten_colors import lighten_color




def main():

    dataset = ExperimentalDataset.load_from_hdf5('data/251128_processed_O2_H2_data.h5')

    pp.pprint(dataset.processing_parameters)

    print(dataset.experiments['NB-346'].processed_data['O2_rate_constant'])
    
    # Get list of experiment names in the "Reference" group
    #reference_experiments = dataset.overview_df[dataset.overview_df['Group'] == 'Reference']['Experiment'].tolist()
    reference_experiments = ['NB-349']


    for experiment_name in reference_experiments:
        experiment = dataset.experiments[experiment_name]

 

        plt.plot(
            experiment.processed_data['H2_time_reaction'],
            experiment.processed_data['H2_data_smoothed'],
            label = f'H2 - {experiment_name}',
            color = lighten_color(experiment.color, amount = 0.5)
        )

        plt.plot(
            experiment.processed_data['O2_time_reaction'],
            experiment.processed_data['O2_data_smoothed'],
            label = f'O2 - {experiment_name}',
            color = experiment.color
        )






        # plt.plot(
        #     experiment.raw_data['H2_time_s'],
        #     experiment.raw_data['H2_umol_L'],
        #     label = f'H2 - {experiment_name}',
        #     color = lighten_color(experiment.color, amount = 0.5)
        # )

        # plt.plot(
        #     experiment.raw_data['O2_time_s'],
        #     experiment.raw_data['O2_data'],
        #     label = f'O2 - {experiment_name}',
        #     color = experiment.color
        # )



    plt.legend()

    plt.show()


def secondary():

    dataset = ExperimentalDataset.load_from_hdf5('data/test_251128_processed_O2_H2_data.h5')

    print(dataset.experiments['NB-316'].processed_data['O2_flexible_fit_max_rate'])

    

if __name__ == "__main__":
    #main()
    secondary()  
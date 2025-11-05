import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors


from pyKES.database.database_experiments import ExperimentalDataset


def lighten_color(color, amount=0.5):
    """
    Lightens the given color by mixing it with white.
    
    Parameters
    ----------
    color : str or tuple
        Color to lighten (matplotlib color)
    amount : float
        Amount to lighten (0-1). 0 = original color, 1 = white
    
    Returns
    -------
    tuple
        Lightened RGB color
    """
    try:
        c = mcolors.to_rgb(color)
    except ValueError:
        c = color
    
    c = np.array(c)
    white = np.array([1, 1, 1])

    return tuple(c + (white - c) * amount)

def main():

    dataset = ExperimentalDataset.load_from_hdf5('data/251105_processed_O2_H2_data.h5')
    
    # Get list of experiment names in the "Reference" group
    #reference_experiments = dataset.overview_df[dataset.overview_df['Group'] == 'Reference']['Experiment'].tolist()
    reference_experiments = ['NB-331']


    for experiment_name in reference_experiments:
        experiment = dataset.experiments[experiment_name]

        # plt.plot(
        #     experiment.processed_data['H2_time_diff'],
        #     experiment.processed_data['H2_data_diff'],
        #     label = f'H2 - {experiment_name}',
        #     color = lighten_color(experiment.color, amount = 0.5)
        # )

        # plt.plot(
        #     experiment.processed_data['O2_time_diff'],
        #     experiment.processed_data['O2_data_diff'],
        #     label = f'O2 - {experiment_name}',
        #     color = experiment.color
        # )

        plt.plot(
            experiment.raw_data['H2_time_s'],
            experiment.raw_data['H2_umol_L'],
            label = f'H2 - {experiment_name}',
            color = lighten_color(experiment.color, amount = 0.5)
        )

        plt.plot(
            experiment.raw_data['O2_time_s'],
            experiment.raw_data['O2_data'],
            label = f'O2 - {experiment_name}',
            color = experiment.color
        )



    plt.legend()

    plt.show()


    

if __name__ == "__main__":
    main()  
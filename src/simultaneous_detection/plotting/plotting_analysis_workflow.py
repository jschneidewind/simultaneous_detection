import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 12
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

from pyKES.database.database_experiments import ExperimentalDataset
from pyKES.utilities.resolve_attributes import resolve_experiment_attributes

import pprint as pp

from simultaneous_detection.data_parsing.processing_parameters import PLOTTING_INSTRUCTIONS

def main():

    dataset = ExperimentalDataset.load_from_hdf5('data/251130_processed_O2_H2_data.h5')

    experiment = dataset.experiments['NB-353']

    fig, ax = plt.subplots(nrows = 3, ncols = 1, figsize = (4.9, 8))
    fig.subplots_adjust(left = 0.19, right = 0.69, top = 0.97, bottom = 0.08, hspace=0.6)

    PLOTTING_DATA = resolve_experiment_attributes(
        PLOTTING_INSTRUCTIONS['time_series_instructions'],
        experiment,
        mode = 'permissible'
    )

    ### Plot A

    irradiation_start = experiment.metadata['Unisense Irradiation start [s]']
    irradiation_end = experiment.metadata['Unisense Irradiation end [s]']

    ax[0].plot(PLOTTING_DATA['Raw (H2)']['x'], PLOTTING_DATA['Raw (H2)']['y'],
        '.', color = 'gray', label = 'Raw data H$_2$')    

    ax[0].plot(PLOTTING_DATA['Raw (O2)']['x'], PLOTTING_DATA['Raw (O2)']['y'],
        '.', color = 'black', label = 'Raw data O$_2$')
    
    ax[0].legend(handlelength=1, handletextpad=0.5, columnspacing=1, 
                 borderpad=0.3, labelspacing=0.3, framealpha = 0.95,
                 loc='center left', bbox_to_anchor=(1.02, 0.5))
    
    ax[0].set_xlabel('Time / s')
    ax[0].set_ylabel('Concentration / μmol·L$^{-1}$')

    ax[0].text(0.15, 0.75, 'I',transform=ax[0].transAxes,fontsize=18, fontweight='bold')
    ax[0].text(0.45, 0.75, 'II',transform=ax[0].transAxes,fontsize=18, fontweight='bold')
    ax[0].text(0.85, 0.75, 'III',transform=ax[0].transAxes,fontsize=18, fontweight='bold')

    ax[0].axvline(x=irradiation_start, color='black', linestyle='--')
    ax[0].axvline(x=irradiation_end, color='black', linestyle='--')


    # Get the data limits from the x-axis
    x_min, x_max = ax[0].get_xlim()

    tick_locations = [0, 1000, 2000]
    ax[0].set_xticks(tick_locations)

    # Convert data coordinate to axes fraction (0-1 range)
    reaction_start_axes_frac = (irradiation_start - x_min) / (x_max - x_min)
    reaction_end_axes_frac = (irradiation_end - x_min) / (x_max - x_min)

    # Create a connection line from reaction_start on x-axis to left edge of plot
    con1 = patches.ConnectionPatch(
        xyA=(reaction_start_axes_frac,0),  # Start at reaction_start on x-axis
        xyB=(0,1),     # End at left edge, top of plot
        coordsA='axes fraction', coordsB='axes fraction',
        axesA=ax[0], axesB=ax[1],
        color='black', linestyle='--', linewidth=1.5
    )
    ax[0].add_patch(con1)
    
    con2 = patches.ConnectionPatch(
        xyA=(reaction_end_axes_frac,0),  # Start at reaction_start on x-axis
        xyB=(1,1),     # End at left edge, top of plot
        coordsA='axes fraction', coordsB='axes fraction',
        axesA=ax[0], axesB=ax[1],
        color='black', linestyle='--', linewidth=1.5
    )
    ax[0].add_patch(con2)


    ### Plot B

    ax[1].plot(PLOTTING_DATA['Reaction (H2)']['x'], PLOTTING_DATA['Reaction (H2)']['y'],   
        '.', color = 'gray', label = 'Data H$_2$')

    ax[1].plot(PLOTTING_DATA['Reaction (O2)']['x'], PLOTTING_DATA['Reaction (O2)']['y'],   
        '.', color = 'black', label = 'Data O$_2$')

    ax[1].plot(PLOTTING_DATA['Poly fit (H2)']['x'], PLOTTING_DATA['Poly fit (H2)']['y'],        
            color = 'orange', label = 'Fit H$_2$')

    ax[1].plot(PLOTTING_DATA['Poly fit (O2)']['x'], PLOTTING_DATA['Poly fit (O2)']['y'],        
            color = 'red', label = 'Fit O$_2$')

    ax[1].legend(handlelength=1, handletextpad=0.5, columnspacing=1, 
                 borderpad=0.3, labelspacing=0.3, framealpha = 0.95,
                 loc='center left', bbox_to_anchor=(1.02, 0.5))
    
    ax[1].set_xlabel('Time / s')
    ax[1].set_ylabel('Concentration / μmol·L$^{-1}$')

    ### Plot C

    ax[2].plot(PLOTTING_DATA['Rate (H2)']['x'], PLOTTING_DATA['Rate (H2)']['y'],
        '.', color = 'gray', label = 'Rate H$_2$')
    
    ax[2].plot(PLOTTING_DATA['Rate (O2)']['x'], PLOTTING_DATA['Rate (O2)']['y'],
        '.', color = 'black', label = 'Rate O$_2$')

    ax[2].plot(PLOTTING_DATA['Rate poly fit (H2)']['x'], PLOTTING_DATA['Rate poly fit (H2)']['y'],
        color = 'orange', label = 'Fit H$_2$')

    ax[2].plot(PLOTTING_DATA['Rate poly fit (O2)']['x'], PLOTTING_DATA['Rate poly fit (O2)']['y'],
        color = 'red', label = 'Fit O$_2$')   

    max_rate_idx_H2 = np.argmax(PLOTTING_DATA['Rate poly fit (H2)']['y'])
    max_rate_idx_O2 = np.argmax(PLOTTING_DATA['Rate poly fit (O2)']['y'])

    ax[2].plot(PLOTTING_DATA['Rate poly fit (H2)']['x'][max_rate_idx_H2],
               PLOTTING_DATA['Rate poly fit (H2)']['y'][max_rate_idx_H2],
               'o', markersize = 10, label = 'Max. rate H$_2$', color = 'darkorange')
    
    ax[2].plot(PLOTTING_DATA['Rate poly fit (O2)']['x'][max_rate_idx_O2],
               PLOTTING_DATA['Rate poly fit (O2)']['y'][max_rate_idx_O2],
               'o', markersize = 10, label = 'Max. rate O$_2$', color = 'red')

    ax[2].legend(handlelength=1, handletextpad=0.5, columnspacing=1, 
                 borderpad=0.3, labelspacing=0.3, framealpha = 0.95,
                 loc='center left', bbox_to_anchor=(1.02, 0.5))
    
    ax[2].set_xlabel('Time / s')
    ax[2].set_ylabel('Rate / μmol·L$^{-1}$·s$^{-1}$')

    ax[0].text(-0.37, 0.95, 'A',transform=ax[0].transAxes,fontsize=22, fontweight='bold')
    ax[1].text(-0.37, 0.95, 'B',transform=ax[1].transAxes,fontsize=22, fontweight='bold')
    ax[2].text(-0.37, 0.95, 'C',transform=ax[2].transAxes,fontsize=22, fontweight='bold')

    fig.text(x=0.26, y=0.675, s='1. Baseline correction', 
         fontsize=12, fontweight='bold', 
         ha='left', va='center')
    fig.text(x=0.26, y=0.65, s='2. Fitting', 
         fontsize=12, fontweight='bold', 
         ha='left', va='center')
    
    fig.text(x=0.07, y=0.335, s='3. Differentiation', 
         fontsize=12, fontweight='bold', 
         ha='left', va='center')

    
    arrow = patches.FancyArrow(
        x=0.45, y=0.35,           # Start position
        dx=0, dy=-0.04,            # Direction vector
        width=0.08,               # Width of arrow
        head_width=0.15,          # Width of arrow head
        head_length=0.02,         # Length of arrow head
        length_includes_head=True,
        color='grey',
        transform=fig.transFigure  # Use figure coordinates (0-1)
    )
    fig.patches.append(arrow)     # Add to figure

    #fig.savefig('Figures/Data_Processing.pdf', dpi = 500)

    plt.show()


if __name__ == "__main__":
    main()


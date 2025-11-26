import matplotlib.pyplot as plt
import numpy as np

from pyKES.plotting.plotting_tools import plot_analysis_results
from pyKES.plotting.lighten_colors import lighten_color



def main():
    
    fig, ax = plt.subplots(2,2, figsize=(8, 6))
    fig.tight_layout(pad=3.0)
    fig.subplots_adjust(right=0.98)

    y_axis_label = 'Max. rate / μmol·L$^{-1}$·s$^{-1}$'
    data_labels = {'H2 max rate (flexible)': 'H$_2$',
                   'O2 max rate (flexible)': 'O$_2$'}
    
    viridis = plt.cm.viridis
    colors = [viridis(i) for i in np.linspace(0, 0.85, 4)]

    # Create color dictionaries for each plot
    # Each plot uses one color from 'colors', with H2 as a lighter hue
    colors_dict_0 = {
        'O2 max rate (flexible)': colors[0],
        'H2 max rate (flexible)': lighten_color(colors[0], amount=0.3)
    }
    colors_dict_1 = {
        'O2 max rate (flexible)': colors[1],
        'H2 max rate (flexible)': lighten_color(colors[1], amount=0.3)
    }
    colors_dict_2 = {
        'O2 max rate (flexible)': colors[2],
        'H2 max rate (flexible)': lighten_color(colors[2], amount=0.3)
    }
    colors_dict_3 = {
        'O2 max rate (flexible)': colors[3],
        'H2 max rate (flexible)': lighten_color(colors[3], amount=0.3)
    }

    plot_analysis_results(
        'data/plotting_data/Intensity_analysis_results_20251124_185820.json',
        ax = ax[0,0],
        linestyles= "-",
        markersize = 8,
        xlabel = 'Irradiance / mW·cm$^{-2}$',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_0,
        )
    
    plot_analysis_results(
        'data/plotting_data/Temperatur_analysis_results_20251125_144814.json',
        ax = ax[0,1],
        linestyles= "-",
        markersize = 8,
        xlabel = 'Temperature / °C',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_1,
        )
    
    plot_analysis_results(
        'data/plotting_data/Loading_analysis_results_20251125_143036.json',
        ax = ax[1,0],
        linestyles= "-",
        markersize = 8,
        xlabel = 'Co-catalyst loading / wt. fraction Rh/Cr',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_2,
        )
        
        
    plot_analysis_results(
        'data/plotting_data/D2O_analysis_results_20251125_142902.json',
        ax = ax[1,1],
        markersize = 8,
        xlabel = 'D$_2$O',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_3,
        )
    
    ax[0][0].text(-0.23, 1.05, 'A',transform=ax[0][0].transAxes,fontsize=22, fontweight='bold')
    ax[0][1].text(-0.23, 1.05, 'B',transform=ax[0][1].transAxes,fontsize=22, fontweight='bold')
    ax[1][0].text(-0.23, 1.05, 'C',transform=ax[1][0].transAxes,fontsize=22, fontweight='bold')
    ax[1][1].text(-0.23, 1.05, 'D',transform=ax[1][1].transAxes,fontsize=22, fontweight='bold')

    plt.show()

if __name__ == "__main__":
    main()
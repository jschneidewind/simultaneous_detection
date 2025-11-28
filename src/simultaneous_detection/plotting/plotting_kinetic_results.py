import matplotlib.pyplot as plt
import numpy as np
import pprint as pp

from pyKES.plotting.plotting_tools import plot_analysis_results, load_json_data
from pyKES.plotting.lighten_colors import lighten_color



def main():
    
    fig, ax = plt.subplots(2,2, figsize=(8, 6))
    fig.tight_layout(pad=3.0)
    fig.subplots_adjust(right=0.98, bottom = 0.1, top = 0.94)

    y_axis_label = 'Max. rate / μmol·L$^{-1}$·s$^{-1}$'
    data_labels = {'H2 max rate (polyfit)': 'H$_2$',
                   'O2 max rate (polyfit)': 'O$_2$'}
    
    viridis = plt.cm.viridis
    colors = [viridis(i) for i in np.linspace(0, 0.85, 4)]

    # Create color dictionaries for each plot
    # Each plot uses one color from 'colors', with H2 as a lighter hue
    colors_dict_0 = {
        'O2 max rate (polyfit)': colors[0],
        'H2 max rate (polyfit)': lighten_color(colors[0], amount=0.3)
    }
    colors_dict_1 = {
        'O2 max rate (polyfit)': colors[1],
        'H2 max rate (polyfit)': lighten_color(colors[1], amount=0.3)
    }
    colors_dict_2 = {
        'O2 max rate (polyfit)': colors[2],
        'H2 max rate (polyfit)': lighten_color(colors[2], amount=0.3)
    }
    colors_dict_3 = {
        'O2 max rate (polyfit)': colors[3],
        'H2 max rate (polyfit)': lighten_color(colors[3], amount=0.3)
    }

    plot_analysis_results(
        'data/plotting_data/Irra_analysis_results_20251127_182340.json',
        ax = ax[0,0],
        linestyles= "-",
        markersize = 8,
        xlabel = 'Irradiance / mW·cm$^{-2}$',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_0,
        )
    
    plot_analysis_results(
        'data/plotting_data/Temp_analysis_results_20251127_182426.json',
        ax = ax[0,1],
        linestyles= "-",
        markersize = 8,
        xlabel = 'Temperature / °C',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_1,
        )
    
    plot_analysis_results(
        'data/plotting_data/Cata_analysis_results_20251127_182412.json',
        ax = ax[1,0],
        linestyles= "-",
        markersize = 8,
        xlabel = 'Co-catalyst loading / wt. fraction Rh/Cr',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_2,
        )
        
        
    plot_analysis_results(
        'data/plotting_data/D2O_analysis_results_20251127_182353.json',
        ax = ax[1,1],
        markersize = 8,
        xlabel = 'D$_2$O',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_3,
        )
    
    data_D2O = load_json_data('data/plotting_data/D2O_analysis_results_20251127_182353.json')
    
    rate_H2_H2O = data_D2O['plotting_data']['H2 max rate (polyfit)']['data']['False']['mean']
    rate_H2_D2O = data_D2O['plotting_data']['H2 max rate (polyfit)']['data']['True']['mean']
    rate_O2_H2O = data_D2O['plotting_data']['O2 max rate (polyfit)']['data']['False']['mean']
    rate_O2_D2O = data_D2O['plotting_data']['O2 max rate (polyfit)']['data']['True']['mean']

    KIE_H2 = rate_H2_H2O / rate_H2_D2O
    KIE_O2 = rate_O2_H2O / rate_O2_D2O

    ax[1][1].text(0.5, 0.5, f'KIE(H$_2$) = {KIE_H2:.1f}\nKIE(O$_2$) = {KIE_O2:.1f}', 
                  transform=ax[1][1].transAxes, fontsize=14, ha='center', va='center')

    ax[0][0].text(-0.23, 1.05, 'A',transform=ax[0][0].transAxes,fontsize=22, fontweight='bold')
    ax[0][1].text(-0.23, 1.05, 'B',transform=ax[0][1].transAxes,fontsize=22, fontweight='bold')
    ax[1][0].text(-0.23, 1.05, 'C',transform=ax[1][0].transAxes,fontsize=22, fontweight='bold')
    ax[1][1].text(-0.23, 1.05, 'D',transform=ax[1][1].transAxes,fontsize=22, fontweight='bold')

    fig.savefig('Figures/Kinetic_Results.pdf', dpi = 500)

    plt.show()

if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import pprint as pp

from pyKES.plotting.plotting_tools import plot_analysis_results, load_json_data
from pyKES.plotting.lighten_colors import lighten_color



def main():
    
    fig = plt.figure(figsize=(9, 6))
    gs = GridSpec(2, 4, figure=fig)  # 2 rows, 4 columns for finer control
    
    # Create axes: top row and bottom-left span 2 columns each
    ax = [[None, None], [None, None]]
    ax[0][0] = fig.add_subplot(gs[0, 0:2])  # top-left (spans cols 0-1)
    ax[0][1] = fig.add_subplot(gs[0, 2:4])  # top-right (spans cols 2-3)
    ax[1][0] = fig.add_subplot(gs[1, 0:2])  # bottom-left (spans cols 0-1)
    
    # Two smaller subplots in place of ax[1][1]
    ax_d1 = fig.add_subplot(gs[1, 2])  # bottom-right left half
    ax_d2 = fig.add_subplot(gs[1, 3])  # bottom-right right half
    
    fig.tight_layout(pad=3.0)
    fig.subplots_adjust(right=0.98, bottom = 0.1, top = 0.94)

    y_axis_label = 'Max. rate / μmol·L$^{-1}$·s$^{-1}$'
    data_labels = {'H2 max rate (polyfit)': 'H$_2$',
                   'O2 max rate (polyfit)': 'O$_2$'}
    
    data_labels_gas_phase = {'H2 max rate (polyfit, gas phase)': 'H$_2$',
                   'O2 max rate (polyfit, gas phase)': 'O$_2$'}
    
    viridis = plt.cm.viridis
    colors = [viridis(i) for i in np.linspace(0, 0.75, 4)]

    # Create color dictionaries for each plot
    # Each plot uses one color from 'colors', with H2 as a lighter hue
    colors_dict_0 = {
        'O2 max rate (polyfit)': colors[0],
        'H2 max rate (polyfit)': lighten_color(colors[0], amount=0.6)
    }
    colors_dict_1 = {
        'O2 max rate (polyfit)': colors[1],
        'H2 max rate (polyfit)': lighten_color(colors[1], amount=0.6)
    }
    colors_dict_2 = {
        'O2 max rate (polyfit)': colors[2],
        'H2 max rate (polyfit)': lighten_color(colors[2], amount=0.6)
    }
    colors_dict_3 = {
        'O2 max rate (polyfit)': colors[3],
        'H2 max rate (polyfit)': lighten_color(colors[3], amount=0.6)
    }

    colors_dict_3_gas_phase = {
        'O2 max rate (polyfit, gas phase)': colors[3],
        'H2 max rate (polyfit, gas phase)': lighten_color(colors[3], amount=0.6)
    }

    markers_dict = {
        'O2 max rate (polyfit)': 'o',
        'H2 max rate (polyfit)': 'D',
        'O2 max rate (polyfit, gas phase)': 'o',
        'H2 max rate (polyfit, gas phase)': 'D'
    }

    marker_size_dict = {
        'O2 max rate (polyfit)': 8,
        'H2 max rate (polyfit)': 6,
        'O2 max rate (polyfit, gas phase)': 8,
        'H2 max rate (polyfit, gas phase)': 6
    }

    plot_analysis_results(
        'data/plotting_data/Irra_analysis_results_20251127_182340.json',
        ax = ax[0][0],
        linestyles= "-",
        marker = markers_dict,
        markersize = marker_size_dict,
        xlabel = 'Irradiance / mW·cm$^{-2}$',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_0,
        )
    
    plot_analysis_results(
        'data/plotting_data/Temp_analysis_results_20251127_182426.json',
        ax = ax[0][1],
        linestyles= "-",
        marker = markers_dict,
        markersize = marker_size_dict,
        xlabel = 'Temperature / °C',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_1,
        )
    
    plot_analysis_results(
        'data/plotting_data/Cata_analysis_results_20251127_182412.json',
        ax = ax[1][0],
        linestyles= "-",
        marker = markers_dict,
        markersize = marker_size_dict,
        xlabel = 'Co-catalyst loading / wt. fraction Rh/Cr',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_2,
        )
        
        
    plot_analysis_results(
        'data/plotting_data/D2O_analysis_results_20251127_182353.json',
        ax = ax_d1,  # Use the first of the two smaller subplots
        marker = markers_dict,
        markersize = marker_size_dict,
        xlabel = 'D$_2$O',
        ylabel = y_axis_label,
        result_labels = data_labels,
        colors = colors_dict_3,
        )
    
    plot_analysis_results(
        'data/plotting_data/D2O_analysis_results_20251204_125649.json',
        ax = ax_d2,  # Use the first of the two smaller subplots
        marker = markers_dict,
        markersize = marker_size_dict,
        xlabel = 'D$_2$O',
        ylabel = y_axis_label,
        result_labels = data_labels_gas_phase,
        colors = colors_dict_3_gas_phase,
        )


    # Adjust x-axis limits to center the data points
    xlim = ax_d1.get_xlim()
    x_range = xlim[1] - xlim[0]
    ax_d1.set_xlim(xlim[0] - 0.1 * x_range, xlim[1] + 0.1 * x_range)
    ax_d1.set_title('Liquid phase', fontweight='bold')

    ax_d2.set_xlim(xlim[0] - 0.1 * x_range, xlim[1] + 0.1 * x_range)
    ax_d2.set_title('Gas phase', fontweight='bold')
    
    data_D2O = load_json_data('data/plotting_data/D2O_analysis_results_20251127_182353.json')
    
    rate_H2_H2O = data_D2O['plotting_data']['H2 max rate (polyfit)']['data']['False']['mean']
    rate_H2_D2O = data_D2O['plotting_data']['H2 max rate (polyfit)']['data']['True']['mean']
    rate_O2_H2O = data_D2O['plotting_data']['O2 max rate (polyfit)']['data']['False']['mean']
    rate_O2_D2O = data_D2O['plotting_data']['O2 max rate (polyfit)']['data']['True']['mean']

    KIE_H2 = rate_H2_H2O / rate_H2_D2O
    KIE_O2 = rate_O2_H2O / rate_O2_D2O

    ax_d1.text(0.5, 0.4, f'KIE(H$_2$) =\n{KIE_H2:.1f}\nKIE(O$_2$) =\n{KIE_O2:.1f}', 
                  transform=ax_d1.transAxes, fontsize=12, ha='center', va='center')
    

    data_D2O_gas = load_json_data('data/plotting_data/D2O_analysis_results_20251204_125649.json')

    rate_H2_H2O_gas = data_D2O_gas['plotting_data']['H2 max rate (polyfit, gas phase)']['data']['False']['mean']
    rate_H2_D2O_gas = data_D2O_gas['plotting_data']['H2 max rate (polyfit, gas phase)']['data']['True']['mean']
    rate_O2_H2O_gas = data_D2O_gas['plotting_data']['O2 max rate (polyfit, gas phase)']['data']['False']['mean']
    rate_O2_D2O_gas = data_D2O_gas['plotting_data']['O2 max rate (polyfit, gas phase)']['data']['True']['mean']

    KIE_H2_gas = rate_H2_H2O_gas / rate_H2_D2O_gas
    KIE_O2_gas = rate_O2_H2O_gas / rate_O2_D2O_gas

    ax_d2.text(0.5, 0.4, f'KIE(H$_2$) =\n{KIE_H2_gas:.1f}\nKIE(O$_2$) =\n{KIE_O2_gas:.1f}',
                transform=ax_d2.transAxes, fontsize=12, ha='center', va='center')
               


    ax[0][0].text(-0.23, 1.05, 'A',transform=ax[0][0].transAxes,fontsize=18, fontweight='bold')
    ax[0][1].text(-0.23, 1.05, 'B',transform=ax[0][1].transAxes,fontsize=18, fontweight='bold')
    ax[1][0].text(-0.23, 1.05, 'C',transform=ax[1][0].transAxes,fontsize=18, fontweight='bold')
    ax_d1.text(-0.63, 1.05, 'D',transform=ax_d1.transAxes,fontsize=18, fontweight='bold')
    ax_d2.text(-0.63, 1.05, 'E',transform=ax_d2.transAxes,fontsize=18, fontweight='bold')

    fig.savefig('Figures/Kinetic_Results.pdf', dpi = 500)

    plt.show()

if __name__ == "__main__":
    main()
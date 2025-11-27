import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import rcParams
from matplotlib.lines import Line2D

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 12
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Arial'
rcParams['mathtext.it'] = 'Arial:italic'
rcParams['mathtext.bf'] = 'Arial:bold'

from pyKES.database.database_experiments import ExperimentalDataset
from pyKES.utilities.resolve_attributes import resolve_experiment_attributes

from simultaneous_detection.data_parsing.processing_parameters import GROUP_MAPPING, PLOTTING_INSTRUCTIONS


def plot_experiment_group(
    dataset: ExperimentalDataset,
    experiment_group: str,
    figure_title: str,
    plotting_instructions: dict,
    plotting_styles: dict = None,
    viridis_range: tuple = (0.2, 0.8),
    subplot_title_format: str = "{value}",
    xlabel: str = "Time / s",
    ylabel: str = "Concentration / μmol·L$^{-1}$",
    xlim: tuple = None,
    ylim: tuple = None,
    figsize_per_row: tuple = (8, 3),
    subplots_adjustments: dict = None,
    legend_location: tuple = (0.5, 0.95),
    save_figure: bool = False,
    save_path: str = None,
) -> tuple:
    """
    Generate a matplotlib figure with subplots for each unique condition value
    within an experiment group.

    Parameters
    ----------
    dataset : ExperimentalDataset
        The experimental dataset loaded from HDF5.
    experiment_group : str
        The name of the experiment group (e.g., 'Intensity', 'Loading').
        Must be a key in GROUP_MAPPING.
    figure_title : str
        Title for the entire figure.
    plotting_instructions : dict
        Dictionary mapping data labels to x/y paths. Each key should be a label
        (e.g., 'Reaction (H2)', 'Reaction (O2)') and the value should be a dict
        with 'x' and 'y' keys pointing to data paths in the experiment.
        Example: {'Reaction (H2)': {'x': 'processed_data/H2_time_reaction',
                                    'y': 'processed_data/H2_data_reaction'}}
    plotting_styles : dict, optional
        Dictionary mapping data labels to matplotlib line style kwargs.
        Example: {'Reaction (H2)': {'linestyle': '--', 'linewidth': 1.5},
                  'Reaction (O2)': {'linestyle': '-', 'linewidth': 1.5}}
        If not provided, H2 data uses dashed lines and O2 uses solid lines.
    viridis_range : tuple, optional
        Range of the Viridis colormap to use (min, max), default (0.2, 0.8).
    subplot_title_format : str, optional
        Format string for subplot titles. Use {value} as placeholder for the
        condition value. Example: "{value} mW/cm²" or "Irradiance: {value} mW/cm²"
    xlabel : str, optional
        Label for x-axis, default "Time / s".
    ylabel : str, optional
        Label for y-axis, default "Concentration / μmol·L$^{-1}$".
    xlim : tuple, optional
        Tuple of (xmin, xmax) to set x-axis limits for all subplots.
        If None, limits are determined automatically.
    ylim : tuple, optional
        Tuple of (ymin, ymax) to set y-axis limits for all subplots.
        If None, limits are determined automatically.
    figsize_per_row : tuple, optional
        Figure size (width, height) per row of subplots, default (8, 3).
    save_figure : bool, optional
        Whether to save the figure to file, default False.
    save_path : str, optional
        Path to save the figure. Required if save_figure is True.

    Returns
    -------
    tuple
        (fig, axes) - The matplotlib figure and axes array.
    """
    # Validate experiment group
    if experiment_group not in GROUP_MAPPING:
        raise ValueError(f"Unknown experiment group: {experiment_group}. "
                         f"Must be one of {list(GROUP_MAPPING.keys())}")
    
    group_metadata_path = GROUP_MAPPING[experiment_group]
    
    # Default plotting styles: H2 dashed, O2 solid
    if plotting_styles is None:
        plotting_styles = {}
        for label in plotting_instructions.keys():
            if 'H2' in label:
                plotting_styles[label] = {'linestyle': '--', 'linewidth': 1.5}
            elif 'O2' in label:
                plotting_styles[label] = {'linestyle': '-', 'linewidth': 1.5}
            else:
                plotting_styles[label] = {'linestyle': '-', 'linewidth': 1.5}
    
    # Filter experiments by group and Active status
    active_experiments = []
    for exp_name, experiment in dataset.experiments.items():

        group = experiment.metadata['group']
        active = experiment.metadata['Active']

        if group == experiment_group and str(active).upper() == 'TRUE':
            active_experiments.append(experiment)  
    
    # Get unique condition values
    if group_metadata_path is None:
        # For 'Reference' group, all experiments go in one subplot
        unique_values = [None]
        experiments_by_value = {None: active_experiments}

    else:
        metadata_dict = {'Value': group_metadata_path}

        experiments_by_value = {}

        for exp in active_experiments:
            value_dict = resolve_experiment_attributes(metadata_dict, exp)
            value = value_dict['Value']

            if value not in experiments_by_value:
                experiments_by_value[value] = []

            experiments_by_value[value].append(exp)
        
        # Sort unique values
        unique_values = sorted(experiments_by_value.keys(), 
                               key=lambda x: float(x) if isinstance(x, (int, float)) or 
                                   (isinstance(x, str) and x.replace('.', '').replace('-', '').isdigit()) 
                                   else str(x))
    
    # Calculate subplot layout (2 columns, unless only 1 subplot)
    n_subplots = len(unique_values)
    if n_subplots == 1:
        n_cols = 1
        n_rows = 1
    else:
        n_cols = 2
        n_rows = int(np.ceil(n_subplots / n_cols))
    
    # Create figure with dynamic size
    fig_width = figsize_per_row[0]
    fig_height = figsize_per_row[1] * n_rows
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(fig_width, fig_height))
    
    # Ensure axes is always 2D array for consistent indexing
    if n_subplots == 1:
        axes = np.array([[axes]])
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    elif n_cols == 1:
        axes = axes.reshape(-1, 1)
    
    # Flatten axes for easy iteration
    axes_flat = axes.flatten()
    
    # Set up Viridis colormap
    viridis = plt.get_cmap('viridis')
    
    # Plot each subplot
    for idx, value in enumerate(unique_values):
        ax = axes_flat[idx]
        experiments = experiments_by_value[value]
        n_experiments = len(experiments)
        
        # Generate colors from Viridis range
        if n_experiments == 1:
            color_positions = [np.mean(viridis_range)]
        else:
            color_positions = np.linspace(viridis_range[0], viridis_range[1], n_experiments)
        
        # Plot each experiment
        for exp_idx, experiment in enumerate(experiments):
            color = viridis(color_positions[exp_idx])
            
            # Resolve plotting data for this experiment
            plotting_data = resolve_experiment_attributes(plotting_instructions, experiment)
            
            # Plot each data series with the same color
            for label, data in plotting_data.items():

                style = plotting_styles.get(label, {})
                ax.plot(
                    data['x'], data['y'],
                    color=color,
                    label=None,  # No legend entries for individual experiments
                    **style
                )
        
        # Set subplot title
        if value is not None:
            title = subplot_title_format.format(value=value)
        else:
            title = experiment_group
        ax.set_title(title)
        
        # Set axis labels
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # Set axis limits if provided
        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)
    
    # Hide unused subplots
    for idx in range(n_subplots, len(axes_flat)):
        axes_flat[idx].set_visible(False)
    
    # Create custom legend with line styles
    legend_handles = []
    for label in plotting_instructions.keys():
        style = plotting_styles.get(label, {})
        # Use a neutral color for legend
        handle = Line2D([0], [0], color='gray', label=label, **style)
        legend_handles.append(handle)
    
    # Add legend to figure (outside subplots)
    fig.legend(handles=legend_handles, loc='upper center', 
               bbox_to_anchor=legend_location, ncol=len(legend_handles),
               frameon=True, framealpha=0.95)
    
    # Adjust layout first, then add title
    fig.tight_layout()
    
    # Make room at top for title and legend, then add title
    if subplots_adjustments:
        fig.subplots_adjust(**subplots_adjustments)

    fig.suptitle(figure_title, fontsize=14, fontweight='bold')

    
    # Save figure if requested
    if save_figure:
        if save_path is None:
            raise ValueError("save_path must be provided when save_figure is True")
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to: {save_path}")
    
    return fig, axes


def main():
    # Example usage
    dataset = ExperimentalDataset.load_from_hdf5('data/251129_processed_O2_H2_data.h5')
    
    # Define which data series to plot
    plotting_instructions = {
        'Reaction (H$_2$)': PLOTTING_INSTRUCTIONS['time_series_instructions']['Reaction (H2)'],
        'Reaction (O$_2$)': PLOTTING_INSTRUCTIONS['time_series_instructions']['Reaction (O2)'],
    }
    
    # Define custom styles
    plotting_styles = {
        'Reaction (H$_2$)': {'linestyle': '--', 'linewidth': 1.5},
        'Reaction (O$_2$)': {'linestyle': '-', 'linewidth': 1.5},
    }
    
    fig, axes = plot_experiment_group(
        dataset=dataset,
        experiment_group='Intensity',
        figure_title='H$_2$ and O$_2$ Evolution by Irradiance',
        plotting_instructions=plotting_instructions,
        plotting_styles=plotting_styles,
        viridis_range=(0.2, 0.8),
        subplot_title_format="{value} mW/cm$^2$",
        xlabel="Time / s",
        ylim = (-10, 140),
        ylabel=r"Concentration / $\mu$mol$\cdot$L$^{-1}$",
        save_figure=False,
        save_path=None,
    )

    fig, axes = plot_experiment_group(
        dataset=dataset,
        experiment_group='Loading',
        figure_title='H$_2$ and O$_2$ Evolution by co-catalys loading',
        plotting_instructions=plotting_instructions,
        plotting_styles=plotting_styles,
        viridis_range=(0.2, 0.8),
        subplot_title_format="{value} Loading",
        xlabel="Time / s",
        ylabel=r"Concentration / $\mu$mol$\cdot$L$^{-1}$",
        save_figure=False,
        save_path=None,
    )

    fig, axes = plot_experiment_group(
        dataset=dataset,
        experiment_group='Temperature',
        figure_title='H$_2$ and O$_2$ Evolution by temperature',
        plotting_instructions=plotting_instructions,
        plotting_styles=plotting_styles,
        viridis_range=(0.2, 0.8),
        subplot_title_format="{value} Temp (°C)",
        xlabel="Time / s",
        ylabel=r"Concentration / $\mu$mol$\cdot$L$^{-1}$",
        subplots_adjustments={'top': 0.6},
        legend_location=(0.5, 0.9),
        figsize_per_row= (8, 4),
        save_figure=False,
        save_path=None,
    )
    
    fig, axes = plot_experiment_group(
        dataset=dataset,
        experiment_group='Reference',
        figure_title='H$_2$ and O$_2$ Evolution by Reference',
        plotting_instructions=plotting_instructions,
        plotting_styles=plotting_styles,
        viridis_range=(0.2, 0.8),
        subplot_title_format="{value} Reference",
        xlabel="Time / s",
        ylabel=r"Concentration / $\mu$mol$\cdot$L$^{-1}$",
        subplots_adjustments={'top': 0.6},
        legend_location=(0.5, 0.9),
        figsize_per_row= (8, 4),
        save_figure=False,
        save_path=None,
    )

    fig, axes = plot_experiment_group(
        dataset=dataset,
        experiment_group='D2O',
        figure_title='H$_2$ and O$_2$ Evolution by D2O',
        plotting_instructions=plotting_instructions,
        plotting_styles=plotting_styles,
        viridis_range=(0.2, 0.8),
        subplot_title_format="{value} D2O",
        xlabel="Time / s",
        ylabel=r"Concentration / $\mu$mol$\cdot$L$^{-1}$",
        subplots_adjustments={'top': 0.6},
        legend_location=(0.5, 0.9),
        figsize_per_row= (8, 4),
        save_figure=False,
        save_path=None,
    )

    plt.show()


    
if __name__ == "__main__":
    main()

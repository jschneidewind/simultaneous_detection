import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from pyKES.plotting.plotting_tools import load_json_data

# Physical constants
R = 8.314  # J/(mol·K) - Universal gas constant


def arrhenius_analysis(temperatures_celsius: np.ndarray, rates: np.ndarray, rate_errors: np.ndarray = None):
    """
    Perform Arrhenius analysis to determine activation energy.
    
    The Arrhenius equation: k = A * exp(-Ea / RT)
    Linearized form: ln(k) = ln(A) - Ea/(R*T)
    
    Parameters:
    -----------
    temperatures_celsius : array-like
        Temperatures in Celsius
    rates : array-like
        Reaction rates at each temperature
    rate_errors : array-like, optional
        Standard deviation of rates at each temperature
    
    Returns:
    --------
    dict with activation energy, pre-exponential factor, and fit statistics
    """
    # Convert temperatures to Kelvin
    temperatures_K = temperatures_celsius + 273.15
    
    # Calculate 1/T (in 1/K)
    inv_T = 1.0 / temperatures_K
    
    # Calculate ln(k)
    ln_k = np.log(rates)
    
    # Perform linear regression: ln(k) = ln(A) - Ea/(R*T)
    # slope = -Ea/R, intercept = ln(A)
    slope, intercept, r_value, p_value, std_err = stats.linregress(inv_T, ln_k)
    
    # Calculate activation energy
    Ea_J_mol = -slope * R  # J/mol
    Ea_kJ_mol = Ea_J_mol / 1000  # kJ/mol
    
    # Calculate pre-exponential factor
    A = np.exp(intercept)
    
    # Calculate error in Ea from standard error of slope
    Ea_error_kJ_mol = std_err * R / 1000
    
    return {
        'Ea_kJ_mol': Ea_kJ_mol,
        'Ea_error_kJ_mol': Ea_error_kJ_mol,
        'A': A,
        'ln_A': intercept,
        'slope': slope,
        'r_squared': r_value**2,
        'p_value': p_value,
        'inv_T': inv_T,
        'ln_k': ln_k,
        'temperatures_K': temperatures_K
    }


def plot_arrhenius(result: dict, title: str = "Arrhenius Plot", ax=None, color='blue', label='Data'):
    """Create an Arrhenius plot with the linear fit."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = ax.get_figure()
    
    inv_T = result['inv_T']
    ln_k = result['ln_k']
    
    # Plot data points
    ax.scatter(inv_T * 1000, ln_k, s=100, c=color, zorder=5, label=label)
    
    # Plot linear fit
    inv_T_fit = np.linspace(inv_T.min() * 0.995, inv_T.max() * 1.005, 100)
    ln_k_fit = result['ln_A'] + result['slope'] * inv_T_fit
    ax.plot(inv_T_fit * 1000, ln_k_fit, color=color, linestyle='-', linewidth=2)
    
    # Labels and formatting
    ax.set_xlabel('1000/T (K$^{-1}$)', fontsize=12)
    ax.set_ylabel('ln(k)', fontsize=12)
    ax.set_title(title, fontsize=14)
    
    ax.grid(True, alpha=0.3)
    
    return fig, ax


def extract_rate_data(data: dict, rate_key: str):
    """Extract temperature and rate data from the JSON structure."""
    rate_data = data['plotting_data'][rate_key]['data']
    
    temperatures = []
    mean_rates = []
    std_rates = []
    
    for temp_str, values in rate_data.items():
        temperatures.append(float(temp_str))
        mean_rates.append(values['mean'])
        std_rates.append(values['std'])
    
    # Convert to numpy arrays and sort by temperature
    temperatures = np.array(temperatures)
    mean_rates = np.array(mean_rates)
    std_rates = np.array(std_rates)
    
    sort_idx = np.argsort(temperatures)
    return temperatures[sort_idx], mean_rates[sort_idx], std_rates[sort_idx]


def print_analysis_results(name: str, temperatures: np.ndarray, rates: np.ndarray, 
                           std_rates: np.ndarray, result: dict):
    """Print formatted analysis results."""
    print(f"\n{'=' * 60}")
    print(f"ARRHENIUS ANALYSIS - {name}")
    print("=" * 60)
    print("\nInput Data:")
    print(f"{'Temperature (°C)':<20} {'Rate (µmol/L/s)':<20} {'Std Dev':<15}")
    print("-" * 55)
    for t, r, s in zip(temperatures, rates, std_rates):
        print(f"{t:<20.1f} {r:<20.5f} {s:<15.5f}")
    
    print(f"\nResults:")
    print(f"  Activation Energy (Ea): {result['Ea_kJ_mol']:.2f} ± {result['Ea_error_kJ_mol']:.2f} kJ/mol")
    print(f"  Pre-exponential factor (A): {result['A']:.4e}")
    print(f"  ln(A): {result['ln_A']:.2f}")
    print(f"\n  Fit Statistics:")
    print(f"    R² = {result['r_squared']:.4f}")
    print(f"    p-value = {result['p_value']:.2e}")
    print(f"    Slope = {result['slope']:.2f} K")


def main():
    data = load_json_data('data/plotting_data/Temp_analysis_results_20251127_182426.json')
    
    # Extract H2 and O2 data
    h2_temps, h2_rates, h2_std = extract_rate_data(data, 'H2 max rate (polyfit)')
    o2_temps, o2_rates, o2_std = extract_rate_data(data, 'O2 max rate (polyfit)')
    
    # Perform Arrhenius analysis for both
    h2_result = arrhenius_analysis(h2_temps, h2_rates, h2_std)
    o2_result = arrhenius_analysis(o2_temps, o2_rates, o2_std)
    
    # Print results
    print_analysis_results("H2 Maximum Reaction Rate", h2_temps, h2_rates, h2_std, h2_result)
    print_analysis_results("O2 Maximum Reaction Rate", o2_temps, o2_rates, o2_std, o2_result)
    
    # Summary comparison
    print("\n" + "=" * 60)
    print("SUMMARY COMPARISON")
    print("=" * 60)
    print(f"\n{'Species':<10} {'Ea (kJ/mol)':<20} {'R²':<10}")
    print("-" * 40)
    print(f"{'H2':<10} {h2_result['Ea_kJ_mol']:.2f} ± {h2_result['Ea_error_kJ_mol']:.2f}    {h2_result['r_squared']:.4f}")
    print(f"{'O2':<10} {o2_result['Ea_kJ_mol']:.2f} ± {o2_result['Ea_error_kJ_mol']:.2f}    {o2_result['r_squared']:.4f}")
    
    # Create combined Arrhenius plot
    fig, ax = plt.subplots(figsize=(10, 7))
    
    plot_arrhenius(h2_result, ax=ax, color='blue', label='H$_2$')
    plot_arrhenius(o2_result, ax=ax, color='red', label='O$_2$')
    
    ax.set_title("Arrhenius Analysis - H$_2$ and O$_2$ Production Rates", fontsize=14)
    
    # Add annotation with results for both
    textstr = '\n'.join([
        'H$_2$:',
        f"  $E_a$ = {h2_result['Ea_kJ_mol']:.2f} ± {h2_result['Ea_error_kJ_mol']:.2f} kJ/mol",
        f"  $R^2$ = {h2_result['r_squared']:.4f}",
        '',
        'O$_2$:',
        f"  $E_a$ = {o2_result['Ea_kJ_mol']:.2f} ± {o2_result['Ea_error_kJ_mol']:.2f} kJ/mol",
        f"  $R^2$ = {o2_result['r_squared']:.4f}"
    ])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.75, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
    
    ax.legend(loc='lower left')
    plt.tight_layout()
    
    # Save figure
    fig.savefig('figures/arrhenius_plot.png', dpi=300, bbox_inches='tight')
    fig.savefig('figures/arrhenius_plot.pdf', bbox_inches='tight')
    print(f"\nPlots saved to figures/arrhenius_plot.png and figures/arrhenius_plot.pdf")
    
    plt.show()


if __name__ == "__main__":
    main()
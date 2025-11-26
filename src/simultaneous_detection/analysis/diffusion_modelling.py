import numpy as np
import matplotlib.pyplot as plt

from pyKES.reaction_ODE import parse_reactions, solve_ode_system, plot_solution

def main():

    reactions = [
        '[H2O] > [O2-aq], k1',
        '[O2-aq] > [O2-g], k2',
        '[H2O] > [H2-aq], k1 ; factor1',
        '[H2-aq] > [H2-g], k2 ; factor2',
    ]

    rate_constants = {'k1': 1.0E-11, 
                      'k2': 1.0E-2}

    other_multipliers = {
        'factor1': 2.0,
        'factor2': 1.68,
    }   

    initial_conditions = {
        '[H2O]': 55.5 * 1e6,  # in umol/L
    }

    times = np.linspace(0, 12000, 10000)

    parsed_reactions, species = parse_reactions(reactions)

    solution = solve_ode_system(parsed_reactions, species, rate_constants, 
                                initial_conditions, times, other_multipliers)
    

    # print(species)

    ratio_gas_phase = solution[:, species.index('[H2-g]')][1:] / solution[:, species.index('[O2-g]')][1:]
    ratio_liquid_phase = solution[:, species.index('[H2-aq]')][1:] / solution[:, species.index('[O2-aq]')][1:]

    max_liquid_phase_rate_H2 = np.max(np.diff(solution[:, species.index('[H2-aq]')][20:]) / np.diff(times[20:]))
    max_liquid_phase_rate_O2 = np.max(np.diff(solution[:, species.index('[O2-aq]')][20:]) / np.diff(times[20:]))

    print("Max liquid phase rate H2 (umol/L/s):", max_liquid_phase_rate_H2)
    print("Max liquid phase rate O2 (umol/L/s):", max_liquid_phase_rate_O2)
    print("Ratio of max rates (H2/O2):", max_liquid_phase_rate_H2 / max_liquid_phase_rate_O2)


    # Plot results

    fig, ax = plt.subplots(figsize=(10, 6))

    plot_solution(species, times, solution, ax = ax, exclude_species=['[H2O]'])

    ax.plot(times[1:], ratio_gas_phase, label='[H2-g]/[O2-g]', linestyle='--', color='black')
    ax.plot(times[1:], ratio_liquid_phase, label='[H2-aq]/[O2-aq]', linestyle=':', color='gray')

    ax.legend()

    plt.show()


    

if __name__ == "__main__":
    main()
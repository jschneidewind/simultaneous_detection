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

    rate_constants = {'k1': 1.0E-9, 
                      'k2': 1.0E-4}

    other_multipliers = {
        'factor1': 2.0,
        'factor2': 1.68,
    }   

    initial_conditions = {
        '[H2O]': 55.5 * 1e6,  # in umol/L
    }

    times = np.linspace(0, 900, 10000)

    parsed_reactions, species = parse_reactions(reactions)

    solution = solve_ode_system(parsed_reactions, species, rate_constants, 
                                initial_conditions, times, other_multipliers)
    

    # print(species)

    # ratio_gas_phase = solution[:, species.index('[H2-g]')] / solution[:, species.index('[O2-g]')]
    # ratio_liquid_phase = solution[:, species.index('[H2-aq]')] / solution[:, species.index('[O2-aq]')]


    # Plot results

    fig, ax = plt.subplots(figsize=(10, 6))

    plot_solution(species, times, solution, ax = ax, exclude_species=['[H2O]'])

    # ax.plot(times, ratio_gas_phase, label='[H2-g]/[O2-g]', linestyle='--', color='black')
    # ax.plot(times, ratio_liquid_phase, label='[H2-aq]/[O2-aq]', linestyle=':', color='gray')

    ax.legend()

    plt.show()


    

if __name__ == "__main__":
    main()
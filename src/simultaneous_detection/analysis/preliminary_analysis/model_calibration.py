import numpy as np
import matplotlib.pyplot as plt

from pyKES.reaction_ODE import parse_reactions, solve_ode_system, plot_solution

def main():

    reactions = ['[H2O] > [O2-int], k1',
                '[O2-int] > [O2-aq], k2',
                '[O2-aq] > [O2-g], k3',
                '[H2O] > [H2-int], k4',
                '[H2-int] > [H2-aq], k5',
                '[H2-aq] > [H2-g], k6']

    rate_constants = {'k1': 1.0E-7, 
                      'k2': 1.0E-3,
                      'k3': 1.0E-1,
                      'k4': 1.0E-7,
                      'k5': 1.0E-3,
                      'k6': 1.0E-1,}
 
    initial_conditions = {
        '[H2O]': 55.5 * 1e6,  # in umol/L
    }

    times = np.linspace(0, 1200, 10000)

    parsed_reactions, species = parse_reactions(reactions)

    solution = solve_ode_system(parsed_reactions, species, rate_constants, 
                                initial_conditions, times)
    

    # print(species)

    # ratio_gas_phase = solution[:, species.index('[H2-g]')] / solution[:, species.index('[O2-g]')]
    # ratio_liquid_phase = solution[:, species.index('[H2-aq]')] / solution[:, species.index('[O2-aq]')]


    # Plot results

    fig, ax = plt.subplots(figsize=(10, 6))

    plot_solution(species, times, solution, ax = ax, exclude_species=['[H2O]', '[O2-int]', '[H2-int]', '[O2-g]', '[H2-g]'])

    # ax.plot(times, ratio_gas_phase, label='[H2-g]/[O2-g]', linestyle='--', color='black')
    # ax.plot(times, ratio_liquid_phase, label='[H2-aq]/[O2-aq]', linestyle=':', color='gray')

    ax.legend()

    plt.show()


    

if __name__ == "__main__":
    main()




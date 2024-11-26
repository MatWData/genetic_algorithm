# This script uses Optuna to find the best parametes for my genetic algorithm scipt.
# It takes ~12 minutes to run which may be seen as pointless as genetic algorithms are designed to be better and more efficient than the brute-force alternative
# After running it has returned the best parametes in best_params.json for viewing.
# Occured to me during the trials that some of the results acquired by this scipt can be seen as a 'red-herring' because of genetic algorithms natural flaw of finding NEAR optimal solutions as well as THE optimal solution.

import optuna
import json
from genetic_algorithm import genetic_algorithm

def objective(trial):
    # Define the range of each hyperparameter that Optuna will optimise
    selection_method = trial.suggest_categorical("selection_method", ['roulette', 'rank', 'tournament'])
    population_size = trial.suggest_int("population_size", 20, 200)
    num_generations = trial.suggest_int("num_generations", 100, 2000)
    crossover_rate = trial.suggest_float("crossover_rate", 0.5, 0.9, log=True)
    mutation_rate = trial.suggest_float("mutation_rate", 0.05, 0.5, log=True)

    # Run genetic algorithm with the suggested parameters
    best_solution, best_score, _ = genetic_algorithm(
        selection_method=selection_method,
        population_size=population_size,
        num_generations=num_generations,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate
    )

    # Return the best score for the trial
    return best_score 

if __name__ == '__main__':
    pruner = optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=10, interval_steps=5)
    study = optuna.create_study(
        direction='maximize', 
        #sampler=optuna.samplers.TPESampler(),
        pruner=pruner
    )

    study.optimize(objective, n_trials=25)

    # Display best parameters and scores found by Optuna
    print(f"Best Parameters: {study.best_params}")
    print(f"Best Score: {study.best_value}")

    # Save those best params into a json
    # This takes ~12 minutes to run - so this is nice to have but pretty pointless if we're trying to beat brute-force algorithms 
    with open('best_params.json', 'w') as file:
        json.dump(study.best_params, file)

    # Retrieve and display the best solution using optimised parameters
    best_solution, best_score, population, _ = genetic_algorithm(
        selection_method=study.best_params['selection_method'],
        population_size=study.best_params['population_size'],
        num_generations=study.best_params['num_generations'],
        crossover_rate=study.best_params['crossover_rate'],
        mutation_rate=study.best_params['mutation_rate']
    )

    print(f'Best Solution Found: {best_solution}')
    print(f'Best Score Found: {best_score}')



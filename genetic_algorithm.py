import random
from performance_matrix import PERFORMANCE_MATRIX
from utility_functions import (
    fitness_function,
    ordered_crossover,
    mutation,
    parent_selection,
    init_population
)

def genetic_algorithm(
        selection_method: str = "roulette",
        performance_matrix: list[list[int]] = PERFORMANCE_MATRIX,
        population_size: int = 20,
        num_generations: int = 100,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.3
):
    """
    Runs a Genetic Algorithm to find the optimal assignment of employees to tasks based on a performance matrix.

    Args:
        selection_method (str): The method used for parent selection. Valid options are "roulette", "rank", or "tournament". Defaults to "roulette".
        performance_matrix (list[list[int]]): The 2D list representing the performance scores for each employee-task combination. Defaults to PERFORMANCE_MATRIX.
        population_size (int): The number of individuals in the population. Defaults to 20.
        num_generations (int): The number of generations to run the algorithm for. Defaults to 100.
        crossover_rate (float): The probability of performing crossover between two parents. Defaults to 0.8.
        mutation_rate (float): The probability of performing mutation on an offspring. Defaults to 0.3.

    Returns:
        tuple: A tuple containing
            - best_solution (list[int]): The chromosome representing the best assignment found.
            - best_score (int): The fitness score of the best_solution.
            - population (list[list[int]]): The final population of chromosomes.
    """
    # Initialise the population with random chromosomes of size: population_size
    population = init_population(performance_matrix, population_size)
    num_employees = len(performance_matrix)

    generation_scores = []

    for _ in range(num_generations):
        # Sort the population by fitness
        population = sorted(
            population,
            key = lambda x: fitness_function(x, performance_matrix),
            reverse=True
        )

        # Add the generations best fitness to a list for evaluation of progress.
        best_fitness = fitness_function(population[0], performance_matrix)
        generation_scores.append(best_fitness)
        #print(f"Generatiuon {generation} - Best fitness: {best_fitness}")

        # Add the best performing individual chromosome to the next generation (elitism)
        new_population = []
        new_population.append(population[0])

        # Generation new random individuals to fill the population
        while len(new_population) < population_size:

            # Select parents using the preffered selection method.
            parent1 = parent_selection(population, performance_matrix, method=selection_method)
            parent2 = parent_selection(population, performance_matrix, method=selection_method)
            
            # Apply crossover with certain probability
            if random.random() < crossover_rate:
                child = ordered_crossover(parent1, parent2)
            else: 
                # Copy the parent if there is no crossover this time.
                child = parent1.copy()
            
            # Apply mutation with certain probaility
            if random.random() < mutation_rate:
                child = mutation(child, num_employees)
            
            # Add child to the population
            new_population.append(child)
        
        population = new_population
    
    # Find thebest solution in the final population.
    best_solution = max(
        population,
        key = lambda x: fitness_function(x, performance_matrix)
    )
    best_score = fitness_function(best_solution, performance_matrix)

    #print(f"Best Solution: {best_solution}")
    print(f"Best Score: {best_score}")

    return (best_solution, best_score, population, generation_scores)

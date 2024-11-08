import random
from performance_matrix import PERFORMANCE_MATRIX
from genetic_algorithm import (
    fitness_function,
    chromosome_encoder,
    crossover,
    mutation,
    roulette_selection,
    rank_selection,
    tournament_selection
)

def init_population(size: int) -> list[int]:
    return [chromosome_encoder(PERFORMANCE_MATRIX) for _ in range(size)]

def parent_selection(
        population: list[int], 
        performance_matrix, 
        method: str = "roulette"
    ) -> list[int]:
    """
    Finds the best parent by the specified method.

    Args:
        population (list): list of chromosomes.
        performance_matrix (list): 2D list of performance scores.
        method (str): Method of parent selection. Valid inputs are "roulette", "rank", and "tournament".

    Returns:
        list: A parent chromosome.
    """
    if method == 'roulette':
        return roulette_selection(population, performance_matrix)
    if method == 'rank':
        return rank_selection(population, performance_matrix)
    if method == 'tournament':
        return tournament_selection(population, performance_matrix)
    else:
        raise ValueError("Invalid method.")


def genetic_algorithm(
        selection_method: str = "roulette",
        performance_matrix: list[list[int]] = PERFORMANCE_MATRIX,
        population_size: int = 20,
        num_generations: int = 100,
        crossover_rate: float = 0.8,
        crossover_points: int = 1,
        mutation_rate : float = 0.1,
        
):
    population = init_population(population_size)
    num_employees = len(performance_matrix)
    num_tasks = len(performance_matrix[0])

    for generation in range(num_generations):

        population = sorted(
            population,
            key = lambda x: fitness_function(x, performance_matrix),
            reverse=True
        )
        best_fitness = fitness_function(population[0], performance_matrix)
        print(f"Generatiuon {generation} - Best fitness: {best_fitness}")

        new_population = []
        new_population.append(population[0])

        while len(new_population) < population_size:
            parent1 = parent_selection(population, performance_matrix, method=selection_method)
            parent2 = parent_selection(population, performance_matrix, method=selection_method)

            if random.random() < crossover_rate:
                child = crossover(parent1, parent2, points=crossover_points)
            else: 
                child = parent1.copy()
            
            if random.random() < mutation_rate:
                child = mutation(child, num_employees)

            new_population.append(child)
        
        population = new_population
    
    best_solution = max(
        population,
        key = lambda x: fitness_function(x, performance_matrix)
    )
    best_score = fitness_function(best_solution, performance_matrix)

    print(f"Best Solution: {best_solution}")
    print(f"Best Score: {best_score}")

    return best_solution, best_score


if __name__ == '__main__':
    genetic_algorithm()
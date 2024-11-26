from itertools import permutations
from utility_functions import fitness_function

def brute_force_algorithm(performance_matrix: list[list[int]]) -> list:
    """
    Finds the optimal solution using brute force by evaluating all possible task assignments:

    Args:
        performance_matrix (list[list[int]]): 2D List representing performance of each employee on each task.

    Returns:
        tuple: A tuple containing the optimal solution and its fitness score.
    """
    num_employees = len(performance_matrix)
    num_tasks = len(performance_matrix[0])

    all_assignments = permutations(range(1, num_employees+1), num_tasks)
    best_score = float('-inf')

    for assignment in all_assignments:
        # Calculate the fitness score for the current assignment
        score = fitness_function(assignment, performance_matrix)

        # Update the best solution if this one is better
        if score >= best_score:
            best_solution = assignment
            best_score = score

    return list(best_solution), best_score
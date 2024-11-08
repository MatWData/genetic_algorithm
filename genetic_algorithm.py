import random

def fitness_function(assignment :list[int], performance_matrix: list[list[int]]) -> int:
    """
    This function returns the fitness of the indivdual chromosome based on the performance matrix scores. This is used to optimise the algorithm.
    
    Args:
        assignment (list): 1-dimensional list containing which task (index) is performed by which employee (value).
        performance_matrix (list): The 2-dimensional list containing scores for each task-employee combination.

    Returns:
        int: The overall score of all assignments. 
    """
    # Gets the score from the relevent performance_matrix index and sums them together
    fitness = sum(
        performance_matrix[employee][task] for task, employee in enumerate(assignment)
    )
    return fitness


def chromosome_encoder(performance_matrix: list[list[int]]) -> list[int]:
    """
    Generates a random chromosome where each task is addigned to a unique employee.

    Args: 
        performance_matrix (list): The 2-dimensional list containing scores for each task-employee combination. 

    Returns:
        list: A list of length 10, where each index represents a task and the value represents the assigned employee
    """
    # Select 10 random and unique employees out of the 13
    # This list will represent which employees (value) are assigned to which task (index)
    chromosome = random.sample(range(len(performance_matrix)), 10)

    return chromosome

def crossover(parent1: list[int], parent2: list[int], points: int = 1) -> list[int]:
    """
    Returns a child from two parents using either one-point or two-points crossover.

    Args:
        parent1 (list): First parent chromosome.
        parent2 (list): Second parent chromosome.
        points (int, optional): The number of crossover points. Valid values are 1 or 2. Defaults to 1.

    Returns:
        list: A list representing the child chromosome created from the crossover.
    """

    # Check that point value is valid
    if points not in [1,2]:
        raise ValueError("Points argument must be either 1 or 2.")
    
    # Check that parents are same length, avoid potential index out of range errors.
    if len(parent1) != len(parent2):
        raise AttributeError(f"Length of parents are different: parent 1 {len(parent1)}, parent 2: {len(parent2)}")

    if points == 1:
        # One-point crossover
        crossover_point = random.randint(1, len(parent1) - 1) # Avoid 0 or len as the crossover point
        child = parent1[:crossover_point] + parent2[crossover_point:]
    
    if points == 2:
        # Two-point crossover
        # While loop to ensure there is no duplicate int generated
        crossover_point1, crossover_point2 = 0, 0
        while crossover_point1 == crossover_point2:
            crossover_point1 = random.randint(1, len(parent1) - 1)
            crossover_point2 = random.randint(1, len(parent1) - 1)

        # form child with parent2 center
        child = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]

    return child

def mutation(chromosome: list[int], num_employees: int) -> list[int]:
    """
    Makes a small change to one of the values in the list.

    Args:
        chromosome (list[int]): A list of integers representing the tasks (index) and the employees assigned (value).
        num_employees (int): Number of employees in population.   

    Returns: 
        list[int]: The mutated list.
    """
    # Random mutation choice
    mutation_type = random.choice(["swap", "replace"])

    if mutation_type == "swap":
        # Swap Mutation -> Select two random incidies (tasks) and swap the values (employees)

        indx1, indx2 = random.sample(range(len(chromosome)), 2)
        chromosome[indx1], chromosome[indx2] = chromosome[indx2], chromosome[indx1]

    elif mutation_type == "replace":
        # Replace Mutation -> Selects a random index (task) and replaces with an unassigned employee (value)

        # Get random index (employee) to replace
        emp_to_replace = random.randint(0, len(chromosome) - 1)

        # Get a random employee that is NOT currently assigned
        current_employees = set(chromosome)
        all_employees = set(range(num_employees))
        unassigned_employees = list(all_employees - current_employees)

        new_employee = random.choice(unassigned_employees)
        chromosome[emp_to_replace] = new_employee
        
    return chromosome


def roulette_selection(
        population: list, 
        performance_matrix: list[list[int]]
    ) -> list[int]:
    """
    Selects a parent from population using roulette wheel selection.

    Args: 
        population (list): List of chromosomes.
        performance_matrix (list): 2d list of performance scores for tasks.

    Returns:
        list: A parent chromosome
    """

    total_fitness = sum(fitness_function(individual, performance_matrix) for individual in population)

    pick = random.uniform(0, total_fitness)
    current = 0

    for individual in population:
        current += fitness_function(individual, performance_matrix)
        if current >= pick:
            return individual

def rank_selection(
        population: list[int],
        performance_matrix: list[list[int]]
) -> list[int]:
    """
    Selects a parent using rank-based selection.

    Args: 
        population (list): List of chromosomes.
        performance_matrix (list): 2D list of performance scores.

    Returns:
        list: A parent chromosome.
    """
    ranked_population = sorted(
        population, 
        key=lambda ind: fitness_function(ind, performance_matrix),
        reverse=True
    )

    total_ranks = sum(range(1, len(population) +1))
    rank_probability = [
        (len(ranked_population) - rank) / total_ranks for rank in range(len(ranked_population))
    ]

    selected_index = random.choices(
        range(len(ranked_population)), 
        weights=rank_probability, 
        k=1
    )

    return ranked_population[selected_index[0]]

def tournament_selection(
        population: list[int], 
        performance_matrix: list[list[int]], 
        size: int = 3
    ) -> list[int]:
    """
    Selects a parent using tournament-based selection.

    Args: 
        population (list): List of chromosomes.
        performance_matrix (list): 2D list of performance scores.
        size (int, optional): Number of individuals to compete in the tournament. Defaults to 3.

    Returns:
        list: A parent chromosome.
    """
    tournament = random.sample(population, size)

    parent = max(
        tournament,
        key = lambda ind: fitness_function(ind, performance_matrix)         
    )

    return parent

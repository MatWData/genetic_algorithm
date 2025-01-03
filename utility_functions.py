import random

def init_population(performance_matrix: list, size: int) -> list[int]:
    """
    Initialise population of chromosomes of size: size.

    Args:
        performance_matrix (list[list[int]]): 2D list of performance scores for each employee:task pair.
        size (int): Number of chromosomes to be initialised in population.

    Returns:
        list: Population of Chromosomes (list[int]).
    """
    return [chromosome_encoder(performance_matrix) for _ in range(size)]

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
        performance_matrix[employee-1][task] for task, employee in enumerate(assignment)
    )
    return fitness


def chromosome_encoder(performance_matrix: list[list[int]]) -> list[int]:
    """
    Generates a random chromosome where each task is assigned to a unique employee.

    Args: 
        performance_matrix (list): The 2-dimensional list containing scores for each task-employee combination. 

    Returns:
        list: A list of length 10, where each index represents a task and the value represents the assigned employee
    """
    # Select 10 random and unique employees out of the 13 using permutation encoding.
    # This list will represent which employees (value) are assigned to which task (index)
    chromosome = random.sample(range(1, len(performance_matrix)+1), 10)

    return chromosome

def ordered_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    """
    Performs Ordered Crossover on two parents to produce a valid child chromosome.

    Args:
        parent1 (list): First parent chromosome.
        parent2 (list): Second parent chromosome.

    Returns:
        list: A list representing the child chromosome created from the crossover.
    """

    # Initialise the child chromosome
    size = len(parent1)
    child = [None]*size

    # Get the segment to be copied from parent 1 to the child 
    start, end = sorted(random.sample(range(size), 2))
    child[start:end + 1] = parent1[start:end + 1]

    genes_in_child = set(child[start:end + 1])

    # Copy non-duplicate genes from their positions into the child
    for i in range(size):
        if child[i] is None and parent2[i] not in genes_in_child:
            child[i] = parent2[i]
            genes_in_child.add(parent2[i])
    
    # for any remaining None genes, fill from parent2 in order.
    for i in range(size):
        if child[i] is None:
            for gene in parent2:
                if gene not in genes_in_child:
                    child[i] = gene
                    genes_in_child.add(gene)
                    break
        
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
        all_employees = set(range(1, num_employees+1))
        unassigned_employees = list(all_employees - current_employees)

        new_employee = random.choice(unassigned_employees)
        chromosome[emp_to_replace-1] = new_employee
        
    return chromosome


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

    Raises:
        ValueError: When an invalid method is passed. Valid methods are: "roulette", "rank", "tournament".
    """
    # Return the correct method selection, or raise error if method invalid.
    if method == 'roulette':
        return roulette_selection(population, performance_matrix)
    elif method == 'rank':
        return rank_selection(population, performance_matrix)
    elif method == 'tournament':
        return tournament_selection(population, performance_matrix)
    else:
        raise ValueError(f"Invalid method: {method}")


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
    # Calculate fitness of each chromosome in the population
    total_fitness = sum(fitness_function(individual, performance_matrix) for individual in population)

    # Return the first individual which when summed with all preceding indivduals is >= than a randomly generated number between 0, total_fitness
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
    # Sort population by fitness
    ranked_population = sorted(
        population, 
        key=lambda ind: fitness_function(ind, performance_matrix),
        reverse=True
    )

    # Get the probability of choice based on those rankings
    total_ranks = sum(range(1, len(population) +1))
    rank_probability = [
        (len(ranked_population) - rank) / total_ranks for rank in range(len(ranked_population))
    ]

    # Use the probabilities to select one parent.
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
    # Pick a random subset of size {size} and return the best one
    tournament = random.sample(population, size)
    parent = max(
        tournament,
        key = lambda ind: fitness_function(ind, performance_matrix)         
    )

    return parent

from chess import *
from other_tools import *
import random
import numpy as np

"""
Used the logic from this post 
https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6
and the Local Search Power Point.
"""


# create a population with each parent having N chromosomes
def create_population(pop_size, chrom_size):
    population = []
    for i in range(0, pop_size):
        parent = list(random.sample(range(0, chrom_size), chrom_size))
        population.append(parent)

    return population


# calculating the fitness score for all the current parents in the population
def cal_pop_fitness(population):
    fitness = []
    for parent in population:
        fitness.append(count_safe_queens(parent))
    return fitness


# select the N best parents in the mating pool, return then as a list of parents
def select_best(population, fitness, num_parents=1):
    if len(population) < num_parents:
        return None

    parents = []
    temp_fitness = fitness.copy()

    # find N number of best parents, return their indices within the population
    for i in range(num_parents):
        # find current max value
        max_value = max(temp_fitness)
        # find its index in original fitness list and save it
        max_index = temp_fitness.index(max_value)
        parents.append(population[max_index])
        # remove the max value from tmp list to find the next largest fitness score
        temp_fitness[max_index] = -1

    return parents


# Cross over N parents and create N combination of children, and return the children
def cross_over(parents):
    num_parents = len(parents)
    children = []

    for i in range(num_parents):
        child = []
        # Take a subset of each parents and append to make N children
        for offset in range(num_parents):
            split_parent = np.array_split(np.array(parents[(i + offset) % num_parents]), num_parents)
            child += split_parent[offset].tolist()
        children.append(child)

    return children


# Given a mutation probability and a some children
# randomly mutate a chromosome with a random valid chromosome
def mutate(children):
    if random.random() <= MUTATE_CHANCE:
        for i in range(len(children)):
            rand_idx = random.randint(0, len(children[i]) - 1)
            rand_q = random.randint(0, len(children[i]) - 1)
            children[i][rand_idx] = rand_q
    return children

# This function is used to check if the functions created are working properly
def debug_genetic_algorithm():
    num_parents = 2
    new_population = create_population(POPSIZE, TABLESIZE)

    for random_state in new_population:
        print('Random state ' + str(random_state))
        #print_table(random_state)

    fitness = cal_pop_fitness(new_population)
    print('Fitness score of each parent in the population: ' + str(fitness) + '\n')

    parents = select_best(new_population, fitness, num_parents)

    print('The best ' + str(num_parents) + ' parents are: \n')
    for parent in parents:
        print(str(parent) + ' With a fitness score of: ' + str(count_safe_queens(parent)))
        #print_table(parent)

    offspring = cross_over(parents)

    print('The crossover creates offspring ' + str(offspring))
    print('With a fitness score of: ' + str(count_safe_queens(offspring)))
    print_state(offspring)

    original_offspring = offspring.copy()
    offspring = mutate(offspring)
    if original_offspring != offspring:
        print('Child mutated from ' + str(original_offspring) + ' to new child of ' + str(offspring))
        print('The crossover creates child ' + str(offspring))
        print('With a fitness score of: ' + str(count_safe_queens(offspring)))
        print_state(offspring)


def genetic_algorithm():
    new_population = create_population(POPSIZE, TABLESIZE)

    best_result = -1
    best_state = []

    for generation in range(NUM_GENERATIONS):
        # Fancy printing of generation number
        # print(make_ordinal(generation + 1) + ' Generation')

        # Find the fitness for each chromosome in the population
        fitness = cal_pop_fitness(new_population)

        # Select the best parents in the population for mating
        parents = select_best(new_population, fitness, NUM_PARENTS)

        # Generate the crossover
        offspring = cross_over(parents)

        # Adding variation using random mutation
        offspring_mutation = mutate(offspring)

        # The best result in the current population
        curr_state = select_best(new_population, fitness)
        curr_result = count_safe_queens(curr_state[0])
        if best_result < curr_result:
            best_result = curr_result
            best_state = curr_state[0]

        # Creating new population based on the parents and offspring (randomly only add only 1 parent idk why)
        new_population[0:] = [parents[random.randint(0, len(parents)-1)]]
        new_population += offspring_mutation
        # print('Current best result is : ' + str(curr_state[0]) + ' with a score of ' + str(curr_result))

    print("Best solution is state : ", best_state)
    best_state = remove_attacking_queens(best_state)
    print_state(best_state)
    print("Best solution fitness : ", best_result)

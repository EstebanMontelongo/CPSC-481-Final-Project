from chess import *
from other_tools import *
from constants import *
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
def cal_pop_fitness(population, table_size):
    fitness = []
    for parent in population:
        fitness.append(count_safe_queens(parent, table_size))
    return fitness


# select the N best parents in the mating pool, return then as a list of parents
def select_best(population, fitness, num_parents=1):
    if len(population) < num_parents:
        print("The number of parents must be smaller or equal to the population size")
        quit()

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


# Cross over two random parents with random combination
def cross_over(parents, num_offspring):
    children = []

    if len(parents[0]) == 1 or len(parents) == 1:
        children.append(list([0]))
        return children

    for i in range(num_offspring):
        rand_idx1 = np.random.randint(1, len(parents))
        rand_idx2 = np.random.randint(1, len(parents))
        c = np.random.randint(1, len(parents[0]))
        child = parents[rand_idx1][0:c] + parents[rand_idx2][c:]
        children.append(child)

    return children


# Given a mutation probability and a some children
# randomly mutate a chromosome with a random valid chromosome
def mutate(children, mutate_chance):
    if random.random() <= mutate_chance:
        for i in range(len(children)):
            rand_idx = random.randint(0, len(children[i]) - 1)
            rand_q = random.randint(0, len(children[i]) - 1)
            children[i][rand_idx] = rand_q
    return children


def genetic_algorithm():
    new_population = create_population(POPSIZE, TABLESIZE)

    best_result = -1
    best_state = []

    for generation in range(NUM_GENERATIONS):

        # Find the fitness for each chromosome in the population
        fitness = cal_pop_fitness(new_population, TABLESIZE)

        # Select the best parents in the population for mating
        parents = select_best(new_population, fitness, NUM_PARENTS)

        # Generate the crossover
        offspring = cross_over(parents, POPSIZE)

        # Adding variation using random mutation
        offspring_mutation = mutate(offspring, MUTATE_CHANCE)

        # The best result in the current population
        curr_state = select_best(new_population, fitness)
        curr_result = count_safe_queens(curr_state[0], TABLESIZE)
        if best_result < curr_result:
            best_result = curr_result
            best_state = curr_state[0]

        # Fancy printing of generation number
        print(make_ordinal(generation + 1) + ' Generation best result is ' + str(max(fitness)))
        # exit loop if best result is equal to size of board
        if best_result == TABLESIZE:
            break

        # Creating new population based on a random number of surviving parents and their offspring
        number_surviving = np.random.randint(1, len(parents))
        parents_fitness = cal_pop_fitness(parents, TABLESIZE)
        best_parents = select_best(parents, parents_fitness, number_surviving)
        new_population[0:] = best_parents
        new_population += offspring_mutation

    print("Best solution is state : ", best_state)
    best_state = remove_attacking_queens(best_state, TABLESIZE)
    print_state(best_state, TABLESIZE)
    print("Best solution fitness : ", best_result)

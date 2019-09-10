# This is a genetic algorithm to find the best solution to
# find the highest point of f(x) = x^2, 0 <= x <= 31

from random import randint

# Environment variables - Delimiters
size = 4 # Total individuals on each generation
mutation_odds = 1 # Odds to mutate
generations = 5 # Total generations

perfection = 31 # In our case all 5 bits equal to '1', or integer 31
answer = False

# Calculate fitness of an individual
# In our case it is pretty straight forward
def fitness (individual):
    return int(individual, 2)

# Pick the parents
# Function will receive : current population, a list containing the fitness sum
# of each individual and the total fitness of the population
#
# It will pick a random int between 0 and total_fitness (indiv_odds)
# and find the first individual
# Then decrease the first individual fitness from the total fitness and
# from all individuals after that one, including itself
# This will turn the fitness of that individual into 0 and keep the fitness
# of the next individuals, making it impossible for the first individual to
# reproduce with itself
def parents (population, indiv_odds, temp_odds):
    temp_indiv_odds = indiv_odds[:]

    pick = randint(0, temp_odds - 1)
    for index in range(size + 1):
        if pick < temp_indiv_odds[index]:
            break
    first = population[index - 1]

    pos = index
    for index in range(pos, size + 1):
        temp_indiv_odds[index] -= fitness(first)
    temp_odds -= fitness(first)

    pick = randint(0, temp_odds - 1)
    for index in range(size + 1):
        if pick < temp_indiv_odds[index]:
            break
    second = population[index - 1]

    return first, second

# Mutate gene from an individual
# Simply change from 0 to 1 and vice versa in a given random position
def mutate (individual, position):
    if (individual[position] == '0'):
        individual = individual[:position] + '1' + individual[position + 1:]
    else:
        individual = individual[:position] + '0' + individual[position + 1:]
    return individual

# Generate initial population
population = []
for _ in range(size):
    # This will generate a random int between 0 and 31 (included)
    # convert to binary
    # and format to 5 bits with the leading 0s
    population.append("{:05b}".format(randint(0, 31)))

# ===========================

for current_gen in range(generations):

    print("Generation #" + str(current_gen + 1))
    print(population)
    print('=====================================')
    print()

    # We need to calculate the total fitness to do elitism
    # The 'best' individuals will reproduce
    # Total fitness will sum the fitness of each individual
    # individual_odds will create a list that contains the sum of the current individual
    # and all the previous ones.
    #
    # If the best individual is found within the current generation,
    # the script will end
    #
    individual_odds = [0]
    total_fitness = 0
    for n, individual in enumerate(population):
        total_fitness += fitness(individual)
        individual_odds.append(total_fitness)
        if (fitness(individual) == perfection):
            answer = True

    if (answer):
        print('Individual found!')
        break

    # This will loop to pick the parents and append to a list containing
    # the next generation.
    # If a mutation happens, it will do a mutation in a random gene (position)
    # of the last generated child
    #
    new_generation = []
    for _ in range(size):
        first, second = parents(population, individual_odds, total_fitness)
        new_generation.append(first[:3] + second[3:])
        if mutation_odds > randint(0, 100):
            new_generation[-1] = mutate(new_generation[-1], randint(0, 4))

    population = new_generation

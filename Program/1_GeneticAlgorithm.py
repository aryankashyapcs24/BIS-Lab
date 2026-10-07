# Genetic Algorithm

import random

stops = ["A", "B", "C", "D", "E"]

distance = {
    "A": {"A": 0, "B": 4, "C": 7, "D": 6, "E": 3},
    "B": {"A": 4, "B": 0, "C": 5, "D": 3, "E": 6},
    "C": {"A": 7, "B": 5, "C": 0, "D": 4, "E": 8},
    "D": {"A": 6, "B": 3, "C": 4, "D": 0, "E": 5},
    "E": {"A": 3, "B": 6, "C": 8, "D": 5, "E": 0}
}


def route_distance(route):
    total = 0

    for i in range(len(route) - 1):
        total += distance[route[i]][route[i + 1]]


    total += distance[route[-1]][route[0]]

    return total


def fitness(route):
    return 1 / route_distance(route)


def initialize_population(size):
    population = []

    for _ in range(size):
        route = stops.copy()
        random.shuffle(route)
        population.append(route)

    return population


def selection(population):
    population.sort(key=fitness, reverse=True)

    #best half
    return population[:len(population) // 2]


def crossover(parent1, parent2):

    start = random.randint(0, len(parent1) - 2)
    end = random.randint(start + 1, len(parent1) - 1)

    child = [None] * len(parent1)


    child[start:end] = parent1[start:end]

    remaining = [x for x in parent2 if x not in child]

    j = 0

    for i in range(len(child)):
        if child[i] is None:
            child[i] = remaining[j]
            j += 1

    return child


def mutation(route):

    i, j = random.sample(range(len(route)), 2)

    route[i], route[j] = route[j], route[i]

    return route




def genetic_algorithm(population_size=10, generations=100):

    population = initialize_population(population_size)

    for generation in range(generations):


        fitness_values = [fitness(route) for route in population]


        parents = selection(population)

        new_population = []


        while len(new_population) < population_size:


            parent1, parent2 = random.sample(parents, 2)


            child = crossover(parent1, parent2)


            child = mutation(child)


            new_population.append(child)


        population = new_population

    best_solution = min(population, key=route_distance)

    return best_solution


best_route = genetic_algorithm()

print("Best Bus Route:")
print(" -> ".join(best_route))

print("Minimum Distance:",
      route_distance(best_route))
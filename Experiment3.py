import time
from random import random, choice


### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###


# READ GRID FILE #
def read_file(path):
    g = open(path, "r")
    lines = g.readlines()
    g.close()
    return lines


# EXTRUCTS INTEGERS FROM GRID FILE AND
# CREATE A LIST OF INDIVIDUAL POPULATION VALUES
def create_grid(lis):
    k = []
    l = [i for i in lis if "-" not in i]  # list of strings not including "----!---"
    for i in l:
        for j in i:
            if j.isdigit():
                k.append(int(j))
            elif j != '!':
                k.append(0)
    return k


# GET AVAILABLE CELLS FROM THE INDIVIDUAL #
def get_available_cells(lis):
    a = []
    for i in lis:
        current = []
        for j in range(len(i)):
            if i[j] == 0:
                current.append(j)

        a.append(current)
    return a


# CREATE LIST OF ROWS FOR INDIVIDUAL
def get_rows(g):
    lis = []
    i = 0
    while len(g) > i:
        lis.append(g[i:i + 9])
        i += 9
    return lis


# CREATE LIST OF COLUMNS FOR INDIVIDUAL
def get_colums(g):
    clmn = [g[i::9] for i in range(9)]
    return clmn


# CREATE LIST OF BOXES FOR INDIVIDUAL
def get_boxes(rws):
    bxes = []
    i = 0
    for item in range(3):
        j = 0
        r = rws[i:i + 3]
        i += 3
        for t in range(3):
            a = []
            for row in r:
                a = a + row[j:j + 3]
            bxes.append(a)
            j += 3
    return bxes


# EVALUATES FITNESS OF ROWS/COLUMNS/BOXES BASED ON NUMBER OF UNIQUE VALUES #
def evaluate(lis):
    results = 0
    for item in lis:
        results += len(set(item)) / 9

    return results / 9


# EVALUATES FITNESS OF INDIVIDUAL IN PERCENTAGE BASED ON FITNESS OF ITS ROWS, COLUMNS, BOXES
def evaluate_ind(individual):
    r = get_rows(individual)
    c = get_colums(individual)
    b = get_boxes(r)

    return (evaluate(r) + evaluate(c) + evaluate(b)) / 3


# EACH CHILD’S ROW  CONSISTS OF 2 HAVES:
# FIRST HALF IS HALF OF FIRST PARENT’S ROW AND SECOND HALF IS HALF OF SECOND PARENT’S ROW
def crossover_ind(parent, parent2):
    r1 = get_rows(parent)
    r2 = get_rows(parent2)
    child = [[]] * 9
    for row in range(len(child)):
        child[row] = r1[row][:(len(r1[row]) // 2)] + r2[row][(len(r2[row]) // 2):]

    return [j for i in child for j in i]



# MUTATE INDIVIDUAL BY REPLACING VALUE IN AVAILABLE CELL WITH RANDOM INTEGER 1-9
def mutate_ind(individual, cells, m):
    for item in cells:
        if random() < m:
            individual[item] = choice([i for i in range(1, 10)])
    return individual


### POPULATION-LEVEL OPERATORS ###

# CREATE LISTS OF INDIVIDUALS BY REPLACING 0s IN AVAILABLE CELLS WITH RANDOM INTEGERS 1-9
def create_pop(p, cells, lis):
    pop = []
    for i in range(p):
        f2 = create_grid(lis)
        for j in cells:
            f2[j] = choice([i for i in range(1, 10)])
        pop.append(f2)
    return pop


# EVALUATE POPULATION
def evaluate_pop(population):
    return [evaluate_ind(i) for i in population]


# SELECT BEST FIT INDIVIDUALS FROM POPULATION
def select_pop(population, fitness, size, s):
    selected = sorted(zip(population, fitness), key=lambda ind_fit: ind_fit[1], reverse=True)
    return [pop for pop, fit in selected[:int(size * s)]]


# CROSSOVER POPULATION
def crossover_pop(population, size):
    return [crossover_ind(choice(population), choice(population)) for _ in range(size)]


# MUTATE POPULATION
def mutate_pop(population, cells, m):
    return [mutate_ind(ind, cells, m) for ind in population]




# EVOLUTION ALGORITHM#
def experiment(p,m,s, cells, lis):
    population = create_pop(p, cells, lis)
    fitness_pop = evaluate_pop(population)
    best_pop = []
    best_fit = 0
    generation = 0
    while best_fit != 1.0 and generation < 5000:
        selected = select_pop(population, fitness_pop, p, s)
        crossover = crossover_pop(selected, p)
        population = mutate_pop(crossover, cells, m)
        fitness_pop = evaluate_pop(population)
        best = sorted(zip(population, fitness_pop), key=lambda ind_fit: ind_fit[1], reverse=True)
        best_fit = best[0][1]  # best fitness in population
        generation += 1
        best_pop = best[0][0]  # best individual
    print(" "*3 +"Generation ", generation, " best fitness ", best_fit)
    return best_pop


pop_sizes = [10, 100, 1000, 10000]

mutation_rates_grid1 = [0.02, 0.044, 0.04, 0.04]
truncation_rates_grid1 = [0.5, 0.5, 0.5, 0.5]

mutation_rates_grid2 = [0.03, 0.027, 0.027, 0.03]
truncation_rates_grid2 = [0.2, 0.5, 0.5, 0.5]


def results_grid1():
    print("Experiment3 on grid1\n")
    l1 = [i.strip('\n') for i in read_file("grid1")]
    grid1 = create_grid(l1)
    available_cells1 = [i for i in range(len(grid1)) if grid1[i] == 0]  # indices if avaliable cells in individual
    solution = []  # sudoku solution
    for i in range(len(pop_sizes)):
        pop_size = pop_sizes[i]
        mutation_rate = mutation_rates_grid1[i]
        selection_proportion = truncation_rates_grid1[i]
        print("Population size: ", pop_size, " Mutation rate : ", mutation_rate, " Selection rate : ", selection_proportion)
        print()
        for runs in range(5):
            start = time.time()
            solution = experiment(pop_size, mutation_rate, selection_proportion, available_cells1, l1)
            end = time.time()
            print(" "*3 +"Sample: ", runs + 1, " Time: ", end - start)
            print()
    print("Solution: ")
    # prints best solution to sudoku
    r = get_rows(solution)
    for i in r:
        print(i)

results_grid1()





def results_grid2():
    print("Experiment3 on grid2\n")
    l2 = [i.strip('\n') for i in read_file("grid2")]
    grid2 = create_grid(l2)
    available_cells2 = [i for i in range(len(grid2)) if grid2[i] == 0]  # indices if avaliable cells in individual
    solution = [] # sudoku solution
    for i in range(len(pop_sizes)):
        pop_size = pop_sizes[i]
        mutation_rate = mutation_rates_grid2[i]
        selection_proportion = truncation_rates_grid2[i]
        print("Population size", pop_size, " Mutation rate : ", mutation_rate, " Selection rate : ", selection_proportion)
        for runs in range(5):
            start = time.time()
            solution = experiment(pop_size, mutation_rate, selection_proportion, available_cells2, l2)
            end = time.time()
            print("Sample: ", runs + 1, "Time", end - start)
            print()
    print("Solution: ")
    # prints best solution to sudoku
    r = get_rows(solution)
    for i in r:
        print(i)

results_grid2()
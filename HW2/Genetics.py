import numpy as np
from pysat.formula import CNF

from copy import deepcopy
from random import randint, choice, random


def check_satisfation(clause, state):
    clauses = deepcopy(clause)

    for l in state:
        i = 0
        while i < len(clauses):
            if l in clauses[i]:
                clauses.remove(clauses[i])
            else:
                i = i + 1
    return len(clauses)


def population_sort(clauses, populat, k):
    tmp = [0] * k
    for i in range(k):
        tmp[i] = check_satisfation(clauses[:], populat[i])

    for i in range(k):
        for j in range(i, k):
            if tmp[i] > tmp[j]:
                tmp[i], tmp[j] = tmp[j], tmp[i]
                populat[i], populat[j] = populat[j], populat[i]


def population_cross(populat, k):
    newP = [0] * k
    nbL = len(populat[0])
    for i in range(k):
        limit = randint(0, nbL - 1)
        newP[i] = populat[randint(0, k - 1)][:limit] + populat[randint(0, k - 1)][limit:]
    return newP


def clone(clauses, populat, k):
    newP = []
    chances = []
    nbC = len(clauses)
    for i in range(k):
        chances = chances + ([i] * int((nbC - check_satisfation(clauses[:], populat[i])) / 10))

    for i in range(k):
        newP.append(populat[choice(chances)])

    return newP


def mutate(population, rate):
    nbL = len(population[0])
    rate = random() % rate
    k = len(population)
    limit = int(len(population) * rate)
    for i in range(limit):
        r = randint(0, nbL - 1)
        population[randint(2, k - 1)][r] = population[i][r] * -1


def fitness(population, clauses):
    f = 0.0
    nbC = len(clauses)
    for i in population:
        f = f + (nbC - check_satisfation(clauses[:], i)) / float(len(clauses))
    return f / len(population)


def random_solution(nbL):
    l = []
    for x in range(1, nbL + 1):
        sign = randint(0, 1)
        if sign:
            l.append(x)
        else:
            l.append(-x)

    return l


def genetic(clauses, nbL, k, nbIter, rate):
    nbC = len(clauses)
    nbIter = 100
    population = [0] * k
    for i in range(k):
        population[i] = random_solution(nbL)

    bestVal = 0

    for i in range(nbIter):

        population_sort(clauses, population, k)
        bestVal = (len(clauses) - check_satisfation(clauses[:], population[0])) / float(len(clauses))

        if bestVal == 1:
            print("SOLUTION FOUND!")
            print(population[0])

            print(str(bestVal))
            print(population[0])
            return (population[0], bestVal)

        print("Population fitness: " + str(fitness(population, clauses)) + "\t BestVal: " + str(bestVal))

        clonedP = clone(clauses, population, k)

        newP = population_cross(clonedP, k)

        mutate(newP, rate)

        population_sort(clauses, newP, k)
        population = population[:int(k * 0.15) + 1] + newP[:int(k * 0.85)]

    print(str(bestVal))
    print(population[0])
    return (population[0], bestVal)



lines = np.loadtxt("database.cnf", dtype=int, delimiter="  ", unpack=False)

cnf = CNF()
for line in lines:
    cnf.append(line[:-1].tolist())
print(cnf.clauses)


genetic(cnf.clauses, cnf.nv, 200, 1000000000, 0.2)
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


def random_solution(nv):
    l = []
    for x in range(1, nv + 1):
        sign = randint(0, 1)
        if sign:
            l.append(x)
        else:
            l.append(-x)
    return l


def disturb(solution):
    return [var * -1 if random() < 0.01 else var for var in solution]


def next_temperature(i, n_iterations):

    return (1 - (i + 1) / n_iterations)


lines = np.loadtxt("database.cnf", dtype=int, delimiter="  ", unpack=False)
cnf = CNF()
for line in lines:
    cnf.append(line[:-1].tolist())


def simulated_annealing(clause, n_iterations):
    scores = []
    solution = random_solution(cnf.nv)
    best_eval = len(clause) - check_satisfation(cnf.clauses, solution)
    curr, curr_eval = solution, best_eval
    temperature = 5
    for i in range(n_iterations):
        curr = disturb(solution)
        curr_eval = len(clause) - check_satisfation(cnf.clauses, curr)
        delta = best_eval - curr_eval
        if delta <= 0 or random() < np.exp(-delta / temperature):
            solution = curr
            best_eval = curr_eval
        scores.append(curr_eval)
        temperature = next_temperature(i, n_iterations)
        if i % 1000 == 0:
            print("iteration " + str(i) + "/" + str(n_iterations) + " Score =" + str(curr_eval))
    return scores, solution


scores, solution = simulated_annealing(cnf.clauses, 1000000)
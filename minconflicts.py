#!/usr/bin/python
import random
import time
from board import *

MAX_ITER = 100000000
BIG_INT = 100000000

def generate_random_assignment(n):
    r = range(0, n)
    random.shuffle(r)
    return r

def generate_greedy_assignment(n):
   r = []
	

def count_conflicts(pos, val, assignment):
    c = 0
    for p, v in enumerate(assignment):
        if p == pos: 
            continue
        if v == assignment[pos]:
            c += 1
        if abs(p - pos) == abs(v - val):
            c += 1
    return c
    

def is_solution(assignment):
    c = 0
    for pos, val in enumerate(assignment):
        c += count_conflicts(pos, val, assignment)
    return c == 0


def get_conflicted_variables(assignment):
    result = []
    for pos, val in enumerate(assignment):
        if count_conflicts(pos, val, assignment):
            result.append(pos)
    return result


def get_min_conflict_value_for(var, assignment):
    min = BIG_INT
    result_candidates = []
    for val in xrange(0, len(assignment)):
        c = count_conflicts(var, val, assignment)
        if c <= min:
            if c < min:
                result_candidates = []
                min = c
            result_candidates.append(val)
    if result_candidates:
        return result_candidates[random.randrange(0, len(result_candidates))]
    else:
        return None

def send(q, a, s):
    q.put(dict(board=a, solution=s))

def solve(n):
    assignment = generate_random_assignment(n)
    board = [-1 for i in range(n)]
    aux = {"board": board, "solution":False}
    q = Queue()
    q.put(aux)
    p2 = Process(target=draw_board, args=(q,))
    p2.start()
    number_iter = 0
    print assignment
    t1 = time.time()
    for i in xrange(0, MAX_ITER):
        if is_solution(assignment):
            q.put({"board": assignment, "solution":True})
            break
        q.put({"board": assignment, "solution":False})        
        vars = get_conflicted_variables(assignment)
        var = vars[random.randrange(0, len(vars))]
        value = get_min_conflict_value_for(var, assignment)
        assignment[var] = value
        number_iter += 1

	t2 = time.time()
    delta_time = t2 - t1
    print delta_time
    draw_stats(number_iter, round(delta_time, 8))
    #return None

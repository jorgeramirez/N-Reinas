#!/usr/bin/python
import random
import time
from board import *

"""
min-conflict algorithm for CSP

Based on aima-python module.
"""

class UniversalDict:
    """
    A universal dict maps any key to the same value. We use it here
    as the domains dict for CSPs in which all vars have the same domain.
    >>> d = UniversalDict(42)
    >>> d['life']
    42
    """
    def __init__(self, value): 
        self.value = value
    
    def __getitem__(self, key): 
        return self.value
    
    def __repr__(self): 
        return '{Any: %r}' % self.value
    

def queen_constraint(A, a, B, b):
    """
    Constraint is satisfied (true) if A, B are really the same variable,
    or if they are not in the same row, down diagonal, or up diagonal.
    """
    return A == B or (a != b and A + a != B + b and A - a != B - b)



class NQueensCSP:
    """
    Make a CSP for the nQueens problem for search with min_conflicts.
    Suitable for large n, it uses only data structures of size O(n).
    Think of placing queens one per column, from left to right.
    That means position (x, y) represents (var, val) in the CSP.
    The main structures are three arrays to count queens that could conflict:
        rows[i]      Number of queens in the ith row (i.e val == i)
        downs[i]     Number of queens in the \ diagonal
                     such that their (x, y) coordinates sum to i
        ups[i]       Number of queens in the / diagonal
                     such that their (x, y) coordinates have x-y+n-1 = i
    """
    def __init__(self, n):
        self.vars = range(n)
        self.domains = UniversalDict(range(n))
        self.neighbors = UniversalDict(range(n))
        self.constraints = queen_constraint
        self.rows = [0] * n   # Number of queens in the ith row (i.e val == i)
        self.ups = [0] * (2 * n - 1) # Number of queens in the \ diagonal
        self.downs = [0] * (2 * n - 1) # Number of queens in the / diagonal
        self.initial = {}
        self.nassigns = 0
    
    def nconflicts(self, var, val, assignment): 
        """
        The number of conflicts, as recorded with each assignment.
        Count conflicts in row and in up, down diagonals. If there
        is a queen there, it can't conflict with itself, so subtract 3.
        """
        n = len(self.vars)
        c = self.rows[val] + self.downs[var + val] + self.ups[var - val + n - 1]
        if assignment.get(var, None) == val:
            c -= 3
        return c

    def assign(self, var, val, assignment):
        """Assign var, and keep track of conflicts."""
        oldval = assignment.get(var, None)
        if val != oldval:
            if oldval is not None: # Remove old val if there was one
                self.record_conflict(assignment, var, oldval, -1)
            self.record_conflict(assignment, var, val, +1)
            self.nassigns += 1
            assignment[var] = val
    
    def unassign(self, var, assignment):
        """Remove var from assignment (if it is there) and track conflicts."""
        if var in assignment:
            self.record_conflict(assignment, var, assignment[var], -1)
            del assignment[var]
        
    def record_conflict(self, assignment, var, val, delta):
        """Record conflicts caused by addition or deletion of a Queen."""
        n = len(self.vars)
        self.rows[val] += delta
        self.downs[var + val] += delta
        self.ups[var - val + n - 1] += delta
        
    def conflicted_vars(self, current):
        """
        Return a list of variables in current assignment that are in conflict
        """
        return [var for var in self.vars
                if self.nconflicts(var, current[var], current) > 0]


def min_conflicts(csp, max_steps=1000000): 
    """
    Solve a CSP by stochastic hillclimbing on the number of conflicts.
    """
    # Generate a complete assignement for all vars (probably with conflicts)
    current = {}
    csp.current = current
    n = len(csp.vars)
    board = [-1 for i in range(n)]
    aux = {"board": board, "solution":False}
    q = Queue()
    q.put(aux)

    p2 = Process(target=draw_board, args=(q, n))
    p2.start()    
    number_iter = 0
    for var in csp.vars:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    
    # Now repeapedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            q.put({"board": current.values(), "solution":True})
            break
        q.put({"board": current.values(), "solution":False})
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
        number_iter += 1
    return number_iter


def min_conflicts_value(csp, var, current):
    """
    Return the value that will give var the least number of conflicts.
    If there is a tie, choose at random.
    """
    return argmin_random_tie(csp.domains[var],
                             lambda val: csp.nconflicts(var, val, current)) 


def argmin_random_tie(seq, fn):
    """
    Return an element with lowest fn(seq[i]) score; break ties at random.
    """
    best_score = fn(seq[0]); n = 0
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score; n = 1
        elif x_score == best_score:
            n += 1
            if random.randrange(n) == 0:
                    best = x
    return best


def solve(n):
    """
    Solves the NQuensCSP and returns the number of steps.
    """
    t1 = time.time()
    number_iter = min_conflicts(NQueensCSP(n))
    t2 = time.time()
    delta_time = (t2 - t1) * 1000
    draw_stats(number_iter, round(delta_time, 5))

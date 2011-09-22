#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------
#Program name:
#N queen solver
#
#import multiprocessing

from board import *
import time

nodos_visitados = 0
def conflict(state,X):
    """This function checks for any conflicts when placing a
Queen on the board.The state variable is a tuple which contains
the postiions of all the queens already placed and X is the
position for which checking is being done.Note here that X also
is X co-ordinate of the piece being placed.Y refers to Y coordinate."""
    Y=len(state)
    for i in range(Y):
        if abs(state[i]-X) in (0, Y-i):
            return True
    return False

def queens(num,sol,state=()):
    """This generator uses backtracing and recursion to place the
the queens.The result is a generator containing all the possible
solutions."""
    global nodos_visitados
    for pos in range(num):
        estado = state+(pos,)
        while len(estado) != num:
            estado = estado+(-1,)
        nodos_visitados = nodos_visitados + 1
        solucion = {"solution": False, "board" : estado}
        sol.put(solucion)
        if not conflict(state,pos):
            if len(state)==num-1:
                yield (pos,)
            else:
                for result in queens(num,sol,state+(pos,)):
                    yield (pos,)+result

def backtracking(queen_number, uno):
    global nodos_visitados
    board = [-1 for i in range(queen_number)]
    q = Queue()
    aux = {"board": board, "solution":False}
    q.put(aux)
    p2 = Process(target=draw_board, args=(q, queen_number))
    p2.start()
    t1 = time.time()
    for solution in queens(queen_number,q):
        solucion = {"solution": True, "board" : solution}
        q.put(solucion)
        if solution and uno:
            break
    t2 = time.time()
    tiempo = (t2-t1) * 1000
    draw_stats(nodos_visitados, round(tiempo, 5))

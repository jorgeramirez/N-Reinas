import random
import math
import time
from board import *
	
def actualizar_prohibidos(reinas, N):
	prohibidos = list()
	for var in range(N):
		lista = list()
		prohibidos.insert(var, lista)
	for col in range(N):
		if reinas[col] != -1: #hay una reina en la columna col
			for fil in range(N):
				if fil not in prohibidos[col]:
					prohibidos[col].append(fil) #se prohibe toda esa fila
			for k in range(N):
				reina = reinas[col]
				if not reina in prohibidos[k]:
					prohibidos[k].append(reina) #se prohibe toda esa columna
			
			#diagonales
			reina = reinas[col]
			for col2 in range(N):
				for fil2 in range(N):
					if reina - col == fil2 - col2 or reina + col == fil2 + col2 or col - col2 == reina - fil2 or col - col2 ==fil2 - reina:
						if not fil2 in prohibidos[col2]:
							prohibidos[col2].append(fil2)
	return prohibidos

	
def actualizar_permitidos(prohibidos, N):
	permitidos = list()
	for v in range(N):
		lista = list()
		permitidos.insert(v, lista)

	for col in range(N):
		for fil in range(N):
			if not fil in prohibidos[col] and not fil in permitidos[col]:
				permitidos[col].append(fil)
	return permitidos

def vegas(N):
	#INICIALIZACIONES
    reinas = list()
    board = [-1 for i in range(N)]

    q = Queue()
    aux = {"board": board, "solution":False}
    q.put(aux)

    p2 = Process(target=draw_board, args=(q, N))
    p2.start()


    for i in range(N):
        reinas.insert(i, -1)

    prohibidos = list()
    for i in range(N):
        lista = list()
    prohibidos.insert(i, lista)

    permitidos = list()
    t1 = time.time()
    nodos = 0
    column = 0
	##################

    while column < N:
		
        prohibidos = actualizar_prohibidos(reinas, N)

        permitidos = actualizar_permitidos(prohibidos, N)

        if len(permitidos[column]) != 0:
            fila = random.choice(permitidos[column])
		
            reinas[column] = fila
            column += 1
        else:
            reinas[column] = -1
            if column > 0:
                column -= 1
		
        nodos += 1
        print "Reinas"
        print reinas
        solucion = {"solution": False, "board" : reinas}
        q.put(solucion)
    solucion = {"solution": True, "board" : reinas}
    q.put(solucion)
    t2 = time.time()
    tiempo = t2 - t1
    print "Tiempo:"
    print tiempo
    print "Nodos:"
    print nodos
    draw_stats(nodos, round(tiempo, 8))

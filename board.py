#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from multiprocessing import Process, Queue

def draw_board(q, n):
    """ Draw a chess board with queens, as determined by the the_board. """
    pygame.init()
    colors = [(255,250,250), (0,0,0), (255,255,0)]    # set up colors [white, black,yellow]

    surfaceSz = 640          # Proposed physical surface size.
    sq_sz = surfaceSz // n    # sq_sz is length of a square.
    surfaceSz = n * sq_sz     # Adjust to exact multiple of sq_sz

    # Create the surface of (width, height), and its window.
    pygame.display.set_caption("Simulador")    
    surface = pygame.display.set_mode((surfaceSz, surfaceSz))


    ball = pygame.image.load("queen.png")
    if ball.get_width() > sq_sz:
		ball = pygame.transform.scale(ball, (sq_sz - 10, sq_sz - 10)) 

    # Use an extra offset to centre the ball in its square.
    # If the square is too small, offset becomes negative,
    # but it will still be centered :-)
    ball_offset = (sq_sz-ball.get_rect()[2]) // 2

    while True:

        # look for an event from keyboard, mouse, etc.
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break;

        if not q.empty():
            e = q.get()
            the_board = e["board"]
            solution = e["solution"]

        # Draw a fresh background (a blank chess board)
        for row in range(n):         # Draw each row of the board.
            c_indx = row % 2           # Alternate starting color
            for col in range(n):       # Run through cols drawing squares
                the_square = (col*sq_sz, row*sq_sz, sq_sz, sq_sz)
                if solution and (col, row) in enumerate(the_board):
                    surface.fill(colors[2], the_square)
                else:    
                    surface.fill(colors[c_indx], the_square)
              # now flip the color index for the next square
                c_indx = (c_indx + 1) % 2
        pygame.time.delay(50)
        # Now that squares are drawn, draw the queens.
        for (col, row) in enumerate(the_board):
            if row != -1:
                surface.blit(ball,
                    (col*sq_sz+ball_offset,row*sq_sz+ball_offset))

        pygame.display.flip()
        if solution:
            pygame.time.delay(300)
        else:
            pygame.time.delay(50)


    pygame.quit()
    
def draw_stats(nodos, tiempo):
    pygame.init()
    color = (255,250,250)  # white
    pygame.display.set_caption("Resultados")
    surface = pygame.display.set_mode((240, 240))
    my_font = pygame.font.SysFont('Courier', 16)

    while True:
        ev = pygame.event.poll()    # look for any event
        if ev.type == pygame.QUIT:  # window close button clicked?
            break
        surface.fill((0, 200, 255), surface.get_rect())        			            
        text1 = my_font.render('Nodos expandidos: ' + str(nodos), True, (0,0,0))	
        text2 = my_font.render('Tiempo de ejecucion: ' + str(tiempo) + " ms", True, (0,0,0))
        surface.blit(text1, (10, 10))
        surface.blit(text2, (10, 40))
        pygame.display.flip()
        
    pygame.quit()

		
	

if __name__ == '__main__':
    q = Queue()
    for i in range(10):
        q.put({"board": [6, 2, 3, 1, 6, 3, 6], "solution": False})    
        q.put({"board": [0, 5, 3, 1, 6, 4, 2], "solution": True})
    #draw_stats()
    q.put({"board": [6, 2, 3, 1, 6, 3, 6], "solution": False})    
    q.put({"board": [0, 5, 3, 1, 6, 4, 2], "solution": True})
    draw_board(q)    # 7 x 7 to test window size
    #draw_board([6, 4, 2, 0, 5, 7, 1, 3])
    #draw_board([9, 6, 0, 3, 10, 7, 2, 4, 12, 8, 11, 5, 1])  # 13 x 13
    #draw_board([11, 4, 8, 12, 2, 7, 3, 15, 0, 14, 10, 6, 13, 1, 5, 9])

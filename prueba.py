import pygame

def draw_board(the_board):
    """ Draw a chess board with queens, as determined by the the_board. """

    pygame.init()
    colors = [(255,0,0), (0,0,0)]    # set up colors [red, black]

    n = len(the_board)        # this is an NxN chess board.
    surfaceSz = 480           # Proposed physical surface size.
    sq_sz = surfaceSz // n    # sq_sz is length of a square.
    surfaceSz = n * sq_sz     # Adjust to exact multiple of sq_sz

    # Create the surface of (width, height), and its window.
    surface = pygame.display.set_mode((surfaceSz, surfaceSz))

    ball = pygame.image.load("queen.png")

    # Use an extra offset to centre the ball in its square.
    # If the square is too small, offset becomes negative,
    # but it will still be centered :-)
    ball_offset = (sq_sz-ball.get_rect()[2]) // 2

    while True:

        # look for an event from keyboard, mouse, etc.
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break;

        # Draw a fresh background (a blank chess board)
        for row in range(n):         # Draw each row of the board.
          c_indx = row % 2           # Alternate starting color
          for col in range(n):       # Run through cols drawing squares
              the_square = (col*sq_sz, row*sq_sz, sq_sz, sq_sz)
              surface.fill(colors[c_indx], the_square)
              # now flip the color index for the next square
              c_indx = (c_indx + 1) % 2

        # Now that squares are drawn, draw the queens.
        for (col, row) in enumerate(the_board):
          surface.blit(ball,
                   (col*sq_sz+ball_offset,row*sq_sz+ball_offset))

        pygame.display.flip()


    pygame.quit()

if __name__ == '__main__':
    draw_board([0, 5, 3, 1, 6, 4, 2])    # 7 x 7 to test window size
    

import pygame
from util import *
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 40, 40
BLACK = (0, 0, 0)
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid")
    clock = pygame.time.Clock()
    running = True
    grid = Grid(ROWS, COLS, WIDTH, HEIGHT, screen)
    grid.get_cell(1, 2).state = 2
    grid.get_cell(-3, -1).state = 3
    grid.get_cell(3, 5).state = 1


    pressed = False
    current_state = 1
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse down")
                pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                print("Mouse up")
                pressed = False
            if pressed:
                pos = pygame.mouse.get_pos()
                #If left click
                if pygame.mouse.get_pressed()[0]:
                    current_state = 1
                    print("Left click")
                #If right click
                elif pygame.mouse.get_pressed()[2]:
                    current_state = 0
                if grid.get_cell_from_mouse(pos).state == 1 or grid.get_cell_from_mouse(pos).state == 0:
                    grid.get_cell_from_mouse(pos).state = current_state


        # Run when space is pressed
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            grid.run_algorithm("A*")

        screen.fill((30, 30, 30))
        grid.draw()
        pygame.display.update()
        

    pygame.quit()

if __name__ == "__main__":
    main()
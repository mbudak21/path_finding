import pygame, time

class Grid(): #states: 0 = empty, 1 = wall, 2 = start, 3 = end, 4 = path
    #State colors
    EMPTY = (150, 150, 150)
    WALL = (30, 30, 30)
    START = (255, 0, 0)
    END = (0, 255, 0)
    PATH = (0, 255, 0)

    def __init__(self, rows, cols, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.w = width / cols
        self.h = height / rows
        self.done = False
        self.screen = screen
        Grid_cell.grid = self
        self.grid = [[Grid_cell(i, j) for i in range(cols)] for j in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                self.grid[i][j].set_neighbors()
        
    
    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.grid[i][j]
                if cell.state == 0:
                    color = self.EMPTY
                elif cell.state == 1:
                    color = self.WALL
                elif cell.state == 2:
                    color = self.START
                elif cell.state == 3:
                    color = self.END
                elif cell.state == 4:
                    color = self.PATH
                pygame.draw.rect(self.screen, color, (cell.x*self.w, cell.y*self.h, self.w-1, self.h-1))
    
    
    def get_cell(self, x, y):
        return self.grid[y][x]

    
    def get_cell_from_mouse(self, mouse_pos):
        row = int(mouse_pos[1] / self.h)
        col = int(mouse_pos[0] / self.w)
        return self.grid[row][col]
    
    def run_algorithm(self, algorithm):
        if not self.done:
            try:
                if algorithm == "test":
                    self.test()
                    self.done = True
                if algorithm == "A*":
                    self.A_star()
            except AttributeError:
                print("Algorithm not implemented")
        
    
    def test(self):
        #Find the start and end cells
        for y in range(self.rows):
            for x in range(self.cols):
                if self.get_cell(x ,y).state == 2:
                    start_cell = self.get_cell(x ,y)
                if self.get_cell(x ,y).state == 3:
                    end_cell = self.get_cell(x ,y)
        print(f"Start: {start_cell}")
        print(f"End: {end_cell}")

        #Paint the neighbors of the wall cells
        neighbors = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j].state == 1:
                    for neighbor in self.grid[i][j].get_neighbors():
                        neighbors.append(neighbor)
        for neighbor in neighbors:
            neighbor.state = 1
            time.sleep(0.1)
            self.draw()
            pygame.display.update()



    def A_star(self, start_cell, end_cell):
        """
        F = G + H
        G = cost(length) of the path from start to current cell
        H = estimated cost of the path from current cell to end
        """
        #Find the start and end cells
        for y in range(self.rows):
            for x in range(self.cols):
                if self.get_cell(x ,y).state == 2:
                    start_cell = self.get_cell(x ,y)
                if self.get_cell(x ,y).state == 3:
                    end_cell = self.get_cell(x ,y)
        print(f"Start: {start_cell}")
        print(f"End: {end_cell}")

        #Create open and closed lists
        open_list = []
        closed_list = []

        #Add start cell to open list
        open_list.append(start_cell)




    def print(self):
        for i in range(self.rows):
            if i != 0:
                print("")
            for j in range(self.cols):
                print(self.grid[i][j], end=" ")
    
class Grid_cell():
    grid = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #states: 0 = empty, 1 = wall, 2 = start, 3 = end, 4 = path
        self.state = 0
        self.neighbors = []


    def set_neighbors(self):
        if self.x > 0: #Left
            self.neighbors.append(self.grid.get_cell(self.x-1, self.y))
        if self.x < self.grid.cols-1: #Right
            self.neighbors.append(self.grid.get_cell(self.x+1, self.y))
        if self.y > 0: #Up
            self.neighbors.append(self.grid.get_cell(self.x, self.y-1))
        if self.y < self.grid.rows-1: #Down
            self.neighbors.append(self.grid.get_cell(self.x, self.y+1))
        
    def get_neighbors(self):
        return self.neighbors


    # def get_heuristic(self, neighbor, end):
    #     return abs(neighbor.x - end.x) + abs(neighbor.y - end.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

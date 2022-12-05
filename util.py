import pygame, time

class Grid(): 
    #states: 0 = empty, 1 = wall, 2 = start, 3 = end, 4 = path, 5 = open_list, 6 = closed_list
    #State colors
    EMPTY = (150, 150, 150) 
    WALL = (30, 30, 30)
    START = (200, 200, 0)
    END = (200, 200, 0)
    OPEN = (0, 255, 0)
    CLOSED = (255, 0, 0)
    PATH = (255, 0, 255) 

    def __init__(self, rows, cols, width, height, screen = None):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.w = width / cols
        self.h = height / rows
        self.screen = screen
        self.diagonal = True
        self.done = False
        Grid_cell.grid = self
        self.matrix = [[Grid_cell(i, j) for i in range(cols)] for j in range(rows)]
 
    
    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.matrix[i][j]
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
                elif cell.state == 5:
                    color = self.OPEN
                elif cell.state == 6:
                    color = self.CLOSED
                pygame.draw.rect(self.screen, color, (cell.x*self.w, cell.y*self.h, self.w-1, self.h-1))
                
    
    def get_cell(self, x, y):
        return self.matrix[y][x]

    
    def get_cell_from_mouse(self, mouse_pos):
        row = int(mouse_pos[1] / self.h)
        col = int(mouse_pos[0] / self.w)
        return self.matrix[row][col]
    
    def run_algorithm(self, algorithm):
        if algorithm == "test" and self.done == False:
            self.test()
            self.done = True
        elif algorithm == "A*" and self.done == False:
            self.A_star()
            self.done = True
        else:
            if self.done == True:
                print("Algorithm already run")
            else:
                print("Algorithm not found")

        
    
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
                if self.matrix[i][j].state == 1:
                    for neighbor in self.matrix[i][j].get_neighbors():
                        neighbors.append(neighbor)
        for neighbor in neighbors:
            neighbor.state = 1
            time.sleep(0.1)
            self.draw()
            pygame.display.update()



    def A_star(self):
        """
        F = G + H
        G = cost(length) of the path from start to current cell
        H = estimated cost of the path from current cell to end
        """

        #Define the heuristic function
        def get_h(cell):
            # # Manhattan distance
            # return abs(cell.x - end_cell.x) + abs(cell.y - end_cell.y)

            #Euclidean distance
            return ((cell.x - end_cell.x)**2 + (cell.y - end_cell.y)**2)**0.5



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
        #We do this because we need to start with a cell
        open_list.append(start_cell)
        
        loops = 0
        while len(open_list) > 0:
            
            lowest_f_index = 0
            for i in range(len(open_list)):
                if open_list[i].f < open_list[lowest_f_index].f:
                    lowest_f_index = i
            current_cell = open_list[lowest_f_index]
            if current_cell == end_cell:

                #find the path
                path = []
                temp = current_cell
                while temp.previous != None:
                    path.append(temp)
                    temp = temp.previous
                    temp.state = 4

                print(f"Found path in {loops} loops")
                self.done = True
                break
            
            open_list.remove(current_cell)
            closed_list.append(current_cell)
            current_cell.state = 6

            for neighbor in current_cell.get_neighbors():

                if neighbor not in closed_list and neighbor.state != 1:
                    tempG = current_cell.g + 1 #1 is the distance between two cells

                    newPath = False
                    if neighbor in open_list:
                        if tempG < neighbor.g:
                            neighbor.g = tempG
                            newPath = True
                    else:
                        neighbor.g = tempG
                        newPath = True
                        open_list.append(neighbor)
                        neighbor.state = 5
                    
                    if newPath:
                        neighbor.h = get_h(neighbor)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.previous = current_cell

            self.draw()
            pygame.display.update()
            print(loops)
            loops += 1
        else:
            print("No path found")

    def print(self):
        for i in range(self.rows):
            if i != 0:
                print("")
            for j in range(self.cols):
                print(self.matrix[i][j], end=" ")
    
class Grid_cell():
    grid = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #states: 0 = empty, 1 = wall, 2 = start, 3 = end, 4 = path
        self.state = 0

        self.f = 0
        self.g = 0
        self.h = 0
        self.previous = None


        
    def get_neighbors(self):
        neighbors = []
        # Implement a get neighbors function, instead of storing the neighbors in a list
        if self.x < self.grid.cols - 1: #right
            neighbors.append(self.grid.matrix[self.y][self.x+1])
        if self.x > 0: #left
            neighbors.append(self.grid.matrix[self.y][self.x - 1])
        if self.y < self.grid.rows - 1: #down
            neighbors.append(self.grid.matrix[self.y + 1][self.x])
        if self.y > 0: #up
            neighbors.append(self.grid.matrix[self.y - 1][self.x])

        return neighbors


    # def get_heuristic(self, neighbor, end):
    #     return abs(neighbor.x - end.x) + abs(neighbor.y - end.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

import pygame
import time
import random
from queue import PriorityQueue

#colours
WHITE = (255, 255, 255)
CYAN = (0, 100, 100)
RED = (255 ,0 ,0)
 
X=Y=20             #X=Y=int(input("Enter the maze size"))
w = 20                  # width of cell(Magnification)


# set up pygame window
WIDTH = w*(Y+2)
HEIGHT = w*(X+2)
FPS = 60
SPEED = 0.01

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Solver")
clock = pygame.time.Clock()

# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
grid = []
visited = []
stack = []
solution = {}
Maze_map = {}


# build the grid
def build_grid(X, Y, w):
    x, y= 0, 0
    for i in range(1,X+1):
        x = w                                                           # set x coordinate to start position
        y = y + w                                                        # start a new row
        for j in range(1, Y+1):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])           # top of cell
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])   # right of cell
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])   # bottom of cell
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])           # left of cell
            grid.append((x,y))                                            # add cell to grid list
            Maze_map[x,y]={"right":0, "left":0, "up":0, "down":0}
            x = x + w                                                    # move cell to new position

#Animation functions

def push_up(x, y):
    pygame.draw.rect(screen, CYAN, (x + 1, y - w + 1, w-1, 2*w-1), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                              # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(screen, CYAN, (x +  1, y + 1, w-1, 2*w-1), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, CYAN, (x - w +1, y +1, 2*w-1, w-1), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, CYAN, (x +1, y +1, 2*w-1, w-1), 0)
    pygame.display.update()


def single_cell( x, y):
    pygame.draw.rect(screen, WHITE, (x +1, y +1, w-2, w-2), 0)          # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, CYAN, (x +1, y +1, w-2, w-2), 0)        # used to re-colour the path after single_cell
    pygame.display.update()                                        # has visited cell


def solution_cell(x,y):
    pygame.draw.circle(screen, RED, (x+(w/2), y+(w/2)), w/4, 0)             # used to show the solution
    pygame.display.update()                                        # has visited cell


def createMaze(x,y):
    single_cell(x, y)                                              # starting positing of maze
    stack.append((x,y))                                            # place starting cell into stack
    visited.append((x,y))                                          # add starting cell to visited list
    while len(stack) > 0:                                          # loop until stack is empty
        time.sleep(SPEED)                                            # slow program now a bit
        cell = []                                                  # define cell list
        if (x + w, y) not in visited and (x + w, y) in grid:       # right cell available?
            cell.append("right")                                   # if yes add to cell list

        if (x - w, y) not in visited and (x - w, y) in grid:       # left cell available?
            cell.append("left")

        if (x , y + w) not in visited and (x , y + w) in grid:     # down cell available?
            cell.append("down")

        if (x, y - w) not in visited and (x , y - w) in grid:      # up cell available?
            cell.append("up")

        if len(cell) > 0:                                          # check to see if cell list is empty
            cell_chosen = (random.choice(cell))                    # select one of the cell randomly

            if cell_chosen == "right":                             # if this cell has been chosen
                Maze_map[x,y]["right"]=1
                if(x+w,y) in grid:
                    Maze_map[x+w,y]["left"]=1
                push_right(x, y)                                   # call push_right function
                solution[(x + w, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
                x = x + w                                          # make this cell the current cell
                visited.append((x, y))                              # add to visited list
                stack.append((x, y))                                # place current cell on to stack

            elif cell_chosen == "left":
                Maze_map[x,y]["left"]=1
                if(x-w,y)in grid:
                    Maze_map[x-w,y]["right"]=1
                push_left(x, y)
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                Maze_map[x,y]["down"]=1
                if(x,y+w)in grid:
                    Maze_map[x,y+w]["up"]=1       #X IS VERTICAL AND Y IS HORIZONTAL AXIS
                push_down(x, y)
                solution[(x , y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                Maze_map[x,y]["up"]=1
                if(x,y-w)in grid:
                    Maze_map[x,y-w]["down"]=1
                push_up(x, y)
                solution[(x , y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            single_cell(x, y)                                     # use single_cell function to show backtracking image
            time.sleep(SPEED)                                       # slow program down a bit
            backtracking_cell(x, y)                               # change colour to WHITE to identify backtracking path


def plotRoute(x,y):
    solution_cell(x, y)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (w,w):                                     # loop until cell position == start position
        x, y = solution[x, y]                                    # "key value" now becomes the new key
        solution_cell(x, y)                                      # animate route back
        time.sleep(SPEED)

def h(cell1,cell2):
    x1, y1=cell1
    x2, y2=cell2
    return abs(x1-x2)+abs(y1-y2)

start=()
path={}

def A_Star(x,y):
    start=(x,y)#end cell of the maze
    end=(20,20)#starting cell of the maze 
    gCost={}
    fCost={}
    for i in grid:
        gCost[i]=float('inf')
        fCost[i]=float('inf')
    gCost[start]=0
    fCost[start]=gCost[start]+h(start,end)

    print(gCost)
    print(fCost)

    pQueue=PriorityQueue()

    pQueue.put((fCost[start],h(start,end),start))

    while not pQueue.empty():
        currCell=pQueue.get()[2]
        if currCell==end:
            break
        for i in ("left","right","up","down"):
            neighbourCell=()
            if Maze_map[currCell][i]==1:
                if i=="left":
                    neighbourCell=(currCell[0]-w,currCell[1])
                if i=="right":
                    neighbourCell=(currCell[0]+w,currCell[1])
                if i=="up":
                    neighbourCell=(currCell[0],currCell[1]-w)
                if i=="down":
                    neighbourCell=(currCell[0],currCell[1]+w)
                
                new_gCost=gCost[currCell]+w
                new_fCost=new_gCost+h(neighbourCell,end)

                if new_fCost<fCost[neighbourCell]:
                    gCost[neighbourCell]=new_gCost
                    fCost[neighbourCell]=new_fCost
                    pQueue.put((new_fCost,h(neighbourCell,end),neighbourCell))
                    path[neighbourCell]=currCell

build_grid(X, Y, w)             # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
x, y = w, w                     # starting position of grid
createMaze(x,y)                 # call build the maze  function
#A_Star(w*X,w*Y)

# cell=()
# for i in path.keys():
#     cell=path[i]
#     solution[cell]=i

# print(solution)

plotRoute(w*X, w*Y)             # call the plot solution function


running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False

# ==============================================================================
"""PolyMaze Maze Generator"""
# ==============================================================================
__author__  = "Lemaire Pierre & Rawat Eshane"
__version__ = "Random Maze generator 1.1"
__date__    = "2015-03-30"
# =======================================================

import random

class maze_generator(object):
    def __init__(self):
        #Maze dimensions
        self.width = 50
        self.height = 50
        #Initial stack
        self.maze = []
        #Directions within the maze for the constructor
        self.xdir = [0,1,0,-1]
        self.ydir = [-1,0,1,0]

    def new_maze(self, x, y):
        self.maze = [[0 for i in range(self.width)] for j in range(self.height)]
        return self.carve_maze(x,y)

    #Depth search, maybe add Prim's and Kruskal's algo to diversify maze types + braided maze
    def carve_maze(self, x, y):
        self.maze[y][x]=1
        while True:
            neighbours = [] 
            for i in range(4):
                nx = x + self.xdir[i]
                ny = y + self.ydir[i]
                if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height:
                    if self.maze[ny][nx] == 0:
                        check = 0
                        for j in range(4):
                            another_x = nx + self.xdir[j]
                            another_y = ny + self.ydir[j]
                            if another_x >= 0 and another_x < self.width and another_y >= 0 and another_y < self.height:
                                if self.maze[another_y][another_x] == 1:
                                    check += 1
                        if check == 1: 
                            neighbours.append(i)
            if len(neighbours) > 0:
                z = neighbours[random.randint(0, len(neighbours) - 1)]
                x += self.xdir[z]
                y += self.ydir[z]
                self.carve_maze(x, y)
            else: 
                break
        return self.maze


def main():
    d = maze_generator()
    d.Maze_mesh_up()


if __name__ == "__main__" :
    main()

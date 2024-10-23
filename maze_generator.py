import numpy as np
import random
import pygame
import sys

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
def create_maze(width, height):
    maze = np.zeros((height, width), dtype=np.uint8)                        
    disjoint_set = DisjointSet(width * height)                              
                                                                            
                                                                            
    walls = []
    for y in range(height):
        for x in range(width):
            if x < width - 1:
                walls.append(((y, x), (y, x + 1)))
            if y < height - 1:
                walls.append(((y, x), (y + 1, x)))

    random.shuffle(walls)

    for (y1, x1), (y2, x2) in walls:
        cell1 = y1 * width + x1
        cell2 = y2 * width + x2
        
        if disjoint_set.find(cell1) != disjoint_set.find(cell2):
            disjoint_set.union(cell1, cell2)
            if x1 == x2:
                maze[min(y1, y2), x1] |= 2  
                maze[max(y1, y2), x1] |= 8  
            if y1 == y2:
                maze[y1, min(x1, x2)] |= 4  
                maze[y1, max(x1, x2)] |= 1  

    return maze

def draw_maze(maze, cell_size):
    height, width = maze.shape
    pygame.init()
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption('Maze Generator')

    white = (255, 255, 255)
    black = (0, 0, 0)

    screen.fill(white)

    for y in range(height):
        for x in range(width):
            if not maze[y, x] & 1:  
                pygame.draw.line(screen, black, (x * cell_size, y * cell_size), (x * cell_size, (y + 1) * cell_size))
            if not maze[y, x] & 2:  
                pygame.draw.line(screen, black, ((x + 1) * cell_size, (y + 1) * cell_size), (x * cell_size, (y + 1) * cell_size))
            if not maze[y, x] & 4:  
                pygame.draw.line(screen, black, ((x + 1) * cell_size, y * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size))
            if not maze[y, x] & 8:  
                pygame.draw.line(screen, black, ((x + 1) * cell_size, y * cell_size), (x * cell_size, y * cell_size))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    width = 15
    height = 15
    cell_size = 30 

    maze = create_maze(width, height)
    draw_maze(maze, cell_size)

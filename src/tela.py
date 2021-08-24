import pygame

import networkx as nx

import random

import time

import heapq

try:
    pygame.init()
except:
    print("Erro. Programa não inicializado")


WIDTH = 500
HEIGHT = 600
FPS = 30

tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption ("Mazegen")


# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)

w=20

# build the grid
def build_grid(x, y, w):
    x = 0
    y = 0 
    for i in range(1,21):
        x = 20                                                            
        y = y + 20                                                        
        for j in range(1, 21):
            pygame.draw.line(tela, WHITE, [x, y], [x + w, y])           
            pygame.draw.line(tela, WHITE, [x + w, y], [x + w, y + w])   
            pygame.draw.line(tela, WHITE, [x + w, y + w], [x, y + w])   
            pygame.draw.line(tela, WHITE, [x, y + w], [x, y])           
            x = x + 20                                                    


def up(y, x):
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, GREEN, (x + 1, y - 20 + 1, 19, 39), 0)        
    pygame.display.update()                                              
    #time.sleep(2)

def down(y, x):   
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, GREEN, (x +  1, y + 1, 19, 39), 0)
    pygame.display.update()
    #time.sleep(2)


def left(y, x):
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, GREEN, (x - 20 +1, y +1, 39, 19), 0)
    pygame.display.update()
    #time.sleep(2)


def right(y, x):
    x=20*(x+1)
    y=20*(y+1)
    pygame.draw.rect(tela, GREEN, (x +1, y +1, 39, 19), 0)
    pygame.display.update()
    #time.sleep(2)


#Random DFS

G = nx.grid_2d_graph(20,20)


def randUnvisitedNeighbor(vertex):
    unvNeigh = []
    neigh = G[vertex]
    for (x, y) in neigh:
        if G.nodes[(x, y)] != {'visited': 1} :
            unvNeigh.append((x, y))

    if len(unvNeigh) >= 1:
        chosenVertex = random.choice(unvNeigh)

    else:
        chosenVertex = False

    return chosenVertex

def moveCell(vertex, nextVertex):
    (x, y) = vertex
    (x2, y2) = nextVertex

    if x == x2:
        if y < y2:
            time.sleep(.05)
            right(x, y)
        else:
            time.sleep(.05)
            left(x, y)
    else:
        if x < x2:
            time.sleep(.05)
            down(x, y)
        else:
            time.sleep(.05)
            up(x, y)

#Instead of iterating through the neigbors it chooses one randomly
def randomDFS(vertex):
    G.nodes[vertex]['visited'] = 1
    nextVertex = randUnvisitedNeighbor(vertex)

    while nextVertex:
        moveCell(vertex, nextVertex)
        randomDFS(nextVertex)
        nextVertex = randUnvisitedNeighbor(vertex)
    
#MST MAZE
def randomEdgesWeight():
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.randint(0,100)
#=====================================================================================
def Prim():
    h = []
    s = []
    a = []
    i =0
    rep=-1
    temp = []
    for (x, y) in G.nodes():
        a.append(101)
        heapq.heappush(h, (a[20*x + y], (x, y)))

    while(h != []):
        heapq.heapify(h)
        u = heapq.heappop(h)
        if rep == -1:
            u = (0, (0,0))
        if rep != -1:
            for (x, y) in G[u[1]]:
                if (x ,y) in s:
                    temp.append((x, y))

            lesser = -1
            lesserxy = 0
            for (x, y) in temp:
                if lesser < a[20*x + y]:
                    lesser = a[20*x + y]
                    lesserxy = (x, y)
            moveCell(u[1], lesserxy)
            temp = []

        rep = 1
        s.append(u[1])
        neigh = G[u[1]]
        for (x, y) in neigh:
            if (x, y) not in s:
                if G.edges[u[1],(x, y)]['weight'] < a[20*x + y]:
                    a[20*x + y] = G.edges[u[1],(x, y)]['weight']
                    for i in range(len(h)):
                        if h[i][1] == (x, y):
                            h[i] = (a[20*x + y], (x, y))      
                            break          
#====================================================================================
def createMaze():
    startVertex = (0, 0)
    randomDFS(startVertex)

build_grid(40, 0, 20) 
#createMaze()
randomEdgesWeight()
Prim()

sair = True

while sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = False
    pygame.display.update()

pygame.quit()
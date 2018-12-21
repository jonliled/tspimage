#!/usr/bin/env python

# import time
import pygame
import itertools
# import pandas as pd
import numpy as np
#import travelUtils as tu
#import tkinter as tk
import time
import os
import random


################################################################################
################################ Pygame ######################################## 
################################################################################

display_width  = 800
display_height = 600
x_min = 10
y_min = 10
x_max = display_width - 10
y_max = display_height - 10

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))

################################################################################
################################ Colours ####################################### 
################################################################################

black = (0,0,0)
white = (255,255,255)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)

################################################################################
################################ Classes ####################################### 
################################################################################

class Node():
    x = None
    y = None
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_end(self, end):
        self.ends.append(end)

    def draw(self, screen, colour, r, w=0):
        pygame.draw.circle(screen, colour, (self.x, self.y), r, w)

class Edge():
    start = None
    end   = None
    
    def __init__(self, start_node, end_node):
        self.start = (start_node.x, start_node.y)
        self.end   = (end_node.x, end_node.y)

    def draw(self, screen, colour, w=1):
        pygame.draw.line(screen, colour, self.start, self.end, w)

################################################################################
################################ Functions ##################################### 
################################################################################

def distance(edge):
    x1 = edge.start[0]
    x2 = edge.end[0]
    y1 = edge.start[1]
    y2 = edge.end[1]
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def cost(node1, node2):
    return np.sqrt((node2.x - node1.x)**2 + (node2.y - node1.y)**2)

def permutations(edges):
    return itertools.permutations(edges)

def enumerate(nodes, screen):
    best_tour = None
    shortest = None
    current = 0

    # Clear screen
    screen.fill(white)    
    pygame.display.update()
    print(nodes)
    print("Creating list of all possible permutations.")
    if len(nodes) >= 10:
        print("This may take a while...")
    tours = permutations(nodes)
    tours = list(tours)
    print(len(tours))
    print("Done!")
    
    for tour in tours:
        if best_tour is not None:
            for node in best_tour:
                node.draw(screen, blue)
        tour.append(tour[0])
        print("Tour:", tour)
        for edge in tour:
            print(edge.start, edge.end)
            edge.draw(screen, blue)
            pygame.display.update()
            current += distance(edge)
        current += distance(tour[1])

        if shortest == None:
            shortest = current
            best_tour = tour
        elif current < shortest:
            shortest = current
            best_tour = tour 

        print("Best route:", best_tour)
        
            
def create_nodes(n):
    nodes = []
    for i in range(n):
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        nodes.append(Node(x,y))
    return nodes

def create_edges(nodes):
    edges = []
    for i in nodes:
        for j in nodes:
            if not i == j:
                edges.append(Edge(i,j))
    return edges

################################################################################
################################## Main ######################################## 
################################################################################


n = 5
nodes = create_nodes(n)
edges = create_edges(nodes)

a = ['a', 'b', 'c', 'd']

tours = list(itertools.permutations(a))
print(tours)
print(len(tours))

enumerate(nodes, screen)

exit = False
while(not exit):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit = True
            else:
                nodes = create_nodes(n)
                edges = create_edges(nodes)
    screen.fill(white)
    for node in nodes:
        node.draw(screen, black, 3)
        for edge in edges:
            edge.draw(screen, black)
    pygame.display.update()

pygame.quit()
quit()

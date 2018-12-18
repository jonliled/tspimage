#!/usr/bin/env python

# import time
import pygame
import itertools
# import pandas as pd
import numpy as np
#import travelUtils as tu
import tkinter as tk
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

def enumerate(edges, screen):
    best_tour = None
    shortest = None
    current = 0

    print("Creating list of all possible permutations.")
    if len(edges) >= 10:
        print("This may take a while...")
    tours = permutations(edges)

    for tour in tours:
        for edge in tour:
            edge.draw(screen, blue)
            current += distance(edge)
        current += distance(tour[1])

        if shortest == None:
            shortest = current
            best_tour = tour
        elif current < shortest:
            shortest = current
            best_tour = tour 
            
        
        

        

def brute(tours, canvas):
    costs = [] 
    cheapest = -1
    cheapest_tour = None
    m_tours = []
    n = 0

    for i in range(len(tours)):
        current_cost = 0
        current_tour = []
        for j in range(len(tours[0])):
            if j > 0:
                dist = (cost(tours[i][j], tours[i-1][j-1]))
                if dist > 0:
                    current_cost += dist
                    x1 = tours[i-1][j-1].x
                    y1 = tours[i-1][j-1].y
                    x2 = tours[i][j].x
                    y2 = tours[i][j].y
                else:
                    continue
            current_tour.append(tours[i][j].name)
            costs.append(current_cost)
        if cheapest == -1 and len(current_tour) == len(tours[0]):
            cheapest = current_cost
            cheapest_tour = current_tour
            print("Cheapest")
            print(current_cost, cheapest_tour)
        elif current_cost <= cheapest and len(current_tour) == len(tours[0]):
            print("Cheapest")
            print(current_cost)
            cheapest = current_cost
            cheapest_tour = current_tour
        n += 1
        print("Tours tested:", n, "/", len(tours))
        print("Current tour", current_cost, current_tour)
        print("Shortest so far: ", cheapest, cheapest_tour)
        os.system('clear')
    
    for city in cheapest_tour:
        print(city)
    #tu.Draw_Line(canvas, x1, y1, x2, y2)

    print("Tours tested:", n, "/", len(tours))
    print("Current tour", current_cost, current_tour)
    print("Shortest so far: ", cheapest, cheapest_tour)

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
print(len(tours))

enumerate(edges, screen)

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

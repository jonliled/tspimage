#!/usr/bin/env python

import numpy as np
import pygame
import random
import itertools

################################################################################
################################ Pygame ######################################## 
################################################################################

display_width  = 800
display_height = 600
x_min = 20
y_min = 20
x_max = display_width - 10
y_max = display_height - 100
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))

################################################################################
################################ Colours ####################################### 
################################################################################


black = (0,0,0)
white = (255,255,255)
red   = (170, 57, 57)
green = (122, 159, 53)
blue  = (34, 102, 102)
lblue = (102, 153, 153)



################################################################################
################################ Variables ##################################### 
################################################################################

fontsize = 25
font = pygame.font.SysFont(None, fontsize)


################################################################################
################################ Functions ##################################### 
################################################################################


def distance(start_node, end_node):
    x1 = start_node[1]
    x2 = end_node[1]
    y1 = start_node[2]
    y2 = end_node[2]
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def create_nodes(n):
    nodes = []
    for i in range(n):
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        nodes.append([i, x, y])
    nodes_array = np.array(nodes)
    return nodes

def create_edges(nodes):
    edges = []
    for i, node_i in enumerate(nodes):
        for j, node_j in enumerate(nodes):
            if i == j:
                continue
            node_start = node_i
            node_end = node_j
            length = distance(node_start, node_end)
            edges.append([i, j, length])
    edges = np.array(edges)
    return edges


def draw_full(screen, edges, nodes, colour=black, width=3):
        
    for node in nodes:
        x = node[1]
        y = node[2]
        txt = str(node[0])

        pygame.draw.circle(screen, colour, (x,y), 5, 0)
        text_to_screen(txt, black, (x -20,y -20))

    for edge in edges:

        ns = int(edge[0])
        ne = int(edge[1])

        xs = nodes[ns][1]
        xe = nodes[ne][1]
        ys = nodes[ns][2]
        ye = nodes[ne][2]

        start_pos = (xs, ys)
        end_pos = (xe, ye)

        pygame.draw.line(screen, colour, start_pos, end_pos, width)


def draw_route(screen, route, nodes, colour=black, width=3):
    for i, n in enumerate(route):
        pygame.draw.circle(screen, colour, (nodes[n][1], nodes[n][2]), 5, 0)

    for i, n in enumerate(route[:-1]):
        xs = nodes[route[i]][1]
        ys = nodes[route[i]][2]
        xe = nodes[route[i+1]][1]
        ye = nodes[route[i+1]][2]
        
        start = (xs, ys)
        end = (xe, ye)
        pygame.draw.line(screen, colour, start, end, width)

        x = nodes[route[i]][1] - 20
        y = nodes[route[i]][2] - 20
        pos = (x,y)
        txt = str(nodes[route[i]][0])

        text_to_screen(txt, black, pos)
        

def route_permutations(nodes):
    nodelist = [i for i in range(len(nodes))]
    routes = list(itertools.permutations(nodelist))

    route = []
    for r in routes:
        current = []
        for node in r:
            current.append(node)
        current.append(r[0])
        current = tuple(current)
        route.append(current)
    return route


def route_length(route, nodes):
    length = 0
    for i, r in enumerate(route[:-1]):
        length += distance(nodes[route[i]], nodes[route[i+1]])
        return length


def text_to_screen(txt, colour, pos):
    screen_text = font.render(txt, True, colour)
    screen.blit(screen_text, pos)


def full_enumeration(screen, nodes):
    edges = create_edges(nodes)

    routes = route_permutations(nodes)

    shortest = None
    shortest_route = None
    for route in routes:
        length = route_length(route, nodes)
        if shortest == None:
            shortest = length
            shortest_route = route
        if length < shortest:
            shortest = length
            shortest_route = route

        screen.fill(blue)
    
        if not shortest_route == None:
            draw_route(screen, shortest_route, nodes, green, 3)

        draw_route(screen, route, nodes, lblue, 3)

        pygame.draw.line(screen, black, (0, y_max), (display_width, y_max), 3)

       
        text_to_screen("Full enumeration", black, (display_width/2 - 40, y_max + 10))

        text_to_screen("Current route:", black, (20, y_max + 50))
        text_to_screen(str(route), black, (150, y_max + 50))
        text_to_screen("Length:", black, (325, y_max + 50))
        text_to_screen(str(length)[:5], black, (425, y_max + 50))

        text_to_screen("Shortest route:", black, (20, y_max + 70))
        text_to_screen(str(shortest_route), black, (150, y_max + 70))
        text_to_screen("Length:", black, (325, y_max + 70))
        text_to_screen(str(shortest)[:5], black, (425, y_max + 70))
    
        pygame.display.update()

    screen.fill(blue)
    draw_route(screen, shortest_route, nodes, green, 3)
    pygame.draw.line(screen, black, (0, y_max), (display_width, y_max), 3)

    text_to_screen("Full enumeration", black, (display_width/2 - 40, y_max + 10))

    text_to_screen("Shortest route:", black, (20, y_max + 70))
    text_to_screen(str(shortest_route), black, (150, y_max + 70))
    text_to_screen("Length:", black, (325, y_max + 70))
    text_to_screen(str(shortest)[:5], black, (425, y_max + 70))

    pygame.display.update()


def nearest_neighbour(screen, nodes, edges):
    route = []
    length = 0
    nodelist = nodes
    current_node = 0
    next_node = None
    edgelist = np.empty([1,3])
    print(edgelist)
    while (len(nodelist) > 0):
        for edge in edges:
            if edge[0] == current_node:
                edgelist = np.vstack([edgelist, edge])
                for edge in edgelist:
                    if edge[2] == min(edgelist[:,2]):
                        next_node = edge[1]
                        edges = np.delete(edges, (edgelist), axis=0)
    print(route)

################################################################################
################################ Main ########################################## 
################################################################################


n = 4
nodes = create_nodes(n)
edges = create_edges(nodes)


screen.fill(blue)
draw_full(screen, edges, nodes)
pygame.draw.line(screen, black, (0, y_max), (display_width, y_max), 3)

pygame.display.update()

exit = False
while(not exit):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit = True

            if event.key == pygame.K_SPACE:
                nodes = create_nodes(n)
                edges = create_edges(nodes)
                screen.fill(blue)
                draw_full(screen, edges, nodes)
                pygame.draw.line(screen, black, (0, y_max), (display_width, y_max), 3)
                pygame.display.update()

            if event.key == pygame.K_e:
                full_enumeration(screen, nodes)


pygame.quit()
quit()

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
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)



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
        x = nodes[route[i]][1] - 20
        y = nodes[route[i]][2] - 20
        pos = (x,y)
        txt = str(nodes[route[i]][0])
        
        text_to_screen(txt, black, pos)

    for i, n in enumerate(route[:-1]):
        xs = nodes[route[i]][1]
        ys = nodes[route[i]][2]
        xe = nodes[route[i+1]][1]
        ye = nodes[route[i+1]][2]
        
        start = (xs, ys)
        end = (xe, ye)
        pygame.draw.line(screen, colour, start, end, width)

        
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

''' Perform a full enumeration on a set of nodes and edges to find the
optimal solution to a TSP'''
def brute(screen, nodes, edges):
    length = None
    shortest_route = None

    print("Creating list of all possible permutations...")

    routes = route_permutations(nodes)

    print("Done!\n")

    print("Calculating the length of each route...")

    # Start of loop
    for current_route in routes:

        screen.fill(white)
        # Draw current and shortest routes
        draw_route(screen, current_route, nodes, black, 5)
        if shortest_route != None:
#            draw_route(screen, shortest_route, nodes, c, 3)
            pass
        current_length = route_length(current_route, nodes)
        if length == None:
            length = current_length
            shortest_route = current_route
        else:
            if (current_length < length):
                length = current_length
                shortest_route = current_route

        text_to_screen("Current route:", black, [450,425])
        text_to_screen(str(current_route), black, [600,425])

        text_to_screen("Current length:", black, [450,450])
        text_to_screen(str(current_length), black, [600,450])
        
        text_to_screen("Shortest route:", black, [450,475])
        text_to_screen(str(shortest_route), black, [600,475])
        
        text_to_screen("Shortest length:", black, [450,500])
        text_to_screen(str(length), black, [600,500])

        pygame.display.update()

    print("Done!\n")
    print("Shortest route:", shortest_route)
    print("Length: ", length)
    
    return (shortest_route, length)


################################################################################
################################ Main ########################################## 
################################################################################


print("\n-- Start of program --\n")


n = 8
nodes = create_nodes(n)

test_nodes = np.array(
   [[0, 500, 300], 
    [1, 100, 550],
    [2, 250, 20],
    [3, 300, 300]],
)

edges = create_edges(nodes)

routes = route_permutations(nodes)

shortest = None
shortest_route = None
for route in routes:
    if n < 7:
        clock.tick(20)
    length = route_length(route, nodes)
    if shortest == None:
        shortest = length
        shortest_route = route
    if length < shortest:
        shortest = length
        shortest_route = route

    screen.fill(white)
    
    if not shortest_route == None:
        draw_route(screen, shortest_route, nodes, green, 3)

    draw_route(screen, route, nodes, black, 3)

    pygame.draw.line(screen, black, (0, y_max), (display_width, y_max), 3)

    text_to_screen("Current route:", black, (20, y_max + 10))
    text_to_screen(str(route), black, (150, y_max + 10))
    text_to_screen("Length:", black, (300, y_max + 10))
    text_to_screen(str(length)[:5], black, (375, y_max + 10))

    text_to_screen("Shortest route:", black, (20, y_max + 30))
    text_to_screen(str(shortest_route), black, (150, y_max + 30))
    text_to_screen("Length:", black, (300, y_max + 30))
    text_to_screen(str(shortest)[:5], black, (375, y_max + 30))
    
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
#    draw(screen, edges, nodes, colour=black, width=3)


print("\n-- End of program --\n")

pygame.quit()
quit()

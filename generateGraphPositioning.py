import pygame
import numpy as np
from time import time

def createSpatialRepresentation(iterations = -1):
    '''
    This functions reads the graph from graph.txt and until the program is closed computes graph's spatial
    arrangement. Upon saving, the positions are saved to graphPositions.txt. It is possible to call this function
    without drawing the graph by setting iterations to the number of iterations we want to perform.
    '''

    # SIMULATION VARIABLES
    L = 0.2
    LINEAR_DRAG = 0.4
    SQUARE_DRAG = 0.4
    dt = 0.01
    INFO = False

    # load graph edge representation from txt file and
    # convert it to adjacency list

    f = open("temp/graph.txt", "r")
    lines = f.readlines()
    G = [[] for _ in range(int(lines[0]))]

    for line in lines[1:]:
        a, b = list(map(int, line.split()))
        G[a].append(b)

    f.close()

    maxNeighbours = len(max(G, key=lambda x: len(x)))
    positions = np.random.uniform(low=-1, high=1, size=[len(G), 2])
    velocities = np.zeros([len(G), 2])

    if iterations != -1:
        updateSimulation(L, LINEAR_DRAG, SQUARE_DRAG, G, positions, velocities, dt, INFO)
        return

    pygame.init()
    HEIGHT = 800
    WIDTH = 800
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Graph visualizer")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update simulation state
        updateSimulation(L, LINEAR_DRAG, SQUARE_DRAG, G, positions, velocities, dt, INFO)

        # draw to screen
        drawStart = time()
        screen.fill((0,0,0))

        # find max/min x/y
        xMax, xMin = max(positions, key=lambda x: x[0])[0], min(positions, key=lambda x: x[0])[0]
        yMax, yMin = max(positions, key=lambda x: x[1])[1], min(positions, key=lambda x: x[1])[1]
        intervals = np.array([xMax - xMin, yMax - yMin])
        offset = np.array([xMin, yMin])
        screenDims = np.array([WIDTH, HEIGHT])
        
        toScreenCoords = lambda x:  ((x - offset) / intervals * 0.8 + 0.1) * screenDims

        for i, neighbours in enumerate(G):
            for u in neighbours:
                if i < u:
                    
                    pos1 = toScreenCoords(positions[i])
                    pos2 = toScreenCoords(positions[u])
                    v = positions[i] - positions[u]
                    length = np.sqrt(np.sum(v*v))
                    c = (min(2*L, length) / (2*L)) * 255
                    pygame.draw.line(screen, (255 - c, 0, c), pos1, pos2)

        for i, pos in enumerate(positions):
            neighbours = len(G[i])
            size = max(3, neighbours * 10 / maxNeighbours)
            c = 255*neighbours/maxNeighbours
            pygame.draw.circle(screen, (55, c, c), toScreenCoords(pos), size)
        
        pygame.display.flip()

        if INFO:
            print("Drawing took:", time() - drawStart)

    pygame.quit()

    f = open("temp/graphPositions.txt", "w")
    for pos in positions:
        f.write(str(pos[0]) + " " + str(pos[1]) + "\n")
    f.close()

def updateSimulation(L, LD, SD, G, positions, velocities, dt, info):

    simStart = time()

    for i, neighbours in enumerate(G):
        pos = positions[i]
        bitmask = np.zeros(len(G))
        bitmask[neighbours] = 1
        neighboursPos = positions[bitmask == 1]
        bitmask[i] = 1
        nonNeighbourPos = positions[bitmask != 1]

        # neighbours are connected by spring
        v = neighboursPos - pos
        length = np.sqrt(np.sum(v*v, axis=1))
        scale = np.reshape(length - L, (len(length), -1))
        length = np.reshape(length, (len(length), -1))
        v /= length
        v *= scale * dt
        v = np.sum(v, axis=0)
        velocities[i] += v

        # non neighbours are repelled using force ~ 1/distance^2
        if len(nonNeighbourPos) != 0:
            v = nonNeighbourPos - pos
            length = np.sum(v*v, axis=1)
            length = np.reshape(length, (len(length), -1))
            v /= length
            v *= dt * 0.001
            v = np.sum(v, axis=0)
            velocities[i] -= v

    positions += velocities * dt

    # calculate drag
    dragStart = time()
    unit_vel = velocities / np.reshape(np.linalg.norm(velocities, axis=1), (-1, 1))
    val_vel =  np.reshape(np.sqrt(np.sum(velocities*velocities, axis=1)), (-1, 1))
    velocities -= (LD * val_vel + SD * val_vel * val_vel) * dt * unit_vel

    simEnd = time()
    if info:
        print("Simulation took =", simEnd - simStart, "FORCES =", dragStart - simStart, "DRAG =", simEnd - dragStart)

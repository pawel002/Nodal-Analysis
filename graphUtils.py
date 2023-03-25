import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import numpy as np
from math import log
from random import shuffle
from copy import deepcopy 

def writeGraphToFile(graph):
    f = open("temp/graph.txt", "w")
    f.write(str(len(graph)) + "\n")
    for u, neighbours in enumerate(graph):
        for v in neighbours:
            f.write(str(u) + " " + str(v[0]) + "\n")
    f.close()

def loadPositionsFromFile():
    f = open("temp/graphPositions.txt", "r")
    lines = f.readlines()
    return [list(map(float, line.split())) for line in lines]


def graphValidator(graph):
    M = [[0 for i in range(len(graph))] for j in range(len(graph))]
    for i, n in enumerate(graph):
        for j in n:
            jIdx = j[0]
            M[i][jIdx] = j[1]

    for i in range(len(graph)):
        for j in range(len(graph)):
            if M[i][j] != M[j][i]:
                print(i, j, "Generated wrong!")
                return
    
    print("Graph generated properly.")
    
def visualizeGraph(graph, positions):
    plt.scatter(*zip(*positions), zorder=10)
    for i, neighbours in enumerate(graph):
        for j, res in neighbours:
            if i < j:
                plt.plot([positions[i][0], positions[j][0]], [positions[i][1], positions[j][1]], c="black")
    plt.show
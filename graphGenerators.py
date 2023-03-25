import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import numpy as np
from math import log
from random import shuffle
from copy import deepcopy 

def generateCompleteGraph(size, minRes, maxRes):
    G = [[[j, 0] for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(i+1, size):
            res = np.random.uniform(minRes, maxRes)
            G[i][j][1] = res
            G[j][i][1] = res
    for i in range(size):
        G[i].pop(i)
    return G

def generateTreeGraph(size, minRes, maxRes):
    edges = [[i, j] for i in range(size) for j in range(i+1, size)]
    G = [[] for _ in range(size)]
    shuffle(edges)
    parent = [i for i in range(size)]
    c = 0
    for edge in edges:

        v1, v2 = edge

        while parent[v1] != v1:
            v1 = parent[v1]

        while parent[v2] != v2:
            v2 = parent[v2]

        if v1 != v2:
            parent[v2] = v1
            res = np.random.uniform(minRes, maxRes)
            G[v1].append((v2, res))
            G[v2].append((v1, res))
            c += 1

        if c == size - 1:
            break

    return G

def generateRegularGraph(size, regularCoef, minRes, maxRes):
    graph = nx.random_regular_graph(n=size, d=regularCoef)
    while not nx.is_connected(graph):
        graph = nx.random_regular_graph(n=size, d=regularCoef)

    G = [[] for i in range(size)]
    for edge in graph.edges():
        u, v = edge
        res = np.random.uniform(minRes, maxRes)
        G[u].append([v, res])
        G[v].append([u, res])

    return G

def generateGridGraph(size1, size2, minRes, maxRes):
    G = [[] for _ in range(size1 * size2)]
    for i in range(size1 * size2):
        for j in [1, size1]:

            nextIdx = i + j
            if (nextIdx % size1 == 0 and j == 1) or nextIdx >= size1 * size2:
                continue
            
            res = np.random.uniform(minRes, maxRes)
            G[i].append([nextIdx, res])
            G[nextIdx].append([i, res])

    positions = [[i, j] for i in range(size2) for j in range(size1)]
    return G, positions

def generateSmallWorldGraph(size, coef, prob, minRes, maxRes):
    graph = nx.newman_watts_strogatz_graph(n=size, k=coef, p=prob)

    G = [[] for _ in range(size)]
    for u, v in graph.edges():
        res = np.random.uniform(minRes, maxRes)
        G[u].append((v, res))
        G[v].append((u, res))

    R = 10
    angle = 2*np.pi / size
    positions = [[R*np.sin(angle*i), R*np.cos(angle*i)] for i in range(size)]
    return G, positions

def generateErdosRenyiGraph(size, minRes, maxRes):
    prob = 0.001
    graph = nx.fast_gnp_random_graph(n=size, p=prob)
    while not nx.is_connected(graph):
        prob += 0.001
        graph = nx.fast_gnp_random_graph(n=size, p=prob)

    G = [[] for _ in range(size)]
    for u, v in graph.edges():
        res = np.random.uniform(minRes, maxRes)
        G[u].append((v, res))
        G[v].append((u, res))

    return G

def mergeTwoGraphsWithBrigde(graph1, graph2, BridgeRes):
    # find node with least adjacent nodes
    idx1, s1 = 0, len(graph1[0])
    for i, n in enumerate(graph1):
        if len(n) < s1:
            idx1, s1 = i, len(n)

    idx2, s2 = 0, len(graph2[0])
    for i, n in enumerate(graph2):
        if len(n) < s2:
            idx2, s2 = i, len(n)

    G = [n for n in graph1]
    for n in graph2:
        G.append([[len(graph1) + x[0], x[1]] for x in n])

    #  connect idx1 and idx2 + len(G1)
    G[idx1].append([idx2 + len(graph1), BridgeRes])
    G[idx2 + len(graph1)].append([idx1, BridgeRes])
    return G
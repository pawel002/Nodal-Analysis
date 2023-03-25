import numpy as np

def nodalAnalysis(graph, start, end, SEM):
    G = np.zeros([len(graph), len(graph)])
    edges = []
    for u, neighbours in enumerate(graph):
        for v in neighbours:
            if u < v[0]:
                edges.append([u, v[0], v[1]])

    for u, v, r in edges:
        val = 1 / r
        G[u][u] += val
        G[u][v] -= val
        G[v][u] -= val
        G[v][v] += val

    G[start] = np.zeros(len(graph))
    G[start][start] = 1
    G[end] = np.zeros(len(graph))
    G[end][end] = 1

    I = np.zeros(len(graph))
    I[start] = SEM
    I[end] = 0

    P = np.linalg.solve(G, I.T)

    solution = []
    for u, neighbours in enumerate(graph):
        for v in neighbours:
            if u < v[0]:
                solution.append([u, v[0], (P[u] - P[v[0]]) / v[1], v[1]])

    return solution
import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import numpy as np
from math import log
from random import shuffle
from copy import deepcopy 

from graphUtils import *
from nodalAnalysisSolver import *
from generateGraphPositioning import createSpatialRepresentation

def solutionValidator(solution, start, end, SEM):
    # find current that goes through circuit
    current = 0
    for u, v, I, R in solution:
        if u == start or v == start:
            current += abs(I)

    # applying tellegens theorem
    s = - current * SEM
    for u, v, I, R in solution:
        s += I * I * R

    if s < 0.0001:
        print("Tellegens theorem check passed.")
    else:
        print("Tellegens theorem check NOT PASSED!")

    print("Sum:", s)

def visualizeSolution(graph, solution, positions, start, end, name):

    fig, ax = plt.subplots(1, 2, gridspec_kw={'width_ratios': [10, 1]})
    ax[0].axis('off')
    maxNeighbours = len(max(graph, key=lambda x: len(x)))

    # draw nodes
    for i, pos in enumerate(positions):

        neighbours = len(graph[i])
        size = 2*max(3, neighbours * 10 / maxNeighbours)

        if i == start:
            ax[0].scatter([pos[0]], [pos[1]], s=size, c = "blue", zorder = 5)
        elif i == end:
            ax[0].scatter([pos[0]], [pos[1]], s=size, c = "red", zorder = 5)
        else:
            ax[0].scatter([pos[0]], [pos[1]], s=size, c = "black", zorder = 5)

    # find max and min current
    minI = abs(min(solution, key=lambda x: abs(x[2]))[2])
    maxI = abs(max(solution, key=lambda x: abs(x[2]))[2])
    intervalI = maxI - minI

    # color bar
    cmap = mpl.cm.cool
    norm = mpl.colors.Normalize(vmin=minI, vmax=maxI)

    cb1 = mpl.colorbar.ColorbarBase(ax[1], cmap=cmap,
                                    norm=norm,
                                    orientation='vertical')
    cb1.set_label('Amps')

    # annotation opints container
    annotationPointsX = []
    annotationPointsY = []

    annotation = ax[0].annotate(
        text='',
        xy=(0, 0),
        xytext=(15, 15),
        textcoords='offset points',
        bbox={'boxstyle': 'round', 'fc': 'w'},
        arrowprops={'arrowstyle': '->'},
        zorder = 10
    )
    
    annotation.set_visible(False)

    for u, v, I, R in solution:
        # normalize amperage
        col = (abs(I) - minI) / intervalI
        col = max(min(col, 1.0), 0.0)
        finalColor = (col, 1.0 - col, 1.0)

        # plot line
        ax[0].plot([positions[u][0], positions[v][0]], [positions[u][1], positions[v][1]], c=finalColor)
        
        # plot direction of the current
        mx = (positions[v][0] + positions[u][0]) / 2
        my = (positions[v][1] + positions[u][1]) / 2
        dx = positions[v][0] - positions[u][0]
        dy = positions[v][1] - positions[u][1]
        l = np.sqrt(dx*dx + dy*dy)
        dx /= l*100
        dy /= l*100

        if I < 0:
            dx, dy = -dx, -dy

        ax[0].arrow(mx, my, dx, dy, shape='full', lw=0, length_includes_head=True, head_width=l/10, color=finalColor, zorder=5)

        annotationPointsX.append(mx)
        annotationPointsY.append(my)
        
    ax[0].set_title("Plot of a " + name + " graph with " + str(len(graph)) + " nodes and " + str(len(solution)) + " edges.")

    # creating live annotations
    scatter = ax[0].scatter(annotationPointsX, annotationPointsY, s = 50, c="r", alpha=0)

    def hover(event):
        annotation_visbility = annotation.get_visible()
        if event.inaxes == ax[0]:
            contained, idx = scatter.contains(event)
            if contained:
                i = idx['ind'][0]

                data_point_location = scatter.get_offsets()[i]
                annotation.xy = data_point_location

                text_label = f'I = {abs(solution[i][2]):0.6f} \nR = {solution[i][3]:0.6f}'
                annotation.set_text(text_label)

                annotation.set_alpha(0.4)

                annotation.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if annotation_visbility:
                    annotation.set_visible(False)
                    fig.canvas.draw_idle()
                

    fig.canvas.mpl_connect('motion_notify_event', hover)

    plt.show()

def graphWrapper(graph, start, end, SEM, name, pos=-1):
    
    graphValidator(graph)
    if pos == -1:
        writeGraphToFile(graph)
        createSpatialRepresentation()
        positions = loadPositionsFromFile()
    else:
        positions = pos

    solution = nodalAnalysis(graph, start, end, SEM)
    solutionValidator(solution, start, end, SEM)
    visualizeSolution(graph, solution, positions, start, end, name)
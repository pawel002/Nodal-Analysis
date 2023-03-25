# Nodal Analysis

## Description

This program lets you generate graphs with edges being resistors, apply a voltage source between two arbitrary nodes and solve it using nodal analysis. The solution is then visualized using a force-directed graph drawing technique implemented by me in pygame. The final visualization of the current is then created using matplotlib.

## Requirements
Code is written in python3 and uses the following libraries (with version that it certainly works on):

- matplotlib 3.4.3
- numpy 1.21.2
- networkx 3.0

## Generation

Users can select one of a few methods of graph generation (with appropriate parameters for a given type of graph):

- Complete Graph
- Tree
- Regular Graph
- 2D Grid Graph
- Small-World
- Erdos-Renyi Graph

Also, there is a method which can merge two graphs with a bridge.

## Solution

The solution is obtained through [Nodal Analysis](https://en.wikipedia.org/wiki/Nodal_analysis) in a matrix form, where the potential of staring node is equal to E and sink node is equal to 0. Having potential and resistance between two points, Ohm's law is used to obtain current. The solution is checked using Tellegen's theorem.

## Visualization

Some of the graphs have their own method of generating visualization, e.g. grid graph where nodes are placed on a 2D grid and small-world graph where nodes are placed on a circle. For other graphs, my force-directed graph drawing is used. Simulation places the nodes in random place on the plane and nodes that are connected via an edge are connected with a spring that follows Hooke's law and the edges that aren't connected repel each other with force proportional to 1/distance^2. The user can change the initial length of springs and the linear and square drag coefficient. After the placement of nodes is saved, then the visualization of current is generated. The color bar describes the amperage on each edge and arrows describe the direction of the current. Upon hovering on the middle of an edge, you will see the exact values of the resistance and current.

## Results

Two gifs which show the process of "untangling" the graph.


https://user-images.githubusercontent.com/95650330/227727781-e8fa7a30-e31a-4843-bb99-52c6f9321b94.mp4


https://user-images.githubusercontent.com/95650330/227727790-c0746151-30a8-4d6b-87a2-6e12c7ad02fb.mp4

Here are some end results that I got using this program.

https://github.com/pawel002/Nodal-Analysis/blob/main/graphs.png?raw=true





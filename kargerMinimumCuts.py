"""
The file contains the adjacency list representation of a simple undirected graph.
There are 200 vertices labeled 1 to 200.
The first column in the file represents the vertex label, and the particular row (other entries except the first column) tells all the vertices that the vertex is adjacent to.
So for example, the 6th row looks like : "6 155 56  52  120 ......".
This just means that the vertex with label 6 is adjacent to (i.e., shares an edge with) the vertices with labels 155,56,52,120,......,etc

Your task is to code up and run the randomized contraction algorithm for the min cut problem and use it on the above graph to compute the min cut.
(HINT: Note that you'll have to figure out an implementation of edge contractions.
Initially, you might want to do this naively, creating a new graph from the old every time there's an edge contraction.
But you should also think about more efficient implementations.)
(WARNING: As per the video lectures, please make sure to run the algorithm many times with different random seeds,
and remember the smallest cut that you ever find.)  Write your numeric answer in the space provided.
So e.g., if your answer is 5, just type 5 in the space provided.
"""

import random
import copy
import math

class KargerMinCut:
    def __init__(self, fileName):
        self.graph = {}
        self.edge_count = 0
        self.vertex_count = 0

        f = open(fileName, "r")

        for line in f:
            items = line.rstrip('\n').rstrip('\t').rstrip(" ").split("\t")
            vertex = items[0]
            edges = items[1:]
            self.graph[vertex] = edges
            self.edge_count += len(edges)
            self.vertex_count += 1


    def find_min_cut(self, graph):
        edge_count = self.edge_count
        while len(graph) > 2:
            v1, v2 = self.pick_random_edge(graph, edge_count)

            edge_count -= len(graph[v1])
            edge_count -= len(graph[v2])

            for adj in graph[v2]:
                if adj != v1:
                    # merge all of the edges of v2 with v1
                    graph[v1].append(adj)
                    # update all vertices that point to an edge in v2 to point to v1 instead
                    graph[adj].append(v1)

                # remove all references to deleted node v2
                graph[adj].remove(v2)
            
                

            # update the total number of edges
            edge_count += len(graph[v1])

            # remove v2 from graph
            del graph[v2]

        # once we get to two nodes in the graph
        for edges in graph.values():
            min_cut = len(edges)
        return min_cut
            

    def pick_random_edge(self, graph, edge_count):
        # selects a number from 1 to edge_count inclusive
        rand_edge = random.randint(1, edge_count)
        for vertex, vertex_edge in graph.items():
            if len(vertex_edge) < rand_edge:
                rand_edge -= len(vertex_edge)
            else:
                v1 = vertex
                v2 = graph[v1][rand_edge-1]
                return (v1, v2)
    
    def min_cut(self):
        i = 0
        min_cut = float('inf')
        while i < (self.vertex_count):
              # A deep copy creates a new object
              cuts = self.find_min_cut(copy.deepcopy(self.graph))
              if cuts < min_cut:
                  min_cut = cuts
              i += 1
        return min_cut

s = KargerMinCut("kargerMinCut.txt")
ans = s.min_cut()
print(ans)

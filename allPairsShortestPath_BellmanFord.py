"""
Implementing All Pairs Shortest Path using Bellman Ford


Strucute of text file:
The first line indicates the number of vertices and edges, respectively.
Each subsequent line describes an edge (the first two numbers are its tail and head, respectively) and its length (the third number).
NOTE: some of the edge lengths are negative.
NOTE: These graphs may or may not have negative-cost cycles.

Your task is to compute the "shortest shortest path".
Precisely, you must first identify which, if any, of the three graphs have no negative cycles.
For each such graph, you should compute all-pairs shortest paths and remember the smallest one (i.e., compute min_u,v v∈V d(u,v)min where d(u,v) denotes the shortest-path distance from u to v). 

If each of the three graphs has a negative-cost cycle, then enter "NULL" in the box below.
If exactly one graph has no negative-cost cycles, then enter the length of its shortest shortest path in the box below.
If two or more of the graphs have no negative-cost cycles, then enter the smallest of the lengths of their shortest shortest paths in the box below.

"""


import time
class Graph:

    def __init__(self):
        self.graph = []

    def addEdge(self, s, d, w):
        self.graph.append([s, d, w])

    def __iter__(self):
        return iter(self.graph)

class BellmanFord:
    def __init__(self, fileName):
        self.graph = Graph()
        self.vertexCount = 0
        
        f = open(fileName, "r")
        firstline = True

        for line in f:
            # extract the number of vertices from the first line of the txt file
            if firstline:
                graphInfo = line.rstrip('\n').split(" ")
                self.vertexCount = int(graphInfo[0])
                firstline = False
                continue

            # build the graph from the txt file
            # file organized with [vertex1 vertex2 edge_cost]
            v1, v2, weight = line.rstrip('\n').split(" ")
            self.graph.addEdge(int(v1),int(v2),int(weight))

    def bellman_ford(self, src):
        # array indexed at zero
        # add a decoy element at position zero since vertices start at 1
        dist = [float("Inf")] * (self.vertexCount+1)
        prev = [-1] * (self.vertexCount+1)
        # Mark the source vertex
        dist[src] = 0
        prev[src] = src
        shortestPath = float('inf')

        # use updatedDist variable to keep track of if the dist array changes in an iteration
        # if there are no changes then we can stop early
        updatedDist = True

        # only want to iterate vertexCount-1 times
        i = 1
        dest = None
        while updatedDist and i < self.vertexCount:
            updatedDist = False
            
            for s, d, w in self.graph:
                if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                    dist[d] = dist[s] + w
                    if dist[d] < shortestPath:
                        shortestPath = dist[d]
                        dest = d
                    
                    prev[d] = s
                    updatedDist = True
            i += 1
                

        # check if there is a negative cycle
        # run it once more to see if we find a shortest path better than the optimal solution
        for s, d, w in self.graph:  
            if dist[s] != float("Inf") and dist[s] + w < dist[d]:  
                raise Exception("Graph contains negative weight cycle")


        
        path = self.getPath(prev, dest) if shortestPath != float("inf") else None        

        return shortestPath, path

    # method to print out the shortest path
    def getPath(self, prev, dest):
        path = ""

        # Base case: where dest is the source
        if prev[dest] == dest:
            path += str(dest)
        
        else:
            path += self.getPath(prev, prev[dest])
            path += " -> " + str(dest)

        return path

    def getShortestPath(self):
        start = time.time()
        shortestPath = float('inf')
        path = None

        # want to get the shortest path starting at each vertex, and return the smallest of all those paths
        for v in range(1, self.vertexCount+1):
            singleSrcShortestPath = self.bellman_ford(v)
            if singleSrcShortestPath[0] < shortestPath:
                shortestPath = singleSrcShortestPath[0]
                path = singleSrcShortestPath[1]
        end = time.time()
        print("total time: ", end - start)
        return shortestPath, path

            
            
bf = BellmanFord("g3.txt")
ans = bf.getShortestPath()
print("shortest path: %f, path: %s" % (ans[0], ans[1]))


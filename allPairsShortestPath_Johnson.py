"""
Implementing All Pairs Shortest Path using Johnson's algorithm
- implements both Bellman Ford and Dijkstra


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
class Vertex:
    def __init__(self, key):
        self.id = key
        # map adjacent nodes to the edge length
        self.connectedTo = {}

    def addNeighbour(self, nbr, weight):
        self.connectedTo[nbr] = weight

    def getConnections(self):
        return self.connectedTo.keys()

    def getEdges(self):
        return [[self.id, v, weight] for v, weight in self.connectedTo.items()]

    def updateEdge(self, weights):
        for d in self.connectedTo.keys():
            self.connectedTo[d] += weights[self.id] - weights[d]

class Graph:
    def __init__(self):
        self.vertList = {}

    def addVertex(self, key):
        if key not in self.vertList:
            newVertex = Vertex(key)
            self.vertList[key] = newVertex

    def addEdge(self, source, dest, weight):
        # check to make sure the source and dest keys are in the vertList
        # if not need to create Vertex
        if source not in self.vertList:
            self.addVertex(source)

        if dest not in self.vertList:
            self.addVertex(dest)

        # get the source vertex and add the connection to the dest vertex
        self.vertList[source].addNeighbour(dest, weight)

    def getVertex(self, key):
        return self.vertList[key]
        
    def getVertices(self):
        return self.vertList.values()

    # called by saying for item in graph
    def __iter__(self):
        return iter(self.vertList.values())

    def getEdges(self):
        #return [v.getEdges() for v in self.vertList.values()]
        edges = []
        for v in self.vertList.values():
            edges.extend(v.getEdges())
        return edges

    def updateEdges(self, weights):
        for v in self.vertList.values():
            v.updateEdge(weights)

"""
implementing a min heap by using a binary tree 

to make the heap work efficiently, we will take advantage of the logarithmic nature of the binary tree
to guarantee log performance, the tree must be balanced
a balanced binary tree has roughly the same number of nodes in the left and right subtrees
keep the tree balanced by creating a complete binary tree

the left child of a parent at position p is found at position 2p
the right child of parent at position p is found at position 2p+1

at index 0 just set a default value, use index 1 as the root
left child is 2*1 = 2, right child is 2*1+1 = 3
"""
class MinHeap:
    def __init__(self):
        # using a list implementation
        # has a single element of [Vertex(-inf), -inf]
        # this is because of the 2p and 2p+1 rule and so simple integer division can be used
        self.heapList = [[Vertex(float('-inf')), float('-inf')]]
        # current size is zero
        self.currentSize = 0
        # keep a dict to map the vertex to it's position in the heap 
        self.pos = {}


    # on the initial insert of all items in the heap, we are setting the distance to infinity
    # just append them all in the heapList, don't need to worry about inserting in any order since they all have the same distance
    def initInsert(self, vertex, dist, i):
        self.heapList.append([vertex, dist])
        # set the position to the current index in the heapList
        self.pos[vertex] = i
        self.currentSize += 1
        
    # insert method - O(logn)
    # append new item to the end of the list
    # appending guarantees we will maintain a complete tree but we will violate the heap structure property
    # can regain the heap structure by comparing the newly added item with its parent
    # if new item is less than parent, swap

    def insert(self, vertex, dist):
        #start by appending the item to the list
        self.heapList.append([vertex, dist])
        self.currentSize += 1
        self.pos[vertex] = self.currentSize
        #want to percolate up the item at the currentSize index
        self.percUp(self.currentSize)

    def percUp(self,i):
        while i // 2 > 0:
            #if the value at the new index is less then the parent index, swap
            if self.heapList[i][1] < self.heapList[i // 2][1]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp

                # update the positing of the swapped vertices
                self.pos[self.heapList[i // 2][0]] = i // 2
                self.pos[self.heapList[i][0]] = i

            i = i // 2
        

    # delete min method
    # the root of the tree (index 1) is the min item, easy to delete
    # then we need to restore the heap structure
    # first take the last item in the list and move it to the root
    # then percolate down the new root to its proper position
    # run time is the depth of the tree O(logn)

    def percDown(self, i):
        
        #check to make sure there is a child node
        while (i*2) <= self.currentSize:

            #get the minimum child
            mc = self.minChild(i)

            #if the child is less than the item, swap
            if self.heapList[i][1] > self.heapList[mc][1]:

                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp

                # update the positions of the swapped vertices
                self.pos[self.heapList[mc][0]] = mc
                self.pos[self.heapList[i][0]] = i

            #set the new i to be the index of the child
            i = mc

    def minChild(self, i):
        #if there is no right child, then we know to return the left child
        if i*2+1 > self.currentSize:
            return i*2

        #else return whichever child is smaller
        else:
            if self.heapList[i*2][1] < self.heapList[i*2+1][1]:
                return i*2
            else:
                return i*2+1

    def delMin(self):
        #keep track of the value we are deleting
        retval = self.heapList[1]
        #set the root element to the last element
        self.heapList[1] = self.heapList[self.currentSize]

        # update the positon of the vertex that has just been moved up to the root
        self.pos[self.heapList[1][0]] = 1
        
        #update the current size
        self.currentSize -= 1
        #remove last item with pop
        self.heapList.pop()
        #percDown the new value at the root
        self.percDown(1)
        #return the deleted root value
        return retval
            

    def changeDistance(self, v, dist):
        # get the current position of the vertex in the heapList
        i = self.pos[v]
        # update the distance
        self.heapList[i][1] = dist
        # move the item up if it is now smaller then it's parent
        self.percUp(i)
 
        
            

class Johnson:
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
            s, d, w = line.rstrip('\n').split(" ")
            self.graph.addEdge(int(s),int(d),int(w))

        # add a source vertex 0 and connect to all other vertices with a distance of 0
        for v in range(1, self.vertexCount+1):
            self.graph.addEdge(0,v,0)
        

    def bellman_ford(self, src):
        # array indexed at zero
        # add a decoy element at position zero since vertices start at 1
        dist = [float("Inf")] * (self.vertexCount+1)
        # Mark the source vertex
        dist[src] = 0
        
        # use updatedDist variable to keep track of if the dist array changes in an iteration
        # if there are no changes then we can stop early
        updatedDist = True

        # only want to iterate vertexCount-1 times
        i = 1
        while updatedDist and i < self.vertexCount:
            updatedDist = False
            
            for s, d, w in self.graph.getEdges():
                if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                    dist[d] = dist[s] + w
                    
                    updatedDist = True
                    
            i += 1
                

        # check if there is a negative cycle
        # run it once more to see if we find a shortest path better than the optimal solution
        for s, d, w in self.graph.getEdges():  
            if dist[s] != float("Inf") and dist[s] + w < dist[d]:  
                raise Exception("Graph contains negative weight cycle") 
                

        return dist

    def dijkstra(self, src, weights):
        minHeap = MinHeap()
        distances = [float('inf')] * (self.vertexCount+1)
        prev = [-1] * (self.vertexCount+1)
        prev[src] = src
        i = 1
        for vertex in self.graph:
            minHeap.initInsert(vertex, float('inf'), i)
            i += 1

        
        startVertex = self.graph.getVertex(src)
        distances[src] = 0

        minHeap.changeDistance(startVertex, 0)
        
        # Note: don't need to keep track of visited vertices
        # vertices that have been visited are already populated with the shortes path
        # the condition newDis < self.distances[nbr] will never be true for visited vertices
        while minHeap.currentSize:
            
            v, dis = minHeap.delMin()

            for nbr, weight in v.connectedTo.items():
                
                newDis = dis + weight
                if newDis < distances[nbr]:
                    distances[nbr] = newDis
                    # update the distance if we've found a shorter path
                    d = self.graph.getVertex(nbr)
                    minHeap.changeDistance(d, newDis)
                    prev[nbr] = v.id

        minDist = float('inf')
        dest = None
        for i in range(1, self.vertexCount+1):
            if i != src:
                distances[i] -= weights[src] - weights[i]
                if distances[i] < minDist:
                    minDist = distances[i]
                    dest = i

        # if a path shortest path to another vertex exists, get the path
        # minDist will only be infinite is the vertex doesn't point to any other vertices
        
        path = self.getPath(prev, dest) if minDist != float("inf") else None
        return minDist, path

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
        
        # run bellman_ford once on the source node 0
        # this will return an array of a weight for each vertex
        # the weight is used to update the edge costs to make all edges positive
        weights = self.bellman_ford(0)
        self.graph.updateEdges(weights)

        shortestPath = float('inf')
        path = None
        for vertex in range(1, self.vertexCount+1):
            # get the shortest path using vertex as the source
            singleSrcShortestPath = self.dijkstra(vertex, weights)
            if singleSrcShortestPath[0] < shortestPath:
                shortestPath = singleSrcShortestPath[0]
                path = singleSrcShortestPath[1]

        end = time.time()
        print("total time: ", end - start)
        return shortestPath, path

j = Johnson("g3.txt")
ans = j.getShortestPath()
print("shortest path: %f, path: %s" % (ans[0], ans[1]))


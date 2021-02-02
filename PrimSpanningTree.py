import random

class Vertex:
    def __init__(self, key):
        self.key = key
        self.connectedTo = {}

    def addEdge(self, vertex, weight):
        self.connectedTo[vertex] = weight

    def getConnections(self):
        return self.connectedTo.items()


class Graph:
    def __init__(self):
        self.vertList = {}

    def addEdge(self, v1, v2, weight):
        if v1 not in self.vertList:
            self.vertList[v1] = Vertex(v1)
        if v2 not in self.vertList:
            self.vertList[v2] = Vertex(v2)
        
        self.vertList[v1].addEdge(v2, weight)
        self.vertList[v2].addEdge(v1, weight)

    def getVertex(self, key):
        return self.vertList[key]

class MinHeap:
    def __init__(self, vertexCount):
        # using an array implementation to build a min heap
        # think of it as a complete binary tree
        # set a decoy element at positon 0, don't want to use position zero
        # the root will be at position 1 in the array
        # left child at position 2*parentIndex
        # right child at position 2*parentIndex+1
        self.heapList = [[Vertex(float('-inf')), float('-inf')]]
        self.size = 0

        # keep track of the position of each vertex in the array
        # this is used to delete a specific element in the heap
        self.positions = {}

        # want to initialize the heap with to contain all vertices with a min edge of inf
        # don't care about ordering because the key will be the same for every vertex
        for i in range(1, vertexCount+1):
            vertex = str(i)
            self.heapList.append([vertex, float('inf')])
            self.positions[vertex] = i
            self.size += 1

    def __len__(self):
        return self.size


    # insert method - O(logn)
    # append new item to the end of the list
    # appending guarantees we will maintain a complete tree but we will violate the heap structure property
    # can regain the heap structure by comparing the newly added item with its parent
    # if new item is less than parent, swap
    
    def insert(self, vertex, cost):
        # add new element to the end of the list
        self.heapList.append([vertex, cost])
        self.size += 1
        # move the elment up to where it belongs in the heap
        self.percUp(self.size)
        self.positions[vertex] = self.size

    def percUp(self, i):
        while i // 2 > 0:
            #if the value at the new index is less then the parent index, swap
            if self.heapList[i][1] < self.heapList[i // 2][1]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp

                # need to update the positions of the swapped vertices
                self.positions[self.heapList[i // 2][0]] = i // 2
                self.positions[self.heapList[i][0]] = i

            i = i // 2


    # extract min method
    # the root of the tree (index 1) is the min item, easy to delete
    # then we need to restore the heap structure
    # first take the last item in the list and move it to the root
    # then percolate down the new root to its proper position
    # run time is the depth of the tree O(logn)

    def extractMin(self):
        #keep track of the value we are deleting
        retval = self.heapList[1]
        #set the root element to the last element
        self.heapList[1] = self.heapList[self.size]

        self.positions[self.heapList[1][0]] = 1
        
        #update the current size
        self.size -= 1
        #remove last item with pop
        self.heapList.pop()
        #percDown the new value at the root
        self.percDown(1)
        #return the deleted root value
        return retval

    def percDown(self, i):
        
        #check to make sure there is a child node
        while (i*2) <= self.size:

            #get the minimum child
            mc = self.minChild(i)

            #if the child is less than the item, swap
            if self.heapList[i][1] > self.heapList[mc][1]:

                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp

                # update the positions of the swapped vertices
                self.positions[self.heapList[mc][0]] = mc
                self.positions[self.heapList[i][0]] = i

            #set the new i to be the index of the child
            i = mc

    def minChild(self, i):
        #if there is no right child, then we know to return the left child
        if i*2+1 > self.size:
            return i*2

        #else return whichever child is smaller
        else:
            if self.heapList[i*2][1] < self.heapList[i*2+1][1]:
                return i*2
            else:
                return i*2+1

    def update(self, vertex, newCost):
        # get the current min edge cost of the vertex
        index = self.positions[vertex]
        currCost = self.heapList[index][1]

        if newCost < currCost:
            # want to update the min edge cost of the heap
            # once we change it, need to restore the heap structure by percolating up
            self.heapList[index][1] = newCost
            self.percUp(index)
            
                         

class MinSpanningTree:
    def __init__(self, fileName):
        self.graph = Graph()
        self.vertexCount = 0
        
        f = open(fileName, "r")
        firstline = True

        for line in f:
            # extra the number of vertices from the first line of the txt file
            if firstline:
                graphInfo = line.rstrip('\n').split(" ")
                self.vertexCount = int(graphInfo[0])
                firstline = False
                continue

            # build the graph from the txt file
            # file organized with [vertex1 vertex2 edge_cost]
            v1, v2, weight = line.rstrip('\n').split(" ")
            self.graph.addEdge(v1,v2,int(weight))

    def __pickStartVertex(self):
        return str(random.randrange(1, self.vertexCount + 1))

    # option 1:
    # slow method O(mn)
    def minSpanningTree(self):
        seen = set()
        # keep track of the overall cost of the minimum spanning tree
        mstCount = 0
        
        # choose any random vertex to start
        startVertex = self.__pickStartVertex()

        # add startVertex to seen set
        seen.add(startVertex)

        # while there are still vertices to consider
        # find the cheapest edge [u,v] where u is in seen and v is not
        while len(seen) < self.vertexCount:
            minEdge = float('inf')
            nextVertex = None

            # iterate through all vertices in seen
            # replace the minEdge, nextVertex when we find a smaller edge
            for v in seen:
                v1 = self.graph.getVertex(v)
                for v2, edge in v1.getConnections():
                    if v2 not in seen:
                        if edge < minEdge:
                            minEdge = edge
                            nextVertex = v2

            if not nextVertex:
                # this would only occur if we can't get from one node to another
                raise Exception("Error: input graph is not connected")
            
            
            seen.add(nextVertex)
            mstCount += minEdge
        
        return mstCount

    # option 2:
    # fast method O(mlogn)
    def minSpanningTreeHeap(self):
        minHeap = MinHeap(self.vertexCount)
        seen = set()
        # keep track of the overall cost of the minimum spanning tree
        mstCount = 0

        # choose any random vertex to start
        startVertex = self.__pickStartVertex()
        # update the heap to show the startVertex has an edge cost of zero
        minHeap.update(startVertex, 0)
        
        while minHeap:
            minVertex, minEdge = minHeap.extractMin()
            seen.add(minVertex)
            mstCount += minEdge

            v1 = self.graph.getVertex(minVertex)

            for v2, edge in v1.getConnections():
                if v2 not in seen:
                    # need to compare edge costs
                    # if the connection from v1 to v2 has a smaller edge cost than v2 currently has saved, need to update the edge cost
                    minHeap.update(v2, edge)

        return mstCount 
                    
        
MST = MinSpanningTree("edges.txt")
ans1 = MST.minSpanningTree()
print(ans1)
ans2 = MST.minSpanningTreeHeap()
print(ans2)

    
    
    

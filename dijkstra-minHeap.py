class Vertex:
    def __init__(self, key):
        self.id = key
        # map adjacent nodes to the edge length
        self.connectedTo = {}

    def addNeighbour(self, nbr, weight):
        self.connectedTo[nbr] = weight

    def getConnections(self):
        return self.connectedTo.keys()

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
        self.vertList[source].addNeighbour(self.vertList[dest], weight)

    def getVertex(self, key):
        return self.vertList[key]
        
    def getVertices(self):
        return self.vertList.values()

    # called by saying for item in graph
    def __iter__(self):
        return iter(self.vertList.values())

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

    def insert(self, k):
        #start by appending the item to the list
        self.heapList.append(k)
        self.currentSize += 1
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


        
class Solution:
    def __init__(self):
        self.graph = Graph()

        # default this to inf for all vertexs
        self.distances = {}

    def buildGraph(self, fileName):
        f = open(fileName, "r")

        for line in f:
            items = line.rstrip('\n').strip().split("\t")
            source, neighbours = items[0], items[1:]

            self.graph.addVertex(int(source))

            for nbr in neighbours:
                dest, weight = nbr.split(",")
                self.graph.addEdge(int(source), int(dest), int(weight))


    def shortest_path(self, start):
        minHeap = MinHeap()
        i = 1
        for vertex in self.graph:
            self.distances[vertex] = float('inf')
            minHeap.initInsert(vertex, float('inf'), i)
            i += 1

        
        startVertex = self.graph.getVertex(start)
        self.distances[startVertex] = 0

        minHeap.changeDistance(startVertex, 0)
        
        # Note: don't need to keep track of visited vertices
        # vertices that have been visited are already populated with the shortes path
        # the condition newDis < self.distances[nbr] will never be true for visited vertices
        while minHeap.currentSize:
            
            v, dis = minHeap.delMin()

            for nbr, weight in v.connectedTo.items():
                
                newDis = dis + weight
                if newDis < self.distances[nbr]:
                    self.distances[nbr] = newDis
                    # update the distance if we've found a shorter path
                    minHeap.changeDistance(nbr, newDis)
                    
        return self.distances
                


s = Solution()
s.buildGraph("dijkstrasData.txt")
distances = s.shortest_path(1)


ans = [(k.id,v) for k,v in distances.items() if k.id in [7,37,59,82,99,115,133,165,188,197]]
print(sorted(ans, key=lambda x: x[0]))



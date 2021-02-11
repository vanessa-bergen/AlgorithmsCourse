"""

In this programming problem you'll code up the dynamic programming algorithm for computing a maximum-weight independent set of a path graph.

This file describes the weights of the vertices in a path graph (with the weights listed in the order in which vertices appear in the path).
It has the following format:

[number_of_vertices]

[weight of first vertex]

[weight of second vertex]

...

For example, the third line of the file is "6395702," indicating that the weight of the second vertex of the graph is 6395702. 

Your task in this problem is to run the dynamic programming algorithm (and the reconstruction procedure) from lecture on this data set.
The question is: of the vertices 1, 2, 3, 4, 17, 117, 517, and 997, which ones belong to the maximum-weight independent set?
(By "vertex 1" we mean the first vertex of the graph---there is no vertex 0.)
In the box below, enter a 8-bit string, where the ith bit should be 1 if the ith of these 8 vertices is in the maximum-weight independent set, and 0 otherwise.
For example, if you think that the vertices 1, 4, 17, and 517 are in the maximum-weight independent set and the other four vertices are not, then you should enter the string 10011010 in the box below.

"""

class MaxWeightIndependentSet:
    def __init__(self, fileName):

        self.weights = [0]
        
        
        f = open(fileName, "r")
        firstline = True
        i = 1
        for line in f:
            # extract the number of vertices from the first line of the txt file
            if firstline:
                graphInfo = line.rstrip('\n').split(" ")
                self.vertexCount = int(graphInfo[0])
                firstline = False
                continue

            weight = int(line.rstrip('\n'))
            self.weights.append(weight)
        

    def calcMaxWeight(self):
        # use the cache to store the maximum values without any adjacent vertices
        cache = [0 for _ in range(self.vertexCount+1)]
        cache[1] = self.weights[1]
        
        for i in range(2, self.vertexCount + 1):
            # cases for the max weight at i:
            # case 1: don't include vertex i and take the previous max weight
            # case 2: or include vertex i, add weights[i] to the previous max weight at i-2 so that adjacent node isn't included
            cache[i] = max(cache[i-1], cache[i-2] + self.weights[i])

        # last element in the cache will be the max weight
        maxWeight = cache[-1]

        # retrace the path
        path = self.getPath(cache)

        outputString = ""
        for i in [1,2,3,4,17,117,517,997]:
            outputString += str(1) if i in path else str(0)

        return maxWeight, outputString
        

    def getPath(self, cache):
        i = len(cache)-1
        path = []

        # traverse the path right to left
        while i > 0:
            # case 1 wins, don't include the vertex in the current path
            if cache[i-1] >= cache[i-2] + self.weights[i]:
                i -= 1
            else:
                # case 2 wins, vertex is included in path, decrement i by 2 since the neighbour cannot be included in the path
                path = [i] + path
                i -= 2

        return path
            
            
        

s = MaxWeightIndependentSet("mwis.txt")
maxWeight, output = s.calcMaxWeight()
print("max weight: %i, output string: %s" % (maxWeight, output))

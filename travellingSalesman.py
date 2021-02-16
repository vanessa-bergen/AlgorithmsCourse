"""
In this assignment you will implement one or more algorithms for the traveling salesman problem, such as the dynamic programming algorithm covered in the video lectures.
Here is a data file describing a TSP instance.

The first line indicates the number of cities.
Each city is a point in the plane, and each subsequent line indicates the x- and y-coordinates of a single city.  

The distance between two cities is defined as the Euclidean distance --- that is, two cities at locations (x,y) and (z,w) have distance sqrt((x-z)^2 + (y-w)^2) between them.  

In the box below, type in the minimum cost of a traveling salesman tour for this instance, rounded down to the nearest integer.

"""

import math
from collections import defaultdict
class TSP:
    def __init__(self, fileName, start):
        self.graph = []
        self.memo = []
        self.N = 0
        self.start = start
        
        cities = []
        
        f = open(fileName, "r")
        firstline = True

        for line in f:
            # extra the number of vertices from the first line of the txt file
            if firstline:
                graphInfo = line.rstrip('\n')
                self.N = int(graphInfo)
                firstline = False
                continue

            # add the city's coordinates
            x, y = line.rstrip('\n').split(" ")
            cities.append((float(x),float(y)))

        
        self.memo = defaultdict(dict)
        self.buildGraph(cities)
        self.solve()
        minCost = self.minTourCost()
        print(minCost)

    def buildGraph(self, cities):

        # building an adjacency matrix to store the distances
        for i in range(self.N):
            self.graph.append([])
            for j in range(self.N):
                
                if i == j:
                    self.graph[i].append(0)
                else:
                    x,y = cities[i]
                    z,w = cities[j]

                    dist = math.sqrt((x-z)**2 + (y-w)**2)

                    self.graph[i].append(dist)

        for i in range(self.N):
            if i == self.start:
                continue
            # store the distance from the starting point to every other city in memo
            # use binary representation to show which nodes have been visited
            # ex: if start city = 0 and  destination city i = 2
            # then the binary representation is 101 to show cities 0 and 2
            # value of memo[101] is another dictionary which will have the last node visited and the distance
            self.memo[1<<self.start | 1<<i] = { i : self.graph[self.start][i] }
            
                
    def solve(self):
        # s is the size of the subset we want to look at
        # so when s is 3, we want to look at vertices {1,2,3}
        for s in range(3, self.N + 1):
            # geneate all bit sets
            # so when s is 3 this will return 0111, 1110, 1101, 1011
            for subset in self.combinations(s, self.N):
                # need the start vertex to be included in the subset
                if self.notIn(self.start, subset):
                    continue

                for next in range(self.N):
                    if next == self.start or self.notIn(next, subset):
                        continue

                    # need to set the bit set to not include the next vertex
                    state = subset ^ (1<<next)
                    minDist = float('inf')

                    for end in range(self.N):
                        if end == self.start or end == next or self.notIn(end, subset):
                            continue
                        # get the distance from the end node to the next node
                        newDist = self.memo[state].get(end, float('inf')) + self.graph[end][next]
                        # store the newDist, if it's smaller then the minDist
                        minDist = min(minDist, newDist)

                    # update memo with the minDist, set next as the last node visited
                    self.memo[subset][next] = minDist
        

    def minTourCost(self):
        # the endState is the binary representation for all nodes visited
        # so if N = 4, the endState would be 1111
        endState = (1 << self.N) - 1
        minDist = float('inf')

        # iterate through each possible end node, and keep track of the minimum distance
        for e in range(self.N):
            if e == self.start:
                continue
            minDist = min(self.memo[endState].get(e, float('inf')) + self.graph[e][self.start], minDist)
        return minDist
            

    # used to generate all the bit combinations
    def combinations(self, s, N):
        combos = []
        
        def backtrack(combo, start, bits):
            if bits == 0:
                combos.append(combo)
                return
            
            for i in range(start, N):
                # flip on the ith bit in the combo
                combo |= 1 << i
                backtrack(combo, i+1, bits-1)

                # flip off the ith bit
                # perform a logical AND with the inverted 1<<i
                combo &= ~(1<<i)

        backtrack(0,0,s)
        
        return combos
                

    def notIn(self, i, subset):
        return 1<<i & subset == 0
                
                
        
s = TSP("tsp.txt", 0)

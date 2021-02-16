"""
In this assignment we will revisit an old friend, the traveling salesman problem (TSP).
This week you will implement a heuristic for the TSP, rather than an exact algorithm, and as a result will be able to handle much larger problem sizes.

The first line indicates the number of cities.
Each city is a point in the plane, and each subsequent line indicates the x- and y-coordinates of a single city.

The distance between two cities is defined as the Euclidean distance --- that is,
two cities at locations (x,y) and (z,w) have distance sqrt((x-z)^2 + (y-w)^2) between them.

You should implement the nearest neighbor heuristic:

1. Start the tour at the first city.
2. Repeatedly visit the closest city that the tour hasn't visited yet.
   In case of a tie, go to the closest city with the lowest index.
   For example, if both the third and fifth cities have the same distance from the first city (and are closer than any other city), then the tour should begin by going from the first city to the third city.
3. Once every city has been visited exactly once, return to the first city to complete the tour.

In the box below, enter the cost of the traveling salesman tour computed by the nearest neighbor heuristic for this instance, rounded down to the nearest integer.

"""

import math, time
class TSP:
    def __init__(self, fileName):
        cities = [0]
        
        f = open(fileName, "r")
        firstline = True

        for line in f:
            # extra the number of vertices from the first line of the txt file
            if firstline:
                graphInfo = line.rstrip('\n')
                self.N = int(graphInfo)
                firstline = False
                continue

            # build the graph from the txt file
            # file organized with [vertex1 vertex2 edge_cost]
            city, x, y = line.rstrip('\n').split(" ")
            cities.append((float(x),float(y)))

        self.tsp(cities)

    def tsp(self, cities):
        start = time.time()
        seen = set()
        # start with city 1
        seen.add(1)
        last = 1
        path = []
        totalDist = 0

        while len(seen) < self.N:
            minDist = float('inf')
            next = None
            
            x,y = cities[last]
            
            path.append(last)
            for i in range(1, self.N+1):
                if i in seen:
                    continue
                z,w = cities[i]

                # cities are sorted by the x coordinate
                # if the difference in x values is > then minDist, the we know there is no other city that could be closer
                deltaX = abs(x-z)
                if deltaX > minDist:
                    break

                # check to see if the distance between the two cities is smaller then minDist
                # if it is, want to keep track of that distance and set that city to be the next to visit
                dist = math.sqrt((x-z)**2 + (y-w)**2)
                if dist < minDist:
                    minDist = dist
                    next = i

                
            # mark the next city as visited, and add to the total distance
            seen.add(next)
            totalDist += minDist
            last = next

        # adding the distance back to city one
        x,y = cities[1]
        z,w = cities[last]
        totalDist += math.sqrt((x-z)**2 + (y-w)**2)

        end = time.time()
        print("total time: ", end - start)
        print("path travelled: ", path)
        print("min distance: ", totalDist)
        
            
tsp = TSP("tsp_big.txt")

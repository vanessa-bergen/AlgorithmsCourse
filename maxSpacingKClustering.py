"""
In this programming problem and the next you'll code up the clustering algorithm from lecture for computing a max-spacing k-clustering.

This file describes a distance function (equivalently, a complete graph with edge costs).  It has the following format:

[number_of_nodes]

[edge 1 node 1] [edge 1 node 2] [edge 1 cost]

[edge 2 node 1] [edge 2 node 2] [edge 2 cost]

There is one edge (i,j) for each choice of 1<=i<j<=n where n is the number of nodes.

For example, the third line of the file is "1 3 5250", indicating that the distance between nodes 1 and 3 (equivalently, the cost of the edge (1,3)) is 5250.
You can assume that distances are positive, but you should NOT assume that they are distinct.

Your task in this problem is to run the clustering algorithm from lecture on this data set, where the target number k of clusters is set to 4.
What is the maximum spacing of a 4-clustering?

"""

class UnionFind:
    def __init__(self, N):
        # array used to keep track of the parent nodes
        self._id = list(range(N+1))
        # the number of clusters
        self._count = N
        # keep track of the rank of each node
        self._rank = [0] * (N+1)

    def find(self, p):
        # want to return the parent of p
        root = p
        while root != self._id[root]:
            root = self._id[root]

        # perform path compression
        # rewire each node in the path to point to the root node
        while p != root:
            next = self._id[p]
            self._id[p] = root
            p = next

        return root

    def count(self):
        return self._count

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        i = self.find(p)
        j = self.find(q)

        # p and q already belong to the same cluster
        if i == j:
            return

        # merge smaller group into the larger group
        # ranks stay the same unless the two cluster are the same size
        # in that case the rank of the new root will increase by one
        if self._rank[i] < self._rank[j]:
            self._id[i] = j
        elif self._rank[i] > self._rank[j]:
            self._id[j] = i
        else:
            self._id[j] = i
            self._rank[i] += 1

        # once a union has been performed, decrease the cluster count
        self._count -= 1


class maxSpaceKClustering:
    def __init__(self, fileName):
        clusterCount = 0
        self.edges = []

        f = open(fileName, "r")
        firstline = True

        for line in f:
            # extract the number of vertices from the first line of the txt file
            if firstline:
                graphInfo = line.rstrip('\n').split(" ")
                clusterCount = int(graphInfo[0])
                firstline = False
                continue

            # build the graph from the txt file
            # file organized with [node1 node2 edge_cost]
            n1, n2, weight = line.rstrip('\n').split(" ")
            self.edges.append((int(weight),int(n1),int(n2)))

        self.unionFind = UnionFind(clusterCount)

        self.edges.sort()
   
    def solve(self, k):
        
        for i in range(len(self.edges)):
            
            if self.unionFind.count() == k:
                break
            
            w,v1,v2 = self.edges[i]
            self.unionFind.union(v1, v2)


        # once there are k clusters, iterate through each edge
        # want to find the minDistance between two nodes that are not in the same cluster
        minDistance = float('inf')
        for w,v1,v2 in self.edges:
            if not self.unionFind.connected(v1,v2):
                minDistance = min(minDistance, w)

        return minDistance
        


s = maxSpaceKClustering("clustering1.txt")
ans = s.solve(4)
print(ans)

"""
In this question your task is again to run the clustering algorithm from lecture, but on a MUCH bigger graph.
So big, in fact, that the distances (i.e., edge costs) are only defined implicitly, rather than being provided as an explicit list.

The format is:

[# of nodes] [# of bits for each node's label]

[first bit of node 1] ... [last bit of node 1]

[first bit of node 2] ... [last bit of node 2]

For example, the third line of the file "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1" denotes the 24 bits associated with node #2.

The distance between two nodes uu and vv in this problem is defined as the Hamming distance--- the number of differing bits --- between the two nodes' labels.
For example, the Hamming distance between the 24-bit label of node #2 above and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3 (since they differ in the 3rd, 7th, and 21st bits).

The question is: what is the largest value of kk such that there is a kk-clustering with spacing at least 3?
That is, how many clusters are needed to ensure that no pair of nodes with all but 2 bits in common get split into different clusters?

NOTE: The graph implicitly defined by the data file is so big that you probably can't write it out explicitly, let alone sort the edges by cost.
So you will have to be a little creative to complete this part of the question.
For example, is there some way you can identify the smallest distances without explicitly looking at every pair of nodes?

"""

from collections import defaultdict
from itertools import combinations

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
        self.bits = 0
        self.data = []

        f = open(fileName, "r")
        firstline = True

        for line in f:
            # extract the number of vertices from the first line of the txt file
            if firstline:
                graphInfo = line.rstrip('\n').split(" ")
                clusterCount = int(graphInfo[0])
                self.bits = int(graphInfo[1])
                firstline = False
                continue

            # build the graph from the txt file
            node = "".join(line.strip().split(" "))
            # converting the binary string to an int
            intNode = int(node,2)
            self.data.append(intNode)

        
        self.unionFind = UnionFind(clusterCount)

    def distance_0_items(self, nodes):
        distance0 = defaultdict(list)

        # get all duplicate numbers
        # map the number to the index
        # ex: if '01' exists twise, want distance0['01'] = [index1, index2]
        for i, d in enumerate(self.data):
            distance0[d].append(i)
            

        # get all combinations of duplicate numbers and add to the nodes list
        # ex: if '01' is in there 3 times, at indexes 0,2,3 want to merge nodes [(0,2),(0,3),(2,3)]
        for k, lst in distance0.items():
            if len(lst) > 1:
                combos = combinations(lst, 2)
                nodes.extend(combos)

    def distance_1_items(self, nodes):

        # want to map all possible values that have a hamming distance of 1 form the node
        # ex: if num = '00' and the index of the node is 0
        # want to add to the dist1_keys dict {'01':0, '10':0} since both '01' and '10' have a hamming distance of 1 with '00'
        def dist_1(num, pairs, index):
            for i in range(self.bits):
                dist_1 = num ^ (1 << i)   
                pairs[dist_1].append(index)  

        
        dist1_present = defaultdict(list)
        # map the possible combinations with the node index that have a hamming distance of 1
        dist1_keys = defaultdict(list)
        
        # For each node, generate all other values that have a hamming distance of 1 from that node
        for i, d in enumerate(self.data):
            
            if d in dist1_keys:
                # nodes of distance 1 to d exists, store it in dist1_present
                dist1_present[d].append(i)
            dist_1(d, dist1_keys, i)

        for key, val in dist1_present.items():
            # create all pairs with hamming distance 1
            for d in val:
                for c in dist1_keys[key]:
                    nodes.append([d, c])

    def distance_2_items(self, nodes):
        # map all possible values with a hamming distance of 2 from the node
        def dist_2(num, pairs, index):
            for i in range(0,self.bits-1):
                for j in range(i+1, self.bits):
                    dist_2 = num ^ (1 << i)     
                    dist_2 = dist_2 ^ (1 << j)     
                    pairs[dist_2].append(index)  
            
        dist2_present = defaultdict(list)
        dist2_keys = defaultdict(list)
        
        
        for i, d in enumerate(self.data):
            if d in dist2_keys:
                dist2_present[d].append(i)
            dist_2(d, dist2_keys, i)

        for key, val in dist2_present.items():
            # create all pairs with hamming distance 2
            for d in val:
                for c in dist2_keys[key]:
                    nodes.append([d, c])
        
        
    
    def solve(self):
        
        nodesToMerge = []

        # add all node pairs that have a hamming distance less then or equal to 2
        self.distance_0_items(nodesToMerge)
        self.distance_1_items(nodesToMerge)
        self.distance_2_items(nodesToMerge)

        for pair in nodesToMerge:
            node1, node2 = pair
            self.unionFind.union(node1, node2)

        # after all the unions with distances <= 2 are complete, return the total number of clusters
        return self.unionFind.count()


s = maxSpaceKClustering("clustering_big.txt")
ans = s.solve()
print(ans)


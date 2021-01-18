"""
The file contains the edges of a directed graph.
Vertices are labeled as positive integers from 1 to 875714.
Every row indicates an edge, the vertex label in first column is the tail and the vertex label in second column is the head (recall the graph is directed, and the edges are directed from the first column vertex to the second column vertex).
So for example, the 11th row looks liks : "2 47646". This just means that the vertex with label 2 has an outgoing edge to the vertex with label 47646

Your task is to code up the algorithm from the video lectures for computing strongly connected components (SCCs), and to run this algorithm on the given graph.

Output Format: You should output the sizes of the 5 largest SCCs in the given graph, in decreasing order of sizes, separated by commas (avoid any spaces). So if your algorithm computes the sizes of the five largest SCCs to be 500, 400, 300, 200 and 100, then your answer should be "500,400,300,200,100" (without the quotes). If your algorithm finds less than 5 SCCs, then write 0 for the remaining terms. Thus, if your algorithm computes only 3 SCCs whose sizes are 400, 300, and 100, then your answer should be "400,300,100,0,0" (without the quotes).  (Note also that your answer should not have any spaces in it.)
"""

# Using a stack to perform DFS becuase the recursion stack exceeds in Python


import heapq

class GraphNode(object):

    def __init__(self, value, pointer = None, reversePointer = None):
        
        self.value = value

        # list of outgoing edges 
        self.pointer = set()
        # list of outgoing edges in reversed graph
        self.reversePointer = set()
        
    def addForward(self, node):
        self.pointer.add(node)
    def addReverse(self, node):
        self.reversePointer.add(node)

class SCC(object):
    def __init__(self):
        self.nodes = {}

    
    def setNodes(self, fileName):
        # read the file and build the graph
        f = open(fileName, "r")

        for line in f:
            line = line.strip().rstrip('\n')
            
            val1, val2 = line.split(" ")

            # create the graph nodes if they don't already exist
            if val1 not in self.nodes:
                node1 = GraphNode(val1)
                self.nodes[val1] = node1
                
            if val2 not in self.nodes:
                node2 = GraphNode(val2)
                self.nodes[val2] = node2

            # add the outgoing edges for the forware and reversed graph
            self.nodes[val1].addForward(self.nodes[val2])
            self.nodes[val2].addReverse(self.nodes[val1])

    def loop1(self):
        seen = set()
        stack = []
        # use order to keep track of finishing times
        # first element in order has the first finishing time and so on
        # can change this to be a dictionary and keep a variable to keep track of current finishing time
        order = []

        for node in self.nodes.values():
            
            if node not in seen:
                seen.add(node)
                stack.append(node)
                

                while stack:
                    
                    edge_found = False
                    current = stack.pop()
                    for neighbour in current.reversePointer:
                       
                        
                        if neighbour not in seen:
                            seen.add(neighbour)
                            # need to append the current node again, otherwise we would miss the finishing time for it
                            stack.append(current)
                            stack.append(neighbour)
                            edge_found = True
                            break

                    # if there are no edges found, we've hit the last node we can explore
                    # add the node to the order array to mark the finishing time
                    if not edge_found:
                        order.append(current)
        return order

    def loop2(self, order):
        seen = set()
        sccs = {}
        stack = []

        # going through the finishing times in reverse
        for node in reversed(order):
            if node not in seen:
                # this node is a leader of a scc, add it to the sccs dict with a count of 1
                sccs[node.value] = 1
                seen.add(node)
                stack.append(node)

                while stack:
                    current = stack.pop()
                    for neighbour in current.pointer:
                        if neighbour not in seen:
                            seen.add(neighbour)
                            stack.append(neighbour)
                            # adding to the count of elements in the scc with the leader node
                            sccs[node.value] += 1
        return sccs

scc = SCC()
scc.setNodes("scc.txt")
order= scc.loop1()
sccs = scc.loop2(order)
# return the 5 largest sccs
print(heapq.nlargest(5, sccs.values()))

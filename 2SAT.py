"""
2SAT using DFS to find strongly connected components

In this assignment you will implement one or more algorithms for the 2SAT problem.

The file format is as follows.
In each instance, the number of variables and the number of clauses is the same, and this number is specified on the first line of the file.
Each subsequent line specifies a clause via its two literals, with a number denoting the variable and a "-" sign denoting logical "not".
For example, the second line of the first data file is "-16808 75250", which indicates the clause -x_{16808} OR x_{75250}.

Your task is to determine which of the 6 instances are satisfiable, and which are unsatisfiable.  In the box below, enter a 6-bit string, where the ith bit should be 1 if the ith instance is satisfiable, and 0 otherwise.  For example, if you think that the first 3 instances are satisfiable and the last 3 are not, then you should enter the string 111000 in the box below.

"""

class GraphNode(object):

    def __init__(self, value, adj = None, reverseAdj = None):
        self.value = value
        self.adj = []
        self.reverseAdj = []
        
    def addForward(self, node):
        self.adj.append(node)

    def addReverse(self, node):
        self.reverseAdj.append(node)

    def getAdj(self, reverse):
        return self.adj if not reverse else self.reverseAdj

class SCC(object):
    def __init__(self, fileName):
        self.nodes = {}
        self.nodeCount = 0

        f = open(fileName, "r")
        firstline = True

        for line in f:
            if firstline:
                graphInfo = line.rstrip('\n').split(" ")
                self.nodeCount= int(graphInfo[0])
                firstline = False
                continue
            
            line = line.strip().rstrip('\n')
            
            val1, val2 = (int(val) for val in line.split(" "))

            # for every value denoting a variable, add a GraphNode for value and not(value)
            # use a negative sign to denote logical not
            
            if val1 not in self.nodes:
                self.nodes[val1] = GraphNode(val1)
                self.nodes[-val1] = GraphNode(-val1)
                
            if val2 not in self.nodes:
                self.nodes[val2] = GraphNode(val2)
                self.nodes[-val2] = GraphNode(-val2)

            # make two edged for every clause: not(val1) -> val2 and not(val2) -> val1
            # these edges mean if not val1 then val2 and if not val2 then val1
            
            self.nodes[-val1].addForward(self.nodes[val2])
            self.nodes[val2].addReverse(self.nodes[-val1])

            self.nodes[-val2].addForward(self.nodes[val1])
            self.nodes[val1].addReverse(self.nodes[-val2])


    def loop1(self):
        seen = set()
        order = []

        def dfs(node, seen):
            for adj in node.getAdj(True):
                if adj not in seen:
                    seen.add(adj)
                    dfs(adj, seen)
            order.append(node)

        # go throught the reversed graph and get the topological ordering
        for node in self.nodes.values():
            if node not in seen:
                seen.add(node)
                dfs(node, seen)
        
        return order

    def loop2(self, order):
        seen = set()
        sccs = {}
        # component will be used as the ID for the strongly connected component
        # if two nodes have the same component ID, then they are in the same strongly connected component
        component = 0

        def dfs(node, seen):
            seen.add(node)
            for adj in node.getAdj(False):
                if adj not in seen:
                    dfs(adj, seen)

            # set the component that the node belongs in
            sccs[node.value] = component


        while order:
            # going through the topological order in revesre
            v = order.pop()
            if v not in seen:
                # increment the id of the component
                component += 1
                dfs(v, seen)

        # return the mappings of each node and the component they belong to
        return sccs

    def check2SAT(self, sccs):
        # if any variable x1 and not(x1) exist in the same component, then it's not satifiable
        # this means one edge requires x1 to be True and one requires x1 to be False
        for i in range(1, self.nodeCount+1):
            if i not in sccs:
                i += 1
                continue
            if sccs[i] == sccs[-i]:
                return False
            
        return True
                

scc = SCC("2sat6.txt")
order = scc.loop1()
sccs = scc.loop2(order)
isSatisfied = scc.check2SAT(sccs)
print("2-SAT is satisfied: ", isSatisfied)

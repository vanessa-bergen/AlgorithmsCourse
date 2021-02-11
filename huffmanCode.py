"""

In this programming problem and the next you'll code up the greedy algorithm from the lectures on Huffman coding.

This file describes an instance of the problem. It has the following format:

[number_of_symbols]

[weight of symbol #1]

[weight of symbol #2]

...

For example, the third line of the file is "6852892," indicating that the weight of the second symbol of the alphabet is 6852892.
(We're using weights instead of frequencies, like in the "A More Complex Example" video.)

Your task in this problem is to run the Huffman coding algorithm from lecture on this data set.

What is the maximum length of a codeword in the resulting Huffman code?
Continuing the previous problem, what is the minimum length of a codeword in your Huffman code?

"""

from collections import deque

class TreeNode:
    def __init__(self, freq, char, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
        self.huff = ''

    # Gets called on comparison using < operator, return TreeNode with smallest frequency
    def __lt__(self, other):
        return self.freq < other.freq
        
class Huffman:
    def __init__(self,fileName):
        nodes =[]

        # want to keep track of the characters with the largest and smallest frequencies
        # the most frequent char will have the minimum length of a codeword
        # least frequent char will have the maximum length of a codeword
        maxFreqChar = [float('-inf'), None]
        minFreqChar = [float('inf'), None]

        f = open(fileName, "r")
        firstline = True
        i = 1
        for line in f:
            # extract the number of symbols from the first line 
            if firstline:
                graphInfo = line.rstrip('\n').split(" ")
                charCount = int(graphInfo[0])
                firstline = False
                continue

            weight = int(line.rstrip('\n'))

            # update characters with largest and smallest frequencies
            if weight > maxFreqChar[0]:
                maxFreqChar = [weight, str(i)]
            if weight < minFreqChar[0]:
                minFreqChar = [weight, str(i)]

            # create the TreeNode, use i as the char
            node = TreeNode(weight, str(i))
            i += 1
            nodes.append(node)

        # sort by increasing frequencies
        #nodes.sort(key=lambda x:x.freq)
        
        # sort TreeNodes by increasing frequencies, and store in queue
        nodes = deque(sorted(nodes, key=lambda x:x.freq))
        self.solve(nodes, minFreqChar[1], maxFreqChar[1])

        

    def solve(self, nodes, minFreqChar, maxFreqChar):
        # solving using two queues
        mergedNodes = deque()
        
        root = None

        # while there are at least 2 nodes remaining
        while len(nodes) + len(mergedNodes) > 1:

            # get two TreeNodes with the smallest frequences and remove them from the queues
            if not mergedNodes or (nodes and nodes[0] < mergedNodes[0]):
                left = nodes.popleft()
            else:
                left = mergedNodes.popleft()

            if not mergedNodes or (nodes and nodes[0] < mergedNodes[0]):
                right = nodes.popleft()
            else:
                right = mergedNodes.popleft()

            # add the huffman code
            left.huff = 0
            right.huff = 1

            # create the new merged node
            # combine the two chars and add the two frequencies
            # add the new node to the mergedNodes queue, this queue will remain in sorted order since merged nodes will only increase in frequency
            newNode = TreeNode(left.freq + right.freq, left.char+right.char, left, right)
            mergedNodes.append(newNode)

            # keep track of the root node, which will be the final node used to decode the tree 
            root = newNode

        huffmanCodes = {}
        # get the codes for each char and store in dictionary
        self.decode(root, huffmanCodes)

        print(huffmanCodes)
        print("max length: %i, min length: %i" % (len(huffmanCodes[minFreqChar]), len(huffmanCodes[maxFreqChar])))

    def decode(self, node, huffmanCodes, val=''):
        code = val + str(node.huff)

        if node.left:
            self.decode(node.left, huffmanCodes, code)
        if node.right:
            self.decode(node.right, huffmanCodes, code)

        if not node.left and not node.right:
            huffmanCodes[node.char] = code


h = Huffman("huffman.txt")

"""
In this programming problem and the next you'll code up the knapsack algorithm from lecture.

This file describes a knapsack instance, and it has the following format:

[knapsack_size][number_of_items]

[value_1] [weight_1]

[value_2] [weight_2]

...

For example, the third line of the file is "50074 659", indicating that the second item has value 50074 and size 659, respectively.

You can assume that all numbers are positive.  You should assume that item weights and the knapsack capacity are integers.

"""


import sys 
  
# use setrecursionlimit to modify the default recursion limit set by python  
sys.setrecursionlimit(10**6) 

class Knapsack:
    def __init__(self, fileName):

        # defaulting value at index 0 to 0, since items in backpack start at index 1
        values = [0]
        weights = [0]

        f = open(fileName, "r")
        firstline = True
        
        for line in f:
            # extract the number of vertices from the first line of the txt file
            if firstline:
                graphInfo = line.rstrip('\n').split(" ")
                capacity= int(graphInfo[0])
                firstline = False
                continue
            value, weight = line.rstrip('\n').split(" ")

            values.append(int(value))
            weights.append(int(weight))
        
        self.knapsack(capacity, values, weights)
        self.knapsack_lessSpace(capacity, values, weights)
        self.knapsack_recursive(capacity, values, weights)

    # option 1: knapsack using 2D array
    def knapsack(self, capacity, values, weights):
        if capacity < 0 or not values or not weights:
            raise Exception("Invalid input")

        dp = [[0 for _ in range(capacity+1)] for _ in range(len(values))]

        for i in range(1, len(values)):
            v = values[i]
            w = weights[i]
            for j in range(1, capacity+1):
                # set the current value to the last value
                # this is case 1 where item i is excluded from the knapsack
                dp[i][j] = dp[i-1][j]

                # if there is room for item i, j >= the capacity of item i
                # see if adding the value of item i, increases the value of the knapsack
                if j >= w and dp[i-1][j-w] + v > dp[i][j]:
                    # case 2 where item i in included
                    dp[i][j] = dp[i-1][j-w] + v

        # trace backwards to get items in knapsack
        # start at the last item
        # compare to row above, if items differ that we know the item is included
        # then we need to subtract the backpack capacity of that item

        items = []
        while i > 0:
            if dp[i][j] != dp[i-1][j]:
                # item is included
                items = [i] + items
                # subtract the capacity of that item
                j -= weights[i]
            
            i -= 1

        print("max value: ", dp[-1][-1])
        print("items in backpack: ", items)

    
    # option 2: knapsack using 1D array
    def knapsack_lessSpace(self, capacity, values, weights):
        if capacity < 0 or not values or not weights:
            raise Exception("Invalid input")
        
        dp = [0 for _ in range(capacity+1)]

        # iterate through all items 
        for i in range(1,len(values)): 
          
            # traverse dp array from right to left
            # see if item should be included or not
            for j in range(capacity,weights[i]-1,-1): 
                dp[j] = max(dp[j] , values[i] + dp[j-weights[i]])
        
        print("max value: ", dp[-1])

    # option 3: knapsack recursive version
    def knapsack_recursive(self, capacity, values, weights):
        if capacity < 0 or not values or not weights:
            raise Exception("Invalid input")

        # want to cache reults so that the same subproblems aren't caculated over and over again
        cache = {}
        
        def helper(w, item, cache):
            
            if (w, item) in cache:
                return cache[(w, item)]

            # base case, capacity is 0 or the item does not exist
            if w == 0 or item == len(values):
                cache[(w, item)] = 0
                return 0

            # case 1: item is not included in the knapsack
            if weights[item] > w:
                cache[(w, item)] = helper(w, item+1, cache)
                return cache[(w, item)]

            # case 2: need to determine if the item should be included
            # return the case with the max value
            include = values[item] + helper(w-weights[item], item+1, cache)
            exclude = helper(w, item+1, cache)
            cache[(w, item)] = max(include, exclude)
            return max(include, exclude)

        maxVal = helper(capacity, 1, cache)
        print("max value: ", maxVal)

        
ks = Knapsack("knapsack1.txt")

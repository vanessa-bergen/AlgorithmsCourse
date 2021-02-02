class WeightedSum:
    def __init__(self, fileName):
        self.arr = []
        f = open(fileName, "r")
        firstline = True

        for line in f:
            if firstline:
                firstline=False
                continue
            weight, length = line.rstrip('\n').split(" ")
            
            self.arr.append([int(weight),int(length)])

    def orderByDifference(self):
        # creating a new array with the sorted order
        # sorted first by the difference w-l
        # use the weight as the tie breaker
        return sorted(self.arr, key = lambda job: (job[0]-job[1], job[0]), reverse=True)

    def orderByRatio(self):
        # sort by the ratio w/l
        # ties don't matter
        return sorted(self.arr, key= lambda job: job[0]/job[1], reverse=True)

    def minWeightedSum(self):
        completionTime = 0
        totalSum = 0
        #orderedArr = self.orderByDifference()
        orderedArr = self.orderByRatio()

        for job in orderedArr:
            # add the length to the completion time
            completionTime += job[1]
            # add the weighted completion time cj * wj to the sum
            totalSum += completionTime * job[0]

        return totalSum

   
    
ws = WeightedSum("jobs.txt")
ans = ws.minWeightedSum()
print(ans)

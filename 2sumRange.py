"""
The goal of this problem is to implement a variant of the 2-SUM algorithm covered in this week's lectures.

The file contains 1 million integers, both positive and negative (there might be some repetitions!).
This is your array of integers, with the i^th row of the file specifying the i^th entry of the array.

Your task is to compute the number of target values t in the interval [-10000,10000] (inclusive)
such that there are distinct numbers x,y in the input file that satisfy x+y=t.
(NOTE: ensuring distinctness requires a one-line addition to the algorithm from lecture.)

Write your numeric answer (an integer between 0 and 20001) in the space provided.
"""


import bisect

# note:
# can't add the same number to get a target value ie: x+x=t can't be included in the count
# don't want to include duplicate targets ie: if x+y=t and w+z=t we only want the count to increment once
 
# option 1: using binary search
def twoSumRange(fileName, targetRange):
    f = open(fileName, "r")
    numbers = []
    count = 0
    seen = set()
    
    for line in f:
        num = int(line.rstrip('\n'))
        numbers.append(num)

    numbers.sort()

    for i in range(len(numbers)):
        # iterate through each number in the array
        # set the complements, maxVal and minVal, that add to the bound of the target
        # ie: val+maxVal = 10000 (upper target range) and val+minVal = -10000 (lower target range)
        val = numbers[i]
        maxVal = targetRange - val
        minVal = -targetRange - val

        # use bisect to determine the positions where the maxVal and minVal would fit in the array
        upperBound = bisect.bisect_right(numbers, maxVal)
        lowerBound = bisect.bisect_left(numbers, minVal)

        # loop through the range in the array
        # all numbers in that range will can be added with val to produce a number in the targetRange
        for j in range(lowerBound, upperBound):
            sum = val + numbers[j]
            # if we have not already counted that target, add to the count
            if sum not in seen and val != numbers[j]:
                # use seen to keep track of all targets that have already been calculated
                seen.add(sum)
                count += 1
    return count
        
# option 2: using a dictionary
def twoSumRangeSlow(fileName, targetRange):
    numbers = []
    count = 0

    for line in f:
        num = int(line.rstrip('\n'))
        numbers.append(num)

    # very slow
    # sinces numbers has 1 million items
    # each time we get a target we are possibly looping through 1 million times to try and find a match
    for target in range(-targetRange, targetRange+1):
        for num in numbers:
            
            complement = target - num

            # only need to get the target sum once
            # so once we find the number and the complement that adds up to target, break out of the loop to move to next target
            if complement in numbers and num != complement:
                count += 1
                break
    return count



ans = twoSumRange("2sum.txt", 10000)
print(ans)




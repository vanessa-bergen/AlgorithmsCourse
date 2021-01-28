"""
The goal of this problem is to implement the "Median Maintenance" algorithm (covered in the Week 3 lecture on heap applications).
The text file contains a list of the integers from 1 to 10000 in unsorted order; you should treat this as a stream of numbers, arriving one by one.
Letting x_i denote the ith number of the file, the kth median m_k is defined as the median of the numbers x_1,...,x_k.
(So, if k is odd, then m_k is ((k+1)/2)th smallest number among x_1,...,x_k; if k is even, then m_k is the (k/2)th smallest number among x_1,...,x_k)

In the box below you should type the sum of these 10000 medians, modulo 10000 (i.e., only the last 4 digits).
That is, you should compute (m_1+m_2+m_3 + ...+ m_10000) mod 10000
"""

import heapq

def medianMaintenance(fileName):
    # max heap used to keep track of the smallest numbers
    lowHeap = []
    # min heap used to keep track of the largest numbers
    highHeap = []
    sum = 0

    f = open(fileName, "r")

    for line in f:
        number = int(line.rstrip('\n').strip())

        # always add the number to the lowHeap
        # allowing the lowHeap to have one more element than the highHeap
        # use a negative number to make it a max heap (largest number will really be the smallest)
        heapq.heappush(lowHeap, -number)

        # rebalancing step
        # take the largest value from lowHeap and add to highHeap
        maxVal = heapq.heappop(lowHeap)
        heapq.heappush(highHeap, -maxVal)

        # now we need to make sure that the highHeap is not a bigger size then the lowHeap
        # if it is, transger the smallest element in the highHeap to the lowHeap
        if len(lowHeap) < len(highHeap):
            minVal = heapq.heappop(highHeap)
            heapq.heappush(lowHeap, -minVal)


        # now we can calculate the median
        # for this question, the median will always be the max number in the lowHeap
        """
        if we were actually calculating the median then whenever the size of the two heaps are the same we would take an average of the max val in the lowHeap and the min val in the highHeap
        
        median taking the average ex:
        median = -lowHeap[0] if len(lowHeap) > len(highHeap) else float((-lowHeap[0] + highHeap[0]) / 2.0)
        """

        sum += -lowHeap[0]

    return sum % 10000


ans = medianMaintenance("median.txt")
print(ans)

    
    

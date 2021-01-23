"""
The file contains all of the integers between 1 and 10,000 (inclusive, with no repeats) in unsorted order.
The integer in the ith row of the file gives you the ith entry of an input array.

Your task is to compute the total number of comparisons used to sort the given input file by QuickSort.
As you know, the number of comparisons depends on which elements are chosen as pivots, so we'll ask you to explore three different pivoting rules.

You should not count comparisons one-by-one.
Rather, when there is a recursive call on a subarray of length m, you should simply add m-1 to your running total of comparisons.
(This is because the pivot element is compared to each of the other m-1m−1 elements in the subarray in this recursive call.)
"""

class QuickSort:
    def __init__(self, filename):
        self.arr = []
        self.buildArray(filename)
        self.comparisons = 0

    def buildArray(self, fileName):
        f = open(fileName, "r")

        for line in f:
            item = line.rstrip('\n').strip()
            self.arr.append(int(item))
        
    def quickSort(self, l, r):
        
        # if the length of the array we are partitioning on is <= 1, array is already sorted
        if r - l > 1:
            # this means we will perform r-l-1 comparisons
            self.comparisons += r-l-1

            """
            Question 1:
            Setting the pivot to the first element in the array
            """
            # pivot = self.arr[l]

            """
            Question 2:
            Setting the pivot to the last elemen in the array

            Get the value of the last element
            then swap the last element with the first element
            """
            # pivot = self.arr[r-1]
            # self.swap(l, r-1)

            """
            Question 3: 
            Setting the pivot using the three median rule
            Pick the median of the first, mid and last element in the array
            """
            
            medianIndex = self.getMedian(l, (r-l-1)//2 + l, r-1)
            pivot = self.arr[medianIndex]
            self.swap(l, medianIndex)


            i = l + 1

            for j in range(l+1, r):
                if self.arr[j] < pivot:
                    self.swap(i, j)
                    i += 1

            
            self.swap(l, i-1)

            self.quickSort(l, i-1)
            self.quickSort(i, r)


    def swap(self, i, j):
        tmp = self.arr[i]
        self.arr[i] = self.arr[j]
        self.arr[j] = tmp

    def getMedian(self, x, y, z):
        # x is either the median or the max
        if self.arr[x] > self.arr[y]:
            if self.arr[x] < self.arr[z]:
                median = x
            elif self.arr[y] > self.arr[z]:
                median = y
            else:
                median = z
        
        else:
            if self.arr[x] > self.arr[z]:
                median = x
            elif self.arr[y] < self.arr[z]:
                median = y
            else:
                median = z

        # return the index of the median value
        return median
        


s = QuickSort("QuickSort.txt")
s.quickSort(0, len(s.arr))
print(s.arr)
print(s.comparisons)

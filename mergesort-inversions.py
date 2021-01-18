"""
This file contains all of the 100,000 integers between 1 and 100,000 (inclusive) in some order, with no integer repeated.

Your task is to compute the number of inversions in the file given, where the ith row of the file indicates the ith entry of an array.

Because of the large size of this array, you should implement the fast divide-and-conquer algorithm covered in the video lectures.
"""

def buildArray(fileName):
    arr = []

    # building the array from the text file
    f = open(fileName, "r")
    for row in f:
        # remove any leading or trailing whitespaces and the new line character
        row = row.strip().rstrip('\n')
        arr.append(int(row))
    return arr

def merge_sort(arr):
    # base case: if len(arr) <= 1 then the array doesn't need to be sorted
    # returns 0 inversions
    inv_count = 0
    
    if len(arr) > 1:
        # splitting the array in two halves
        mid = int(len(arr)/2)
        lefthalf = arr[:mid]
        righthalf = arr[mid:]
        
        # pass the halved arrays into the merge_sort function
        # when this call finishes, the array will be sorted and it returns the inversions count
        inv_count += merge_sort(lefthalf)
        inv_count += merge_sort(righthalf)

        # at this point lefthalf and righthalf are sorted
        # call combine to sort and merge into one arr
        inv_count += combine(lefthalf, righthalf, arr)

    return inv_count

def combine(left, right, arr):
    inv_count = 0

    # pointers to track where we are in the merging process
    i = j = k = 0

    # want to reassemble the two halves in sorted order back into the array
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            # if there is an element in the right half that's greater then an element in the left, then we know there's at least one inversion
            # inversions = the number of elements remaining in the left array when the element from the right array is copied over 
            inv_count += len(left)-i
            arr[k] = right[j]
            j += 1
        k += 1

    # if we finished adding the whole right array, then we need to finish adding the left array
    # left is already in sorted order, so we can just add it to arr
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    # if there are still elements in right, then we add them to the arr
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

    return inv_count


arr = buildArray("IntegerArray.txt")
ans = merge_sort(arr)
print(ans)

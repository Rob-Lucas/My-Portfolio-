# Name: Robert Lucas    
# OSU Email: Lucasrob@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5 MinHeap
# Due Date: 3/6/2023
# Description: Uses a Minheap to navigate a Dynamic Array


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)
    
#------------------------------------------------------------------------------------------------------

    def add(self, node: object) -> None:
        """
        This method adds a new object to MinHeap while maintain heap property.
        """
        # Add new element to the end of the heap
        self._heap.append(node)
        # # Get the index of the newly added element
        new_index = self._heap.length() - 1
        # # Get the index of the parent of the newly added element
        parent_index = (new_index - 1) // 2

        #While the parent of the newly added element is greater than the new element
        while new_index > 0 and self._heap[parent_index] > self._heap[new_index]:
            # Swap the new element with its parent
            self._heap[new_index], self._heap[parent_index] = self._heap[parent_index], self._heap[new_index]
            # Update the indices of the new element and its parent
            new_index = parent_index
            parent_index = (new_index - 1) // 2

    def is_empty(self) -> bool:
        """
        Returns True if Heap object is empty and False otherwise.
        """
        return self._heap.length() == 0


    def get_min(self) -> object:
        """
        Return the minimum object of the Heap
        """
        if self._heap.length() == 0:
            raise MinHeapException("Heap is empty")
        return self._heap.get_at_index(0)
    
    def remove_min(self) -> object:
        """
        Removes the minimum value from the heap.
        """
        if self._heap.is_empty():
            raise MinHeapException

        # swap root with last element
        root = self._heap[0]
        last_element = self._heap[self._heap.length()-1]
        self._heap[0] = last_element
        self._heap.remove_at_index(self._heap.length() - 1)
        # percolate down
        _percolate_down(self._heap,0)
        return root
    

    def build_heap(self, da: DynamicArray) -> None:
        """
        Receives a DynamicArray and builds a proper minheap from it.
        """
        # Clear the current heap
        self._heap = DynamicArray()

        # Add each element from the input DynamicArray to the heap
        for i in da:
            self._heap.append(i)

        # Percolate down each element starting from the middle of the heap
        mid_index = (self._heap.length() - 1) // 2
        for i in range(mid_index, -1, -1):
            _percolate_down(self._heap, i)

    def size(self) -> int:
        """
        Returns the size of the heap.
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears out the heap.
        """
        self._heap = DynamicArray()

    # def pop(self) -> object:            # I was having problems with remove_min and once I got it working I did not want to put this back in an mess it up
    #     """
    #     Helper method:
    #     Removes the last element of the heap and replaces the first element
    #     """
    #     last_elem = self._heap[self._heap.length() - 1]
    #     self._heap[0] = None
    #     self._heap[0] = last_elem
    #     self._heap[self._heap.length() - 1] = None
    #     self._heap._size -= 1

def heapsort(da: DynamicArray) -> None:
    """
    Takes in a DynamicArray object and returns a MaxHeap sorted. 
    Does not return any values.
    """
    # First step is to build a max heap from the input array these are both O(NlogN)
    n = da.length()
    for i in range(n // 2 - 1, -1, -1):
        j = i
        while 2 * j + 1 < n:
            k = 2 * j + 1
            if k + 1 < n and da[k + 1] > da[k]:
                k += 1
            if da[k] > da[j]:
                da[k],da[j] = da[j],da[k]
                j = k
            else:
                break
    
    # Next, perform the heap sort by repeatedly removing the maximum element
    # and placing it at the end of the array
    for i in range(n-1, 0, -1):
        da[0],da[i] = da[i],da[0]
        j = 0
        while 2 * j + 1 < i:
            k = 2 * j + 1
            if k + 1 < i and da[k + 1] > da[k]:
                k += 1
            if da[k] > da[j]:
                da[k],da[j] = da[j],da[k]
                j = k
            else:
                break
    
    left_cursor = 0
    right_cursor = da.length()-1
    # reverses the sort of the list to return the desired output.
    while left_cursor != right_cursor:
        da[right_cursor],da[left_cursor] = da[left_cursor],da[right_cursor]
        left_cursor += 1
        right_cursor -= 1

def _percolate_down(da: DynamicArray, parent: int) -> None:
    """
    Move the element at the given index down the heap until the heap property is restored.
    """
    i = parent
    while i < da.length()-1:
        left_child_index = (2 * i) + 1
        right_child_index = (2 * i) + 2

        # if left child exists and is less than parent
        if left_child_index < da.length() and da[left_child_index] < da[i]:
            # if right child exists and is less than left child
            if right_child_index < da.length() and da[right_child_index] < da[left_child_index]:
                da[i], da[right_child_index] = da[right_child_index], da[i]
                i = right_child_index
            else:
                da[i], da[left_child_index] = da[left_child_index], da[i]
                i = left_child_index
        # if right child exists and is less than parent
        elif right_child_index < da.length() and da[right_child_index] < da[i]:
            da[i], da[right_child_index] = da[right_child_index], da[i]
            i = right_child_index
        else:
            break

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

# Name: Robert Lucas
# OSU Email: Lucasrob@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment:  3 Linked List and ADT Implementation
# Due Date: 2/13/2022
# Description: Creating a linked list data structure (singly)

from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Adds a new node to the beginning of the list based off the value provided.
        """
        new_node = SLNode(value)    #These are creating new nodes for the linked list (come up often)
        new_node.next = self._head.next
        self._head.next = new_node


    def insert_back(self, value: object) -> None:
        """
        Add a new node with the provided value to the end of the list.
        """
        new_node = SLNode(value)
        node = self._head
        while node.next: #Traverse to last node
            node = node.next
        node.next = new_node

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Adds a new node to a specific position of the linked list based off the provided value.
        Input: (Index, value)
        """
        if index < 0:
            raise SLLException('Index out of bounds')
        node = self._head
        for i in range(index): #Checks for a spot that exists in the linked list
            if node.next is not None:
                node = node.next
            else:               #Raise exception if the index location is not open.
                raise SLLException('Index out of bounds')
        new_node = SLNode(value, node.next)
        node.next = new_node

    def remove_at_index(self, index: int) -> None:
        """
        Remove the node at the specified index position from the list.
        Input: (index)
        raises SLLException: if the index is out of range
        """
        if index < 0 or index >= self.length():
            raise SLLException("Index out of range")
        current = self._head.next
        prev = self._head
        i = 0
        while i < index:    # iterate to the location of the index. 
            prev = current
            current = current.next
            i += 1
        prev.next = current.next #Updates the links to remove node
        current.next = None

    def remove(self, value: object) -> bool:
        """
        Removes the first node that is the provided value. Does this by incrementing the position in the list
        Input: (the value you wish to remove)
        """
        prev_node = self._head
        curr_node = prev_node.next
        while curr_node is not None:    #Iterates to removal location
            if curr_node.value == value:
                prev_node.next = curr_node.next
                return True #Returns if "value" was found and removed

            prev_node = curr_node
            curr_node = curr_node.next

        return False

    def count(self, value: object) -> int:
        """
        Counts the number of values that match the given value within the linked list.
        Input: (value)
        Result: returns the amount that exist in list.
        """
        count = 0
        node = self._head.next
        while node is not None: #Iterates and counts the quantity of given "value"
            if node.value == value:
                count += 1
            node = node.next
        return count

    def find(self, value: object) -> bool:
        """
        Checks the list and returns True if the provided value object exists in the list,
        otherwise False.
        """
        current = self._head.next
        while current:  #Iterates to check for "value"
            if current.value == value:
                return True
            current = current.next
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        Returns a new Linked List object that contains the nodes as indicated with the input values.
        Input: (starting position, the amount of nodes desired)
        """
        if start_index < 0 or start_index >= self.length(): #Check if within bounds
            raise SLLException("Invalid start index")
        if size < 1:  #Check for size
            raise SLLException("Size must be at least 1")
        node = self._head.next
        for i in range(start_index): #Find starting node
            node = node.next
            if not node:
                raise SLLException("Invalid start index")
        slice_list = LinkedList() 
        for i in range(size): #Add nodes to sliced list
            if node:
                slice_list.insert_back(node.value)
                node = node.next
            else:   #Raise if not enough nodes to slice
                raise SLLException("Not enough nodes to create a slice of the requested size")
        return slice_list


if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")

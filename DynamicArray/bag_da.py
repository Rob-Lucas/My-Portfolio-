# Name: Robert Lucas
# OSU Email: lucasrob@oregonstate.edu   
# Course: CS261 - Data Structures
# Assignment: 2 Dynamic Array and ADT Implementation
# Due Date: 2/6/2023
# Description: This utilizes the use of a bag which uses the dynamic array class for creating an array. This class mainly exists for easier navigation and readability human side. 


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Adds new element to the bag.
        ----
        Input: Value
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        Removes any element from the bag with the given value (just one). Returns True if a removal occurred.
        If not, returns False.
        -----------
        Input: The value in the bag
        Result: True or False
        """
        for i in range(self._da.length()):  #Iterates through the bag for the given value and removes it if found.
            if self._da.get_at_index(i) == value:
                self._da.remove_at_index(i)
                return True
        return False

    def count(self, value: object) -> int:
        """
        Counts the amount of elements which match the given value. 
        ---------
        Input: Value to be checked
        Output: Quantity of value
        """
        count = 0
        for i in range(self._da.length()): 
            if self._da.get_at_index(i) == value: #Counts if the value occurs
                count += 1
        return count

    def clear(self) -> None:
        """
        Deletes all values within the bag permanently. No inputs
        -------
        Result: Empty bag, nothing returned
        """
        self._da = DynamicArray()

    def equal(self, second_bag: "Bag") -> bool:
        """
        Checks two bags which are given for if the bags are equal in value (contain same number of elements and same elements).
        Order of elements does not matter. Returns True if they are equal and False otherwise.
        ----------
        Input: (your bag object).equal(the second bag)
        Result: True or False depending on if they equal
        """
        if self.size() != second_bag.size(): #Returns False if incorrect size
            return False

        for value in self._da:
            count = 0
            for i in second_bag._da: #Checks for quantiy of value in bag
                if value == i:
                    count += 1
            if count != self.count(value): #If quantity is not the same in both bags return False
                return False

        return True

    def __iter__(self):
        """
        Allows iteration within bag class. Returns the current object for indexing.
        """
        self._index = 0 #Private variable for iterating. 
        return self

    def __next__(self):
        """
        Returns next item in bag based on __iter__ variable self._index.
        """
        if self._index >= self._da.length():    
            raise StopIteration
        else:
            item = self._da.get_at_index(self._index)
            self._index += 1
            return item


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)

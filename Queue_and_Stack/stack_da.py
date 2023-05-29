# Name: Robert Lucas
# OSU Email: Lucasrob@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment:  3 Linked List and ADT Implementation
# Due Date: 2/13/2022
# Description: Use dynamic array class to create a Stack ADT class.


from dynamic_array import *


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self):
        """
        Init new stack based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "STACK: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da[i]) for i in range(self._da.length())])
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Adds a new element to the top of the stack based on the given value.
        """
        if self._da.length() == self._da.get_capacity():   #If capacity is maximum, doubles capacity.
            self._da.resize(2 * self._da.get_capacity())
        self._da.append(value)

    def pop(self) -> object:
        """
        Run this method to remove the top element of the stack.
        """
        if self.is_empty():
            raise StackException
        value = self._da[self._da.length() - 1] # Get the value of the top element and remove it from the array
        self._da.remove_at_index(self._da.length() - 1)

        return value

    def top(self) -> object:
        """
        Use this method to determine which item is on the top of the stack.
        """
        if self.is_empty():
            raise StackException("Stack is empty")
        return self._da[self._da.length() - 1]


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# push example 1")
    s = Stack()
    print(s)
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    print(s)

    print("\n# pop example 1")
    s = Stack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))

    print("\n# top example 1")
    s = Stack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)

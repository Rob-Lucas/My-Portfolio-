# Name: Robert Lucas
# OSU Email: lucasrob@oregonstate.edu   
# Course: CS261 - Data Structures
# Assignment: 2 Dynamic Array and ADT Implementation
# Due Date: 2/6/2023
# Description: This is a Dynamic array which contains various methods to allow better access/changing of the object associated within the Dynamic array class. Also has a Mode function. 

from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            print(index, self._size, self._capacity)
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Takes in a value which is the desired new capacity of the DynamicArray. This 
        value then is used to take the existing array, and adjust the total amount of 
        elements allowed within the array. Anything existing within the array is added 
        to the updated array.
        ------------------------------
        Input: Desired Capacity
        Output : Nothing / Changes the Array
        """
        if new_capacity <= 0 or new_capacity < self._size:
            return
        new_data = StaticArray(new_capacity)    
        for i in range(self._size): #Assigns old values to the new array of appropriate size
            new_data.set(i, self.get_at_index(i))
        self._data = new_data
        self._capacity=new_capacity

    def append(self, value: object) -> None:
        """
        Takes in a value which is then appended to the array. The position will 
        be whatever position is at the end of the array. If size is at cap, the 
        capacity is doubled.
        ---------------------------------
        Input : Desired value to append
        Result : Adds to the array.
        """
        size=self._size
        if size == self.get_capacity(): #If size is at maximum, then double it
            self.resize(2 * self.get_capacity())
        self._size += 1
        self._data[self._size-1]= value

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Adds a value to a specified index of the DynamicArray. 0 is the start. 
        If the input is invalid, the method will raise a DynamicArrayException.
        If the array is already full, the capacity of the array will be doubled.
        --------------------------------
        Input : Index Value , Desired value 
        Result : Updated array with all values that were there before but desired value in place of index.
        """
        size = self._size
        if index < 0 or index > self._size: #Raise error if index out of range
            raise DynamicArrayException("Index out of range") 
        
        if self._size == self._capacity: #Change size if size hits maximum
            self.resize(self._capacity * 2)
        self._size += 1        
        for i in range(size, index, -1):    #Set value at index location. 
            self.set_at_index(i, self.get_at_index(i - 1))
        
        self.set_at_index(index, value)

    def remove_at_index(self, index: int) -> None:
        """
        Takes in an index at which you want to remove an element. Once removed,
        the array will shift all values to the left to fill that element. If enough
        values are removed (1/4 the capacity, bot not if below 10) then the capacity size
        will half in its value.
        ------------------------
        Input : Index of Removal (int)
        Result : Updated array with desired element removed.
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException("Invalid index")
        if self._size < self._capacity / 4 and self._capacity > 10:
            self._capacity = max(2 * self._size, 10)
            new_data = StaticArray(self._capacity)
            for i in range(self._size):
                if i < index:
                    new_data[i] = self._data[i]
                elif i > index:
                    new_data[i - 1] = self._data[i]
            self._data = new_data
        else:
            for i in range(index + 1, self._size):
                self._data[i - 1] = self._data[i]
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Has two inputs desired index, and size. These two values are used to return all of 
        the values between the indicated element, and the amount of elements you wish to return.
        Inputs must be int
        -------------
        Input : Index start point, number of elements after that point.
        Result : Returns the values as a new DynamicArray Object.
        """
        if start_index < 0 or start_index >= self._size: #Raise an error if the start index is invalid
            raise DynamicArrayException("Invalid start index")   
        if size < 0 or start_index + size > self._size: #Raise an error if the size is invalid or the slice would exceed the size of the array
            raise DynamicArrayException("Invalid size or not enough elements")
        sliced_array = DynamicArray() #Create a new DynamicArray object for the sliced data
        for i in range(start_index, start_index + size): #Append the requested number of elements to the new DynamicArray object
            sliced_array.append(self._data[i])
        return sliced_array

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Takes in the used Object and combines it with a chosen object of the DynamicArray class.
        Note : This does not take in two objects, it uses one object and then takes in just one object.
        ----------------
        Input:  (your-object).merge(your-second-object)
        Result: Your main object becomes the merged array
        """
        second_da_size = second_da.length()
        for i in range(second_da_size):   #Appends the values of the new array
            self.append(second_da[i])

    def map(self, map_func) -> "DynamicArray":
        """
        Takes in a given map function and creates a new array by using the function on the
        given object. The function is determined by the user.
        -------------------
        Input: Desired Function and its attached object
        Output: New updated array object
        """
        new_da = DynamicArray()
        for i in range(self._size):
            new_da.append(map_func(self.get_at_index(i))) #apply map_func to each element and append it to the new DynamicArray
        return new_da

    def filter(self, filter_func) -> "DynamicArray":
        """
        Creates a new DynamicArray object and populates it with all the values that
        filter_func runs True from the DynamicArray input for the given filter method.
        --------
        Input : Desired Function and its attached object
        Output: New updated array object
        """
        new_da = DynamicArray()
        for i in range(self._size):
            if filter_func(self.get_at_index(i)): #Checks if function returns true
                new_da.append(self.get_at_index(i)) #Populates new object
        return new_da

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Uses given reduce function and returns the resulting value of each element when input 
        into that function. If no parameter is given, the first element of the object is
        the initializer, otherwise, the initializer is taken. If the array contains 
        no elements then the initializer is returned or None is returned if no initializer.

        """
        result = initializer
        if result is None:  #Checking if the initializer is 0 and later if the array is empty 
            if self._size == 0:
                return None #Returns None if no initializer or elements
            result = self._data[0]
            start_index = 1
        else:
            start_index = 0
        for i in range(start_index, self._size):    #runs the loop for the function
            result = reduce_func(result, self._data[i])
        return result

def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    Takes in a DynamicArray object and outputs the mode:
    Return ---> Tuple(Mode, Frequency)
    Input ---> DynamicArray
    """
    current_value = arr.get_at_index(0) #Get current values
    current_frequency = 1
    max_frequency = 1
    mode = DynamicArray()
    mode.append(current_value)
    
    for i in range(0, arr.length()): #Checks frequency of occuring values within array
        if arr.get_at_index(i) == current_value:
            current_frequency += 1
        else:
            if current_frequency > max_frequency:
                mode = DynamicArray()
                mode.append(current_value)
                max_frequency = current_frequency
            elif current_frequency == max_frequency:
                mode.append(current_value)
            current_frequency = 1
        current_value = arr.get_at_index(i)
    return (mode, max_frequency)  # Returns resulting tuple


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")

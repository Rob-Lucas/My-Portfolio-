# Name: Robert Lucas    
# OSU Email: lucasrob@oregonstate.edu
# Course:     CS261 - Data Structures
# Assignment: Assignment 1
# Due Date: 1/30/2023
# Description: Creates various functions for StaticArray class which have unique functions based on their use case.


import random
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------

def min_max(arr: StaticArray) -> (int, int):
    """
    This function takes in one value which is an object of 
    the StaticArray class. This value is then checked for its
    lowest and highest value and returns a tuple of (min,max). 
    """
    min_val = arr.get(0)
    max_val = arr.get(0)       #Set to basic value to initialize. Having these be the first element allows for sorting of single element lists
    for i in range(0, arr.length()):
        if arr.get(i) < min_val:    # Checks element and assess the value and if it is higher than current assigned min value
            min_val = arr.get(i)
        elif arr.get(i) > max_val: # Same as min, just for max
            max_val = arr.get(i)
    return (min_val, max_val)

# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------

def fizz_buzz(arr: StaticArray) -> StaticArray:
    """
    Takes in a StaticArray object and returns a new object for these restrictions
    fizz = number is divisble by 3
    buzz = number is divisible by 5
    fizzbuzz = number is divisible by 3 and 5
    """
    new_arr = StaticArray(arr.length()) #Creates new array for returning
    for i in range(0, arr.length()):
        if arr.get(i) % 3 == 0 and arr.get(i) % 5 == 0: #These check the values of location and assign the new locations depending on the value
            new_arr.set(i,"fizzbuzz")
        elif arr.get(i) % 3 == 0: 
            new_arr.set(i,"fizz")
        elif arr.get(i) % 5 == 0: 
            new_arr.set(i,"buzz")
        else:
            new_arr.set(i,arr.get(i))   #Just sets old value to same location if it passes all checks
    return new_arr

# ------------------- PROBLEM 3 - REVERSE -----------------------------------

def reverse(arr: StaticArray) -> None:
    """
    Takes in a StaticArray object and reverses its contents.
    It does this by taking two cursors, starting from beginning
    and end and sweeps through updating their side with the value on the 
    other side.
    """
    left = 0    # Dictate cursor location
    right = arr.length() - 1    # Dictate cursor location
    while left < right:
        left_cursor = arr.get(left) # These save the information before overwritten
        right_cursor = arr.get(right)
        arr.set(left, right_cursor)
        arr.set(right, left_cursor)
        left += 1
        right -= 1

# ------------------- PROBLEM 4 - ROTATE ------------------------------------

def rotate(arr: StaticArray, steps: int) -> StaticArray:
    """
    Receives two parameters (StaticArray object, Steps to the right or left)
    The steps takes in a value and moves all the values to the right or 
    left by the indicated value. Once done this function returns a new 
    StaticArray object containing the update. 
    Positive = To the Right
    Negative = To the Left
    return --> new_array
    """
    num = arr.length()
    new_arr = StaticArray(num)
    for i in range(num):
        new_arr.set((i + steps) % num, arr.get(i)) #takes the value and iterates rotation while using mod to lower size of steps.
    return new_arr



# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------

def sa_range(start: int, end: int) -> StaticArray:
    """
    Takes in two variables (start,end) and then uses the two
    to build an array with StaticArray and fills in all numbers
    between start and end, it then returns the StaticArray object.
    return --> new_array
    """
    if start < end: #Determines size of start and if start comes before or after end
        new_arr = StaticArray(end - start + 1)  
        for i in range(start, end + 1): 
            new_arr.set(i - start, i)
    elif start > end:
        new_arr = StaticArray(start - end + 1)
        for i in range(end, start + 1):
            new_arr.set(start - i, i)
    else:
        new_arr = StaticArray(1)    #If there is only one value, sets value to start
        new_arr.set(0, start)
    return new_arr


# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------

def is_sorted(arr: StaticArray) -> int:
    """
    Takes in a StaticArray object and checks its order.
    Ascending = return 1
    Descending = return -1
    Neither = return 0
    None = Improper value input
    """
    num = arr.length()
    is_ascending = None #Determines whether the object is ascending or descending by checking each value
    if num == 1:    #Checks if there is only one value in StaticArray
        return 1
    for i in range(1, num):
        if arr.get(i) > arr.get(i-1):   #Determines ascension
            if is_ascending == False:
                return 0
            is_ascending = True
        elif arr.get(i) < arr.get(i-1): #Determines descension
            if is_ascending == True:
                return 0
            is_ascending = False
    if is_ascending == True:
        return 1
    elif is_ascending == False:
        return -1 
    return
# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------

def find_mode(arr: StaticArray) -> (int, int):
    """
    Takes in a StaticArray and checks its values and determines the mode.
    returns ----> (mode, mode_frequency)
    """
    mode = arr.get(0)
    mode_frequency = 1
    current_element = arr.get(0)
    current_frequency = 1
    for i in range(1, arr.length()):
        if current_element == arr.get(i):        # Check if the current element is the same as the previous one
            current_frequency += 1
        else: 
            if current_frequency > mode_frequency: # If not, update the mode and its frequency if needed
                mode = current_element
                mode_frequency = current_frequency
            current_element = arr.get(i)     # Reset the current element and frequency
            current_frequency = 1
    if current_frequency > mode_frequency:    # Check if the final sequence of repeating elements is the mode
        mode = current_element
        mode_frequency = current_frequency
    return (mode, mode_frequency) 

# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------

def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    Takes in a StaticArray and creates a new StaticArray object which saves the values of each element only once.
    If an element occurs twice, it will not place that value into the new array object. The function then sets a 
    second new array to the size of the new array and uses another for loop to populate the values.
    returns -----> solution_arr or a new array object 
    """
    new_arr = StaticArray(arr.length()) #Creates initial object to be populated
    new_size = 0
    for i in range(arr.length()):   #Places all values into new array
        if i == 0 or arr.get(i) != arr.get(i - 1):
            new_arr.set(new_size, arr.get(i))
            new_size +=1
    if new_size == arr.length():    #Saves time if duplications don't exist
        return new_arr
    solution_arr = StaticArray(new_size)    #Adjusts array size to new array value quantity
    for i in range(0,new_size):     # Populates the new array
        solution_arr.set(i, new_arr.get(i))
    return solution_arr


# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------

def count_sort(arr: StaticArray) -> StaticArray:
    """
    Takes in a StaticArray object and sorts a new array based on the values of the input object.
    This is done in order greatest to least.
    returns --> sorted array
    """
    min_value = arr.get(0)
    max_value = arr.get(0)
    len_num = arr.length()
    for i in range(1, len_num): # Find the range of the input array
        if arr.get(i) < min_value:
            min_value = arr.get(i)
        elif arr.get(i) > max_value:
            max_value = arr.get(i)
    count = max_value - min_value + 1
    count_array = StaticArray(count) # Create the count array
    for i in range(count):
        count_array.set(i, 0)
    for i in range(len_num):   # Count the occurrences of each value in the input array
        count_array.set(arr.get(i) - min_value, count_array.get(arr.get(i) - min_value) + 1)
    for i in range(1, count): # Calculate the starting index for each value in the sorted array
        count_array.set(i, count_array.get(i) + count_array.get(i - 1))
    sorted_array = StaticArray(len_num) # Create the sorted array
    for i in range(len_num - 1, -1, -1): 
        sorted_array.set(len_num - count_array.get(arr.get(i) - min_value), arr.get(i))
        count_array.set(arr.get(i) - min_value, count_array.get(arr.get(i) - min_value) - 1)
        
    return sorted_array

# ------------------- PROBLEM 10 - SORTED SQUARES ---------------------------

def sorted_squares(arr: StaticArray) -> StaticArray:
    """
    Takes in a StaticArray object and returns a new organized list from lowest to highest of 
    the values given squared. Orders lowest to highest.
    returns ---> new array object
    """
    len_num = arr.length()
    new_arr = StaticArray(len_num)
    left = 0
    right = len_num - 1
    index = len_num - 1
    
    while left <= right:    #Iterates through the array and replaces values with the sorted squares lowest to highest.
        left_cursor = arr.get(left)
        right_cursor = arr.get(right)
        if abs(left_cursor) > right_cursor:
            new_arr.set(index, left_cursor * left_cursor)
            left += 1
        else:
            new_arr.set(index, right_cursor * right_cursor)
            right -= 1
        index -= 1
    
    return new_arr

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]: 3}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")
        print(result)

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        result = min_max(arr)
        if result:
            print(f"Min: {result[0]: 3}, Max: {result[1]}")
        else:
            print("min_max() not yet implemented")

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-95, -89), (-89, -95)]
    for start, end in cases:
        print(f"Start: {start: 4}, End: {end: 4}, {sa_range(start, end)}")

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = is_sorted(arr)
        space = "  " if result and result >= 0 else " "
        print(f"Result:{space}{result}, {arr}")

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value

        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        before = arr if len(case) < 50 else 'Started sorting large array'
        print(f"Before: {before}")
        result = count_sort(arr)
        after = result if len(case) < 50 else 'Finished sorting large array'
        print(f"After : {after}")

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')

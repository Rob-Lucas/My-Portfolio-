# Name: Robert Lucas
# OSU Email: lucasrob@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 Hashmap
# Due Date: 03/17/2023
# Description:


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key and value pair indicated within the hash map.
        """
        # Check if the table needs to be resized
        if self.table_load() >= 1.0:
            # Double the current capacity
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        # Calculate the bucket index
        index = self._hash_function(key) % self._capacity

        # Get the linked list for the bucket
        linked_list = self._buckets[index]

        # Check if the key already exists in the linked list
        node = linked_list.contains(key)

        if node:
            # Update the value of the existing key
            node.value = value
        else:
            # Add the new key/value pair to the linked list
            linked_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets.
        """
        count = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                count += 1
        return count


    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        if self._size == 0:
            return 0.0
        return self._size / self._capacity


    def clear(self) -> None:
        """
        Clears hash table without adjusting capacity.
        """
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of internal hash table by given int.
        """
        if new_capacity < 1:
            return

        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        new_table = HashMap(new_capacity, self._hash_function)

        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            for node in bucket:
                new_table.put(node.key, node.value)

        self._buckets = new_table._buckets
        self._capacity = new_table._capacity
        
        # Initialize the linked list in each bucket of the new table
        for i in range(self._capacity):
            if not self._buckets[i]:
                self._buckets[i] = LinkedList()

        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

    def get(self, key: str):
        """
        Returns value of associated key. If not in map, return None.
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        
        for node in bucket:
            if node.key == key:
                return node.value
        
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if key exists in hashmap otherwise False.
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]

        for node in linked_list:
            if node.key == key:
                return True

        return False
    
    def remove(self, key: str) -> None:
        """
        Remove key and its associated value from the map.
        Do nothing if key is not in the map.
        """
        index = self._hash_function(key) % self._capacity
        ll = self._buckets[index]

        node = ll.contains(key)
        if node:
            ll.remove(key)
            self._size -= 1


    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a DynamicArray containing all key/value pairs in the hash map
        """
        pairs = DynamicArray()
        for i in range(self._buckets.length()):
            linked_list = self._buckets[i]
            for node in linked_list:
                pairs.append((node.key, node.value))
        return pairs
    
    def get_values(self) -> DynamicArray:
        """
        Helper method for find_mode. Return a DynamicArray containing all values in the hash map
        """
        values = DynamicArray()
        for i in range(self._buckets.length()):
            linked_list = self._buckets[i]
            for node in linked_list:
                values.append(node.value)
        return values

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes in a DynamicArray object and returns a tuple of the 
    mode and how often it appears. (mode,frequency)
    """
    count_map = HashMap()

    # Count the frequency of each item in the array
    for i in range(da.length()):
        key = da[i]
        if count_map.contains_key(key):
            count_map.put(key, count_map.get(key) + 1)
        else:
            count_map.put(key, 1)

    # Find the mode(s) and the highest frequency
    modes = DynamicArray()
    max_count = 0
    
    for i in range(count_map.get_capacity()):
        bucket = count_map._buckets[i]
        if bucket.length() == 0:
            continue
        for node in bucket:
            if node.value > max_count:
                modes = DynamicArray([node.key])
                max_count = node.value
            elif node.value == max_count:
                modes.append(node.key)

    return modes, max_count
# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")

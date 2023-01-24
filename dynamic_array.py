# This work was inspired by William Fiset YouTube series on Data Structures
# https://www.youtube.com/watch?v=tvw4v7FEF1w&list=PLDV1Zeh2NRsB6SWUrDFW2RmDotAfPbeHu&index=5

class StaticArray:
    def __init__(self, capacity=32):
        self.__capacity = capacity
        self.__array = [None for _ in range(capacity)]

    @property
    def array(self):
        return self.__array


class DynamicArray:

    def __init__(self, capacity=32):
        self._length = 0
        self._initial_capacity = capacity
        self._capacity = capacity
        self._static_array = StaticArray(self._capacity).array

    def __str__(self):
        return str(self._static_array)

    @property
    def array(self):
        return self._static_array[:self._length]

    def get(self, pos):
        if pos < 0 or pos > self._length:
            raise IndexError("Index out of bounds")
        return self._static_array[pos]

    @property
    def length(self):
        return self._length

    def clear(self):
        self._length = 0
        self._static_array = [None for _ in range(self._capacity)]

    @property
    def is_empty(self):
        return self._length == 0

    def add(self, value):
        # Warning: values should always be contiguous,
        # there is no point in letting None values between two non None values
        self._double_capacity_when_needed()
        self._static_array[self._length] = value
        self._length += 1

    def append(self, value):
        self._double_capacity_when_needed()
        self._static_array[self._length] = value
        self._length += 1

    def remove_at(self, index):
        if index >= self._length:
            raise IndexError("Index out of bounds")
        for i in range(index, self._length - 1, 1):
            self._static_array[i] = self._static_array[i + 1]
        self._static_array[self._length - 1] = None
        self._length -= 1

    def remove(self, value):
        # All occurrences of value are removed from the array
        count_removed = 0
        for index in range(self._length):
            idx = index - count_removed
            if self._static_array and self._static_array[idx] == value:
                self.remove_at(idx)
                count_removed += 1

    def index_of(self, value):
        # Only return the first element
        for index in range(self._length):
            if self._static_array[index] == value:
                return value
        return None

    def contains(self, value):
        return self.index_of(value) is not None

    def _double_capacity_when_needed(self):
        if self._capacity == self._length:
            self._capacity *= 2
            new_static_array = StaticArray(self._capacity).array
            for i in range(self._length):
                new_static_array[i] = self._static_array[i]
            self._static_array = new_static_array


if __name__ == '__main__':
    array = DynamicArray(capacity=1)
    array.append(1)
    array.append(-6)
    array.append(5)
    print("str(array): ", array)
    print("repr(array): ", repr(array))
    assert array.array == [1, -6, 5]

    assert array._capacity == 4
    array.remove_at(1)
    assert array._capacity == 4

    assert array.array == [1, 5]
    assert array.length == 2

    array.add(0)
    assert array.array == [1, 5, 0]

    assert array.get(2) == 0

    array.remove_at(2)
    assert array.array == [1, 5]

    array.clear()
    print("array._static_array: ", array._static_array)
    assert array._capacity == 4

    array.append(1)
    array.append(2)
    array.append(2)
    assert array.array == [1, 2, 2]

    array.remove(2)
    assert array.array == [1]

    print("All tests passed successfully!")

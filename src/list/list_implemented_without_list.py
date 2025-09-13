from ctypes import py_object


class MyList:
    def __init__(self):
        self.__size = 0
        self._capacity = 1
        self.__list = self.__create(self._capacity)

    def __repr__(self):
        return f"[{', '.join(str(self.__list[i]) for i in range(self.__size))}]"

    def __len__(self):
        return self.__size

    def __getitem__(self, index):
        new_index = index

        if index < 0:
            new_index = self.__size + new_index

        if not 0 <= new_index < self.__size:
            raise IndexError(f"Index '{index}' out of range")

        return self.__list[new_index]

    def append(self, val):
        if self.__size == self._capacity:
            self.__resize(self._capacity * 2)

        self.__list[self.__size] = val
        self.__size += 1

    def pop(self):
        if self.__size == 0:
            raise IndexError(f"List is already empty")

        old_val = self.__list[self.__size - 1]
        self.__list[self.__size - 1] = None

        self.__size -= 1

        self.__shrink()

        return old_val

    def __create(self, capacity):
        return (capacity * py_object)()

    def __resize(self, new_capacity):
        new_arr = self.__create(new_capacity)

        for i in range(self.__size):
            new_arr[i] = self.__list[i]

        self.__list = new_arr
        self._capacity = new_capacity

    def __shrink(self):
        """
        Shrink the capacity of the list every time number of elements are
        lower or equal to capacity.
        """
        if self._capacity > 1 and self.__size <= self._capacity // 4:
            self.__resize(self._capacity // 2)

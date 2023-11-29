import ctypes
from typing import Protocol, Generic, TypeVar


T = TypeVar('T')


class AbsDynArray(Protocol, Generic[T]):
    """
    АТД динамического массива 
    make_array не нужна и должна быть скрыта от пользователя в реализации
    """

    # Конструктор
    def __init__(self, capacity=16) -> None:
        """
        Конструктор

        Постусловие: создан объект класса DynArray
                     с заданным начальным объемом массива
        """

    # Команды
    def append(self, item: T) -> None:
        """
        Вставка в конец массива

        Постусловие: в конец массива добавлено значение item, количесто элементов массива += 1
        Постусловие: объем массива увеличен в 2 раза, при необходмости
        """

    def insert(self, item: T, index: int) -> None:
        """
        Вставка на место index, если index == self.count, то вставка в конец массива

        Предусловие: значение index больше нуля и меньше или равно!, чем значение размера массива

        Постусловие: в конец массива добавлено значение item
        Постусловие: количесто элементов массива count += 1
        Постусловие: объем массива увеличен в 2 раза, при необходмости
        """

    def remove(self, index: int) -> None:
        """
        Удаление элемента на месте index

        Предусловие: значение index больше нуля и меньше, чем значение размера массива

        Постусловие: в конец массива добавлено значение item
        Постусловие: количесто элементов массива count -= 1
        Постусловие: объем массива уменьшен в 2 раза,
                     при необходмости, но не меньше чем базовое значение capacity
        """

    # Запросы
    def __getitem__(self, index: int) -> T:
        """
        Возвращает значение на месте index

        Предусловие: существует значение в массиве с индексом index
        """
        ...

    def __len__(self) -> int:
        """
        Возвращает размер массива
        """
        ...

    def get_insert_status(self) -> int:
        """
        Статус выполнения insert
        """
        ...

    def get_remove_status(self) -> int:
        """
        Статус выполнения remove
        """
        ...

class DynArray(AbsDynArray, Generic[T]):
    INSERT_OK = 1
    INSERT_ERR = 0
    REMOVE_OK = 1
    REMOVE_ERR = 0

    # Конструктор
    def __init__(self, capacity=16) -> None:
        self.capacity = capacity
        self.base_capacity = capacity
        self.count: int = 0
        self.array = (capacity * ctypes.py_object)()

        self._insert_status = self.INSERT_OK
        self._remove_status = self.REMOVE_OK

    # Команды
    def append(self, item: T) -> None:
        if self.count == self.capacity:
            self._make_array(2 * self.capacity)
        self.array[self.count] = item
        self.count += 1

    def insert(self, item: T, index: int) -> None:
        if index < 0 or index > self.count:
            self._insert_status = self.INSERT_ERR
            return

        if self.count == self.capacity:
            self._make_array(2 * self.capacity)

        if index == self.count:
            self.array[self.count] = item
        else:
            for i in range(self.count, index, -1):
                self.array[i] = self.array[i - 1]
            self.array[index] = item
        self.count += 1
        self._insert_status = self.INSERT_OK

    def remove(self, index: int) -> None:
        if index < 0 or index >= self.count:
            self._insert_status = self.REMOVE_ERR
            return

        if (self.count -1) // self.capacity < 0.5:
            self._make_array(max(self.base_capacity, self.capacity // 2))

        for i in range(index, self.count - 1):
            self.array[i] = self.array[i + 1]

        self.count -= 1
        self._insert_status = self.REMOVE_OK

    # Скрытые команды
    def _make_array(self, new_capacity: int) -> None:
        new_array = (new_capacity * ctypes.py_object)()
        for i in range(self.count):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    # Запросы
    def __getitem__(self, index: int) -> T:
        return self.array[index]

    def __len__(self) -> int:
        return self.count

    def get_insert_status(self) -> int:
        return self._insert_status

    def get_remove_status(self) -> int:
        return self._remove_status


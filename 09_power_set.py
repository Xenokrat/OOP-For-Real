from __future__ import annotations
from typing import Protocol, Generic, TypeVar


T = TypeVar('T')


# Для экономии места, не повторяю пред и постусловия для Хэш таблицы
class AbstractHashTable(Protocol, Generic[T]):

    # Конструктор
    def __init__(self, max_size: int) -> None: ...

    # Команды
    def put(self, value: T) -> None: ...
    def remove(self, value: T) -> None: ...
    def clear(self) -> None: ...

    # Запросы
    def __len__(self) -> int: ...
    def isin(self, value: T) -> bool: ...
    def get_put_status(self) -> int: ...
    def get_delete_status(self) -> int: ...


class HashTable(AbstractHashTable, Generic[T]):
    PUT_OK = 0
    PUT_ERR = 1
    DELETE_OK = 0
    DELETE_ERR = 1

    # Конструктор
    def __init__(self, max_size: int) -> None:
        self._max_size = max_size
        self._array = []
        self._put_status = self.PUT_OK
        self._delete_status = self.DELETE_OK

    # Команды
    def put(self, value: T) -> None:
        res = self._seek_slot(value)
        if res == -1:
            self._put_status = self.PUT_ERR
        else:
            self._array[res] = value
            self._put_status = self.PUT_OK

    def remove(self, value: T) -> None:
        res = self._seek_slot(value)
        if res == -1:
            self._delete_status = self.DELETE_ERR
        else:
            self._array[res] = None
            self._delete_status = self.DELETE_OK

    def clear(self) -> None:
        self.__init__(self._max_size)

    # Запросы
    def __len__(self) -> int:
        return len(self._array)

    def isin(self, value: T) -> bool:
        res = self._seek_slot(value)
        return res != -1

    def get_put_status(self) -> int:
        return self._put_status

    def get_delete_status(self) -> int:
        return self._delete_status

    # Вспомогательные функции
    def _hash_func(self, value: T) -> int:
        """
        Hash Функция
        """
        byte_len = len(str(value).encode('utf-8'))
        hash_ = byte_len % self._max_size
        return hash_

    def _seek_slot(self, value: T) -> int:
        """
        Функция для нахождения слота в массиве
        """
        index = self._hash_func(value)
        counter = 0
        while counter < self._max_size:
            slot = self._array[index]
            
            if (slot is None) or (slot == value):
                return index
            index = (index + 2) % self._max_size
            counter += 1
            
        return -1

class AbstractPowerSet(AbstractHashTable, Protocol, Generic[T]):

    # Запросы
    # Тут я не знаю, как правильно, при пересечении, возвращается новый объект сета (более правильно, как мне кажется)
    # или модифицируется состояние текущего?
    # В первом случае, все команды ниже, это запросы, и возвращают они новый объект Сета
    #
    # Предусловия: ну уверен, нужно ли считать ошибкой например объединение множеств разных типов, что легко может произойти в Python
    # но предположу, что достаточно того, что в агрументах аннотирована переменная типа
    # Постусловия не нужны, т.к. создаем новый объект, без модификации текущего

    def intersection(self, other: AbstractPowerSet[T]) -> AbstractPowerSet[T]: 
        """
        создает создан новый объект AbstractPowerSet как пресечение множеств текущего элемента и агрумента
        """
        ...

    def union(self, other: AbstractPowerSet[T]) -> AbstractPowerSet[T]:
        """
        создает объект AbstractPowerSet как объединение множеств текущего элемента и агрумента
        """
        ...

    def difference(self, other: AbstractPowerSet[T]) -> AbstractPowerSet[T]:
        """
        создает новый объект AbstractPowerSet как разница множеств текущего элемента и агрумента
        """
        ...

    def issubset(self, other: AbstractPowerSet[T]) -> bool:
        """
        Возвращает, является ли агрумент other подмножеством текущего множества
        """
        ...


class PowerSet(AbstractPowerSet, HashTable, Generic[T]):

    def intersection(self, other: AbstractPowerSet[T]) -> AbstractPowerSet[T]: 
        new_set = PowerSet(max_size=max(len(self), len(other)))
        for item in self._array:
            if other.isin(item):
                new_set.put(item)
        return new_set

    def union(self, other: AbstractPowerSet[T]) -> AbstractPowerSet[T]:
        new_set = PowerSet(max_size=(len(self) + len(other)))
        for item in self._array:
            new_set.put(item)
        # this is wrong
        for item in other._array:
            new_set.put(item)
        return new_set

    def difference(self, other: AbstractPowerSet[T]) -> AbstractPowerSet[T]:
        new_set = PowerSet(max_size=len(self))
        for item in self._array:
            if not other.isin(item):
                new_set.put(item)
        return new_set

    def issubset(self, other: AbstractPowerSet[T]) -> bool:
        return all(other.isin(item) for item in self._array)


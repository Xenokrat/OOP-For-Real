from typing import Protocol, TypeVar, Generic


T = TypeVar('T', contravariant=True)


class AbstractHashTable(Protocol, Generic[T]):

    # Конструктор
    def __init__(self, max_size: int) -> None:
        """
        Постусловие: создан объект хэш-таблицы с заданным максимальным размером
        """
        ...

    # Команды
    def put(self, value: T) -> None:
        """
        Предусловие: размер max_size позволяет вставить элемент
        Предусловие: механизм разрешения коллизий позволяет вставить элемент
        Постусловие: в хэш таблице находится элемент value
        """
        ...

    def delete(self, value: T) -> None:
        """
        Предусловие: в таблице имеется элемент со значением value (таблица не пуста)
        Постусловие: в хэш таблице не находится элемент value
        """
        ...

    def clear(self) -> None:
        """
        Постусловие: хэш-таблица пуста
        """
        ...

    # Запросы
    def __len__(self) -> int:
        """Возвращает количество элементов в хэш-таблице"""
        ...

    def isin(self, value: T) -> bool:
        """Возвращает находится ли элемент value в хэш-таблице"""
        ...

    def get_put_status(self) -> int:
        """Возвращает статус выполнения put"""
        ...

    def get_delete_status(self) -> int:
        """Возвращает статус выполнения delete"""
        ...


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

    def delete(self, value: T) -> None:
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

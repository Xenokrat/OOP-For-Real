from typing import Protocol, TypeVar, Generic


T = TypeVar('T')


class AbstractNativeDictionary(Protocol, Generic[T]):

    # Конструктор
    def __init__(self, max_size: int) -> None:
        """
        Постусловие: создан объект словаря с заданным максимальным размером
        """
        ...

    # Команды
    def put(self, key: str, value: T) -> None:
        """
        Предусловие: размер max_size позволяет вставить элемент
        Предусловие: механизм разрешения коллизий позволяет вставить элемент
        Постусловие: в словарь добавлены строковый ключ со значением value
        """
        ... 

    def delete(self, key: str) -> None:
        """
        Предусловие: в таблице имеется ключ key
        Постусловие: из таблицы ключ элемент key и его значение
        """
        ...

    def clear(self) -> None:
        """
        Постусловие: пустой словарь
        """
        ...

    # Запросы
    def __len__(self) -> int:
        """Возвращает количество элементов в словаре"""
        ...

    def is_key(self, key: str) -> bool:
        """Возвращает находится ли элемент value в словаре"""
        ...

    def get(self, key: str) -> T:
        """
        Возвращает значение элемента key
        Предусловие: элемент key находится в словаре
        """
        ...

    # Запросы выполнения команд
    def get_put_status(self) -> int:
        """Возвращает статус выполнения put"""
        ...

    def get_delete_status(self) -> int:
        """Возвращает статус выполнения delete"""
        ...

    def get_get_status(self) -> int:
        """Возвращает статус выполнения get"""
        ...


class NativeDictionary(AbstractNativeDictionary, Generic[T]):
    PUT_OK = 0
    PUT_ERR = 1
    DELETE_OK = 0
    DELETE_ERR = 1
    GET_OK = 0
    GET_ERR = 1

    # Конструктор
    def __init__(self, max_size: int) -> None:
        self._max_size = max_size
        self._slots: list[str | None] = [None] * self._max_size
        self._values: list[T | None] = [None] * self._max_size
        self._put_status = self.PUT_OK
        self._delete_status = self.DELETE_OK
        self._get_status = self.GET_OK

    # Приватные функции
    def _hash_func(self, key: str) -> int:
        """
        Hash Функция
        """
        byte_len = len(key.encode('utf-8'))
        return byte_len % self._max_size

    def _seek_slot(self, key: str) -> int:
        """
        Функция для нахождения слота в массиве
        """
        index = self._hash_func(key)
        counter = 0
        while counter < self._max_size:
            slot = self._slots[index]
            if (slot is None) or (slot == key):
                return index
            index = (index + 2) % self._max_size
            counter += 1
        return -1

    # Команды
    def put(self, key: str, value: T) -> None:
        res = self._seek_slot(key)
        if res == -1:
            self._put_status = self.PUT_ERR
        else:
            self._slots[res] = key
            self._values[res] = value
            self._put_status = self.PUT_OK

    def delete(self, key: str) -> None:
        res = self._seek_slot(key)
        if res == -1:
            self._delete_status = self.DELETE_ERR
        else:
            self._slots[res] = None
            self._values[res] = None
            self._delete_status = self.DELETE_OK

    def clear(self) -> None:
        self.__init__(self._max_size)

    # Запросы
    def __len__(self) -> int:
        return len(list(filter(lambda x: x is not None, self._slots)))

    def is_key(self, key: str) -> bool:
        res = self._seek_slot(key)
        return res != -1

    def get(self, key: str) -> T | int:
        res = self._seek_slot(key)
        if res == -1:
            self._get_status = self.GET_ERR
            result = -1
        else:
            result = self._values[res]
            self._get_status = self.GET_OK
        return result

    # Запросы выполнения команд
    def get_put_status(self) -> int:
        return self._put_status

    def get_delete_status(self) -> int:
        return self._delete_status

    def get_get_status(self) -> int:
        return self._get_status


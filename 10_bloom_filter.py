from typing import Protocol, TypeVar, Generic


T = TypeVar('T')

class AbsBloomFilter(Protocol, Generic[T]):

    # Конструктор
    def __init__(self, filter_len: int) -> None:
        """
        Постусловие: создан объект фильтра Блума с заданной длиной
        """
        ...

    # Команды
    def add(self, item: T) -> None:
        """
        Постусловие: в битовую маску добавлены значения, соответствующие результату
                     хэширования string
        """
        ...

    def clear(self) -> None:
        """
        Постусловие: все значения фильтра полностью очищены
        """
        ...

    # Запросы
    def is_value(self, item: T) -> bool:
        """Возвращает, принадлежит ли string фильтру"""
        ...


class BloomFilter(AbsBloomFilter):
    HASH_SALT: list[int] = [17, 223]

    # Конструктор
    def __init__(self, filter_len: int) -> None:
        self._filter_len = filter_len
        self._bitarray = 1 << filter_len

    # Команды
    def add(self, string: str) -> None:
        position_list = self._hash(string)
        for pos in position_list:
            self._bitarray = self._bitarray | (1 << pos)

    def clear(self) -> None:
        self.__init__(self._filter_len)

    # Запросы
    def is_value(self, string: str) -> bool:
        position_list = self._hash(string)
        return all(self._bitarray & (1 << pos) for pos in position_list)

    # Приватные методы
    def _hash(self, string: str) -> list[int]:
        res_list: list[int] = []
        for rand_num in self.HASH_SALT:
            res = 0
            for char in string:
                code = ord(char)
                res = ((res * rand_num) + code) % self._filter_len
            res_list.append(res)
        return res_list


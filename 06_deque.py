from typing import Protocol, TypeVar, Generic


T = TypeVar('T')


# Эта часть аналогична занятию по Queue
class AbstractParentQueue(Protocol, Generic[T]):

    # Constructor
    def __init__(self) -> None:
        """
        Постусловие: создается и инициализируется пустая очередь
        """
        ...

    # Commands
    def add_tail(self, value: T) -> None: 
        """
        Постусловие: добавлен новый элемент value в конец очереди
        """
        ...

    def remove_front(self) -> None: 
        """
        Предусловие: очередь не пустая
        Постусловие: из начала очереди удален последний элемент
        """
        ...

    # Queries
    def size(self) -> int: ...

    def get_front(self) -> T: 
        """
        Предусловие: очередь не пустая
        """
        ...

    def get_remove_front_status(self) -> int:
        """
        Возвращает статус выполения команды remove_front
        """
        ...

    def get_get_front_status(self) -> int:
        """
        Возвращает статус выполения команды get_front
        """
        ...


# АТД для деки
class AbstractDeque(AbstractParentQueue, Protocol):

    # Commands
    def add_front(self) -> None:
        """
        Постусловие: добавлен новый элемент value в начало очереди
        """
        ...

    def remove_tail(self) -> None:
        """
        Предусловие: очередь не пустая
        Постусловие: из конца очереди удален последний элемент
        """
        ...

    # Queries
    def get_tail(self) -> None:
        """
        Предусловие: очередь не пустая
        """
        ...

    def get_remove_tail_status(self) -> int:
        """
        Возвращает статус выполения команды remove_tail
        """
        ...

    def get_get_tail_status(self) -> int:
        """
        Возвращает статус выполения команды get_tail
        """
        ...


# Реализация ParentQueue (которая, однако, не должна подразумевать создание объектов)
class ParentQueue(AbstractParentQueue, Generic[T]):
    REMOVE_FRONT_NIL = 0
    REMOVE_FRONT_OK = 1
    REMOVE_FRONT_ERR = 2
    GET_FRONT_NIL = 0
    GET_FRONT_OK = 1
    GET_FRONT_ERR = 2


    # Constructor 
    def __init__(self) -> None:
        self._array = []
        self._remove_front_status = self.REMOVE_FRONT_NIL
        self._get_front_status = self.GET_FRONT_NIL

    # Commands
    def add_tail(self, value: T) -> None: 
        self._array.insert(0, value)

    def remove_front(self) -> None: 
        if len(self._array) == 0:
            self._remove_front_status = self.REMOVE_FRONT_ERR
        self._array.pop()
        self._remove_front_status = self.REMOVE_FRONT_OK

    def clear(self) -> None: 
        self.__init__()

    # Queries
    def size(self) -> int: 
        return len(self._array)

    def get_front(self) -> T: 
        if len(self._array) == 0:
            self._get_front_status = self.GET_FRONT_ERR
        res = self._array.pop()
        self._get_front_status = self.GET_FRONT_OK
        return res

    def get_remove_front_status(self) -> int:
        return self._remove_front_status

    def get_get_front_status(self) -> int:
        return self._get_front_status


# Конретный класс, для создания объектов для Queue
class Queue(ParentQueue): ...


# Реализация деки
class Deque(ParentQueue, Generic[T]):
    REMOVE_TAIL_NIL = 0
    REMOVE_TAIL_OK = 1
    REMOVE_TAIL_ERR = 2
    GET_TAIL_NIL = 0
    GET_TAIL_OK = 1
    GET_TAIL_ERR = 2

    # Constructor 
    def __init__(self) -> None:
        super().__init__()
        self._remove_tail_status = self.REMOVE_TAIL_NIL
        self._get_tail_status = self.GET_TAIL_NIL

    # Commands
    def add_front(self, value: T) -> None:
        self._array.append(value)

    def remove_tail(self) -> None:
        if self.size() > 0:
            self._array.pop()
            self._remove_tail_status = self.REMOVE_TAIL_OK
        else:
            self._remove_tail_status = self.REMOVE_TAIL_ERR

    # Queries
    def get_tail(self) -> T | int:
        if self.size() > 0:
            return self._array[-1]
        else:
            return 0

    def get_remove_tail_status(self) -> int:
        return self._remove_tail_status

    def get_get_tail_status(self) -> int:
        return self._get_tail_status


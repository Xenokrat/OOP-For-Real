from typing import Protocol, TypeVar, Generic


T = TypeVar('T')


class AbstractQueue(Protocol, Generic[T]):

    # Constructor
    def __init__(self) -> None:
        """
        Постусловие: создается и инициализируется пустая очередь
        """
        ...

    # Commands
    def enqueue(self, value: T) -> None: 
        """
        Постусловие: добавлен новый элемент value в начало очереди
        """
        ...
    def dequeue(self) -> None: 
        """
        Предусловие: очередь не пустая
        Постусловие: из конца очереди удален последний элемент
        """
        ...
    def clear(self) -> None: 
        """
        Постусловие: из очереди удалены все элементы
        """
        ...

    # Queries
    def size(self) -> int: 
        """
        """
        ...
    def peek(self) -> T: 
        """
        Предусловие: очередь не пустая
        """
        ...

    def get_dequeue_status(self) -> int:
        """
        Возвращает статус выполения команды dequeue
        """
        ...

    def get_peek_status(self) -> int:
        """
        Возвращает статус выполения команды peek
        """
        ...


class Queue(AbstractQueue, Generic[T]):
    DEQUEUE_NIL = 0
    DEQUEUE_OK = 1
    DEQUEUE_ERR = 2
    PEEK_NIL = 0
    PEEK_OK = 1
    PEEK_ERR = 2


    # Constructor
    def __init__(self) -> None:
        self._array = []
        self._dequeue_status = self.DEQUEUE_NIL
        self._peek_status = self.PEEK_NIL

    # Commands
    def enqueue(self, value: T) -> None: 
        self._array.insert(0, value)

    def dequeue(self) -> None: 
        if len(self._array) == 0:
            self._dequeue_status = self.DEQUEUE_ERR
        self._array.pop()
        self._dequeue_status = self.DEQUEUE_OK

    def clear(self) -> None: 
        self.__init__()

    # Queries
    def size(self) -> int: 
        return len(self._array)

    def peek(self) -> T: 
        if len(self._array) == 0:
            self._peek_status = self.PEEK_ERR
        res = self._array.pop()
        self._peek_status = self.PEEK_OK
        return res

    def get_dequeue_status(self) -> int:
        return self._dequeue_status

    def get_peek_status(self) -> int:
        return self._peek_status


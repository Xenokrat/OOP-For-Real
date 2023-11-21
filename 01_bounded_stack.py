from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class AbstractBoundedStack(ABC, Generic[T]):
    """
    Абстрактный класс стека, ограниченного по размеру
    """
    POP_NIL: int = 0
    POP_OK: int = 1
    POP_ERR: int = 2

    PEEK_NIL: int = 0
    PEEK_OK: int = 1
    PEEK_ERR: int = 2

    # Теперь команда push больше не явная,
    # и требуется реализация статуса ее работы
    PUSH_NIL: int = 0
    PUSH_OK: int = 1
    PUSH_ERR: int = 2

    @abstractmethod
    def __init__(self, stack_size_cap: int = 32) -> None:
        pass

    @abstractmethod
    def push(self, value: T) -> None:
        """
        Предусловие: стек меньше максимального размера
        Постусловие: в стек добавлено новое значение
        """
        pass

    @abstractmethod
    def pop(self) -> None:
        """
        Предусловие: стек не пустой
        Постусловие: из стека удален верхний элемент
        """
        pass

    @abstractmethod
    def peek(self) -> T:
        """
        Предусловие: стек не пустой
        """
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Постусловие: из стека удаляются все значения
        """
        pass

    # Запросы статусов
    @abstractmethod
    def get_pop_status(self) -> int:
        """
        Возвращает статус выполнения команды pop
        """
        pass

    @abstractmethod
    def get_peek_status(self) -> int:
        """
        Возвращает статус выполнения команды peek
        """
        pass

    @abstractmethod
    def get_push_status(self) -> int:
        """
        Возвращает статус выполнения команды push
        """
        pass


class BoundedStack(AbstractBoundedStack):
    """
    Реализация класса стека, ограниченного по размеру
    Константы наследуются из абстрактного класса
    """

    def __init__(self, stack_size_cap: int = 32) -> None:
        # Скрытые поля
        self._stack: list[T] = []
        self._peek_status: int = self.PEEK_NIL
        self._pop_status: int = self.POP_NIL
        self._push_status: int = self.PUSH_NIL

        assert stack_size_cap > 0, "Размер стека - положительное число"
        self._stack_size_cap = stack_size_cap

    def push(self, value: T) -> None:
        # Проверяем предусловие
        if self.size() < self._stack_size_cap:
            self._stack.append(value)
            self._push_status = self.PUSH_OK
        else:
            self._push_status = self.PUSH_ERR

    def pop(self) -> None:
        if self.size() > 0:
            self._stack.pop()
            self._pop_status = self.POP_OK
        else:
            self._pop_status = self.POP_ERR

    def peek(self) -> T:
        if self.size() > 0:
            result = self._stack[-1]
            self._pop_status = self.PEEK_OK
        else:
            self._pop_status = self.PEEK_ERR
            result = 0
        return result

    def size(self) -> int:
        return len(self._stack)

    def clear(self) -> None:
        self._stack.clear()
        self._peek_status = self.PEEK_NIL
        self._pop_status = self.POP_NIL
        self._push_status = self.PUSH_NIL

    # Запросы статусов
    def get_pop_status(self) -> int:
        return self._pop_status

    def get_peek_status(self) -> int:
        return self._peek_status

    def get_push_status(self) -> int:
        return self._push_status

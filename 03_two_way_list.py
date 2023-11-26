from abc import ABC
from typing import Generic, TypeVar, Self


T = TypeVar('T')


class Node(Generic[T]):
    """
    Реализация Узла списка
    """

    def __init__(self, value: T) -> None:
        """
        Конструктор

        Постусловие: создан новый объект Node со значением value
        """

        self.value = value
        self.left: Self | None = None
        self.right: Self | None = None

# АТД Parent List, в общем, аналогичен АТД из предыдущего занятия


class ParentList(ABC, Generic[T]):
    """
    Частичная реализация для классов связных списков
    Созан как абстрактный класс, чтобы нельзя было создать объект этого класса
    """

    HEAD_OK: int = 1
    HEAD_ERR: int = 2
    TAIL_OK: int = 1
    TAIL_ERR: int = 2
    PUT_RIGHT_OK: int = 1
    PUT_RIGHT_ERR: int = 2
    PUT_LEFT_OK: int = 1
    PUT_LEFT_ERR: int = 2
    RIGHT_OK: int = 1
    RIGHT_ERR: int = 2
    REMOVE_OK: int = 1
    REMOVE_ERR: int = 2
    REPLACE_OK: int = 1
    REPLACE_ERR: int = 2
    GET_OK: int = 1
    GET_ERR: int = 2
    FIND_OK: int = 1
    FIND_ERR: int = 2

    def __init__(self) -> None:
        """
        Конструктор

        Постусловие: создан новый пустой связный список
        """

        self._head: Node | None = None
        self._tail: Node | None = None
        self._cursor: Node | None = None

        self._head_status: int = self.HEAD_OK
        self._tail_status: int = self.TAIL_OK
        self._put_right_status: int = self.PUT_RIGHT_OK
        self._put_left_status: int = self.PUT_LEFT_OK
        self._right_status: int = self.RIGHT_OK
        self._remove_status: int = self.REMOVE_OK
        self._replace_status: int = self.REPLACE_OK
        self._get_status: int = self.FIND_OK
        self._find_status: int = self.FIND_OK

    # Комманды
    # Элементарные операции
    def head(self) -> None:
        """
        Установить курсор на первый узел в списке

        Предусловие: список не пустой
        Постусловие: курсор находится на первом элементе в списке
        """

        if not self.is_value():
            self._head_status = self.HEAD_ERR
        else:
            self._cursor = self._head
            self._head_status = self.HEAD_OK

    def tail(self) -> None:
        """
        Установить курсор на последний узел в списке

        Предусловие: список не пустой
        Постусловие: курсор находится на последнем элементе в списке
        """

        if not self.is_value():
            self._tail_status = self.TAIL_ERR
        else:
            self._cursor = self._tail
            self._tail_status = self.TAIL_OK

    def right(self) -> None:
        """
        Сдвинуть курсор на один узел вправо

        Предусловие: список не пустой и существует узел справа
        Постусловие: курсор смещен к правому элементу
        """

        if not self.is_value():
            self._right_status = self.RIGHT_ERR
        elif self._cursor.right is None:
            self._right_status = self.RIGHT_ERR
        else:
            self._cursor = self._cursor.right
            self._right_status = self.RIGHT_OK

    def put_right(self, value: T) -> None:
        """
        Вставить следом за текущим узлом
        новый узел с заданным значением

        Предусловие: список не пустой
        Постусловие: создан новый узел справа от курсора с значением value
        """

        if not self.is_value():
            self._put_right_status = self.PUT_RIGHT_ERR

        elif self.is_tail():
            self._tail.right = Node(value)
            self._tail.right.left = self._tail
            self._tail = self._tail.right
            self._put_right_status = self.PUT_RIGHT_OK

        else:
            next_node = self._cursor.right
            self._cursor.right = Node(value)
            self._cursor.right.left = self._cursor
            self._cursor.right.right = next_node
            next_node.left = self._cursor.right
            self._put_right_status = self.PUT_RIGHT_OK

    def put_left(self, value: T) -> None:
        """
        Вставить перед текущим узлом
        новый узел с заданным значением

        Предусловие: список не пустой
        Постусловие: создан новый узел справа от курсора с значением value
        """

        if not self.is_value():
            self._put_left_status = self.PUT_LEFT_ERR

        elif self.is_head():
            self._head.left = Node(value)
            self._head.left.right = self._head
            self._head = self._head.left
            self._put_left_status = self.PUT_LEFT_OK

        else:
            left_node = self._cursor.left
            self._cursor.left = Node(value)
            self._cursor.left.right = self._cursor
            self._cursor.left.left = left_node
            left_node.right = self._cursor.left
            self._put_left_status = self.PUT_LEFT_OK

    def remove(self) -> None:
        """
        Удалить текущий узел

        Предусловие: список не пустой
        Постусловие: курсор смещается к правому соседу, если он есть,
                     в противном случае курсор смещается к левому соседу,
                     если он есть
        """

        if not self.is_value():
            self._remove_status = self.REMOVE_ERR

        elif self.size() == 1:
            self.clear()

        elif self.is_tail():
            self._tail = self._tail.left
            self._tail.right = None
            self._cursor = self._tail
            self._remove_status = self.REMOVE_OK

        elif self.is_head():
            self._head = self._head.right
            self._head.left = None
            self._cursor = self._head
            self._remove_status = self.REMOVE_OK

        else:
            left_node = self._cursor.left
            right_node = self._cursor.right
            left_node.right = right_node
            right_node.left = left_node
            self._remove_status = self.REMOVE_OK

    def clear(self) -> None:
        """
        Очистить список

        Постусловие: список пустой
        """

        self.__init__()

    # Комманды
    # Сводимые к другим операции
    def add_tail(self, value: T) -> None:
        """
        Добавить новый узел в хвост списка

        Постусловие: добавлен новый узел со значением value в конец списка
        """

        # Вставка в пустой список
        if not self.is_value():
            self._head = Node(value)
            self._tail = self._head
            self._cursor = self._head
        else:
            # Сделаем этот метод производным от put_right
            cursor = self._cursor
            self.tail()
            self.put_right(value)
            self._cursor = cursor

    def replace(self, value: T) -> None:
        """
        Заменить значение текущего узла на заданное

        Предусловие: курсор на некотором элементе (список не пустой)
        Постусловие: значение текущего узла изменено на value
        """

        if not self.is_value():
            self._replace_status = self.REPLACE_ERR
        else:
            self._cursor.value = value
            self._replace_status = self.REPLACE_OK

    def find(self, value: T) -> None:
        """
        Установить курсор на следующий узел
        с искомым значением (по отношению к текущему узлу)

        Постусловие: если справа существует значение value,
                     то курсор установлен на первый узел с таким значением
        """

        if self.is_value():
            cursor = self._cursor
            while self.get_right_status() == self.RIGHT_OK:
                self.right()
                if self.get() == value:
                    self._find_status = self.FIND_OK
                    return
            # Put cursor back to original place
            self._cursor = cursor
            self._find_status = self.FIND_ERR

    def remove_all(self, value: T) -> None:
        """
        Удалить в списке все узлы с заданным значением

        Постусловие: в списке нет ни одного узла со значением value
        """

        self.head()
        if self.get_head_status() == self.HEAD_ERR:
            return

        self._find_status = self.FIND_OK
        while self.get_find_status() == self.FIND_OK and self.is_value():
            if self.get() == value:
                self.remove()
            else:
                self.find(value)

    # Запросы
    # Элементарные

    def size(self) -> int:
        """
        Посчитать количество узлов в списке.
        """

        self.head()
        if self.get_head_status() == self.HEAD_ERR:
            cnt = 0
        else:
            cnt = 1
            self.right()
            while self.get_right_status() != self.RIGHT_ERR:
                cnt += 1
                self.right()
        return cnt

    def get(self) -> T | None:
        """
        Получить значение текущего узла

        Предусловие: курсор на некотором значении (список не пустой)
        """

        if not self.is_value():
            self._get_status = self.GET_ERR
            return None
        return self._cursor.value

    def is_value(self) -> bool:
        """
        Установлен ли курсор на какой-либо узел в списке (непустой ли список).
        """

        return self._cursor is not None

    # Запросы
    # Производные
    def is_head(self) -> None:
        """
        Находится ли курсор в начале списка?
        """

        return self._head is self._cursor

    def is_tail(self) -> None:
        """
        Находится ли курсор в конце списка?
        """

        return self._tail is self._cursor

    # Запросы на статус выполенения команд

    def get_head_status(self) -> int:
        """Возвращает статус выполения команды head"""
        return self._head_status

    def get_tail_status(self) -> int:
        """Возвращает статус выполнения команды tail"""
        return self._tail_status

    def get_right_status(self) -> int:
        """Возвращает статус выполнения команды right"""
        return self._right_status

    def get_put_right_status(self) -> int:
        """Возвращает статус выполнения команды put_right"""
        return self._put_right_status

    def get_put_left_status(self) -> int:
        """Возвращает статус выполнения команды put_left"""
        return self._put_left_status

    def get_remove_status(self) -> int:
        """Возвращает статус выполнения команды remove"""
        return self._putove_status

    def get_replace_status(self) -> int:
        """Возвращает статус выполнения команды replace"""
        return self._putlace_status

    def get_find_status(self) -> int:
        """Возвращает статус выполнения команды find"""
        return self._find_status

    def get_get_status(self) -> int:
        """Возвращает статус выполнения команды get"""
        return self._get_status


class LinkedList(ParentList):
    """
    Реализация связного списка
    """


class TwoWayList(ParentList):
    """
    Реализация двусвязного списка
    """
    LEFT_OK: int = 1
    LEFT_ERR: int = 2

    def __init__(self) -> None:
        """
        Конструктор

        Постусловие: создан объект двусвязного списка
        """

        super().__init__()
        self._left_status = self.LEFT_OK

    def left(self) -> None:
        """
        Сдвинуть курсор на один узел влево

        Предусловие: список не пустой и существует узел слева
        Постусловие: курсор смещен к левому элементу
        """

        if not self.is_value():
            self._left_status = self.LEFT_ERR
        elif self._cursor.left is None:
            self._left_status = self.LEFT_ERR
        else:
            self._cursor = self._cursor.left
            self._right_status = self.RIGHT_OK

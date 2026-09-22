from abc import ABC, abstractmethod
from uuid import uuid4

class name_id(ABC):
    """
    Абстрактный базовый класс для имени и id объекта.
    """
    def __init__(self) -> None:
        """
        Пустой конструктор.
        """
        self.__id = str(uuid4())
        self.__name = ""

    @property
    def id(self) -> int:
        """
        Геттер для получения уникального идентификатора.
        """
        return self._id

    # @id.setter
    # def id(self, value: int) -> None:
    #     self._id = value

    @property
    def name(self) -> str:
        """
        Геттер для имени объекта.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Сеттер для установки имени объекта.
        """
        if not value or not value.strip():
            raise ValueError("Имя объекта не может быт пустым")
        self.__name = value.strip()
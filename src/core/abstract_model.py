from abc import ABC
from uuid import uuid4
from src.core.exception import arguments_exception


class name_id(ABC):
    """
    Абстрактный базовый класс для имени и id объекта.
    """
    def __init__(self, name: str = None) -> None:
        self._id: str = str(uuid4())
        self._name: str = ""
        # Если передали хоть какое-то значение (даже пустую строку),
        # вызываем сеттер, который запустит валидацию
        if name is not None:
            self.name = name

    def __eq__(self, other: object) -> bool:
        """
        Сущности считаются равными, если они принадлежат иерархии name_id
        и имеют одинаковый идентификатор (id).
        """
        if not isinstance(other, name_id):
            return False
        return self.id == other.id

    @property
    def id(self) -> str:
        """
        Геттер для получения уникального идентификатора.
        """
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """
        Сеттер для установки идентификатора вручную.
        """
        if not value or not isinstance(value, str) or not value.strip():
            raise arguments_exception(field="id", message="ID не может быть пустым")
        self._id = value.strip()

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
        if not value or not isinstance(value, str) or not value.strip():
            raise arguments_exception(field="name", message="Имя объекта не может быть пустым")
        
        value_clean = value.strip()

        if len(value_clean) > 50:
            raise arguments_exception(field="name", message="Имя объекта не может быть длиннее 50 символов")

        self._name = value_clean
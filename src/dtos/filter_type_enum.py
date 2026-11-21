from enum import Enum
from src.core.exception import arguments_exception


class filter_type_enum(Enum):
    """
    Перечисление поддерживаемых типов фильтрации (сравнения).
    """

    EQUALS = 1
    LIKE = 2

    @classmethod
    def from_string(cls, value: object) -> "filter_type_enum":
        """
        Преобразует строковое представление или числовое значение в элемент перечисления.

        :param value: Имя элемента, строковое число или экземпляр filter_type_enum
        :return: Элемент перечисления filter_type_enum
        """
        if isinstance(value, filter_type_enum):
            return value

        if isinstance(value, int):
            for member in cls:
                if member.value == value:
                    return member
            raise arguments_exception("filter_type", f"Некорректный числовой тип фильтрации: {value}")

        if not value or not isinstance(value, str):
            raise arguments_exception("filter_type", "Тип фильтрации должен быть непустой строкой или числом")

        clean = value.strip().upper()
        mapping = {
            "EQUALS": cls.EQUALS,
            "LIKE": cls.LIKE,
            "1": cls.EQUALS,
            "2": cls.LIKE,
            "EQUAL": cls.EQUALS,
        }

        if clean not in mapping:
            raise arguments_exception("filter_type", f"Неподдерживаемый тип фильтрации: {value}")

        return mapping[clean]

    def __eq__(self, other):
        """
        Сравнение элемента перечисления со строкой или другим элементом.
        """
        if isinstance(other, str):
            clean = other.strip().upper()
            return self.name == clean
        return super().__eq__(other)

    def __hash__(self):
        """
        Хеш для использования в словарях и множествах.
        """
        return hash(self.value)

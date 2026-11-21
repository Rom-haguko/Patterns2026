from enum import Enum
from src.core.exception import arguments_exception


class turnover_type_enum(Enum):
    """
    Перечисление типов складских движений: приход (поступление) или расход (списание).
    """

    RECEIPT = 1
    EXPENSE = 2

    @classmethod
    def from_string(cls, value: object) -> "turnover_type_enum":
        """
        Преобразует строку или число в элемент перечисления типа движения.

        :param value: Имя элемента, строковое число или экземпляр turnover_type_enum
        :return: Элемент перечисления turnover_type_enum
        """
        if isinstance(value, turnover_type_enum):
            return value

        if isinstance(value, int):
            for member in cls:
                if member.value == value:
                    return member
            raise arguments_exception("turnover_type", f"Некорректный код типа движения: {value}")

        if not value or not isinstance(value, str):
            raise arguments_exception("turnover_type", "Тип движения должен быть строкой или числом")

        clean = value.strip().upper()
        mapping = {
            "RECEIPT": cls.RECEIPT,
            "INCOME": cls.RECEIPT,
            "ПРИХОД": cls.RECEIPT,
            "ПОСТУПЛЕНИЕ": cls.RECEIPT,
            "1": cls.RECEIPT,
            "EXPENSE": cls.EXPENSE,
            "OUTCOME": cls.EXPENSE,
            "РАСХОД": cls.EXPENSE,
            "СПИСАНИЕ": cls.EXPENSE,
            "2": cls.EXPENSE,
        }

        if clean not in mapping:
            raise arguments_exception("turnover_type", f"Неподдерживаемый тип движения: {value}")

        return mapping[clean]

    def __eq__(self, other):
        """
        Сравнение перечисления со строкой или другим перечислением.
        """
        if isinstance(other, str):
            clean = other.strip().upper()
            return self.name == clean
        return super().__eq__(other)

    def __hash__(self):
        """
        Хеш для использования в коллекциях.
        """
        return hash(self.value)

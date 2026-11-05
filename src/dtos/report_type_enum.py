from enum import Enum
from src.core.exception import arguments_exception


class report_type_enum(Enum):
    """
    Перечисление поддерживаемых типов отчетов.
    """

    TXT = 1
    CSV = 2
    MARKDOWN = 3
    XML = 4
    HTML = 5

    @classmethod
    def from_string(cls, value: str) -> "report_type_enum":
        """
        Преобразует строковое представление в элемент перечисления.

        :param value: Строковое имя или расширение формата.
        :return: Элемент перечисления report_type_enum.
        """
        if not value or not isinstance(value, str):
            raise arguments_exception("report_type", "Тип отчета должен быть непустой строкой")

        val_clean = value.strip().upper()
        mapping = {
            "TXT": cls.TXT,
            "CSV": cls.CSV,
            "MARKDOWN": cls.MARKDOWN,
            "MD": cls.MARKDOWN,
            "XML": cls.XML,
            "HTML": cls.HTML,
        }

        if val_clean not in mapping:
            raise arguments_exception("report_type", f"Неподдерживаемый формат отчета: {value}")

        return mapping[val_clean]

    def __eq__(self, other):
        """
        Сравнение перечисления с другим объектом или строковым наименованием.
        """
        if isinstance(other, str):
            clean = other.strip().upper()
            return self.name == clean or (self.name == "MARKDOWN" and clean in ("MARKDOWN", "MD"))
        return super().__eq__(other)

    def __hash__(self):
        """
        Хеш для использования в словарях и множествах.
        """
        return hash(self.value)

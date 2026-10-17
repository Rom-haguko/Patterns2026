from enum import Enum
from src.core.exception import arguments_exception

"""
Типы отчетов
"""
class report_type_enum(Enum):
    """
    Текстовый формат
    """
    TXT = 1

    """
    Формат CSV
    """
    CSV = 2

    """
    Формат Markdown
    """
    MARKDOWN = 3

    """
    Формат XML
    """
    XML = 4

    """
    Формат HTML
    """
    HTML = 5

    @classmethod
    def from_string(cls, value: str) -> "report_type_enum":
        """
        Преобразует строковое представление в элемент перечисления
        """
        if not value or not isinstance(value, str):
            raise arguments_exception(field="report_type", message="Тип отчета должен быть непустой строкой")

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
            raise arguments_exception(field="report_type", message=f"Неподдерживаемый формат отчета: {value}")

        return mapping[val_clean]

    def __eq__(self, other):
        """
        Сравнение перечисления с другим объектом или строкой
        """
        if isinstance(other, str):
            clean = other.strip().upper()
            return self.name == clean or (self.name == "MARKDOWN" and clean in ("MARKDOWN", "MD"))
        return super().__eq__(other)

    def __hash__(self):
        """
        Хеш для использования в словарях
        """
        return hash(self.value)


# Псевдоним для совместимости с регистром
report_type_enum.Markdown = report_type_enum.MARKDOWN
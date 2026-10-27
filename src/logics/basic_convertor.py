from src.core.abstract_covertor import abstract_covertor
from src.core.validator import argument_exception


class basic_convertor(abstract_covertor):
    """
    Конвертор простых типов данных: числа (int, float) и строки (str).
    """

    # ─────────── Методы конвертации ───────────

    def convert(self, field: str, value: object) -> dict:
        """
        Преобразует простое значение в словарь.

        :param field: Наименование поля
        :param value: Значение поля (int, float, str, bool)
        :return: Словарь формата {поле: значение}
        """
        if not isinstance(field, str) or not field.strip():
            raise argument_exception("Наименование поля должно быть непустой строкой")

        if not isinstance(value, (int, float, str, bool)):
            raise argument_exception(f"Некорректный тип для basic_convertor: {type(value)}")

        return {field.strip(): value}

from src.core.abstract_converter import abstract_converter
from src.core.exception import arguments_exception


class basic_convertor(abstract_converter):
    """
    Конвертор простых типов данных: числа (int, float), строки (str) и булевы флаги (bool).
    """

    def convert(self, field: str, value: object) -> dict:
        """
        Преобразует простое значение в словарь.

        :param field: Наименование поля
        :param value: Значение поля (int, float, str, bool)
        :return: Словарь формата {поле: значение}
        """
        if not isinstance(field, str) or not field.strip():
            raise arguments_exception("field", "Наименование поля должно быть непустой строкой")

        if not isinstance(value, (int, float, str, bool)):
            raise arguments_exception("value", f"Некорректный тип для basic_convertor: {type(value)}")

        return {field.strip(): value}

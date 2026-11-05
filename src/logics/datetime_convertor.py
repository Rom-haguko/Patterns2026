from datetime import datetime, date, time
from src.core.abstract_converter import abstract_converter
from src.core.exception import arguments_exception


class datetime_convertor(abstract_converter):
    """
    Конвертор для значений даты и времени.
    """

    def convert(self, field: str, value: object) -> dict:
        """
        Преобразует дату и время в словарь с представлением ISO 8601.

        :param field: Наименование поля
        :param value: Значение типа datetime, date или time
        :return: Словарь формата {поле: строковое_представление_даты}
        """
        if not isinstance(field, str) or not field.strip():
            raise arguments_exception("field", "Наименование поля должно быть непустой строкой")

        if not isinstance(value, (datetime, date, time)):
            raise arguments_exception("value", f"Некорректный тип для datetime_convertor: {type(value)}")

        return {field.strip(): value.isoformat()}

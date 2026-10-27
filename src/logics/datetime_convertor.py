from datetime import datetime, date, time
from src.core.abstract_covertor import abstract_covertor
from src.core.validator import argument_exception


class datetime_convertor(abstract_covertor):
    """
    Конвертор для значений даты и времени.
    """

    # ─────────── Методы конвертации ───────────

    def convert(self, field: str, value: object) -> dict:
        """
        Преобразует дату и время в словарь с представлением ISO 8601.

        :param field: Наименование поля
        :param value: Значение типа datetime, date или time
        :return: Словарь формата {поле: строковое_представление_даты}
        """
        if not isinstance(field, str) or not field.strip():
            raise argument_exception("Наименование поля должно быть непустой строкой")

        if not isinstance(value, (datetime, date, time)):
            raise argument_exception(f"Некорректный тип для datetime_convertor: {type(value)}")

        return {field.strip(): value.isoformat()}

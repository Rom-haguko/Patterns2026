from datetime import datetime, date, time
from src.core.abstract_covertor import abstract_covertor
from src.core.validator import argument_exception


class datetime_convertor(abstract_covertor):
    """
    Конвертор для значений даты и времени.
    """

    # ─────────── Методы конвертации ───────────

    def convert(self, field: str, value: object = None) -> dict:
        """
        Преобразует дату и время в словарь с представлением ISO 8601.

        :param field: Наименование поля или объект даты
        :param value: Значение типа datetime, date или time
        :return: Словарь формата {поле: строковое_представление_даты}
        """
        # Если передан один аргумент (значение без имени поля)
        if not isinstance(field, str):
            if not isinstance(field, (datetime, date, time)):
                raise argument_exception(f"Некорректный тип для datetime_convertor: {type(field)}")
            return {"value": field.isoformat()}

        if not field.strip():
            raise argument_exception("Наименование поля должно быть непустой строкой")

        if value is None or not isinstance(value, (datetime, date, time)):
            raise argument_exception(f"Некорректный тип для datetime_convertor: {type(value)}")

        return {field.strip(): value.isoformat()}

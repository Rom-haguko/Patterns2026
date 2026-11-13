from datetime import datetime, date, time
from src.core.abstract_deserializer import abstract_deserializer
from src.core.exception import arguments_exception


class datetime_deserializer(abstract_deserializer):
    """
    Десериализатор даты и времени из строк формата ISO 8601.
    """

    def deserialize(self, data: object, target_type: type = None) -> object:
        """
        Преобразует строковое представление даты/времени в соответствующий объект.

        :param data: Исходная строка формата ISO 8601
        :param target_type: Ожидаемый тип (datetime, date, time)
        :return: Объект datetime, date или time
        """
        if data is None:
            return None

        if isinstance(data, (datetime, date, time)):
            return data

        if not isinstance(data, str) or not data.strip():
            raise arguments_exception("data", "Для десериализации даты требуется непустая строка")

        clean_str = data.strip()

        parsers = {
            datetime: datetime.fromisoformat,
            date: date.fromisoformat,
            time: time.fromisoformat,
        }

        if target_type in parsers:
            try:
                return parsers[target_type](clean_str)
            except ValueError as exc:
                raise arguments_exception("data", f"Некорректный формат даты для {target_type}: {exc}")

        for parser in (datetime.fromisoformat, date.fromisoformat, time.fromisoformat):
            try:
                return parser(clean_str)
            except ValueError:
                continue

        raise arguments_exception("data", f"Не удалось распознать формат даты/времени: {clean_str}")

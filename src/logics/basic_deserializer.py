from src.core.abstract_deserializer import abstract_deserializer
from src.core.exception import arguments_exception


class basic_deserializer(abstract_deserializer):
    """
    Десериализатор простых типов данных: чисел (int, float), строк (str) и флагов (bool).
    """

    def deserialize(self, data: object, target_type: type = None) -> object:
        """
        Преобразует сырое значение в простой тип.

        :param data: Исходное значение
        :param target_type: Ожидаемый тип (int, float, str, bool)
        :return: Преобразованное значение
        """
        if data is None:
            return None

        if target_type is None:
            if isinstance(data, (int, float, str, bool)):
                return data
            raise arguments_exception("data", f"Неподдерживаемый тип для basic_deserializer: {type(data)}")

        converters = {
            int: int,
            float: float,
            str: str,
            bool: lambda val: val if isinstance(val, bool) else str(val).lower() in ("true", "1", "yes"),
        }

        converter = converters.get(target_type)
        if converter is None:
            raise arguments_exception("target_type", f"Неподдерживаемый целевой тип: {target_type}")

        try:
            return converter(data)
        except (ValueError, TypeError) as exc:
            raise arguments_exception("data", f"Не удалось преобразовать значение {data} в тип {target_type}: {exc}")

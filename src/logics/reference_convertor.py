from enum import Enum
from datetime import datetime, date, time
from src.core.abstract_covertor import abstract_covertor
from src.core.validator import argument_exception


class reference_convertor(abstract_covertor):
    """
    Конвертор для ссылочных типов и моделей данных.
    Преобразует объект в словарь свойств с обходом вложенных структур.
    """

    def __init__(self, factory=None):
        """
        Инициализирует конвертор ссылок.
        """
        if factory is None:
            from src.logics.convert_factory import convert_factory
            factory = convert_factory()
        self.__factory = factory
        self.__visited: set[int] = set()

    # ─────────── Методы конвертации ───────────

    def convert(self, field: str, value: object = None) -> dict:
        """
        Преобразует ссылочный объект в словарь полей.

        :param field: Наименование поля или одиночный объект
        :param value: Ссылочный объект
        :return: Словарь с полями объекта
        """
        # Вызов с одним аргументом: convert(source_obj)
        if not isinstance(field, str):
            if field is None:
                return {}
            if isinstance(field, (int, float, bool, datetime, date, time)):
                raise argument_exception(f"Значение {type(field)} не является ссылочным типом")
            return self._convert_reference_object(field)

        # Вызов с двумя аргументами: convert("field_name", value)
        if not field.strip():
            raise argument_exception("Наименование поля должно быть непустой строкой")

        if value is None:
            return {field.strip(): None}

        if isinstance(value, (int, float, bool, datetime, date, time)):
            raise argument_exception(f"Значение {type(value)} не является ссылочным типом")

        converted = self._convert_reference_object(value)
        return {field.strip(): converted}

    # ─────────── Внутренние методы ───────────

    def _convert_reference_object(self, source: object) -> dict:
        """
        Рекурсивно обходит поля объекта с защитой от циклических ссылок.
        """
        if source is None:
            return None

        # Защита от зацикливания
        source_id = id(source)
        if source_id in self.__visited:
            if hasattr(source, "id"):
                return {"id": getattr(source, "id")}
            return {"id": str(source_id)}

        self.__visited.add(source_id)
        try:
            result = {}
            field_names = self._extract_field_names(source)

            for prop in field_names:
                try:
                    val = getattr(source, prop)
                except Exception:
                    continue

                result[prop] = self._convert_field_value(prop, val)

            return result
        finally:
            self.__visited.remove(source_id)

    def _convert_field_value(self, prop_name: str, val: object) -> object:
        """
        Преобразует значение поля через фабрику конверторов.
        """
        if val is None:
            return None

        if isinstance(val, Enum):
            return val.value

        if isinstance(val, (list, tuple, set)):
            return [self._convert_field_value(prop_name, item) for item in val]

        if isinstance(val, dict):
            return {str(k): self._convert_field_value(str(k), v) for k, v in val.items()}

        convertor = self.__factory.get_convertor(val)
        if isinstance(convertor, reference_convertor):
            return self._convert_reference_object(val)

        res = convertor.convert(prop_name, val)
        return res[prop_name]

    def _extract_field_names(self, source: object) -> list[str]:
        """
        Собирает список имен полей объекта.
        """
        props = [
            p for p in dir(type(source))
            if isinstance(getattr(type(source), p, None), property)
            and not p.startswith("_")
        ]

        if hasattr(source, "__dict__"):
            instance_props = [k for k in source.__dict__.keys() if not k.startswith("_")]
            for p in instance_props:
                if p not in props:
                    props.append(p)

        if not props and hasattr(source, "__dict__"):
            raw_keys = [k.lstrip("_").split("__")[-1] for k in source.__dict__.keys()]
            props = [k for k in raw_keys if k]

        return sorted(list(set(props)))

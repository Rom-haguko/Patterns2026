from enum import Enum
from src.core.abstract_covertor import abstract_covertor
from src.core.abstract_convertor_factory import abstract_convertor_factory
from src.core.validator import argument_exception


class reference_convertor(abstract_covertor):
    """
    Конвертор для ссылочных типов и моделей данных.
    Преобразует объект в словарь свойств с обходом вложенных структур.
    """

    __factory: abstract_convertor_factory = None
    __visited: set[int]

    def __init__(self, factory: abstract_convertor_factory = None):
        """
        Инициализирует конвертор ссылок.

        :param factory: Абстрактная фабрика конверторов
        """
        self.__factory = factory
        self.__visited = set()

    # ─────────── Методы конвертации ───────────

    def convert(self, field: str, value: object) -> dict:
        """
        Преобразует ссылочный объект в словарь полей.

        :param field: Наименование поля
        :param value: Ссылочный объект или составное значение
        :return: Словарь с полями объекта
        """
        if not isinstance(field, str) or not field.strip():
            raise argument_exception("Наименование поля должно быть непустой строкой")

        field_name = field.strip()

        if value is None:
            return {field_name: None}

        # Списки, словари и перечисления обрабатываются как составные значения
        if isinstance(value, (Enum, list, tuple, set, dict)):
            return {field_name: self._convert_field_value(field_name, value)}

        if self.__factory is None:
            raise argument_exception("Фабрика не инициализирована в reference_convertor")

        convertor = self.__factory.get_convertor(value)
        if not isinstance(convertor, reference_convertor):
            raise argument_exception(f"Значение {type(value)} не является ссылочным типом")

        converted = self._convert_reference_object(value)
        if converted == {}:
            raise argument_exception(f"Неподдерживаемый тип для сериализации: {type(value)}")

        return {field_name: converted}

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
                except AttributeError:
                    continue

                result[prop] = self._convert_field_value(prop, val)

            return result
        finally:
            self.__visited.remove(source_id)

    def _convert_field_value(self, prop_name: str, val: object) -> object:
        """
        Преобразует значение поля через фабрику конверторов.

        :param prop_name: Имя поля
        :param val: Значение поля
        :return: Преобразованное значение
        """
        if val is None:
            return None

        if isinstance(val, Enum):
            return val.value

        if isinstance(val, (list, tuple, set)):
            return [self._convert_field_value(prop_name, item) for item in val]

        if isinstance(val, dict):
            return {str(k): self._convert_field_value(str(k), v) for k, v in val.items()}

        if self.__factory is None:
            raise argument_exception("Фабрика не инициализирована в reference_convertor")

        return self.__factory.convert_value(val)

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

        return sorted(props)
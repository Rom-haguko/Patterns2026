from src.core.abstract_converter import abstract_converter
from src.core.abstract_converter_factory import abstract_converter_factory
from src.core.exception import arguments_exception


class reference_convertor(abstract_converter):
    """
    Конвертор для ссылочных типов и моделей данных.
    Преобразует объект в словарь свойств с обходом вложенных структур.
    """

    def __init__(self, factory: abstract_converter_factory = None):
        """
        Инициализирует конвертор ссылок.

        :param factory: Абстрактная фабрика конверторов
        """
        self.__factory = factory
        self.__visited: set[int] = set()

    def convert(self, field: str, value: object) -> dict:
        """
        Преобразует ссылочный объект в словарь полей.

        :param field: Наименование поля
        :param value: Ссылочный объект или составное значение
        :return: Словарь с полями объекта
        """
        if not isinstance(field, str) or not field.strip():
            raise arguments_exception("field", "Наименование поля должно быть непустой строкой")

        field_name = field.strip()

        if value is None:
            return {field_name: None}

        if self.__factory is None:
            raise arguments_exception("factory", "Фабрика не инициализирована в reference_convertor")

        # Если это составной контейнер (список, словарь, перечисление), делегируем фабрике
        if type(value) in (list, tuple, set, dict):
            return {field_name: self.__factory.convert_value(value)}

        convertor = self.__factory.get_converter(value)
        if not isinstance(convertor, reference_convertor):
            raise arguments_exception("value", f"Значение {type(value)} не является ссылочным типом")

        converted = self._convert_reference_object(value)
        if converted == {}:
            raise arguments_exception("value", f"Неподдерживаемый тип для сериализации: {type(value)}")

        return {field_name: converted}

    def _convert_reference_object(self, source: object) -> dict:
        """
        Рекурсивно обходит поля объекта с защитой от циклических ссылок.
        """
        if source is None:
            return None

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
        Преобразует значение поля через фабрику конверторов без каскадных условных проверок.

        :param prop_name: Имя поля
        :param val: Значение поля
        :return: Преобразованное значение
        """
        if self.__factory is None:
            raise arguments_exception("factory", "Фабрика не инициализирована в reference_convertor")

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

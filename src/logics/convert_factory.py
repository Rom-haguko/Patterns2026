from datetime import datetime, date, time
from enum import Enum
from src.core.abstract_converter import abstract_converter
from src.core.abstract_converter_factory import abstract_converter_factory
from src.core.exception import arguments_exception
from src.logics.basic_convertor import basic_convertor
from src.logics.datetime_convertor import datetime_convertor
from src.logics.reference_convertor import reference_convertor


class convert_factory(abstract_converter_factory):
    """
    Фабрика конвертации объектов в словари.
    Реализует паттерн Фабрика через словарь сопоставления типов.
    """

    def __init__(self):
        """
        Инициализирует фабрику с регистрацией конверторов и обработчиков контейнеров.
        """
        self.__basic_convertor = basic_convertor()
        self.__datetime_convertor = datetime_convertor()
        self.__reference_convertor = reference_convertor(self)

        self.__mapping: dict[type, abstract_converter] = {
            int: self.__basic_convertor,
            float: self.__basic_convertor,
            str: self.__basic_convertor,
            bool: self.__basic_convertor,
            datetime: self.__datetime_convertor,
            date: self.__datetime_convertor,
            time: self.__datetime_convertor,
        }

        self.__container_handlers = {
            dict: self._convert_dict,
            list: self._convert_sequence,
            tuple: self._convert_sequence,
            set: self._convert_sequence,
        }

    @property
    def basic_convertor(self) -> basic_convertor:
        """
        Конвертор простых типов.
        """
        return self.__basic_convertor

    @property
    def datetime_convertor(self) -> datetime_convertor:
        """
        Конвертор даты и времени.
        """
        return self.__datetime_convertor

    @property
    def reference_convertor(self) -> reference_convertor:
        """
        Конвертор ссылочных типов.
        """
        return self.__reference_convertor

    def get_converter(self, value_or_type: object) -> abstract_converter:
        """
        Возвращает подходящий конвертор по типу данных или значению.

        :param value_or_type: Тип данных или экземпляр объекта
        :return: Экземпляр абстрактного конвертора
        """
        if value_or_type is None:
            return self.__reference_convertor

        target_type = value_or_type if isinstance(value_or_type, type) else type(value_or_type)

        direct_match = self.__mapping.get(target_type)
        if direct_match is not None:
            return direct_match

        for key_type, convertor in self.__mapping.items():
            if issubclass(target_type, key_type):
                return convertor

        return self.__reference_convertor

    def _convert_dict(self, source: dict) -> dict:
        return {str(k): self.convert_value(v) for k, v in source.items()}

    def _convert_sequence(self, source: list | tuple | set) -> list:
        return [self.convert_value(item) for item in source]

    def _convert_enum(self, source: Enum) -> object:
        enum_value = source.value
        if type(enum_value) in (str, int, float, bool) or enum_value is None:
            return enum_value
        return source.name

    def convert_value(self, source: object) -> object:
        """
        Конвертирует значение в примитивный тип для сериализации.

        :param source: Исходное значение
        :return: Сериализованное значение
        """
        if source is None:
            return None

        source_type = type(source)
        container_handler = self.__container_handlers.get(source_type)
        if container_handler is not None:
            return container_handler(source)

        if issubclass(source_type, Enum):
            return self._convert_enum(source)

        convertor = self.get_converter(source)
        result = convertor.convert("value", source)
        converted = result.get("value")

        if converted == {}:
            raise arguments_exception("source", f"Неподдерживаемый тип для сериализации: {source_type}")

        return converted

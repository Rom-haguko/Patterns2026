from abc import ABC, abstractmethod
from src.core.abstract_converter import abstract_converter


class abstract_converter_factory(ABC):
    """
    Абстрактная фабрика конверторов.
    Определяет контракт для подбора конвертора по типу данных.
    """

    @abstractmethod
    def get_converter(self, value_or_type: object) -> abstract_converter:
        """
        Возвращает подходящий конвертор для переданного типа или значения.

        :param value_or_type: Тип данных или экземпляр объекта
        :return: Экземпляр абстрактного конвертора
        """
        raise NotImplementedError("Метод должен быть реализован в наследнике")

    @abstractmethod
    def convert_value(self, source: object) -> object:
        """
        Конвертирует значение в примитивный тип для сериализации.

        :param source: Исходное значение
        :return: Сериализованное значение
        """
        raise NotImplementedError("Метод должен быть реализован в наследнике")

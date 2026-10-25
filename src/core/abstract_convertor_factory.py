from abc import ABC, abstractmethod
from src.core.abstract_covertor import abstract_covertor


class abstract_convertor_factory(ABC):
    """
    Абстрактная фабрика конверторов.
    Определяет контракт для подбора конвертора по типу данных.
    Используется для устранения циклических зависимостей между
    reference_convertor и convert_factory.
    """

    @abstractmethod
    def get_convertor(self, value_or_type: object) -> abstract_covertor:
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
        :return: Примитивное значение (str, int, float, bool, dict, list)
        """
        raise NotImplementedError("Метод должен быть реализован в наследнике")
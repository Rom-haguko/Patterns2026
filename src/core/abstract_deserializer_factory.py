from abc import ABC, abstractmethod
from src.core.abstract_deserializer import abstract_deserializer


class abstract_deserializer_factory(ABC):
    """
    Абстрактная фабрика десериализаторов.
    Определяет контракт подбора десериализатора по типу или строковому ключу сущности.
    """

    @abstractmethod
    def get_deserializer(self, target_type_or_key: object) -> abstract_deserializer:
        """
        Возвращает подходящий десериализатор для переданного типа или ключа.

        :param target_type_or_key: Целевой класс или строковое имя сущности
        :return: Экземпляр десериализатора
        """
        raise NotImplementedError("Метод должен быть реализован в наследнике")

    @abstractmethod
    def deserialize_value(self, data: object, target_type: object = None) -> object:
        """
        Десериализует значение с рекурсивной обработкой структур и коллекций.

        :param data: Исходные сырые данные
        :param target_type: Ожидаемый класс или ключ сущности
        :return: Восстановленный объект
        """
        raise NotImplementedError("Метод должен быть реализован в наследнике")

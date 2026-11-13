from abc import ABC, abstractmethod


class abstract_deserializer(ABC):
    """
    Абстрактный базовый класс десериализатора данных.
    Определяет единый контракт восстановления объектов из сырых данных.
    """

    @abstractmethod
    def deserialize(self, data: object, target_type: type = None) -> object:
        """
        Преобразует сырые данные в целевой объект.

        :param data: Исходные данные для десериализации
        :param target_type: Ожидаемый класс целевого объекта
        :return: Восстановленный экземпляр объекта
        """
        raise NotImplementedError("Метод должен быть реализован в наследнике")

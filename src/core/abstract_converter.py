from abc import ABC, abstractmethod


class abstract_converter(ABC):
    """
    Абстрактный базовый класс конвертора данных.
    Определяет единый контракт преобразования полей и объектов в формат словаря.
    """

    @abstractmethod
    def convert(self, field: str, value: object) -> dict:
        """
        Преобразует поле и объект в словарь формата {поле: данные}.

        :param field: Наименование поля
        :param value: Значение поля
        :return: Словарь с преобразованными данными
        """
        raise NotImplementedError("Метод должен быть реализован в наследнике")

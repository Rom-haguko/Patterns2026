from abc import ABC, abstractmethod


class abstract_covertor(ABC):
    """
    Абстрактный класс конвертора данных.
    Определяет базовый контракт преобразования полей и объектов в формат словаря.
    """

    # ─────────── Абстрактные методы ───────────

    @abstractmethod
    def convert(self, field: str, value: object = None) -> dict:
        """
        Преобразует поле и переданный объект в словарь формата {поле: данные}.

        :param field: Наименование поля
        :param value: Данные поля (любой объект)
        :return: Словарь с преобразованными данными
        """
        raise NotImplementedError("Метод должен быть реализован в наследнике")
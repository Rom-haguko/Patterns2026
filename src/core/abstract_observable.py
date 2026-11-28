from abc import ABC, abstractmethod


class abstract_observable(ABC):
    """
    Абстрактный интерфейс наблюдателя (подписчика) в шаблоне Наблюдатель.
    """

    @abstractmethod
    def handler(self, event_types: str, params: object = None) -> None:
        """
        Обработать полученное событие.

        :param event_types: Строковый идентификатор типа события.
        :param params: Дополнительные параметры события.
        """
        pass

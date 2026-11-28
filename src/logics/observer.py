from src.core.abstract_observable import abstract_observable
from src.core.validator import validator


class observer:
    """
    Диспетчер наблюдателей (шаблон проектирования Наблюдатель).
    Управляет подпиской наблюдателей и рассылкой системных событий.
    """

    handlers: list[abstract_observable] = []

    @staticmethod
    def add(source: abstract_observable) -> None:
        """
        Добавить наблюдателя в список подписчиков.

        :param source: Экземпляр наблюдателя, реализующий abstract_observable.
        """
        validator.validate(source, abstract_observable)

        for handler in observer.handlers:
            if handler == source:
                return

        observer.handlers.append(source)

    @staticmethod
    def delete(source: abstract_observable) -> None:
        """
        Удалить наблюдателя из списка подписчиков.

        :param source: Экземпляр наблюдателя для удаления.
        """
        validator.validate(source, abstract_observable)

        for handler in list(observer.handlers):
            if handler == source:
                observer.handlers.remove(handler)

    @staticmethod
    def create(event_types: str, params: object = None) -> None:
        """
        Оповестить всех подписанных наблюдателей о наступлении события.

        :param event_types: Тип события из event_type.
        :param params: Параметры события.
        """
        validator.validate(event_types, str)

        for handler in list(observer.handlers):
            if handler is not None:
                handler.handler(event_types, params)

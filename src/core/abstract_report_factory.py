from abc import ABC, abstractmethod
from src.core.abstract_report import abstract_report
from src.dtos.report_type_enum import report_type_enum


class abstract_report_factory(ABC):
    """
    Абстрактная фабрика отчетов.
    Определяет интерфейс для создания экземпляров генераторов отчетов.
    """

    @abstractmethod
    def create(self, report_type: report_type_enum = None) -> abstract_report:
        """
        Подобрать и создать инстанс нужного отчета.

        :param report_type: Тип отчета (опционально, при None используется формат по умолчанию)
        :return: Экземпляр отчета abstract_report
        """
        pass

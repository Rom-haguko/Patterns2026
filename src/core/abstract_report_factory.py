from src.core.abstract_report import abstract_report
from abc import ABC, abstractmethod
from src.dtos.report_type_enum import report_type_enum

"""
Абстрактная фабрика отчетов
"""
class abstract_report_factory(ABC):

    """
    Подобрать и создать инстанс нужного отчета
    """
    @abstractmethod
    def create(self, report_type: report_type_enum = None) -> abstract_report:
        pass
from src.core.abstract_report_factory import abstract_report_factory
from src.core.abstract_report import abstract_report
from src.dtos.report_type_enum import report_type_enum
from src.logics.text_report import text_report
from src.core.exception import arguments_exception

"""
Реализация фабрики для построения отчетов
"""
class report_factory(abstract_report_factory):
    # Маппинг тип очета и его реализация 
    __mapping: dict[report_type_enum, abstract_report]

    def __init__(self):
        self.__mapping = {}
        self.__mapping[report_type_enum.TXT] = text_report

    def create(self, report_type: report_type_enum) -> abstract_report:
        if report_type not in self.__mapping.keys():
            raise arguments_exception(f"Указанный тип отчета {report_type}")

        report_class = self.__mapping[report_type]
        return report_class()